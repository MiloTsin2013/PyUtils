#!/usr/bin/env python
# coding=utf-8

import sys
import os
import commands  
import mailUtil

class GitMonitor():
    def __init__(self, repoPath):
        self.currentPath = os.path.abspath('.')
        self.expPath = os.path.dirname(mailUtil.__file__)
        self.repoPath = os.path.abspath(repoPath)
    
    def move2(self, path):
        '''移动目录'''
        if os.path.exists(path):
            os.chdir(path)
        else:
            print '{} 不存在'.format(path)

    def pull(self):
        '''拉 Git 仓库'''
        os.system('expect {}/git_login.exp'.format(self.expPath))

    def log(self, after=None, before=None):
        '''获取项目变更列表'''
        cmd = 'git log --oneline --name-status'
        if after:
            cmd += ' --after="{}"'.format(after)
        if before:
            cmd += ' --before="{}"'.format(before)
        print cmd
        output = commands.getoutput(cmd)
        output = [operate for operate in [line.split('\t') for line in output.split('\n')] if operate[0] in ('A','M','D')]
        return output
    
    def resultModify(self, after=None, before=None):
        '''最终变动'''
        log = self.log(after=after, before=before)
        dic = {'A':set(), 'M':set(), 'D':set()}
        for line in log[::-1]:
            dic[line[0]].add(line[1])
        return dic
