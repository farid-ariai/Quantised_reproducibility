# LEDGAR Short-5

## System

```text
You are a legal NLP classifier. Follow the eligibility mask and return only one compact JSON object.
```

## User

```text
Classify the legal clause into exactly one LEDGAR category.

Label catalogue:
{{global_label_id_0}}: {{candidate_label_name_0}}
{{global_label_id_1}}: {{candidate_label_name_1}}
{{global_label_id_2}}: {{candidate_label_name_2}}
{{global_label_id_3}}: {{candidate_label_name_3}}
{{global_label_id_4}}: {{candidate_label_name_4}}

Eligibility mask:
{{eligibility_mask_100_bits}}
Mask position i corresponds to global label ID i. Choose only an ID whose mask value is 1.

Clause:
"""
{{clause_text}}
"""

Return only this JSON object, with no explanation:
{"label": <integer global label ID>}
```
