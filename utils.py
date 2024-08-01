import pandas as pd

def printTasks(tasks, path=None):
    data = {'title' : list(),
            'index' : list(),
            'duration' : list(),
            'parallel' : list(),
            'pre-dependency' : list(),
            'nxt-dependency' : list(),
            'start' : list(),
            'finish' : list()}
       
    for task in tasks:
        data['title'].append(task.title)
        data['index'].append(task.index)
        data['duration'].append(task.duration)         
        data['parallel'].append(task.parallel)
        data['pre-dependency'].append(task.predependency)
        data['nxt-dependency'].append(task.nxtdependency)
        data['start'].append(task.start)
        data['finish'].append(task.finish)
                
    df = pd.DataFrame(data)
    if path:
        df.to_csv(f'{path}/tasks.csv', index=False)
    else:
        df.to_csv('tasks.csv', index=False)
    
    print(df, end='\n\n')
    
def printSchedule(schedule, display=True):
    data = {'sub' : list(),
            'title' : list(),
            'index' : list(),
            'duration' : list(),
            'parallel' : list(),
            'pre-dependency' : list(),
            'nxt-dependency' : list(), 
            'start' : list(),
            'finish' : list(),
            'real start' : list(),
            'real finish' : list()}
    
    start = 0
    for idx, sub in enumerate(schedule.subSchedules):
        for task in sub.tasks:
            data['sub'].append(idx)
            data['title'].append(task.title)
            data['index'].append(task.index)
            data['duration'].append(task.duration)         
            data['parallel'].append(task.parallel)
            data['pre-dependency'].append(task.predependency)
            data['nxt-dependency'].append(task.nxtdependency)
            data['start'].append(task.start)
            data['finish'].append(task.finish)
            data['real start'].append(task.start + start)
            data['real finish'].append(task.finish + start)
            
        start += sub.calTotalTime() 
        
    df = pd.DataFrame(data)
    if display:
        print(df, end='\n\n')
    
    return df

def saveSchedule(schedule, path=None, name=None, display=False):
    df = printSchedule(schedule, display)
    
    if path and name:
        df.to_csv(f'{path}/{name}.csv', index=False)
    elif path:
        df.to_csv(f'{path}/temp.csv', index=False)
        
def printSubSchedules(subSchedule):
    data = {'sub' : list(),
            'title' : list(),
            'index' : list(),
            'duration' : list(),
            'parallel' : list(),
            'pre-dependency' : list(),
            'nxt-dependency' : list(), 
            'start' : list(),
            'finish' : list(),
            'real start' : list(),
            'real finish' : list()}
    
    start = 0
    for idx, sub in enumerate(subSchedule):
        for task in sub.tasks:
            data['sub'].append(idx)
            data['title'].append(task.title)
            data['index'].append(task.index)
            data['duration'].append(task.duration)         
            data['parallel'].append(task.parallel)
            data['pre-dependency'].append(task.predependency)
            data['nxt-dependency'].append(task.nxtdependency)
            data['start'].append(task.start)
            data['finish'].append(task.finish)
            data['real start'].append(task.start + start)
            data['real finish'].append(task.finish + start)
            
        start += sub.calTotalTime() 
        
    df = pd.DataFrame(data)
    print(df, end='\n\n')
    
    return df

                    