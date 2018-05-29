# chinese_wiki_2018

_Collaborator: Ruihan Wang, Daniel Romero, Ceren Budak, Lionel Robert_

This project is an extension based on ICWSM 2017 Chinese Wikipedia paper. The idea is to detect whether the fraction of leaders blocked can explain the results.

The project file is `/home/arkzhang/chinese_wiki_2018`. The data files is under `/data` and the code files is under `/code`. The raw data is `data/full_history.csv`. We use this file as the raw input to generate measures for leaders blocked (with leaders defined in various ways), gini coefficient and reverts. After generating these measures, we combine the data with `data/data_icwsm.csv`.

## Identify leaders
To identify leaders, run `get_blocked_frac.py`. This file requires and goes through `data/full_history.csv` and identifies leaders using
  1. geometric rules (tagged as origin in the code)
  2. inter-quartile rules (users whose level of activity is 1.5 inter-quartiles higher than the third quartile)
  This file generates `article_leader.csv`, which records blocked ratio of leaders.

  | Fieldname   | Remark |
  | ----------  |---------- |
  | `page_id` | id of article |
  | `page_name`   | name of article |
  | `page_ns` | namespace of article |
  | `blocked_frac` | fraction of editors blocked weighted by numrev |
  | `leader_block_frac_origin` | among the leaders defined by geometric rule, the fraction that is blocked weighted by numrev |
  | `block_frac_by_leader_origin` | among all editors blocked, the fraction of leaders defined by geometric rule weighted by numrev |
  | `leader_block_frac_iq` | among the leaders defined by 5iqr rule, the fraction that is blocked weighted by numrev |
  | `block_frac_by_leader_iq` | among all editors blocked, the fraction of leaders defined by 5iqr rule weighted by numrev |

## Analysis
`analysis.Rmd` is the main analysis file. At the current stage, this file
  1. combines the blocked ratio of leaders with the icwsm dataset
  2. replicate the 2017 study.
