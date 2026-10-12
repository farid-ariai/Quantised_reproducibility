# ledgar_cand20_hard

Candidate names follow each example’s selected order; output IDs are local 0–19.

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
10: {{candidate_label_10}}
11: {{candidate_label_11}}
12: {{candidate_label_12}}
13: {{candidate_label_13}}
14: {{candidate_label_14}}
15: {{candidate_label_15}}
16: {{candidate_label_16}}
17: {{candidate_label_17}}
18: {{candidate_label_18}}
19: {{candidate_label_19}}

Text:
"""
{{clause_text}}
"""

Return only this JSON shape, with no explanation:
{"label": <integer_label_id>}
```
