import pandas as pd

def dependencySchedule(schedule, tasks):
    data = {'sub' : list(),
            'title' : list(),
            'index' : list(),
            'pre-dependency' : list(),
            'nxt-dependency' : list(), 
            'start' : list(),
            'finish' : list()}
    
    for idx, sub in enumerate(schedule):
        for task in sub.tasks:
            data['sub'].append(idx)
            data['title'].append(task.title)
            data['index'].append(task.index)
            data['pre-dependency'].append(task.predependency)
            data['nxt-dependency'].append(task.nxtdependency)
            data['start'].append(task.start)
            data['finish'].append(task.finish)
            
    df = pd.DataFrame(data)
    #print(df, end='\n\n')
    
    for task in tasks:
        taskRow = df[(df['title'] == task.title) & (df['index'] == task.index)]
        
        for pre in task.predependency:
            preRow = df[(df['title'] == task.title) & (df['index'] == pre)]
            
            if int(preRow['sub'].iloc[0]) < int(taskRow['sub'].iloc[0]):
                continue
            elif int(preRow['sub'].iloc[0]) == int(taskRow['sub'].iloc[0]):
                if int(preRow['finish'].iloc[0]) <= int(taskRow['start'].iloc[0]):
                    continue
                
            raise Exception('PreDependency Error')
        
        for nxt in task.nxtdependency:
            nxtRow = df[(df['title'] == task.title) & (df['index'] == nxt)]
            
            if int(nxtRow['sub'].iloc[0]) > int(taskRow['sub'].iloc[0]):
                continue
            elif int(nxtRow['sub'].iloc[0]) == int(taskRow['sub'].iloc[0]):
                if int(nxtRow['start'].iloc[0]) >= int(taskRow['finish'].iloc[0]):
                    continue
                
            raise Exception('NxtDependency Error')
          