#!/usr/bin/env python3
"""Read-only task format, identity and dependency gate. Exit 1 on invalid tasks."""
import argparse
import json
import re
import sys
from pathlib import Path
TASK=re.compile(r'^\s*- \[([ xX])\]\s+(T\d{3,})\b\s*(.*)$')
ID=re.compile(r'\bT\d{3,}\b')

def parse_tasks(path):
    tasks=[]; errors=[]; fence=False; seen=set()
    for n,line in enumerate(Path(path).read_text(encoding='utf-8').splitlines(),1):
        if line.lstrip().startswith(('```','~~~')):fence=not fence;continue
        if fence:continue
        m=TASK.match(line)
        if not m:
            if re.match(r'^\s*- \[[ xX]\]',line):errors.append(f'line {n}: task needs T followed by at least three digits')
            continue
        checked,tid,desc=m.groups()
        if tid in seen:errors.append(f'line {n}: duplicate task id {tid}')
        seen.add(tid)
        if re.search(r'(?i)blocked by.*\b'+re.escape(tid)+r'\b',desc):errors.append(f'{tid}: task blocks itself')
        if not desc.strip():errors.append(f'line {n}: empty task description')
        tasks.append({'id':tid,'description':desc,'done':checked.lower()=='x','line':n,
                      'blocked_by':list(dict.fromkeys(x for x in ID.findall(desc) if x!=tid))})
    if not tasks:errors.append('no tasks found')
    edges={t['id']:t['blocked_by'] for t in tasks}
    for t in tasks:
        for dep in t['blocked_by']:
            if dep not in edges:errors.append(f"{t['id']}: unknown dependency {dep}")
    visiting=set();visited=set()
    def visit(tid):
        if tid in visiting:errors.append(f'dependency cycle at {tid}');return
        if tid in visited:return
        visiting.add(tid)
        for dep in edges.get(tid,[]):visit(dep)
        visiting.remove(tid);visited.add(tid)
    for tid in edges:visit(tid)
    return tasks,errors

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('tasks');p.add_argument('--json',action='store_true');a=p.parse_args()
    try:tasks,errors=parse_tasks(a.tasks)
    except (OSError,UnicodeError) as exc:print(f'error: {exc}',file=sys.stderr);return 2
    result={'status':'FAIL' if errors else 'PASS','tasks':tasks,'errors':errors}
    print(json.dumps(result,indent=2) if a.json else '\n'.join(errors) if errors else f'PASS: {len(tasks)} unique tasks; dependency graph is acyclic')
    return bool(errors)
if __name__=='__main__':sys.exit(main())
