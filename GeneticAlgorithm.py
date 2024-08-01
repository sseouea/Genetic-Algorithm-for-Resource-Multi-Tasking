from SubSchedule import *
import random
from BringData import *
import copy
from utils import *
from Schedule import *
import os
from datetime import datetime
from debug import *
import shutil

class geneticAlgorithm:
    def __init__(self, epoch, num, tasks):
        self.tasks = tasks
        self.epoch = epoch
        self.num = num
        self.select = {'model' : None, 'time' : None}
        self.schedules = list()
        self.best = {'epoch' : None, 'model' : None, 'time' : None}
        self.path = None
        
        self.makeDirectory()
        self.makeInitialModel()
        
    def makeDirectory(self):
        if not os.path.exists('./log'):
            os.mkdir('./log')
    
        num = str(len(os.listdir('./log')))
        now = datetime.now()
        now = now.strftime("%Y%m%d%H%M%S")
        path = f'./log/{num}-{now}'
        os.mkdir(path)
        os.mkdir(f'{path}/debug')
        
        self.path = path
        
    def run(self):
        print('=============================================')
        print('Genetic Algorithm Start')
        print(f'Path : {self.path}')
        
        length = len(str(self.epoch - 1))
        for epoch in range(self.epoch):
            self.reproduction()
            self.crossover()
            self.mutation()
            self.selection()
            
            with open(f"{self.path}/result.txt", "a") as f:
                string = str(epoch).rjust(length)
                f.write(f'Epoch {string} | {self.select['time']}mins\n')
            self.save(epoch=epoch, display=False)
                        
            if self.best['time']:
                if self.best['time'] < self.select['time']:
                    continue

            self.best['epoch'] = epoch
            self.best['model'] = copy.deepcopy(self.select['model'])
            self.best['time'] = self.select['time']
            
            ## debug
            dependencySchedule(self.select['model'].subSchedules, self.tasks)
            ##
        
        with open(f"{self.path}/result.txt", "a") as f:
                f.write(f'\nBestModel :\n[Epoch {self.best['epoch']}] {self.best['time']}mins')

        self.save(epoch=None, display=False) #
        print((f'BestModel :\nepoch {self.best['epoch']}, {self.best['time']}mins'))
        print('\nGenetic Algorithm Finish')
        print('=============================================')

    def makeInitialModel(self):
        initialModel = Schedule()
        
        titles = list(set(map(lambda task : task.title, self.tasks)))
        for title in titles:
            tasks = sorted(list(filter(lambda task : task.title == title, self.tasks)), key=lambda t : t.index, reverse=False)
            
            idx = 0
            sub = None
            while idx < len(tasks):
                if tasks[idx].parallel == False:
                    if sub:
                        if sub.countTasks():
                            initialModel.addSubSchedule(sub)
                    
                    sub = SubSchedule()
                    sub.addTask(tasks[idx])
                    initialModel.addSubSchedule(sub)
                    sub = None
                else:
                    if sub == None:
                        sub = SubSchedule()
                    sub.addTask(tasks[idx])
                                        
                idx += 1
                                                
            if sub:
                initialModel.addSubSchedule(sub)
                            
        self.select['model'] = initialModel
        saveSchedule(initialModel, self.path, 'tasks', False)
        
        ## debug
        dependencySchedule(initialModel.subSchedules, self.tasks)
        ##
            
    def selection(self):
        time = -1
        select = None
        
        for schedule in self.schedules:
            _time = schedule.calTotalTime()
            
            if time > _time or time == -1:
                time = _time
                select = schedule
                
        self.select['model'] = select
        self.select['time'] = time
        
    def reproduction(self):
        self.schedules = [copy.deepcopy(self.select['model']) for _ in range(self.num)]
        
    def crossover(self):
        parallel = list(filter(lambda task : task.parallel, self.tasks))
        if not parallel:
            #print('[Warn] Parallel Data Scarcity')
            return
        
        for schedule in self.schedules:
            task = random.choice(parallel)
            if schedule.addTask(task=task, type='merge'):
                schedule.deleteTask(task)

    def mutation(self):
        not_parallel = list(filter(lambda task : not task.parallel, self.tasks))
        if not not_parallel:
            #print('[Warn] UnParallel Data Scarcity')
            return
        
        for schedule in self.schedules:
            task = random.choice(not_parallel)
            if schedule.addTask(task=task, type='insert'):
                schedule.deleteTask(task)
            
    def save(self, epoch=None, display=False):
        if epoch != None:
            name = f'Ep{epoch}_model'
            path = f'{self.path}/debug'
            saveSchedule(self.select['model'], path, name, display)
        else:
            name = f'Best_model'
            saveSchedule(self.best['model'], self.path, name, display) 
       
if __name__ == '__main__':
    path = 'direction_times_labeled.csv'
    tasks = bringData(path)

    for idx in range(10):
        check = True
        genetic = None
        
        while check:
            try:
                genetic = geneticAlgorithm(epoch=200, num=3, tasks=tasks)
                genetic.run()
            
                with open(f"./log/best.txt", "a") as f:
                    f.write(f'Model {idx+1} | {genetic.best['time']} mins\n')
                    
                check = False
            except:
                shutil.rmtree(genetic.path)

                
            
            
        
            
        
            
    