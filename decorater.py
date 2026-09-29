# Decorater wrapers a function in to it with out changing the functionality 
def logger(func):
    def log():
        print("Before function ")
        func()
        print("After function")

    return log

@logger
def test_login():
    print("Login test completed ")


test_login()