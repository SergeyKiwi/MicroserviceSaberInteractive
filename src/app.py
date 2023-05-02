from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from src.models import BuildRequest, BuildResponse
from src.buildsmanager import BuildsManager
from src.config import BUILDS_FILEPATH, TASKS_FILEPATH

buildsManager = BuildsManager(builds_filepath=BUILDS_FILEPATH,
                              tasks_filepath=TASKS_FILEPATH)
buildsManager.update_data()

app = FastAPI()


@app.post('/POST/get_tasks')
async def get_build_tasks(build_request: BuildRequest):
    build = build_request.build

    task_queue = buildsManager.get_task_queue(build)

    if task_queue:
        return BuildResponse(tasks=task_queue)
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'Error': 'Build not found'})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(status_code=400, content={'Error': 'Invalid JSON request!'})
