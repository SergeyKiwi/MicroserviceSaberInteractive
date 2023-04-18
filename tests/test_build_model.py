from src.buildsmanager import BuildsManager
import pytest
from tempfile import NamedTemporaryFile

path_builds = './tests/builds/builds.yaml'
path_tasks = './tests/builds/tasks.yaml'

path_builds_error_yamls = './tests/builds/builds_error_yaml.yaml'
path_tasks_not_all = './tests/builds/tasks_not_all.yaml'


def test_building_fake_data():
    buildsManager = BuildsManager()

    builds = {
        'test_build': [
            'A',
            'B',
            'C'
        ],
        'test_build2': [
            'CC',
            'BB',
            'A'
        ]
    }

    tasks = {
        'A': [
            'AA',
            'AAA'
        ],
        'B': [
            'AAA',
            'BB'
        ],
        'C': [
            'AA',
            'CC',
            'BB',
            'CCC'
        ],
        'AA': [
            '2AA',
            '3AA'
        ],
        'AAA': [],
        'CC': [
            '3CC'
        ],
        'BB': [],
        '3AA': [],
        '2AA': [],
        'CCC': [],
        '3CC': [],
    }        

    assert buildsManager.build_queues_for_builds(builds, tasks) == {
        'test_build': [
            '2AA', '3AA', 'AA', 'AAA', 'A', 'BB', 'B', '3CC', 'CC', 'CCC', 'C'
        ],
        'test_build2': [
            '3CC', 'CC', 'BB', '2AA', '3AA', 'AA', 'AAA', 'A'
        ]
    }


def test_no_task_in_tasks():
    buildsManager = BuildsManager()

    builds = {
        'test_build': [
            'A',
            'B'
        ]
    }

    tasks = {
        'A': [
            'AA',
            'AAA'
        ],
        'B': [
            'AAA',
            'BB'
        ],
        'AA': [
            '2AA',
            '3AA'
        ],        
        'BB': []
    }        

    with pytest.raises(Exception) as exc:
        buildsManager.build_queues_for_builds(builds, tasks)

    assert KeyError == exc.type
    assert "'2AA'" in str(exc.value)


def test_no_task_from_build():
    buildsManager = BuildsManager()

    builds = {
        'test_build': [
            'A',
            'B',
            'C'
        ]
    }

    tasks = {
        'A': [
            'AA',
            'AAA'
        ],
        'B': [
            'AAA',
            'BB'
        ],        
        'AA': [
            '2AA',
            '3AA'
        ],
        'AAA': [],
        'CC': [
            '3CC'
        ],
        'BB': [],
        '3AA': [],
        '2AA': [],
        'CCC': [],
        '3CC': [],
    }        

    with pytest.raises(Exception) as exc:
        buildsManager.build_queues_for_builds(builds, tasks)

    assert KeyError == exc.type
    assert "'C'" in str(exc.value)


def test_update_error_yaml(caplog):   
    buildsManager = BuildsManager(
        builds_filepath=path_builds_error_yamls,
        tasks_filepath=path_tasks)

    buildsManager.update_data()

    assert 'Error reading input data' in caplog.records[1].msg


def test_update_not_all_tasks(caplog):   
    buildsManager = BuildsManager(
        builds_filepath=path_builds,
        tasks_filepath=path_tasks_not_all)

    buildsManager.update_data()

    assert 'Input data error' in caplog.records[0].msg


def test_update(caplog):   
    buildsManager = BuildsManager(
        builds_filepath=path_builds,
        tasks_filepath=path_tasks)

    buildsManager.update_data()

    assert len(caplog.records) == 0