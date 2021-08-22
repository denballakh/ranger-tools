import traceback
import importlib

from _utils import run_tests, TESTS

modules = [
    'test_buffer',
    'test_dat',
    'test_pkg',
    'test_gi',
    'test_gai',
]

for module_name in modules:
    try:
        module = importlib.__import__(module_name)
        TESTS.append(module.TEST)
    except Exception as e:
        print(f'Error while importing module {module_name}:')
        traceback.print_exc()
        print()


run_tests(TESTS)

