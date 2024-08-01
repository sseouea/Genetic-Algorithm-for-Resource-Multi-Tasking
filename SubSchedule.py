import sys

class SubSchedule:
    '''
    if SubSchedule is unparallel:
        only has one task which is unparallel
    
    if SubSchedule is parallel:
        at least one task which is/are parallel
    '''
    
    def __init__(self):
        self.tasks = list()
        self.parallel = None
        
    def countTasks(self):
        return len(self.tasks)
    
    def calTotalTime(self):
        time = 0
        for task in self.tasks:
            if task.finish > time: 
                time = task.finish
        return time
    
    def findTask(self, title, index):
        task = None
        for idx, task in enumerate(self.tasks):
            if task.title == title and task.index == index:
                return idx, task
            
        return -1, None
    
    def existTask(self, title, index):
        idx, _ = self.findTask(title, index)
        
        if idx == -1:
            return False
        else:
            return True
        
    def checkInterval(self, task):
        # interval(time interval) where task is able to be insert
        '''
        p -> q -> r
        p = predecessor // predependency
        r = successor // nxtdependency
        
        preFinish : maximum finish time of predecessor
        nxtStart : minimum start time of successor
        
        * only check the pre/nxt dependency nodes which exist in SubSchedule
          therfore, each of those doesn't mean the ultimate preFinish & nxtStart
        '''
        
        preFinish = None
        nxtStart = None
        
        tasks = sorted(self.tasks, key=lambda t : t.start, reverse=False)
        for idx, _task in enumerate(tasks):
            if task.title == _task.title and _task.index in task.nxtdependency:
                nxtStart = _task
                break
            
        ### debug
        '''
        print('NxtStart Debug')
        print('NxtStart:', nxtStart)
        print('Task:', task.title, task.index, task.predependency, task.nxtdependency, task.start)
        
        for _task in tasks:
            print(_task.title, _task.index, _task.predependency, _task.nxtdependency, _task.start)
        '''
        ###
        
        tasks = sorted(self.tasks, key=lambda t : t.finish, reverse=True) 
        for idx, _task in zip(reversed(range(len(tasks))), tasks):
            if task.title == _task.title and _task.index in task.predependency:
                preFinish = _task
                break
        
        ### debug
        '''
        print('PreFinish Debug')
        print('PreFinish:', preFinish)
        print('Task:', task.title, task.index, task.predependency, task.nxtdependency, task.start)
        
        for _task in tasks:
            print(_task.title, _task.index, _task.predependency, _task.nxtdependency, _task.start)
        '''
        ###
        
        if preFinish != None and nxtStart != None:
            if preFinish.finish > nxtStart.start:
                print('[Error] Task Sequence Error')
            
        return preFinish, nxtStart
        
    def addTask(self, task): 
        '''
        if task is parallel:
            check the time interval that task can be inserted
            
            task.start = begin of time interval
            task.finish = task.start + task.duration
            
            time interval = preFinish.finish ~ nxtStart.start
            case1. the time interval >= duration:
                pass
            case2. the time interval < duration:
                consider tasks which is from same recipe 
                
                1. predecessor exist (o), successor exist (o)
                    - delta = | begin of time interval + duration - finish of time interval |
                    - task 1 = task which start time is same or bigger than finish of time interval
                    - task 2 = task(among task1) which has relation(pre/nxt) to given task
                                (ex. task's predecessor's successor)
                    - plus delta to start time and finish time of task2
                    
                2. predecessor exist (o), successor exist (x)
                    - (caused by short total time -> update the total time by add the task)
                    - no problem, just add // pass
                    
                3. predecessor exist (x), successor exist (o)
                    * similar process with '1'
                    
                    - delta = | duration - finish of time interval |
                      (begin of time interval = 0)
                    - task 1 = task which start time is same or bigger than finish of time interval
                    - task 2 = task(among task1) which has relation(pre/nxt) to given task
                                (ex. task's predecessor's successor)
                    - plus delta to start time and finish time of task2
                    
                4. predecessor exist (x), successor exist (x)
                    - no problem, just add // pass

        if task is unparallel:
            just add (be careful that SubSchedule have only one unparallel task)
        '''
                
        if self.parallel == None:
            self.parallel = task.parallel
            task.start = 0
            task.finish = task.start + task.duration
            self.tasks.append(task)
            return

        preFinish, nxtStart = self.checkInterval(task)
        task.start = preFinish.finish if preFinish != None else 0
        task.finish = task.start + task.duration
        
        if preFinish != None and nxtStart != None:
            if nxtStart.start - preFinish.finish >= task.duration:
                self.tasks.append(task)
                return
        
        if nxtStart != None: 
            delta = preFinish.finish if preFinish != None else 0
            delta = delta + task.duration - nxtStart.start
            
            sameRecipeTask = list(filter(lambda t : t.title == task.title, self.tasks))
            sameRecipeTask = list(map(lambda t : t.index, sameRecipeTask)) # index of same recipe task in subschedule
            relatedTask = task.predependency + task.nxtdependency
            relatedTask = list(filter(lambda t : t in sameRecipeTask, relatedTask))
            
            while True:
                _relatedTask = list()

                for idx in relatedTask:
                    _task = list(filter(lambda t : t.title == task.title and t.index == idx, self.tasks))[0]
                    _relatedTask = _relatedTask + _task.predependency + _task.nxtdependency
               
                _relatedTask = list(filter(lambda t : t in sameRecipeTask, _relatedTask))
                _relatedTask = list(set(_relatedTask) - set(relatedTask))
                
                try:
                    _relatedTask.index(task.index)
                    _relatedTask.remove(task.index) # not yet delete the task
                except:
                    pass
                                
                if len(_relatedTask) == 0:
                    break
                else:
                    relatedTask += _relatedTask
                    
            ### debug
            '''
            print(f'task title : {task.title}, related task : {relatedTask}')
            print('index, pre, nxt, start, finish')
            
            for idx, tasks in self.tasks:
                print(idx, task.predependency, task.nxtdependency, task.start, task.finish)
            '''
            ###

            relatedTask = list(filter(lambda t : t.title == task.title and t.index in relatedTask, self.tasks))
            relatedTask = list(filter(lambda t : t.finish >= nxtStart.start, relatedTask))
            
            for _task in relatedTask:
                _task.start += delta 
                _task.finish += delta
                
            ### debug
            '''
            for idx, tasks in self.tasks:
                print(idx, task.predependency, task.nxtdependency, task.start, task.finish)
                
            x = input('Enter :')
            '''
            ###
            
        else:
            pass # no problem
        
        self.tasks.append(task)

        return
                
    def deleteTask(self, task):
        idx, _ = self.findTask(task.title, task.index)
        if idx == -1:
            print('[Error] Value Error')
        else:
            del self.tasks[idx]
            
        return

            
