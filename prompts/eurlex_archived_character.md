# EURLEX archived character input control

Archived input-policy control, excluded from the main results. Document input: leading 19,968 characters.

## System

```text
You are a legal NLP classifier for EU legislation. Assign only the most relevant EuroVoc subject-matter labels — be selective, not exhaustive. Return only a compact JSON object.
```

## User

```text
Classify the EU legal document by its EuroVoc subject matter.

This is multi-label classification. Each document is tagged with the labels that directly apply to its main subject matter — typically 3 to 6 labels. Be selective: include only labels that clearly fit; do not list every remotely related concept.

Allowed labels:
0: political framework
1: politics and public safety
2: executive power and public service
3: international affairs
4: cooperation policy
5: international security
6: defence
7: EU institutions and European civil service
8: European Union law
9: European construction
10: EU finance
11: civil law
12: criminal law
13: international law
14: rights and freedoms
15: economic policy
16: economic conditions
17: regions and regional policy
18: national accounts
19: economic analysis
20: trade policy
21: tariff policy
22: trade
23: international trade
24: consumption
25: marketing
26: distributive trades
27: monetary relations
28: monetary economics
29: financial institutions and credit
30: free movement of capital
31: financing and investment
32: public finance and budget policy
33: budget
34: taxation
35: prices
36: social affairs
37: social protection
38: health
39: documentation
40: communications
41: information and information processing
42: information technology and data processing
43: natural and applied sciences
44: business organisation
45: business classification
46: management
47: accounting
48: competition
49: employment
50: labour market
51: organisation of work and working conditions
52: personnel management and staff remuneration
53: transport policy
54: organisation of transport
55: land transport
56: maritime and inland waterway transport
57: air and space transport
58: environmental policy
59: natural environment
60: deterioration of the environment
61: agricultural policy
62: agricultural structures and production
63: farming systems
64: cultivation of agricultural land
65: means of agricultural production
66: agricultural activity
67: fisheries
68: plant product
69: animal product
70: processed agricultural produce
71: beverages and sugar
72: foodstuff
73: agri-foodstuffs
74: food technology
75: production
76: technology and technical regulations
77: research and intellectual property
78: energy policy
79: coal and mining industries
80: oil industry
81: electrical and nuclear industries
82: industrial structures and policy
83: chemistry
84: iron, steel and other metal industries
85: mechanical engineering
86: electronics and electrical engineering
87: building and public works
88: wood industry
89: leather and textile industries
90: miscellaneous industries
91: Europe
92: regions of EU Member States
93: America
94: Africa
95: Asia and Oceania
96: economic geography
97: political geography
98: overseas countries and territories
99: United Nations

EU legal document:
"""
{{document_text}}
"""

Return only this JSON shape, with no explanation. List only the integer IDs of labels that clearly apply (use [] only if none apply):
{"labels": [<integer_label_id>, ...]}
```
