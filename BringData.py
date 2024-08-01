import pandas as pd
from Task import *
import random
from utils import *
import sys
import chardet
            
def bringData(path):
    with open(path, 'rb') as f:
        result = chardet.detect(f.read())
        encoding = result['encoding']
    df = pd.read_csv(path, encoding=encoding)
    
    tasks = list()
    for _, row in df.iterrows():
        title = row['title']
        index = int(row['index']) 
              
        duration = row['duration'].replace('-',' ')
        duration = duration.split(' ')
        duration = list(filter(lambda t : t.isdigit(), duration))
        duration.sort(key = lambda t : int(t), reverse=True)
        duration = int(duration[0])
        
        if pd.isna(row['dependency']):
            dependency = list()
        else:
            dependency = row['dependency'].replace(',',' ')
            dependency = dependency.split(' ')
            dependency = list(filter(lambda d : d.isdigit(), dependency))
            dependency = list(map(int, dependency))
            dependency.sort()
        
        parallel  = row['parallel']
         
        task = Task(title, index, duration, dependency, parallel)
        tasks.append(task)
        
    for task in tasks:
        task.setDependency(tasks)
        
    #printTasks(tasks, path=None)
    
    return tasks