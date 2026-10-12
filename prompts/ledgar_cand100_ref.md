# ledgar_cand100_ref

Candidate names follow each example’s selected order; output IDs are local 0–99.

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
50: {{candidate_label_50}}
51: {{candidate_label_51}}
52: {{candidate_label_52}}
53: {{candidate_label_53}}
54: {{candidate_label_54}}
55: {{candidate_label_55}}
56: {{candidate_label_56}}
57: {{candidate_label_57}}
58: {{candidate_label_58}}
59: {{candidate_label_59}}
60: {{candidate_label_60}}
61: {{candidate_label_61}}
62: {{candidate_label_62}}
63: {{candidate_label_63}}
64: {{candidate_label_64}}
65: {{candidate_label_65}}
66: {{candidate_label_66}}
67: {{candidate_label_67}}
68: {{candidate_label_68}}
69: {{candidate_label_69}}
70: {{candidate_label_70}}
71: {{candidate_label_71}}
72: {{candidate_label_72}}
73: {{candidate_label_73}}
74: {{candidate_label_74}}
75: {{candidate_label_75}}
76: {{candidate_label_76}}
77: {{candidate_label_77}}
78: {{candidate_label_78}}
79: {{candidate_label_79}}
80: {{candidate_label_80}}
81: {{candidate_label_81}}
82: {{candidate_label_82}}
83: {{candidate_label_83}}
84: {{candidate_label_84}}
85: {{candidate_label_85}}
86: {{candidate_label_86}}
87: {{candidate_label_87}}
88: {{candidate_label_88}}
89: {{candidate_label_89}}
90: {{candidate_label_90}}
91: {{candidate_label_91}}
92: {{candidate_label_92}}
93: {{candidate_label_93}}
94: {{candidate_label_94}}
95: {{candidate_label_95}}
96: {{candidate_label_96}}
97: {{candidate_label_97}}
98: {{candidate_label_98}}
99: {{candidate_label_99}}

Text:
"""
{{clause_text}}
"""

Return only this JSON shape, with no explanation:
{"label": <integer_label_id>}
```
