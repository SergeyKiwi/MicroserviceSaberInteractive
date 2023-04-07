from src.models import BuildsManager

buildsManager = BuildsManager()

def test_fake_data():
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

    assert buildsManager.build_tasks_queue(builds, tasks) == {'test_build': [
        '2AA', '3AA', 'AA', 'AAA', 'A', 'BB', 'B', '3CC', 'CC', 'CCC', 'C'
    ]}