import inspect


# http://stackoverflow.com/a/582206/3391915

def func(a, b, c):
    frame = inspect.currentframe()
    args, _, _, values = inspect.getargvalues(frame)
    print('function name "%s"' % inspect.getframeinfo(frame)[2])
    for i in args:
        print("    %s = %s" % (i, values[i]))
    return [(i, values[i]) for i in args]

"""
>>> func(1, 2, 3)
function name "func"
    a = 1
    b = 2
    c = 3
[('a', 1), ('b', 2), ('c', 3)]
"""


class JudgeOfExclusivity(object):

    def __init__(self, frame):
        self.args, _, _, self.values = inspect.getargvalues(frame)
        self.params = []

    def is_exclusive(self):
        for name in self.args:
            if name not in self.params and self.values[name]:
                return False
        return True

    def know(self, var):
        callers_local_vars = inspect.currentframe().f_back.f_locals.items()
        var_name = [var_name for var_name, var_val in callers_local_vars if var_val is var][0]
        self.params.append(var_name)

    def names(self):
        return self.params


def clisimu(param1, param2=None, param3=None, param4='default4'):
    judge = JudgeOfExclusivity(inspect.currentframe())
    judge.know(param1)
    judge.know(param3)  # TODO ?
    judge.know(param4)
    print(judge.names())
    print(judge.is_exclusive())
    #print(judge.has_exclusivity_for([param1]))
    

if __name__ == "__main__":
    clisimu('here')
