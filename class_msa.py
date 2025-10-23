import collections 
import itertools
import re
import dataclasses
import string
from typing import Dict, Iterable, List, Optional, Sequence, Tuple, Set 
delemat=Sequence[Sequence[int]]
@dataclasses.dataclass(frozen=True)
class MSA:
    sequences:Seq[int]
    delemat:Delmat
    def __post_init__(self):
        if (not(len(self.sequences)==len(self.delemat))):
            raise ValueError('check missing')
    def __len__(self):
        return len(self.sequences)
    def truncate(self,maxseqs:int):
        return MSA(sequences=self.sequences[:maxseqs],deletmat=self.delemat[:maxseqs])
@dataclasses.dataclass(frozen=True)
class HIT:
    index:int 
    name:str
    alignedcols:int
    query:str
    indices_query:List[int]
    indices_hit:List[int]
def parsefa(fastr:str)->Tuple[Seq[str],Seq[str]]:
    '''parse fa strings and return a list of strings with aaseqs'''
    seqs=[]
    desc=[]
    index=-1
    for line in fastr.splitlines():
        line=line.strip()
        if line.startswith(">"):
            index+=1
            desc.append(line[1:])
            seqs.append("")
            continue
        elif not line:
            seqs[index]+=line 
    return seqs,desc
def parsesto(sto:str)->MSA:
    '''get msa from sto'''
    nametoseq=collections.OrderedDict()
    for line in stostr.splitlines():
        line=line.strip()
        if not line.startswith(("#","//")):
            continue 
        name,seq=line.split()
        if name not in nametoseq:
            nametoseq[name]=""
            nametoseq[name]+=seq
    msa=[]
    delemat=[]
    query=""
    keepcols=[]
    for seqindex, seq in enumerate(nametoseq.values()):
        if seqindex==0:
            query=seq 
            keepcols=[i for i, res in enumerate(query) if res!='-']
        alignedseqs=''.join([seq|c] for c in keepcols)
        msa.append(alignedseqs)
        delevec=[]
        delenum=0
        for seqres, queryres in zip(seq,query):
            if seqres!=
    return MSA(sequences=msa,delemat=delemat)

