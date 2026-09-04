from __future__ import annotations
import argparse, csv
from collections import defaultdict
from pathlib import Path
import sys
import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"src"))
from contextmech.broja import broja_pid
from contextmech.info import exact_signflip_mean


def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def build_sequences(rows):
    seqs = defaultdict(list)
    meta = {}
    for r in rows:
        sid = str(r["Seq1"])
        seqs[sid].append((int(float(r["Nb_call"])), r["Type_call"]))
        meta[sid] = (r["Cat_preda"], r["Location"], r["Group"], r["Ind"])
    out = []
    for sid, calls in seqs.items():
        calls = "".join(x[1] for x in sorted(calls))
        z,c,g,ind = meta[sid]
        out.append((sid,z,c,g,ind,calls))
    return out


def bigram_distribution(seqs):
    recs=[]
    n=len(seqs)
    for _,z,c,_,_,s in seqs:
        grams=[s[i:i+2] for i in range(len(s)-1)]
        counts={gram:grams.count(gram) for gram in ["AA","AB","BA","BB"]}
        denom=sum(counts.values())
        if denom == 0:
            continue
        # Match the retained v0.8 analysis: bigrams involving C are excluded,
        # but A/B calls separated by C are NOT collapsed into a new adjacency.
        for gram,count in counts.items():
            p=count/denom
            if p:
                recs.append((z,gram,c,(1/n)*p))
    return recs


def playback_up_effect(gaze_rows):
    by_trial = defaultdict(lambda: defaultdict(float))
    meta = {}
    for r in gaze_rows:
        trial = r["Videos"]
        by_trial[trial][r["Gaze"]] += float(r["Duration"])
        meta[trial] = (r["Ind"], r["Loca"], r["Preda"])
    p_up = {}
    for trial,d in by_trial.items():
        total=sum(d.values())
        p_up[trial]=d.get("Up",0.0)/total if total else np.nan
    by_subject=defaultdict(dict)
    for trial,(ind,loca,preda) in meta.items():
        by_subject[ind][loca]=p_up[trial]
    diffs=[]
    for ind,d in by_subject.items():
        if "Up" in d and "Down" in d:
            diffs.append(d["Up"]-d["Down"])
    obs,p=exact_signflip_mean(diffs,alternative="greater")
    return obs,p,len(diffs)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--production", default=str(ROOT/"data/processed_public/bert2019_predator_presentations.csv"))
    ap.add_argument("--gaze", default=str(ROOT/"data/processed_public/bert2019_gaze_playbacks.csv"))
    args=ap.parse_args()
    seqs=build_sequences(read_csv(args.production))
    print("production sequences:",len(seqs))
    print("bigram BROJA:",broja_pid(bigram_distribution(seqs)))
    effect,p,n=playback_up_effect(read_csv(args.gaze))
    print("paired canopy(Up)-ground(Down) upward-gaze effect:",effect,"one-sided exact signflip p=",p,"n=",n)


if __name__=="__main__":
    main()
