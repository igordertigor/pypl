def task_test():
    return {
        'actions': ['PYTHONPATH=. py.test tests/*_tests.py'],
        'verbosity': 2,
    }
