import graphviz as gv
import json


class Call:
    def __init__(self, f, args, kwargs, caller=None):
        # call info
        self.f = f
        self.args = args
        self.kwargs = kwargs
        self.caller = caller

        # default values
        self.subcalls = []
        self.depth = 0
        self.height = 1

        # update depth and register as subcall
        if self.caller is not None:
            self.depth = self.caller.depth + 1
            self.caller.subcalls.append(self)

        # perform call
        self.res = self.do_call()

        # update caller height
        if self.caller is not None:
            self.caller.height = max(self.caller.height, self.height + 1)

    def do_call(self):
        CallRecorder.current = self
        res = self.f(*self.args, **self.kwargs)
        CallRecorder.current = self.caller
        return res

    def call_text(self):
        arglist = ", ".join(map(str, self.args))
        arglist += ", ".join(
            "{}={}".format(arg, val)
            for arg, val in (self.kwargs.items()))
        return "{}({})".format(self.f.__name__, arglist)

    def trace(self):
        res = []
        res.append(" │ " * self.depth + self.call_text())
        for subcall in self.subcalls:
            res.append(subcall.trace())
        res.append(" │ " * self.depth + " └─> " + str(self.res))
        return '\n'.join(res)

    def trace2(self):
        res = []
        res.append("  |  " * self.depth + self.call_text())
        for subcall in self.subcalls:
            res.append("  |  " * (self.depth + 1))
            res.append(subcall.trace2())
        res.append("  |  " * (self.depth + 1))
        res.append("  |  " * self.depth + "  \__ résultat : " + str(self.res))
        return '\n'.join(res)

    def json(self):
        def aux(call):
            res = {
                'call': call.call_text(),
                'res': call.res,
                'subcalls': [aux(subcall) for subcall in call.subcalls]
            }
            return res
        return json.dumps(aux(self))

    @staticmethod
    def node_name(number):
        return "node" + str(number)

    def graph(self, verbose_labels=True):
        G = gv.Graph(node_attr={'shape': 'plaintext'})

        def aux(call, current=0, parent=0):
            #label = call.call_text()
            if verbose_labels:
                label = """<
                    <TABLE BORDER="0" CELLBORDER="0">
                    <TR><TD><FONT COLOR='darkgreen'><I>appel {}</I></FONT></TD></TR>
                    <TR><TD BORDER="1" STYLE="rounded"><FONT FACE="courier">{}</FONT></TD></TR>
                    <TR><TD><FONT COLOR='red'>résultat : <FONT FACE="courier">{}</FONT></FONT></TD></TR>
                    </TABLE>
                    >""".format(current + 1, call.call_text(), str(call.res))
            else:
                label = call.call_text()
            name = Call.node_name(current)
            G.node(name, label=label)
            if parent < current:
                G.edge(Call.node_name(parent), name)
            child = current + 1
            for subcall in call.subcalls:
                child = aux(subcall, child, current)
            return child

        aux(self)
        return G

    def render(self, filename=None):
        if filename is None:
            self.graph().render(format='png')
        else:
            self.graph().render(filename, prog='dot', format='png')


from copy import deepcopy

class CallRecorder:
    current = None

    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        call = Call(self.f, args, kwargs, CallRecorder.current)
        if call.caller is None:
            return call
        return deepcopy(call.res)


@CallRecorder
def fibo(n):
    if n <= 1:
        return n
    return fibo(n-1) + fibo(n-2)

# fibo = CallRecorder(fibo)


@CallRecorder
def even(n):
    if n == 0:
        return True
    return odd(n-1)


@CallRecorder
def odd(n):
    if n == 0:
        return False
    return even(n-1)

if __name__ == "__main__":
    call = even(10)
    print(call.height)
    print(call.trace())
    graph = call.graph()
    print(graph.source)
    graph.render()