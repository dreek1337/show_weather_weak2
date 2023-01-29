import time


def message(func):
    def inner(*args, **kwargs):
        print("---Start function---")
        res = func(*args, **kwargs)
        print("---End function---")

        return res

    return inner


def time_it(func):
    def inner(*args, **kwargs):
        now = time.time()
        res = func(*args, **kwargs)
        print(f'Function time completed: {round(time.time() - now, 2)}')

        return res

    return inner


def catch_exception(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            print(f'Error: {err}')

    return inner


@message
@catch_exception
@time_it
def test_def(a, b):
    list(range(10000000)) * 2
    res = a / b
    print(res)
    return res


test_def(2, 2)
test_def(2, 0)
