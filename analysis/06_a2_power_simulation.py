from __future__ import annotations
import argparse, math
from pathlib import Path
import numpy as np
from contextlib import nullcontext

def sigmoid(x):
    return 1/(1+np.exp(-x))

def exact_mcnemar_p(b,c):
    n=b+c
    if n==0: return 1.0
    k=min(b,c)
    tail=sum(math.comb(n,j) for j in range(k+1))/(2**n)
    return min(1.0,2*tail)

def power(N,beta,reps=4000,sigma_subject=.8,seed=20260818):
    rng=np.random.default_rng(seed+N+int(beta*1000))
    reject=0
    for _ in range(reps):
        a=rng.normal(0,sigma_subject,N)
        yA=rng.binomial(1,sigmoid(a+beta))
        yB=rng.binomial(1,sigmoid(a-beta))
        b=int(np.sum((yA==1)&(yB==0)))
        c=int(np.sum((yA==0)&(yB==1)))
        reject += exact_mcnemar_p(b,c)<.05
    return reject/reps

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--reps",type=int,default=4000)
    args=ap.parse_args()
    effects={
        "modest":math.log(.65/.35),
        "medium":math.log(.75/.25),
        "strong":math.log(.85/.15)
    }
    Ns=[8,12,16,20,24,32,40,50,64]
    for label,beta in effects.items():
        vals=[(N,power(N,beta,args.reps)) for N in Ns]
        print(label,vals)

if __name__=="__main__":
    main()
