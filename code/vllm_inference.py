#!/usr/bin/env python3
"""Load a one-GPU or two-GPU vLLM profile and run a Markdown prompt.

Example: python code/vllm_inference.py --profile one_gpu --model MODEL_PATH
  --tokenizer TOKENIZER_PATH --prompt-file prompts/ledgar.md
  --values '{"clause_text":"Prepared clause text"}'

Supply experiment-prepared input text and token-matched filler in --values or
--values-file. --dry-run prints the model settings and filled messages only.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
from typing import Any

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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--config", type=Path, default=ROOT / "configs/vllm.json")
    parser.add_argument("--profile", choices=("one_gpu", "two_gpu"), required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--tokenizer", required=True)
    parser.add_argument("--hf-config-path")
    parser.add_argument("--dtype")
    parser.add_argument("--quantization")
    parser.add_argument("--max-model-len", type=int)
    parser.add_argument("--gpu-memory-utilization", type=float)
    parser.add_argument("--max-new-tokens", type=int)
    parser.add_argument("--input-encoding", choices=("text", "token_ids"))
    parser.add_argument("--prompt-file", required=True, type=Path)
    parser.add_argument("--values", default="{}", help="JSON object containing prompt substitutions")
    parser.add_argument("--values-file", type=Path)
    parser.add_argument("--eligible-ids", nargs="+", type=int)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    config = json.loads(args.config.read_text())[args.profile]
    values = json.loads(args.values_file.read_text()) if args.values_file else {}
    supplied = json.loads(args.values)
    if not isinstance(values, dict) or not isinstance(supplied, dict):
        parser.error("Prompt values must be JSON objects")
    values.update(supplied)
    messages, eligible = prepare_messages(args.prompt_file, values, args.eligible_ids)
    engine = dict(config["engine"])
    if args.max_model_len is not None:
        engine["max_model_len"] = args.max_model_len
    elif args.prompt_file.stem.startswith("eurlex"):
        engine["max_model_len"] = max(engine["max_model_len"], 8192)
    if args.gpu_memory_utilization is not None:
        engine["gpu_memory_utilization"] = args.gpu_memory_utilization
    kwargs = {"model": args.model, "tokenizer": args.tokenizer,
              "dtype": args.dtype or config["dtype"], "seed": config["seed"], **engine}
    if args.model.lower().endswith(".gguf"):
        kwargs["load_format"] = "gguf"
        kwargs["hf_config_path"] = args.hf_config_path or args.tokenizer
    quantization = args.quantization or config.get("quantization")
    if quantization:
        kwargs["quantization"] = quantization
    generation = dict(config["generation"])
    generation["max_new_tokens"] = args.max_new_tokens or (512 if args.prompt_file.stem.startswith("eurlex") else generation["max_new_tokens"])
    encoding = args.input_encoding or ("token_ids" if eligible is not None else config["input_encoding"])
    if args.dry_run:
        print(json.dumps({"engine": kwargs, "messages": messages, "generation": generation,
                          "input_encoding": encoding, "eligible_ids": eligible}, ensure_ascii=False, indent=2))
        return

    os.environ.setdefault("VLLM_USE_DEEP_GEMM", "0")
    os.environ.setdefault("VLLM_DEEP_GEMM_WARMUP", "skip")
    os.environ.setdefault("VLLM_USE_FLASHINFER_SAMPLER", "0")
    from transformers import AutoTokenizer
    from vllm import LLM, SamplingParams
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer, trust_remote_code=engine.get("trust_remote_code", False))
    prompt = render(tokenizer, messages, config["chat"])
    token_ids = tokenizer.encode(prompt, add_special_tokens=False)
    if len(token_ids) + generation["max_new_tokens"] > engine["max_model_len"]:
        raise ValueError("Prompt and answer exceed the context; supply the experiment-prepared input or increase --max-model-len")
    params = {"temperature": generation["temperature"], "top_p": generation["top_p"],
              "max_tokens": generation["max_new_tokens"]}
    if eligible is not None:
        from vllm.sampling_params import StructuredOutputsParams
        schema = {"type": "object", "properties": {"label": {"type": "integer", "enum": eligible}},
                  "required": ["label"], "additionalProperties": False}
        params.update(seed=config["seed"], structured_outputs=StructuredOutputsParams(json=schema))
    llm = LLM(**kwargs)
    inputs = [{"prompt_token_ids": token_ids}] if encoding == "token_ids" else [prompt]
    responses = llm.generate(inputs, sampling_params=SamplingParams(**params), use_tqdm=False)
    if len(responses) != 1 or len(responses[0].outputs) != 1:
        raise ValueError("Expected exactly one model response")
    output = responses[0].outputs[0]
    if eligible is not None:
        value = json.loads(output.text)
        if type(value) is not dict or set(value) != {"label"} or type(value["label"]) is not int or value["label"] not in eligible or output.finish_reason == "length":
            raise ValueError("Controlled output violates the eligible-label contract")
    print(output.text)


if __name__ == "__main__":
    main()
