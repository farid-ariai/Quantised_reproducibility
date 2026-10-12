# case_hold

## System

```text
You are a legal multiple-choice QA evaluator. Choose exactly one answer option ID. Return only a compact JSON object.
```

## User

```text
Read the case context and choose the answer option that best fills the missing holding.

Context:
"""
{{case_context}}
"""

Answer options:
0: {{ending_0}}
1: {{ending_1}}
2: {{ending_2}}
3: {{ending_3}}
4: {{ending_4}}

Return only this JSON shape, with no explanation:
{"answer": <integer_option_id>}
```
