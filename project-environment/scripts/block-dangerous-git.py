#!/usr/bin/env python3
"""Parse the shell hook's JSON and static command tokens without executing them.

Exit 2 blocks a documented dangerous Git operation or an unparseable input.
This hook is a conservative guardrail, not a shell sandbox or alias evaluator.
Python 3 standard library only; quoted static tokens are parsed with shlex.
"""
import json
import os
import shlex
import sys

SEPARATORS={';','&','&&','|','||','(',')','<','>','<<','>>','\n'}
VALUE_OPTIONS={'-C','-c','--git-dir','--work-tree','--namespace','--super-prefix','--config-env','--exec-path'}

def block(reason):
    print(f'BLOCKED: {reason} The user has prevented you from doing this.',file=sys.stderr)
    return 2

def command_tail(tokens,index):
    end=index
    while end<len(tokens) and tokens[end] not in SEPARATORS:end+=1
    return tokens[index:end]

def git_invocation(tokens,index):
    i=index+1
    while i<len(tokens) and tokens[i] not in SEPARATORS:
        token=tokens[i]
        if token in VALUE_OPTIONS:
            if i+1>=len(tokens) or tokens[i+1] in SEPARATORS:return None,[]
            i+=2
        elif token=='--':
            i+=1;break
        elif token.startswith('-'):
            i+=1
        else:break
    if i>=len(tokens) or tokens[i] in SEPARATORS:return None,[]
    return tokens[i],command_tail(tokens,i+1)

def options_before_pathspec(args):
    return args[:args.index('--')] if '--' in args else args

def dangerous(subcommand,args):
    opts=options_before_pathspec(args)
    short=''.join(a[1:] for a in opts if a.startswith('-') and not a.startswith('--'))
    if subcommand=='push':return 'git push'
    if subcommand=='reset' and '--hard' in opts:return 'git reset --hard'
    if subcommand=='clean' and ('f' in short or '--force' in opts):return 'git clean -f'
    if subcommand=='branch':
        delete='D' in short or 'd' in short or '--delete' in opts
        force='D' in short or 'f' in short or '--force' in opts
        if delete and force:return 'git branch -D'
    if subcommand in {'checkout','restore'} and any(x in {'.','./'} for x in args):return f'git {subcommand} .'
    return None

def find_pattern(command, depth=0):
    if depth > 20:
        raise ValueError("static shell wrapper nesting exceeds the analysis limit")
    lexer=shlex.shlex(command,posix=True,punctuation_chars=';&|()<>\n')
    lexer.whitespace_split=True
    tokens=list(lexer)
    for index,token in enumerate(tokens):
        executable=os.path.basename(token)
        if executable=='git':
            subcommand,args=git_invocation(tokens,index)
            pattern=dangerous(subcommand,args)
            if pattern:return pattern
        if executable in {'sh','bash','zsh','dash','ksh','fish'}:
            position=index+1
            while position<len(tokens) and tokens[position] not in SEPARATORS:
                option=tokens[position]
                if option=='--' or not option.startswith(('-', '+')):
                    break
                if option in {'-o','+o','-O','+O','--rcfile','--init-file'}:
                    position+=2
                    continue
                if option=='--command' or (option.startswith('-') and not option.startswith('--') and 'c' in option[1:]):
                    if position+1<len(tokens):
                        pattern=find_pattern(tokens[position+1],depth+1)
                        if pattern:return pattern
                    break
                position+=1
        # Preserve the legacy bare-command patterns, including shell chains.
        if token=='reset' and '--hard' in command_tail(tokens,index+1):return 'reset --hard'
        if token=='push' and '--force' in command_tail(tokens,index+1):return 'push --force'
    return None


def main():
    try:
        value=json.load(sys.stdin)
        if not isinstance(value,dict) or not isinstance(value.get('tool_input'),dict):raise ValueError('tool_input must be an object')
        command=value['tool_input'].get('command','')
        if not isinstance(command,str):raise ValueError('command must be a string')
        pattern=find_pattern(command)
    except (ValueError,TypeError,UnicodeError) as exc:
        return block(f'could not parse the hook input and shell tokens ({exc}), so the command was not checked.')
    if pattern:return block(f"'{command}' matches dangerous pattern '{pattern}'.")
    return 0

if __name__=='__main__':sys.exit(main())
