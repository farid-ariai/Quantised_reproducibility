# ledgar_cand10_random

Candidate names follow each example’s selected order; output IDs are local 0–9.

## System

```text
You are a legal NLP classifier. Choose exactly one label ID from the allowed LEDGAR labels. Return only a compact JSON object.
```

## User

```text
Classify the legal clause into exactly one of the candidate LEDGAR categories.

Allowed labels:
0: {{candidate_label_0}}
1: {{candidate_label_1}}
2: {{candidate_label_2}}
3: {{candidate_label_3}}
4: {{candidate_label_4}}
5: {{candidate_label_5}}
6: {{candidate_label_6}}
7: {{candidate_label_7}}
8: {{candidate_label_8}}
9: {{candidate_label_9}}

Text:
"""
{{clause_text}}
"""

Return only this JSON shape, with no explanation:
{"label": <integer_label_id>}
```
