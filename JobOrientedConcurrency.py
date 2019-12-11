"""
TODO:
    clean up/refactor the code
    add comments
    (maybe add more error handling)
"""

from multiprocessing import Process, Lock, Queue, Pipe

class JocTree:
    def __init__(self):
        self.funcs = {}
        self.startFuncs = []
        self.has_end = False
        self.parent_pipe, self.child_pipe = Pipe()
        self.lock = Lock()

    def add_func(self, infunc):
        self.funcs[infunc] = JocTree.Job(infunc)

    def delete_error_connected(self, infunc):
        raise ValueError("function " + infunc.__name__ + " has connections and could not be deleted")

    def del_func(self, infunc):
        if self.funcs[infunc].can_delete():
            del self.funcs[infunc]
        else:
            delete_error_connected(self, infunc)

    def add_start_func(self, infunc):
        self.funcs[infunc] = JocTree.Job(infunc)
        self.startFuncs.append(infunc)

    def del_start_func(self, infunc):
        if self.funcs[infunc].can_delete():
            del self.funcs[infunc]
            del self.startFuncs[infunc]
        else:
            delete_error_connected(self, infunc)

    def add_end_func(self, infunc):
        self.funcs[infunc] = JocTree.Job(infunc, end=True, child_pipe=self.child_pipe)
        self.has_end = True

    def del_end_func(self, infunc):
        if self.funcs[infunc].can_delete():
            del self.funcs[infunc]
            self.has_end = False
        else:
            delete_error_connected(self, infunc)

    def add_connect(self, func_parent, func_child):
        self.funcs[func_parent].add_child(self.funcs[func_child])
        self.funcs[func_child].inc_amount_of_params()

    def del_connect(self, func_parents, func_child):
        self.funcs[func_parent].del_child(self.funcs[func_child])
        self.funcs[func_child].dec_amount_of_params

    def run(self):
        for n in self.startFuncs:
            Process(target=self.funcs[n].call, args=(None, None, self.lock, True)).start()
        if self.has_end:
            return self.parent_pipe.recv()

    class Job: 

        def __init__(self, func, end=False, child_pipe=None):
            self.func = func
            self.end = end
            self.depend = [] #dependencies, that this one will call, they will be job objects
            self.parqueue = Queue()
            self.amount_of_params = 0
            self.child_pipe = child_pipe

        def add_child(self, in_job):
            self.depend.append(in_job)

        def del_child(self, in_job):
            del self.depend[ JocTree]

        def inc_amount_of_params(self):
            self.amount_of_params += 1

        def dec_amount_of_params(self):
            self.amount_of_params -= 1

        def can_delete(self):
            return (len(self.depend) == 0 and self.amount_of_params == 0)

        def call(self, retval, infunc, l, first=False):

            if first:
                self.call_children(l)

            else:
                l.acquire()
                self.parqueue.put((infunc.__name__, retval))

                if self.parqueue.qsize() == self.amount_of_params:
                    l.release()
                    self.call_children(l)
                else:
                    l.release()

        def call_children(self, l):
            params = {}
            li = []
            l.acquire()

            while self.parqueue.qsize() != 0:
                li.append(self.parqueue.get())

            l.release()
            params.update(li)
            val = self.func(params)

            if self.end:
                self.child_pipe.send(val)
                self.child_pipe.close()
            else:
                for n in self.depend:
                    Process(target=n.call, args=(val, self.func, l)).start()
