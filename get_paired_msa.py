import numpy as np 
import sys
from collections import OrderedDict 
def parsefa(fain):
    records=OrderedDict()
    head,seq=None,[]
    with open(fain) as f:
        for line in f:
            if line.startswith(">"):
                if head is not None:
                    records[head]=''.join(seq)
                    seq=[]
                head=line.rstrip()[1:]
            else:
                seq.append(line.strip())
        if head is not None:
            records[head]=''.join(seq)
    return records
def key_tax(head:str)->str:
    m=re.search(r'\bTaxID[=:]\s*(\d+)\b',head)
    if m:
        return f"TAXID:{m.group(1)}"
    m=re.search(r'\bTax[=:]\s*([^=\s][^=]*?)(?:\s+\w+=|$)',head)
    if m:
        return "TAX:"+m.group(1).strip()
    return "ID:"+head[1:].split()[0]
def writefa(pairs,outfa):
    with open(outfa,'w') as out:
        for k,seq in pairs:
            out.write(f">{k}\n")
            for i in range(0,len(seq),80):
                out.write(seq[i:i+80]+"\n")
def pairmsa(hostaln,pathoaln,outfa,linkerlen=10,gap_cutoff=0.8):
    linker="X"*int(linkerlen)
    H=parsefa(hostaln)
    P=parsefa(pathoaln)
    def ftbygap(d):
        items=list(d.items())
        kept=OrderedDict()
        for head, seq in items:
            if seq.count("-")/float(len(seq))<=gap_cutoff:
                kept[head]=seq
        return kept 
    H=ftbygap(H)
    P=ftbygap(P)
    pairs=[]
    for hhead,hseq in H.items():
        for phead,pseq in P.items():
            pairs.append((f"{hhead}|{phead}",hseq+linker+pseq))
    with open(outfa,'w') as out:
        for k, seq in pairs:
            out.write(f">{k}\n")
            for i in range(0,len(seq),80):
                out.write(seq[i:i+80]+'\n')
if __name__=='__main__':
    hostaln=sys.argv[1]
    pathoaln=sys.argv[2]
    outfa=sys.argv[3]
    pairmsa(hostaln,pathoaln,outfa,linkerlen=10,gap_cutoff=0.8)
