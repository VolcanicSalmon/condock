import numpy as np
import random
import sys
import os
from typing import Dict 
def parse_js(jsin)->Dict[int,float]:
    poses_scores={}
    allposes=[]
    with open(jsin,'r') as input:
        lines=input.readlines()[1:]
        scores=[]
        for line in lines:
            if line.startswith('#'):
                continue
            pos=int(line.split('\t')[0].strip())
            score=float(line.split('\t')[1].strip())
            if score != -1000.0:
                poses_scores[pos]=score
            allposes.append(pos)
    if not poses_scores and allposes:
        poses_scores={pos : np.random.exponential(scale=1.0) for pos in allposes}
    return poses_scores
def js_distr(poses_scores,indexfile):
    keep=[]
    thres=np.quantile(np.array(list(poses_scores.values()),dtype=float),0.25)
    keep=[pos for pos, score in poses_scores.items() if score< thres]
    with open(indexfile,'w') as output:
        for index in keep:
            output.write(f"{index} ")
        output.write(f"\n \n")
if __name__=='__main__':
    jsin=sys.argv[1]
    indexfile=sys.argv[2]
    js_distr(parse_js(jsin),indexfile)
