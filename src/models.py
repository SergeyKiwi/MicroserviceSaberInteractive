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
        self.builds_with_full_task_queue = None

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

    def get_task_queue(self, build):
        task_queue = None

        if self.builds_with_full_task_queue:
            task_queue = self.builds_with_full_task_queue.get(build)

        return task_queue

    def build_tasks_queue(self, builds, tasks):
        try:
            builds_with_full_task_queue = {}

            for name, build_tasks in builds.items():
                queue_task = []

                for task in build_tasks:
                    self.task_queue(tasks, task, queue_task)

                builds_with_full_task_queue[name] = queue_task

            return builds_with_full_task_queue
        except Exception as exc:
            logging.critical(
                "An error in constructing the task queue. Input data error!")
            return None

    def task_queue(self, tasks, task, queue: List):
        """
        Recursively generates a sorted list for each task, taking into account dependencies

        :param tasks: list of all possible tasks
        :param task: the current task for finding dependencies
        :param queue: sorted queue of tasks for building
        """
        if len(tasks[task]) > 0:
            for ts in tasks[task]:
                self.task_queue(tasks, ts, queue)

        if task not in queue:                
            queue.append(task)

    def update_data(self):
        try:
            builds = self.read_file_builds()
            tasks = self.read_file_tasks()

            self.builds_with_full_task_queue = self.build_tasks_queue(
                builds, tasks)
        except Exception as exc:
            logging.error(exc)
            logging.error(
                msg="Error reading input data. Stopping data updates! Rollback to old data.")
