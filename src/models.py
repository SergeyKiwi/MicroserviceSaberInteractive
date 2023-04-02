from pydantic import BaseModel
import yaml
from typing import List
import logging


def read_file_yaml(filepath):
    with open(filepath) as file_yaml:
        data = yaml.safe_load(file_yaml)
        return data


class BuildParameters(BaseModel):
    build: str


class BuildsManager:
    def __init__(self, builds_filepath=None, tasks_filepath=None):
        self.builds_filepath = builds_filepath
        self.tasks_filepath = tasks_filepath

        self.builds = None
        self.tasks = None
        self.builds_with_full_task_sequence = None

    def set_builds_filename(self, filename):
        self.builds_filepath = filename

    def set_tasks_filename(self, filename):
        self.tasks_filepath = filename

    def read_file_builds(self):
        data = read_file_yaml(self.builds_filepath)
        builds = {}

        for build in data['builds']:
            builds[build['name']] = build['tasks']

        return builds

    def read_file_tasks(self):
        data = read_file_yaml(self.tasks_filepath)
        tasks = {}

        for task in data['tasks']:
            tasks[task['name']] = task['dependencies']

        return tasks

    def get_task_sequence(self, build):
        task_sequence = None

        if self.builds_with_full_task_sequence:
            task_sequence = self.builds_with_full_task_sequence.get(build)

        return task_sequence

    def build_task_sequence(self, builds, tasks):
        try:
            builds_with_full_task_sequence = {}

            for name, build_tasks in builds.items():
                queue_task = []

                for task in build_tasks:
                    self.task_sequence(tasks, task, queue_task)

                builds_with_full_task_sequence[name] = queue_task

            return builds_with_full_task_sequence
        except Exception as exc:
            logging.critical("An error in constructing the task sequence. Input data error!")
            return None

    def task_sequence(self, tasks, task, queue: List):
        if len(tasks[task]) > 0:
            for ts in tasks[task]:
                self.task_sequence(tasks, ts, queue)
        queue.append(task)

    def update_data(self):
        try:
            builds = self.read_file_builds()
            tasks = self.read_file_tasks()

            self.builds_with_full_task_sequence = self.build_task_sequence(builds, tasks)
        except Exception as exc:
            logging.error(exc)
            logging.error(msg="Error reading input data. Stopping data updates! Rollback to old data.")


