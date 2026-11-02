#!/usr/bin/env python3
"""Prepare one GitHub issue per task. Default dry run; --apply writes issues.

Requires git and, for --apply, authenticated gh. Matches open AND closed issues
by whole T### identifiers, including T1000. The configured origin must match
--repo exactly. Never closes or modifies the parent issue.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from check_tasks import parse_tasks, ID

def run(args,cwd):
    r=subprocess.run(args,cwd=cwd,text=True,capture_output=True)
    if r.returncode:raise ValueError(f'{args[0]} failed ({r.returncode}): {r.stderr.strip()}')
    return r.stdout

def remote_repo(value):
    m=re.fullmatch(r'(?:https://github\.com/|git@github\.com:|ssh://git@github\.com/)([^/\s]+/[^/\s]+?)(?:\.git)?/?',value.strip())
    if not m:raise ValueError('origin must be an unambiguous github.com HTTPS or SSH repository URL')
    return m[1]

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('tasks');p.add_argument('--root',default='.');p.add_argument('--repo',required=True);p.add_argument('--apply',action='store_true');p.add_argument('--parent',default='');a=p.parse_args()
    try:
        if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',a.repo):raise ValueError('--repo must be owner/repository')
        root=Path(a.root).resolve();tasks_path=Path(a.tasks).resolve()
        tasks_path.relative_to(root)
        tasks,errors=parse_tasks(tasks_path)
        if errors:raise ValueError('; '.join(errors))
        origin=remote_repo(run(['git','remote','get-url','origin'],root))
        if origin.casefold()!=a.repo.casefold():raise ValueError(f'origin {origin} differs from requested repository {a.repo}')
        ordered=[]; emitted=set(); by_id={t['id']:t for t in tasks}
        def emit(t):
            if t['id'] in emitted:return
            for dep in t['blocked_by']:emit(by_id[dep])
            emitted.add(t['id']);ordered.append(t)
        for task in tasks:emit(task)
        pending=[t for t in ordered if not t['done']]
        if not a.apply:
            print(json.dumps({'mode':'dry-run','repository':a.repo,'remote':origin,'source':str(tasks_path),'would_create':pending,'deduplication':'not queried in offline dry run; --apply checks open and closed issues before each creation wave'},indent=2));return 0
        run(['gh','auth','status','--hostname','github.com'],root)
        pages=json.loads(run(['gh','api','--hostname','github.com','--paginate','--slurp',f'repos/{a.repo}/issues?state=all&per_page=100'],root))
        issues=[i for page in pages for i in (page if isinstance(page,list) else [page])]
        if any(not isinstance(i,dict) or not isinstance(i.get('title'),str) for i in issues):raise ValueError('unexpected issue-list response; no issues created')
        existing=set(); issue_numbers={}
        for issue in issues:
            if 'pull_request' not in issue:
                for tid in ID.findall(issue['title']):
                    existing.add(tid);issue_numbers[tid]=issue.get('number')
        created=[];skipped=[]
        for task in pending:
            tid=task['id']
            if tid in existing:skipped.append(tid);continue
            body=f"## Task\n\n{tid}: {task['description']}\n\n## Source\n\n{tasks_path.relative_to(root).as_posix()}:{task['line']}\n"
            if a.parent:body+=f'\n## Parent\n\n{a.parent}\n'
            if task['blocked_by']:body+='\n## Blocked by\n\n'+''.join(f'- {x}'+(f' (#{issue_numbers[x]})' if issue_numbers.get(x) else '')+'\n' for x in task['blocked_by'])
            payload={'title':f"{tid}: {task['description']}",'body':body}
            r=subprocess.run(['gh','api','--hostname','github.com','--method','POST',f'repos/{a.repo}/issues','--input','-'],cwd=root,text=True,input=json.dumps(payload),capture_output=True)
            if r.returncode:raise ValueError(f'issue creation stopped at {tid}; earlier creations remain: {created}; {r.stderr.strip()}')
            issue=json.loads(r.stdout)
            if not issue.get('html_url') or not issue.get('number'):raise ValueError(f'uncertain creation outcome for {tid}; reread the repository before retrying')
            created.append({'task':tid,'number':issue['number'],'url':issue['html_url']});existing.add(tid);issue_numbers[tid]=issue['number']
        print(json.dumps({'mode':'applied','repository':a.repo,'created':created,'skipped':skipped},indent=2));return 0
    except (OSError,ValueError,json.JSONDecodeError) as exc:print(f'error: {exc}',file=sys.stderr);return 2
if __name__=='__main__':sys.exit(main())
