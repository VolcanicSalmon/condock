import re
import zipfile
import os
import sys
zipdir=sys.argv[1]
outdir=sys.argv[2]
os.makedirs(outdir,exist_ok=True)
RANK_RE = re.compile(r"rank(?:ed)?[_-]?0*(\d+)", re.IGNORECASE)
def get_rank0(files):
    pdbs=[file for file in files if file.lower().endswith(".pdb")]
    if not pdbs:
        return None
    def ranking(file):
        m=RANK_RE.search(file)
        return int(m.group(1)) if m else 10**9 
    def relaxed(file):
        return 1 if re.search(r"\bunrelaxed\b",file) else 0 
    rankfiles=[file for file in pdbs if re.search(r"rank[_-]0*1\b",file)]
    rankfiles=rankfiles if rankfiles else pdbs 
    rankfiles.sort(key=lambda f:(ranking(f),relaxed(f)))
    return rankfiles[0]
for z in os.listdir(zipdir):
    if not z.endswith("zip"):
        continue 
    zippath=os.path.join(zipdir,z)
    with zipfile.ZipFile(zippath) as zipin:
        best=get_rank0(zipin.namelist())
        if not best:
            continue 
        outname=os.path.splitext(z)[0]+".pdb"
        outpath=os.path.join(outdir,outname)
        with zipin.open(best) as toget,open(outpath,'wb') as dest:
            dest.write(toget.read())
