#!/usr/bin/env python3
"""Extract Boltz confidence JSONs into a TSV with their file paths for traceability."""
import argparse
import csv
import json
from pathlib import Path

TARGETS={"confidence_score", "iptm", "ptm", "complex_plddt", "plddt", "ranking_score"}

def flatten_values(obj):
    found={}
    if isinstance(obj,dict):
        for k,v in obj.items():
            key=k.lower()
            if key in TARGETS and isinstance(v,(int,float)) and not isinstance(v,bool):
                found[key]=float(v)
            if isinstance(v,(dict,list)):
                for kk,vv in flatten_values(v).items(): found.setdefault(kk,vv)
    elif isinstance(obj,list):
        for v in obj:
            for kk,vv in flatten_values(v).items(): found.setdefault(kk,vv)
    return found

def scan(folder):
    data=[]
    for file in Path(folder).rglob('*.json'):
        if not (file.name.startswith('confidence_') or file.name.startswith('confidences_')):
            continue
        try: values=flatten_values(json.loads(file.read_text()))
        except (ValueError,UnicodeDecodeError): continue
        if not values: continue
        data.append({'model_file':str(file),**values})
    data.sort(key=lambda x:x.get('confidence_score',-1),reverse=True)
    return data

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('folder')
    ap.add_argument('--output',default='results/boltz_metrics_extracted.tsv')
    args=ap.parse_args(); data=scan(args.folder)
    if not data:
        ap.error('No supported confidence_*.json files found; check your Boltz version/output filenames')
    fields=['model_file']+sorted(set().union(*(set(x.keys()) for x in data)) - {'model_file'})
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t');w.writeheader();w.writerows(data)
    print(f'Saved {len(data)} confidence files to {out}')

if __name__=='__main__': main()
