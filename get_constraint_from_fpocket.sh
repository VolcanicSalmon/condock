{ grep '^ATOM' *atm.pdb | awk '{print substr($0, 23, 4)}' | sort -u -n |xargs ; echo ; } > active.txt

~/.local/bin/haddock3-restraints active_passive_to_ambig active.txt ../../../cadpr_active.txt --segid-one A --segid-two Z > restraint.txt
