"""Render the paper's two figures as PDFs, sized for the Springer LNCS text width (12.2 cm).

Input is the notebook's own output: the pooled confusion matrix from unsw_grid_folds.jsonl,
unsw_shap_global.csv and unsw_learning_curve.csv. Nothing is recomputed here.
"""
import json, os, sys
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

RES = sys.argv[1] if len(sys.argv) > 1 else "results/unsw"
GRID = sys.argv[2] if len(sys.argv) > 2 else os.path.join(RES, "unsw_grid_folds.jsonl")
DST = sys.argv[3] if len(sys.argv) > 3 else "figures"

SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
INK, INK2, MUTED, GRID_C, AXIS, SURFACE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7", "#ffffff"
BLUE_RAMP = ["#ffffff", "#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7", "#3987e5",
             "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b"]
SEQ_BLUE = mcolors.LinearSegmentedColormap.from_list("seq_blue", BLUE_RAMP)
plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "axes.edgecolor": AXIS, "axes.linewidth": 0.6, "axes.labelcolor": INK2, "text.color": INK,
    "xtick.color": MUTED, "ytick.color": MUTED, "xtick.labelcolor": INK2, "ytick.labelcolor": INK2,
    "axes.grid": True, "grid.color": GRID_C, "grid.linewidth": 0.6, "axes.axisbelow": True,
    "axes.spines.top": False, "axes.spines.right": False, "axes.titlesize": 7.5,
    "axes.titleweight": "bold", "axes.titlelocation": "left", "font.size": 6.5,
    "legend.frameon": False, "legend.fontsize": 6, "lines.linewidth": 1.2,
    "xtick.major.size": 2, "ytick.major.size": 2, "pdf.fonttype": 42,
})
CLASSES = ["Analysis", "Backdoors", "DoS", "Exploits", "Fuzzers", "Generic", "Normal",
           "Reconnaissance", "Shellcode", "Worms"]

# ---------------------------------------------------------------- Figure 1: confusion matrix
rows = [json.loads(l) for l in open(GRID)]
g = pd.DataFrame(rows).drop_duplicates(subset=["fold", "resampling", "model"])
g = g[(g.model == "XGB") & (g.resampling == "none")]
cm = np.sum(np.array(g["cm"].tolist()), axis=0).astype(float)
pct = cm / cm.sum(1, keepdims=True) * 100
print("confusion matrix from", len(g), "folds; support", int(cm.sum()))

fig, ax = plt.subplots(figsize=(4.8, 3.75))
ax.imshow(pct, cmap=SEQ_BLUE, norm=mcolors.Normalize(0, 100), aspect="auto")
ax.grid(False)
ax.set_xticks(range(10)); ax.set_xticklabels(CLASSES, rotation=42, ha="right", fontsize=6)
ax.set_yticks(range(10)); ax.set_yticklabels(CLASSES, fontsize=6)
ax.set_xlabel("Predicted class", fontsize=7); ax.set_ylabel("True class", fontsize=7)
for s in ax.spines.values():
    s.set_visible(False)
for i in range(10):
    for j in range(10):
        v = pct[i, j]
        if v < 0.05:
            continue
        ax.text(j, i, f"{v:.1f}" if v >= 0.95 else "<1", ha="center", va="center", fontsize=5.4,
                color="white" if v > 60 else INK)
fig.tight_layout(pad=0.4)
p1 = os.path.join(DST, "fig1_confusion.pdf")
fig.savefig(p1, bbox_inches="tight"); plt.close(fig)
print("wrote", p1)

# ---------------------------------------------------------------- Figure 2: SHAP + learning curve
shap_imp = pd.read_csv(os.path.join(RES, "unsw_shap_global.csv"))
lc = pd.read_csv(os.path.join(RES, "unsw_learning_curve.csv"))
fig, axes = plt.subplots(1, 2, figsize=(4.8, 2.2), gridspec_kw=dict(width_ratios=[1, 1.05], wspace=0.42))

top = shap_imp.head(12).iloc[::-1]
ax = axes[0]
ax.barh(np.arange(12), top.mean_abs_shap.values, height=0.68, color=SERIES[0])
ax.set_yticks(np.arange(12)); ax.set_yticklabels(top.feature.values, fontsize=5.6)
ax.set_xlabel("Mean |SHAP|", fontsize=6.5); ax.grid(axis="y", visible=False)
ax.set_title("Top 12 of 43 features", fontsize=7)
for y_, v, c_ in zip(np.arange(12), top.mean_abs_shap.values, top.cum_share_pct.values):
    ax.text(v + 0.02, y_, f"{c_:.0f}%", va="center", fontsize=5, color=INK2)
ax.set_xlim(0, shap_imp.mean_abs_shap.max() * 1.22)

ax = axes[1]
x1 = lc[lc.model == "XGB"].sort_values("n_train")
ax.plot(x1.n_train, x1.val_f1_macro, color=SERIES[0], marker="o", markersize=2.6, label="Macro F1")
ax.plot(x1.n_train, x1.recall_Exploits, color=SERIES[1], marker="s", markersize=2.4, label="Exploits recall")
ax.plot(x1.n_train, x1.recall_DoS, color=SERIES[2], marker="^", markersize=2.6, label="DoS recall")
ax.plot(x1.n_train, x1.recall_Analysis, color=SERIES[3], marker="v", markersize=2.6, label="Analysis recall")
ax.set_xscale("log"); ax.set_xlabel("Training records (log)", fontsize=6.5)
ax.set_ylabel("Macro F1 / recall (%)", fontsize=6.5); ax.set_ylim(0, 104)
ax.grid(axis="x", visible=False)
ax.legend(fontsize=5.4, loc="lower center", bbox_to_anchor=(0.5, -0.02), ncol=2,
          labelspacing=0.2, columnspacing=1.0, handlelength=1.4)
ax.set_title("Validation score against training size", fontsize=7)
fig.tight_layout(pad=0.4)
p2 = os.path.join(DST, "fig2_xai.pdf")
fig.savefig(p2, bbox_inches="tight"); plt.close(fig)
print("wrote", p2)
print("\ncheck: DoS recall", x1.recall_DoS.iloc[0].round(2), "->", x1.recall_DoS.iloc[-1].round(2),
      "| macro F1", x1.val_f1_macro.iloc[0].round(2), "->", x1.val_f1_macro.iloc[-1].round(2))
print("top-5 cumulative share", shap_imp.cum_share_pct.iloc[4], "top-10", shap_imp.cum_share_pct.iloc[9])
