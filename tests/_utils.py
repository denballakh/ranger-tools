import traceback

__all__ = [
    '_common_test',

    'add_to_list',
    'assert_raise',
    'run_tests',

    'TESTS',
]

TESTS = []

def add_to_list(lst):
    def decorator(func):
        lst.append(func)
        return func
    return decorator

def run_tests(test_list: list):
    for test in test_list:
        try:
            # print(f'Running test {test}')
            test()
        except Exception as e:
            print(f'Error in test {test}:')
            # print(e)
            traceback.print_exc()
            print()

class _common_test:
    def __new__(cls):
        tests = []
        for attr in dir(cls):
            if attr.startswith('test_'):
                tests.append(getattr(cls, attr))

        run_tests(tests)

    def dummy(self): pass

def assert_raise(func):
    def decorated():
        try:
            func()
        except:
            pass
        else:
            raise AssertionError(f'Test {func} should raise exception')
    return decorated
