import os
import argparse
from collections import OrderedDict
import json

def parsefa(fain):
    records = OrderedDict()
    head, seq = None, []
    with open(fain) as f:
        for line in f:
            if line.startswith(">"):
                if head is not None:
                    records[head] = ''.join(seq)
                    seq = []
                head = line.rstrip()[1:]  # Remove '>'
            else:
                seq.append(line.strip())
        if head is not None:
            records[head] = ''.join(seq)
    return records

def find_A1(rnaseq):
    try:
        return rnaseq.index('A') + 1
    except ValueError:
        raise ValueError('There is no A')

def write_json(protseq, rnaseq, ccd, apos, jobname, outfile, include_covalent_bonds=True):
    rna_modifications = [
        {
            "modificationType": ccd,
            "basePosition": apos
        }
    ] if ccd else []

    data = {
        "name": jobname,
        "sequences": [
            {
                "rnaSequence": {
                    "count": 1,
                    "sequence": rnaseq,
                    "modifications": rna_modifications
                }
            },
            {
                "proteinChain": {
                    "count": 1,
                    "sequence": protseq,
                    "modifications": []
                }
            }
        ],
        "constraint": {},
        "N_sample": 2,
        "N_cycle": 5,
        "N_step": 100,
        "model_seeds": 2000
    }

    if include_covalent_bonds and ccd:
        data["covalent_bonds"] = [
            {
                "entity1": 1,
                "position1": apos,
                "copy1": 1,
                "atom1": "N6",
                "entity2": 1,
                "position2": apos,
                "atom2": "C1'",
                "copy2": 1
            }
        ]
    else:
        data["covalent_bonds"] = []

    with open(outfile, 'w') as output:
        json.dump(data, output, indent=4)

def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--protseq', required=True)
    parser.add_argument('--rnaseq', required=True)
    parser.add_argument('--ccd', default='')
    parser.add_argument('--jobname', required=True)
    parser.add_argument('--outdir', default='.')
    parser.add_argument('--include_covalent_bonds', action='store_true', help="Include covalent bonds in the output (optional)")
    return parser.parse_args()
if __name__ == '__main__':
    args = read_args()
    prot_records = parsefa(args.protseq)
    rna_records = parsefa(args.rnaseq)

    for prothead, indprot in prot_records.items():
        for rnahead, indrna in rna_records.items():
            try:
                apos = find_A1(indrna)
            except ValueError as e:
                print(f"Skipping {rnahead}: {e}")
                continue

            outfile = os.path.join(args.outdir, f"{args.jobname}_{prothead}_{rnahead}_protenix.json")
            write_json(indprot, indrna, args.ccd, apos, f"{args.jobname}_{prothead}_{rnahead}", outfile, args.include_covalent_bonds)
