# Data

The raw datasets are not stored in this repository. Download them from their owners and put the files
in one folder named `NIDS` (on Google Drive for Colab, or anywhere locally with `NIDS_DIR` pointing to it).

| File | Dataset | Source |
|---|---|---|
| `UNSW-NB15_1.csv` … `UNSW-NB15_4.csv` | UNSW-NB15 raw capture records | UNSW Canberra Cyber, <https://research.unsw.edu.au/projects/unsw-nb15-dataset> |
| `NUSW-NB15_features.csv` | UNSW-NB15 feature description | same as above |
| `MachineLearningCSV.zip` | CICIDS-2017, CICFlowMeter release (~235 MB) | Canadian Institute for Cybersecurity, <https://www.unb.ca/cic/datasets/ids-2017.html> |

Expected layout:

```
NIDS/
├── UNSW-NB15_1.csv
├── UNSW-NB15_2.csv
├── UNSW-NB15_3.csv
├── UNSW-NB15_4.csv
├── NUSW-NB15_features.csv
└── MachineLearningCSV.zip
```

Notes from the audit, worth knowing before you write your own loader:

* `NUSW-NB15_features.csv` spells one column `ct_src_ ltm` with an internal space.
* The attack label appears as both `Backdoor` and `Backdoors`; both must be mapped to one class.
* Ports can be hexadecimal strings; host and timestamp columns are used for ordering only, never as features.
