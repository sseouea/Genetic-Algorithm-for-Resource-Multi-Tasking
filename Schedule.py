import sys
from SubSchedule import *
from Task import *
import random
from utils import *

class Schedule:
    def __init__(self):
        self.subSchedules = list()
        
    def calTotalTime(self):
        time = 0
        
        for sub in self.subSchedules:
            time += sub.calTotalTime()
        return time
        
    def countSubSchedule(self):
        return len(self.subSchedules)
    
    def countTasks(self):
        count = 0
        for sub in self.subSchedules:
            count += sub.countTasks()
        return count
            
    def checkInterval(self, task):  
        # interval(SubSchedule's index) where task is able to be insert
        '''
        p -> q -> r
        p = predecessor // predependency
        r = successor // nxtdependency
        
        preFinish : maximum index of SubSchedule which has predecessor
        nxtStart : minimum index of SubSchedule which has successor
        
        * these index derive by considering overall predecessor and successor of task
          therefore, this is the global interval
        '''
        
        preFinish = list()
        nxtStart = list()
        
        for idx, sub in zip(reversed(range(len(self.subSchedules))), reversed(self.subSchedules)):
            for _idx in task.predependency:
                if sub.existTask(task.title, _idx):
                    preFinish.append(idx)
                    break
                
        for idx, sub in enumerate(self.subSchedules):
            for _idx in task.nxtdependency:
                if sub.existTask(task.title, _idx):
                    nxtStart.append(idx)
                    break
                
        preFinish = max(preFinish) if preFinish else None
        nxtStart = min(nxtStart) if nxtStart else None
        
        if preFinish != None and nxtStart != None:
            if preFinish > nxtStart:
                print('[Error] SubSchedule Sequence Error')
            
        return preFinish, nxtStart
                
    def addByMerge(self, task):
        # task is parallel
        pre, nxt = self.checkInterval(task)
        interval = None
        indices = list()
        
        if pre != None and nxt != None:
            interval = range(pre, nxt+1)
        elif pre != None:
            interval = range(pre, self.countSubSchedule())
        elif nxt != None:
            interval = range(0, nxt+1)
        else:
            interval = range(0, self.countSubSchedule())
            
        for idx in interval:
            if self.subSchedules[idx].parallel == True:
                indices.append(idx)
        
        if not indices:
            #print('[Warn] No Position Satisfying Condition')
            return False
            
        idx = random.choice(indices)
        self.subSchedules[idx].addTask(task)
        
        return True
    
    def addByInsert(self, task):
        # task is parallel
        pre, nxt = self.checkInterval(task)
        interval = None
        indices = list()
        
        if pre != None and nxt != None:
            '''
            min of idx is pre+1
            task cannot be front of task[nxt]
            
            max of idx is nxt
            task cannot be behind of task[nxt]
            '''
            interval = range(pre+1, nxt+1)
        elif pre != None:
            '''
            max of idx is self.countSubSchedule()
            task can be the last
            '''
            interval = range(pre+1, self.countSubSchedule()+1)
        elif nxt != None:
            '''
            min of idx is 0
            task can be the first
            '''
            interval = range(0, nxt+1)
        else:
            interval = range(0, self.countSubSchedule()+1)
        
        '''
        interval is the indices which list().insert(idx, task) is able
        list().insert(idx, task) means the task be front of list[idx]
        -> task - list[idx]
        '''
        for idx in interval:
            if idx == 0:
                # pre is not exist
                if self.subSchedules[idx].parallel == False:
                    indices.append(idx)
                    continue
                
            if idx == self.countSubSchedule():
                # nxt is not exist
                if self.subSchedules[idx-1].parallel == False:
                    indices.append(idx)
                break
            
            if self.subSchedules[idx-1].parallel == False and self.subSchedules[idx].parallel == False: 
                indices.append(idx) 
        
        if not indices:
            #print('[Warn] No Position Satisfying Condition')
            return False
            
        idx = random.choice(indices) ## empty!
        sub = SubSchedule()
        sub.addTask(task)
        self.addSubSchedule(sub, idx)
        
        return True
            
    def addTask(self, task, type=None):
        # type : merge(crossover), insert(mutation)
        '''
        if task is parallel:
            two action: 
            1. merge (combine with existing parallel tasks)
                - addByMerge()
            2. insert (insert between unparallel tasks)(unparallel - parallel* - unparallel)
                - addByInsert()

        if task is unparallel:
            two action: 
            1. divide (divide existing parallel tasks into 2 groups and put it between them)
                - (=) if parallel task in one parallel group moves various times
                      (ex. half of parallel task in a group moves behind to one specific unparallel task)
            2. insert (unparallel- unparallel* - parallel / unparallel - unparallel* - unparallel)
                - unparallel - unparallel* - parallel (=) unparallel - parallel* - unparallel
                - so, only address 'unparallel - unparallel* - unparallel
                - (=) addByInsert() ; only task's parallel is different
        '''
        add = None
        
        if type == None:
            #print('[Warn] Uncomplete Condition')
            return False
        elif type == 'merge':
            if task.parallel == False:
                #print('[Warn] Mismatch Condition')
                return False
            elif task.parallel == True:
                add = self.addByMerge(task)
        elif type == 'insert':
            add = self.addByInsert(task)
        
        return add
    
    def deleteTask(self, task):
        for idx, sub in enumerate(self.subSchedules):
            _idx, _ = sub.findTask(task.title, task.index)
            
            if _idx != -1:
                sub.deleteTask(task)
                if sub.countTasks() == 0:
                    del self.subSchedules[idx]
                    
                return
        
        
    def addSubSchedule(self, sub, idx=None):
        if idx == None:
            self.subSchedules.append(sub)   
        else:
            self.subSchedules.insert(idx, sub)
        
        return
    
    def deleteSubSchedule(self, idx):
        del self.subSchedules[idx]
        
        return
    
        

                            
        