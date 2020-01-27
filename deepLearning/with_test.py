#%%
class WithTest:
    def __init__(self):
        print("init")
    def __enter__(self):
        print("enter")
        return 1
    def __exit__(self,type,value,tb):
        if tb is None:
            print("no exception")
        else:
            print("error occured")
            print(type)
            print(value)
            return None
   

print("befor test")
with WithTest() as test:
    print("in test")
    a=1/0
    print(test)

print("out of test")

# %%
