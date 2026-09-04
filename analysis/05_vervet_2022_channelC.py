from __future__ import annotations
import argparse, csv, math
from pathlib import Path
import numpy as np
from scipy import stats


def main():
    root=Path(__file__).resolve().parents[1]
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",default=str(root/"data/processed_public/vervet2022_one_trial_GLMM.csv"))
    args=ap.parse_args()
    with open(args.input,encoding="utf-8-sig",newline="") as f:
        rows=[{k.strip():v.strip() for k,v in r.items()} for r in csv.DictReader(f)]

    rows=[r for r in rows if float(r["Insight"])>200]
    for var in ["Dist_STRT","Exp_time","Order"]:
        arr=np.array([float(r[var]) for r in rows])
        m,sd=arr.mean(),arr.std(ddof=1)
        for r in rows:
            r["z."+var]=(float(r[var])-m)/sd

    x=[r for r in rows if r["Treatment"]!="Grunt Playback"]
    X=[]; y=[]
    for r in x:
        X.append([
            1.0,
            1.0 if r["Treatment"]=="Leopard Alarm Playback (Alarm)" else 0.0,
            1.0 if r["Predator"]=="Horse" else 0.0,
            1.0 if r["Age"]=="Juveniles" else 0.0,
            1.0 if r["Group"]=="BD" else 0.0,
            r["z.Dist_STRT"],r["z.Order"],r["z.Exp_time"]
        ])
        y.append(math.log(float(r["Pre_Inspection"])))
    X=np.asarray(X); y=np.asarray(y)
    rank=np.linalg.matrix_rank(X)
    beta=np.linalg.lstsq(X,y,rcond=None)[0]
    resid=y-X@beta
    df=len(y)-rank
    s2=(resid@resid)/df
    cov=s2*np.linalg.pinv(X.T@X)
    se=np.sqrt(np.diag(cov))
    t=beta[1]/se[1]
    partial_p=2*stats.t.sf(abs(t),df)

    # Type-I sequential effect with treatment first.
    X0=np.ones((len(y),1))
    X1=np.column_stack([np.ones(len(y)),X[:,1]])
    def rss(M):
        b=np.linalg.lstsq(M,y,rcond=None)[0]
        r=y-M@b
        return float(r@r),np.linalg.matrix_rank(M)
    rss0,r0=rss(X0); rss1,r1=rss(X1); rssf,rf=rss(X)
    mse=rssf/(len(y)-rf)
    seqF=((rss0-rss1)/(r1-r0))/mse
    seqp=stats.f.sf(seqF,r1-r0,len(y)-rf)

    alarm=np.array([float(r["Pre_Inspection"]) for r in x if r["Treatment"].startswith("Leopard")])
    silent=np.array([float(r["Pre_Inspection"]) for r in x if r["Treatment"].startswith("No Playback")])
    print("n:",len(x),"alarm/silent:",len(alarm),len(silent))
    print("raw means:",alarm.mean(),silent.mean())
    print("exact Mann-Whitney p:",stats.mannwhitneyu(alarm,silent,alternative="two-sided",method="exact").pvalue)
    print("Type-I sequential treatment F,p:",seqF,seqp)
    print("partial treatment coefficient,p,ratio:",beta[1],partial_p,math.exp(beta[1]))


if __name__=="__main__":
    main()
