UNSW-NB15 results from the revised run (real capture files, seed 42).

Everything here was produced by NIDS_Full_Methodology_Notebook.ipynb on the four raw
UNSW-NB15 files. The CICIDS-2017 and merged-pool outputs are not included: they need the
235 MB MachineLearningCSV.zip, so they come from the Colab run.

New in this run
  unsw_stratified_leakage_audit.csv   how much of each validation fold has a training copy
  unsw_duplicate_audit.csv            duplicates per class, both variants
  unsw_grouped_fold_audit.csv         proof that no feature vector spans a grouped fold
  unsw_protocol_folds.jsonl           every fit under every split protocol
  table3b_protocol_comparison.csv     the paper's protocol table
  unsw_per_class_recall_by_protocol.csv  which classes the protocol moves
  unsw_day_composition.csv            records per class on each capture day
  unsw_split_composition.csv          class counts on both sides of each single split
  unsw_tenfold_folds.jsonl            the ten-fold resampling grid
  unsw_tenfold_significance.csv       paired t-test and exact Wilcoxon, ten folds
  unsw_paired_ttests.csv              both tests on the five-fold grid
  unsw_shap_global.csv                mean |SHAP| per feature, with cumulative share
  unsw_shap_per_class.csv             mean |SHAP| per feature for each class output
  unsw_learning_curve.csv             macro F1 and per-class recall against training size
  paper_vs_notebook_ledger.csv        every paper number against this run
  figures/                            PNG for reading, PDF for LaTeX

paper_vs_notebook_ledger.csv: all 269 UNSW-side entries match. The rows marked DIFFERS in the
full ledger are CICIDS-2017 and merged-pool numbers, which this run computed on a small
schema-matched stand-in rather than the real corpus.
