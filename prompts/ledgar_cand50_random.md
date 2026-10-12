# ledgar_cand50_random

Candidate names follow each example’s selected order; output IDs are local 0–49.

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
20: {{candidate_label_20}}
21: {{candidate_label_21}}
22: {{candidate_label_22}}
23: {{candidate_label_23}}
24: {{candidate_label_24}}
25: {{candidate_label_25}}
26: {{candidate_label_26}}
27: {{candidate_label_27}}
28: {{candidate_label_28}}
29: {{candidate_label_29}}
30: {{candidate_label_30}}
31: {{candidate_label_31}}
32: {{candidate_label_32}}
33: {{candidate_label_33}}
34: {{candidate_label_34}}
35: {{candidate_label_35}}
36: {{candidate_label_36}}
37: {{candidate_label_37}}
38: {{candidate_label_38}}
39: {{candidate_label_39}}
40: {{candidate_label_40}}
41: {{candidate_label_41}}
42: {{candidate_label_42}}
43: {{candidate_label_43}}
44: {{candidate_label_44}}
45: {{candidate_label_45}}
46: {{candidate_label_46}}
47: {{candidate_label_47}}
48: {{candidate_label_48}}
49: {{candidate_label_49}}

Text:
"""
{{clause_text}}
"""

Return only this JSON shape, with no explanation:
{"label": <integer_label_id>}
```
