# !/usr/bin/env python
# coding=utf-8

import os

class CronUtil():
    class Cron():
        '''
        计划任务对象
        '''
        def __init__(self, minute='*', hour='*', day='*', month='*', week='*', command='', comment=None):
            self.minute = minute.strip()
            self.hour = hour.strip()
            self.day = day.strip()
            self.month = month.strip()
            self.week = week.strip()
            self.command = command.strip()
            self.comment = comment.strip() if comment != None else None
        
        def __repr__(self):
            return '{} {} {} {} {} {} {}'.format(self.minute, self.hour, self.day,
            self.month, self.week, self.command, '# ' + self.comment if self.comment != None else '')
    
    class Comment():
        '''
        注释对象
        '''
        def __init__(self, comment):
            self.comment = comment.strip()
        
        def __repr__(self):
            return '# {}'.format(self.comment)
        
    def __init__(self):
        os.system('crontab -l > crontab.tmp')
        self.cronList = []
        with open('crontab.tmp', 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if line.startswith('#'):
                    comment = CronUtil.Comment(line[1:].strip())
                    self.cronList.append(comment)
                elif line != '':
                    sline = line.split(' ',5)
                    if '#' in sline[-1]:
                        pop = sline.pop().split('#',1)
                        sline.extend(pop)
                    else:
                        sline.append(None)
                    cron = CronUtil.Cron(sline[0], sline[1], sline[2], sline[3], sline[4], sline[5], sline[6])
                    self.cronList.append(cron)

    def __repr__(self):
        return '\n'.join([str(cron) for cron in self.cronList])

    def add(self, line):
        '''
        添加对象，根据内容判断是计划任务还是注释
        '''
        line = line.strip()
        if line.startswith('#'):
            comment = CronUtil.Comment(line[1:].strip())
            self.cronList.append(comment)
        elif line != '':
            sline = line.split(' ',5)
            if '#' in sline[-1]:
                pop = sline.pop().split('#',1)
                sline.extend(pop)
            else:
                sline.append(None)
            cron = CronUtil.Cron(sline[0], sline[1], sline[2], sline[3], sline[4], sline[5], sline[6])
            self.cronList.append(cron)

    def delete(self, comment):
        '''
        根据注释删除对象
        '''
        self.cronList = [cron for cron in self.cronList if cron.comment != comment.strip()]

    def modify(self, line, comment):
        '''
        根据注释，修改对象
        '''
        line = line.strip()
        item = None
        if line.startswith('#'):
            item = CronUtil.Comment(line[1:].strip())
        elif line != '':
            sline = line.split(' ',5)
            if '#' in sline[-1]:
                pop = sline.pop().split('#',1)
                sline.extend(pop)
            else:
                sline.append(None)
            item = CronUtil.Cron(sline[0], sline[1], sline[2], sline[3], sline[4], sline[5], sline[6])
        if item != None:
            for index, cron in enumerate(self.cronList): 
                if cron.comment == comment.strip():
                    self.cronList[index] = item

    def modifyTime(self, time, comment):
        '''
        根据注释，修改计划任务对象的执行时间
        '''
        for index, cron in enumerate(self.cronList): 
            if cron.comment == comment.strip() and isinstance(cron, CronUtil.Cron):
                timeList = time.strip().split(' ')
                # print self.cronList[index]
                self.cronList[index].minute = timeList[0]
                self.cronList[index].hour = timeList[1]
                self.cronList[index].day = timeList[2]
                self.cronList[index].month = timeList[3]
                self.cronList[index].week = timeList[4]
                # print self.cronList[index]
            

    def query(self, comment):
        '''
        根据注释获取相应的第一个对象
        '''
        for index, cron in enumerate(self.cronList): 
            if cron.comment == comment.strip():
                return self.cronList[index]

    def querys(self, comment):
        '''
        根据注释获取所有相同注释内容的对象
        '''
        return [cron for cron in self.cronList if cron.comment == comment.strip()]
            
    def clear(self):
        '''
        清除所有计划任务
        '''
        self.cronList = []
        with open('crontab.tmp', 'w') as f:
            f.write("")
        os.system('crontab crontab.tmp')

    def save(self):
        '''
        保存计划任务
        '''
        with open('crontab.tmp', 'w') as f:
            crons = [str(line)+'\n' for line in self.cronList]
            f.writelines(crons)
        os.system('crontab crontab.tmp')

if __name__ == "__main__":
    cronUtil = CronUtil()
    print cronUtil
    # cronUtil.add('* * * * 1 cd / # test1')
    # cronUtil.add('# test2')
    # cronUtil.delete('test1')
    # cronUtil.modify('* * * * 1 cd ~ # test2', 'test1')
    # cron = cronUtil.query('test2')
    # cron.minute = 1
    # cron = cronUtil.querys('test2')
    # print type(cron[0]), type(cron[1])
    # print cron
    cronUtil.modifyTime('0 21 * * 7', 'test3')
    print cronUtil
    cronUtil.save()
    # cronUtil.clear()