class Task:
    def __init__(self, title=None, index=None, duration=None, dependency=None, parallel=None):
        self.title = title
        self.index = index
        self.duration = duration
        self.predependency = dependency
        self.parallel = parallel
        
        self.start = None
        self.finish = None
        self.nxtdependency = None
        
    def setDependency(self, taskTable):
        tasks = list(filter(lambda t : self.title == t.title, taskTable))
        tasks = list(filter(lambda t : self.index in t.predependency, tasks))
        if tasks:
            tasks = list(map(lambda t : t.index, tasks))
        else:
            tasks = list()
        self.nxtdependency = tasks