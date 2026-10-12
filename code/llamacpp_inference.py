#!/usr/bin/env python3
"""Start a GGUF model with llama.cpp and run a Markdown prompt.

Example: python code/llamacpp_inference.py --model MODEL.gguf
  --tokenizer TOKENIZER_PATH --server llama-server --prompt-file prompts/ledgar.md
  --values '{"clause_text":"Prepared clause text"}'

Supply experiment-prepared input text and token-matched filler in --values or
--values-file. --dry-run prints the server command and filled messages only.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import socket
import subprocess
import time
from typing import Any
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
CONTROLLED = {"ledgar_short_5", "ledgar_padded_5", "ledgar_masked_5_long", "ledgar_full_100"}


def prepare_messages(path: Path, values: dict, eligible: list[int] | None) -> tuple[list[dict], list[int] | None]:
    if path.stem in CONTROLLED:
        if path.stem == "ledgar_full_100":
            if eligible is not None and eligible != list(range(100)):
                raise ValueError("Full-100 requires all 100 eligible IDs")
            eligible = list(range(100))
        elif eligible is None or len(eligible) != 5:
            raise ValueError("This controlled prompt requires five --eligible-ids in their frozen order")
        if len(set(eligible)) != len(eligible) or any(not 0 <= value < 100 for value in eligible):
            raise ValueError("Eligible IDs must be unique and in 0..99")
        labels = json.loads((ROOT / "labels/ledgar_labels.json").read_text())
        for index, label_id in enumerate(eligible):
            values.setdefault(f"global_label_id_{index}", label_id)
            values.setdefault(f"candidate_label_name_{index}", labels[label_id]["name"])
        mask = " ".join("1" if index in eligible else "0" for index in range(100))
        if values.get("eligibility_mask_100_bits", mask) != mask:
            raise ValueError("Eligibility mask differs from --eligible-ids")
        values["eligibility_mask_100_bits"] = mask
    elif eligible is not None:
        raise ValueError("--eligible-ids applies to the four controlled LEDGAR prompts")
    blocks = re.findall(r"```text\n(.*?)\n```", path.read_text(encoding="utf-8"), re.S)
    if len(blocks) != 2:
        raise ValueError("Expected one system message and one user message")

    def substitute(match: re.Match) -> str:
        name = match.group(1)
        if name not in values:
            raise ValueError(f"Missing prompt value: {name}")
        return str(values[name])

    messages = [{"role": role, "content": re.sub(r"\{\{([A-Za-z0-9_]+)\}\}", substitute, text)}
                for role, text in zip(("system", "user"), blocks)]
    return messages, eligible


def render(tokenizer: Any, messages: list[dict], chat: dict) -> str:
    kwargs = {"tokenize": False, "add_generation_prompt": chat["add_generation_prompt"],
              "enable_thinking": chat["enable_thinking"]}
    try:
        return tokenizer.apply_chat_template(messages, **kwargs)
    except TypeError:
        kwargs.pop("enable_thinking")
        return tokenizer.apply_chat_template(messages, **kwargs)


def post(endpoint: str, route: str, payload: dict, timeout: int) -> dict:
    request = urllib.request.Request(endpoint + route, data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                                     headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--config", type=Path, default=ROOT / "configs/llamacpp.json")
    parser.add_argument("--model", required=True)
    parser.add_argument("--tokenizer", required=True)
    parser.add_argument("--server", default=os.environ.get("LLAMA_SERVER", "llama-server"))
    parser.add_argument("--ctx-size", type=int)
    parser.add_argument("--parallel", type=int)
    parser.add_argument("--port", type=int)
    parser.add_argument("--max-new-tokens", type=int)
    parser.add_argument("--input-encoding", choices=("text", "token_ids"))
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--prompt-file", required=True, type=Path)
    parser.add_argument("--values", default="{}", help="JSON object containing prompt substitutions")
    parser.add_argument("--values-file", type=Path)
    parser.add_argument("--eligible-ids", nargs="+", type=int)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    values = json.loads(args.values_file.read_text()) if args.values_file else {}
    supplied = json.loads(args.values)
    if not isinstance(values, dict) or not isinstance(supplied, dict):
        parser.error("Prompt values must be JSON objects")
    values.update(supplied)
    messages, eligible = prepare_messages(args.prompt_file, values, args.eligible_ids)
    options = dict(config["server_options"])
    for name in ("ctx_size", "parallel", "port"):
        value = getattr(args, name)
        if value is not None:
            options[name] = value
    if options["parallel"] < 1 or options["ctx_size"] < 1 or options["ctx_size"] % options["parallel"]:
        parser.error("Context must be positive and divisible by the number of parallel slots")
    if not 1 <= options["port"] <= 65535 or options["host"] != "127.0.0.1":
        parser.error("Use a local server and a valid port")
    generation = dict(config["generation"])
    generation["max_new_tokens"] = args.max_new_tokens or (512 if args.prompt_file.stem.startswith("eurlex") else generation["max_new_tokens"])
    encoding = args.input_encoding or config["input_encoding"]
    command = [args.server, "-m", args.model, "-fit", options["fit"], "-ngl", str(options["gpu_layers"]),
               "-c", str(options["ctx_size"]), "--parallel", str(options["parallel"]), "-fa", options["flash_attention"],
               "-t", str(options["threads"]), "--host", options["host"], "--port", str(options["port"])]
    if args.dry_run:
        print(json.dumps({"server_command": command, "messages": messages, "generation": generation,
                          "input_encoding": encoding, "eligible_ids": eligible}, ensure_ascii=False, indent=2))
        return
    if not Path(args.model).is_file():
        raise FileNotFoundError("The selected GGUF file is missing")
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer, local_files_only=True)
    prompt = render(tokenizer, messages, config["chat"])
    token_ids = tokenizer.encode(prompt, add_special_tokens=False)
    if len(token_ids) + generation["max_new_tokens"] > options["ctx_size"] // options["parallel"]:
        raise ValueError("Prompt and answer exceed a server slot; supply the prepared input or increase --ctx-size")
    with socket.socket() as check:
        check.bind((options["host"], options["port"]))
    endpoint = f"http://{options['host']}:{options['port']}"
    process = subprocess.Popen(command, stdout=subprocess.DEVNULL)
    try:
        deadline = time.monotonic() + args.timeout
        while True:
            if process.poll() is not None:
                raise RuntimeError("llama.cpp exited before the model was ready")
            try:
                with urllib.request.urlopen(endpoint + "/health", timeout=2) as response:
                    if response.status == 200:
                        break
            except (urllib.error.URLError, TimeoutError):
                pass
            if time.monotonic() >= deadline:
                raise TimeoutError("llama.cpp model loading timed out")
            time.sleep(0.5)
        if encoding == "token_ids":
            actual = post(endpoint, "/tokenize", {"content": prompt, "add_special": False, "parse_special": True}, args.timeout)["tokens"]
            if actual != token_ids:
                raise ValueError("Hugging Face and GGUF token IDs differ")
        payload = {"prompt": token_ids if encoding == "token_ids" else prompt, "stream": False,
                   "temperature": generation["temperature"], "top_p": generation["top_p"],
                   "seed": generation["seed"], "n_predict": generation["max_new_tokens"]}
        if eligible is not None:
            alternatives = " | ".join(json.dumps(str(value)) for value in eligible)
            payload["grammar"] = 'root ::= "{\\"label\\":" value "}"\nvalue ::= ' + alternatives + '\n'
            payload["cache_prompt"] = True
        response = post(endpoint, "/completion", payload, args.timeout)
        raw = response.get("content")
        if not isinstance(raw, str):
            raise ValueError("llama.cpp response lacks string content")
        if eligible is not None:
            value = json.loads(raw)
            if type(value) is not dict or set(value) != {"label"} or type(value["label"]) is not int or value["label"] not in eligible or response.get("stopped_limit") or response.get("stop_type") == "limit":
                raise ValueError("Controlled output violates the eligible-label contract")
        print(raw)
    finally:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()


if __name__ == "__main__":
    main()
