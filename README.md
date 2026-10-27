# Unified Multiclass and Cross-Corpus Evaluation of UNSW-NB15 and CICIDS-2017

Code and results for the paper **"Unified Multiclass and Cross-Corpus Evaluation of UNSW-NB15 and
CICIDS-2017"**, submitted to the *2027 7th International Conference on Electrical Engineering and
Information & Communication Technology (ICEEICT 2027)* and currently under review.

> Much of the difficulty usually attributed to an intrusion detector is a property of its corpus.

## What this study does

Published intrusion detection results on UNSW-NB15 and CICIDS-2017 usually come from a single train/test
split, lead with accuracy, and rarely measure the two datasets under one protocol. This repository
evaluates both under **one protocol**:

* stratified 5-fold cross-validation (seed 42), every learned transform fitted on the training fold only;
* **macro AUC-PR** as the primary metric, with accuracy and macro precision, recall and F1;
* capped SMOTE / ADASYN applied to training folds only, compared with a paired t-test and an exact
  Wilcoxon signed-rank test (repeated with ten folds so the test can resolve below p = 0.05);
* five classifiers: Random Forest, XGBoost, LightGBM, TabNet and FT-Transformer;
* a **merged pool** of the four classes the corpora share, and **cross-corpus transfer** in both directions;
* audits of the protocol itself: duplicates and label conflicts, grouped folds, de-duplicated folds,
  time-ordered and per-capture-day splits, SHAP attribution and learning curves.

## Headline results

| Setting | Accuracy | Macro F1 |
|---|---|---|
| UNSW-NB15, XGBoost, no resampling (5-fold CV) | 88.38% | 67.05% |
| CICIDS-2017, capped pool, SMOTE (5-fold CV) | 99.93% | 99.63% |
| Merged pool (4 shared classes), SMOTE | 99.36% | 79.17% |
| Train on one corpus, test on the other | — | ~25% (24.90% / 25.48%) |

* On the merged pool, Backdoor recall is only 33.48%, and it is **zero in both transfer directions**:
  models learn capture-specific statistics rather than transferable attack signatures.
* A model-free analysis of feature-vector conflicts shows that **15.06%** of UNSW-NB15 records sit on
  conflicted vectors (overall accuracy ceiling 91.58%); Analysis and Backdoors are within 6.4 points of
  the best recall any deterministic classifier could reach.
* **40.83%** of every stratified validation fold has an exact copy in its own training fold. Separating
  exact duplicates moves macro F1 by 0.34 points; holding out a capture day moves it by 9.51, almost
  entirely on minority classes.

UNSW-NB15 model comparison (mean ± sd over five folds; `results/unsw/table2_unsw_complete.csv`):

| Model | Resampling | Accuracy | Macro F1 | Macro AUC-PR |
|---|---|---|---|---|
| Random Forest | none | 87.53 ± 0.12 | 65.05 ± 1.45 | 68.90 ± 1.36 |
| XGBoost | none | 88.38 ± 0.12 | **67.05 ± 1.24** | 70.95 ± 0.81 |
| LightGBM | SMOTE | **88.51 ± 0.08** | 66.37 ± 1.34 | **71.69 ± 1.72** |
| TabNet | none | 86.89 ± 0.20 | 54.06 ± 0.65 | 62.96 ± 0.73 |
| FT-Transformer | none | 82.15 ± 0.89 | 37.48 ± 3.65 | 46.22 ± 2.59 |

## Repository layout

```
notebooks/nids_full_methodology.ipynb   every experiment, table and figure, raw files to final numbers
scripts/paper_figs.py                   rebuilds the paper's Figure 1 and Figure 2 from the CSV output
results/unsw/                           tables, per-fold logs (.jsonl) and figures of the reference UNSW-NB15 run
data/README.md                          where to download the datasets and the expected folder layout
requirements.txt                        library versions used for the paper
```

The notebook follows the paper's order: **Part 1** UNSW-NB15, **Part 2** CICIDS-2017, **Part 3** the merged
pool and cross-corpus transfer, **Part 4** summary tables, discussion numbers and a paper-versus-notebook
consistency ledger. Its first cell maps every section and table of the paper to the cell that produces it.

## Reproducing the results

**Google Colab (recommended).**
1. Download the datasets as described in [`data/README.md`](data/README.md) into a Google Drive folder named `NIDS`.
2. Open `notebooks/nids_full_methodology.ipynb` in Colab and choose `Runtime > Run all`; allow Drive access.
3. Results and figures are written to `NIDS/results_final/`. Every expensive loop checkpoints after each
   fold, so after a disconnect a re-run reuses finished folds.

**Locally.**
```bash
pip install -r requirements.txt
export NIDS_DIR=/path/to/NIDS          # folder with the raw files
jupyter nbconvert --to notebook --execute notebooks/nids_full_methodology.ipynb
```

Runtime is roughly 4–5 hours on a free CPU runtime from scratch; set `RUN_TENFOLD = False` in cell 0.2 to skip
the ten-fold significance repeat. A GPU only speeds up the two neural models.

Regenerate the paper figures from a results folder:
```bash
python scripts/paper_figs.py results/unsw results/unsw/unsw_grid_folds.jsonl figures
```

## About the included results

`results/unsw/` is the reference UNSW-NB15 run on the four raw capture files (seed 42); all 269
UNSW-NB15 entries of `paper_vs_notebook_ledger.csv` match the paper. The CICIDS-2017 and merged-pool numbers
need the 235 MB `MachineLearningCSV.zip` and are produced by the full Colab run; the rows marked `DIFFERS` in
the ledger come from a small schema-matched stand-in used only to test the code path, not from the real
corpus. Across machines, XGBoost and SMOTE/ADASYN means can differ by up to about one point because of
floating-point order; the direction of every effect is unchanged.

## Citation

The paper is under review; citation details will be added after the decision. Until then, see
[`CITATION.cff`](CITATION.cff).

## License

Code is released under the [MIT License](LICENSE). The datasets belong to their creators (UNSW Canberra
Cyber; Canadian Institute for Cybersecurity) and are subject to their own terms.
