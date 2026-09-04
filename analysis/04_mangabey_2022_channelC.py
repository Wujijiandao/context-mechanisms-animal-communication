from __future__ import annotations
import argparse, csv
from collections import Counter, defaultdict
from pathlib import Path
import sys, math
import numpy as np
from scipy import stats

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from contextmech.info import mutual_information, clopper_pearson


def response_category(r):
    if int(r["Snake"]) == 1:
        return "snake-like"
    if int(r["Leopard"]) == 1 or int(r["Move>10m"]) == 1:
        return "leopard-like"
    return "none"


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--assessment", default=str(ROOT/"data/processed_public/mangabey2022_first_assessment.csv"))
    ap.add_argument("--retest", default=str(ROOT/"data/processed_public/mangabey2022_retest_trials.csv"))
    ap.add_argument("--permutations",type=int,default=100000)
    args=ap.parse_args()

    with open(args.assessment,encoding="utf-8-sig",newline="") as f:
        raw=list(csv.DictReader(f,delimiter=";"))
    rows=[{k.strip():v.strip() for k,v in r.items()} for r in raw]
    h=np.array([r["stimuli"] for r in rows],dtype=object)
    rr=np.array([response_category(r) for r in rows],dtype=object)
    obs=mutual_information(h,rr)
    responders=[r for r in rows if response_category(r)!="none"]
    matches=sum(
        (r["stimuli"]=="Snake" and response_category(r)=="snake-like") or
        (r["stimuli"]=="Leopard" and response_category(r)=="leopard-like")
        for r in responders
    )

    strata=defaultdict(list)
    for i,r in enumerate(rows):
        strata[(r["age"],r["chimera_model"])].append(i)
    rng=np.random.default_rng(20260818)
    null=[]
    for _ in range(args.permutations):
        hp=h.copy()
        for inds in strata.values():
            labels=hp[inds].copy()
            rng.shuffle(labels)
            hp[inds]=labels
        null.append(mutual_information(hp,rr))
    null=np.asarray(null)
    p=(1+np.sum(null>=obs-1e-15))/(len(null)+1)

    print("I(history; delayed response) bits:",obs)
    print("stratified permutation p:",p,"null mean:",null.mean())
    print("category responders matched:",matches,"/",len(responders))

    # Retest CSV is a direct CSV export of the public workbook.
    with open(args.retest,encoding="utf-8-sig",newline="") as f:
        tab=list(csv.reader(f))
    records=tab[1:12]
    valid=[r for r in records if len(r)>=7 and r[4]!="–"]
    initial_specific=[r for r in valid if str(r[3]).startswith("1")]
    retained=[r for r in initial_specific if str(r[5]) in {"1","1.0"}]
    ci=clopper_pearson(len(retained),len(initial_specific))
    print("long-term category-specific retention:",len(retained),"/",len(initial_specific),"95% CI",ci)


if __name__=="__main__":
    main()
