def update(d, info):
    d.update(info)
    return d


def task_test():
    return {
        'actions': ['PYTHONPATH=. py.test tests/*_tests.py'],
        'verbosity': 2,
    }


def task_develop():
    yield update(
        task_install_dev_dependencies(),
        {'name': 'install_dev_dependencies'})
    yield update(
        task_install_runtime_dependencies(),
        {'name': 'install_runtime_dependences'})


def task_install_dev_dependencies():
    return {
        'actions': ['pip install -r requirements/dev.txt'],
    }


def task_install_runtime_dependencies():
    return {
        'actions': ['pip install -r requirements/run.txt'],
    }


def task_install():
    return {'actions': ['python setup.py install']}


def task_clean():
    return {'actions': ['pip uninstall pypl']}
