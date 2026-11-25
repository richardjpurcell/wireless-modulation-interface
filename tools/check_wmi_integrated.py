#!/usr/bin/env python3
"""Compare the full integrated netlist with the independently specified terminal register."""
import argparse,csv,sys
from pathlib import Path
from check_wmi_netlist import parse,children,field

def check(register,netlist):
    expected={};actual={};errors=[]
    with open(register,newline='') as f:
        for r in csv.DictReader(f):
            k=(r['reference'],r['logical_pin'])
            if k in expected:raise ValueError(f'Duplicate expected terminal {k}')
            expected[k]=r['expected_net']
    root=parse(Path(netlist).read_text())
    for net in children(children(root,'nets')[0],'net'):
        n=field(net,'name');nodes=children(net,'node')
        for node in nodes:
            k=(field(node,'ref'),field(node,'pin'))
            if k[0].startswith('#'):continue
            if k in actual:errors.append(f'Duplicate actual terminal {k}')
            actual[k]='NC' if n.startswith('unconnected-') and len(nodes)==1 and 'no_connect' in field(node,'pintype') else n
    for k,v in expected.items():
        if actual.get(k)!=v:errors.append(f'{k}: expected {v}, got {actual.get(k)}')
    for k in actual.keys()-expected.keys():errors.append(f'Unexpected terminal {k}: {actual[k]}')
    # Check component inventory as well, including components with no exported net nodes.
    refs={k[0] for k in expected}
    comps={field(c,'ref') for c in children(children(root,'components')[0],'comp') if not field(c,'ref').startswith('#')}
    for ref in sorted(comps-refs):errors.append(f'Unexpected component {ref}')
    for ref in sorted(refs-comps):errors.append(f'Missing component {ref}')
    for e in errors:print('FAIL:',e)
    print(f'{len(expected)} expected terminals; {len(errors)} discrepancies')
    return bool(errors)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('expected');p.add_argument('netlist');a=p.parse_args()
    try:sys.exit(int(check(a.expected,a.netlist)))
    except (ValueError,KeyError,IndexError,OSError) as e:print(f'ERROR: {e}',file=sys.stderr);sys.exit(2)
