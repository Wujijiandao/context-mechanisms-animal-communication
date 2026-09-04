from __future__ import annotations
import argparse, csv, math
from collections import defaultdict
from pathlib import Path
import sys
import numpy as np
from scipy import stats

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from contextmech.info import exact_signflip_mean, exact_mcnemar


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input", default=str(ROOT/"data/processed_public/vervet2023_context_data.csv"))
    args=ap.parse_args()
    with open(args.input,encoding="utf-8-sig",newline="") as f:
        rows=list(csv.DictReader(f))
    pairs=defaultdict(dict)
    for r in rows:
        pairs[r["Subject"]][r["Treatment"]]=r
    look=[]; vig=[]; st=[]
    for s,d in sorted(pairs.items()):
        e,c=d["Experiment"],d["Control"]   # Experiment=BGE; Control=non-BGE
        look.append(float(c["LK_Speaker"])-float(e["LK_Speaker"]))
        vig.append(float(c["Vigilance"])-float(e["Vigilance"]))
        st.append((int(c["Startle"]),int(e["Startle"])))
    look=np.asarray(look); vig=np.asarray(vig)
    print("looking mean diff:",look.mean(),"Wilcoxon:",stats.wilcoxon(look).pvalue,
          "exact signflip:",exact_signflip_mean(look)[1])
    print("vigilance mean diff:",vig.mean(),"Wilcoxon:",stats.wilcoxon(vig).pvalue,
          "exact signflip:",exact_signflip_mean(vig)[1])
    b=sum(a==1 and z==0 for a,z in st)
    c=sum(a==0 and z==1 for a,z in st)
    print("startle discordant:",b,c,"exact McNemar:",exact_mcnemar(b,c))


if __name__=="__main__":
    main()
