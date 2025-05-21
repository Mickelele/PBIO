#!/usr/bin/env python3
from Bio import Entrez, SeqIO
import pandas as pd
import matplotlib.pyplot as plt
def main():
    e, k, t, l1, l2 = input("Email: "), input("Key: "), input("TaxID: "), int(input("Min len: ")), int(input("Max len: "))
    Entrez.email, Entrez.api_key, Entrez.tool = e, k, 'T'
    try:
        r = Entrez.read(Entrez.esearch(db="nucleotide", term=f"txid{t}[Organism] AND {l1}:{l2}[Sequence Length]", usehistory="y"))
        if (c := int(r["Count"])) == 0: return print("0 recs.")
        e2, qk = r["WebEnv"], r["QueryKey"]
        recs = list(SeqIO.parse(Entrez.efetch(db="nucleotide", rettype="gb", retmode="text", retstart=0, retmax=20, webenv=e2, query_key=qk), "genbank"))
        if recs:
            SeqIO.write(recs, f"t{t}.gb", "genbank")
            pd.DataFrame([{"A": x.id, "L": len(x.seq), "D": x.description} for x in recs]).sort_values("L", ascending=False).to_csv(f"t{t}.csv", index=0)
            df = pd.DataFrame([{"A": x.id, "L": len(x.seq)} for x in recs])
            df.plot(x="A", y="L", marker="o", linestyle="-", rot=90, figsize=(12,6))
            plt.tight_layout(); plt.savefig(f"t{t}.png")
    except Exception as e:
        print("")
if __name__ == "__main__": main()
