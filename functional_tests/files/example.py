a_string = "This is a global variable"
def foo(x):
    print(a_string)
print(foo(0))

def owner(model):
    print(model)
    def check(x):
        print(model)
        return True
    return  foo(check)
