# chinese_wiki_2018

_Collaborator: Ruihan Wang, Daniel Romero, Ceren Budak, Lionel Robert_

This project is an extension based on ICWSM 2017 Chinese Wikipedia paper. The idea is to detect whether the fraction of leaders blocked can explain the results.

The raw data is `data/full_history.csv`. We use this file to generate measures for leaders blocked (with leaders defined in various ways), gini coefficient and reverts. After generating these measures, we combine the data with `data/data_icwsm.csv`.

## Identify leaders
To identify leaders, run `get_blocked_frac.py`. This file goes through `data/full_history.csv` and identifies leaders using
  1. geometric rules (tagged as origin in the code)
  2. inter-quartile rules (users whose level of activity is 1.5 inter-quartiles higher than the third quartile)
This file generates `article_leader.csv`, which records blocked ratio of leaders.

## Analysis
`analysis.Rmd` is the main analysis file. At the current stage, this file
  1. combines the blocked ratio of leaders with the icwsm dataset
  2. replicate the 2017 study.
