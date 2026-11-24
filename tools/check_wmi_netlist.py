#!/usr/bin/env python3
"""Compare WMI expected CSV with KiCad native S-expression netlist."""
import argparse, csv, re, sys
from pathlib import Path

def parse(text):
    stack=[]; root=[]; current=root
    for t in re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()"]+',text):
        if t=='(': 
            child=[]; current.append(child); stack.append(current); current=child
        elif t==')': current=stack.pop()
        else: current.append(t[1:-1] if t.startswith('"') else t)
    if stack or len(root)!=1: raise ValueError('Invalid netlist')
    return root[0]

def children(n,k): return [x for x in n if isinstance(x,list) and x and x[0]==k]
def field(n,k): return children(n,k)[0][1]
def check(csvfile,netfile,sheet):
    expected={}
    with open(csvfile,newline='') as f:
        for r in csv.DictReader(f):
            key=(r['reference'],r['logical_pin'])
            if key in expected: raise ValueError(f'Duplicate expected terminal {key}')
            expected[key]=r['local_net']
    root=parse(Path(netfile).read_text()); actual={}; errors=[]; groups={}
    for net in children(children(root,'nets')[0],'net'):
        name=field(net,'name'); nodes=children(net,'node')
        for node in nodes:
            key=(field(node,'ref'),field(node,'pin'))
            if key[0].startswith('#'): continue
            if key in actual: errors.append(f'Duplicate actual terminal {key}')
            actual[key]=name
            if name.startswith('unconnected-') and len(nodes)==1 and 'no_connect' in field(node,'pintype'):
                actual[key]='NC'
        groups[name]=nodes
    for key,want in expected.items():
        target='NC' if want=='NC' else sheet.rstrip('/')+'/'+want
        if actual.get(key)!=target: errors.append(f'{key}: expected {target}, got {actual.get(key)}')
    refs={k[0] for k in expected}
    for key,name in actual.items():
        if key not in expected and (key[0] in refs or name.startswith(sheet.rstrip('/')+'/')):
            errors.append(f'Unexpected terminal {key}: {name}')
    for e in errors: print('FAIL:',e)
    print(f'{len(expected)} expected terminals; {len(errors)} discrepancies')
    return bool(errors)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('expected'); p.add_argument('netlist'); p.add_argument('--sheet',default='/WMI-PWR'); a=p.parse_args()
    try: sys.exit(int(check(a.expected,a.netlist,a.sheet)))
    except (ValueError,KeyError,IndexError,OSError) as e: print(f'ERROR: {e}',file=sys.stderr); sys.exit(2)
