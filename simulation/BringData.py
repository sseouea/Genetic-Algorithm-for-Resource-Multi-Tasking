import pandas as pd
from Task import *
import random
from utils import *

def makeData():
    data = {'title' : list(),
            'index' : list(),
            'duration' : list(),
            'parallel' : list(),
            'dependency' : list()}
    
    recipe = {'icecream', 'cake', 'bread', 'cookie', 'drink', 'grape'}
    for title in recipe:
        index = random.randint(0,20)
        for idx in range(index):
            duration = random.randint(1,50)
            parallel = random.choice(['TRUE', 'FALSE'])
            
            dependency = None
            if idx != 0:
                dependency = random.randint(0,idx-1)
                if dependency == 0:
                    dependency = ''
                else:
                    dependency = random.sample(range(1,idx), k=dependency)
                    dependency = list(map(str, dependency))
                    dependency = ' '.join(dependency)
            
            data['title'].append(title)
            data['index'].append(idx)
            data['duration'].append(duration)
            data['parallel'].append(parallel)
            data['dependency'].append(dependency)
            
    df = pd.DataFrame(data)
    df.to_csv('simpleData.csv', index=False)
            
def bringData(path):
    df = pd.read_csv(path)
    
    tasks = list()
    for _, row in df.iterrows():
        title = row['title']
        index = int(row['index'])
        duration = int(row['duration'])
        dependency = list() if pd.isna(row['dependency']) else list(map(int, str(row['dependency']).split(' ')))
        parallel  = row['parallel']
        
        task = Task(title, index, duration, dependency, parallel)
        tasks.append(task)
        
    for task in tasks:
        task.setDependency(tasks)
        
    #printTasks(tasks)
    return tasks