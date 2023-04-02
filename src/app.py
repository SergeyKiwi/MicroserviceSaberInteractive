from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from models import BuildParameters, BuildsManager
from settings import builds_filepath, tasks_filepath

buildsManager = BuildsManager(builds_filepath=builds_filepath,
                              tasks_filepath=tasks_filepath)
buildsManager.update_data()

app = FastAPI()


@app.post('/POST/get_tasks')
async def get_build_tasks(build_parameters: BuildParameters):
    build = build_parameters.build

    task_sequence = buildsManager.get_task_sequence(build)

    if task_sequence:
        return {'tasks': task_sequence}
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'Error': 'Build not found'})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(status_code=400, content={'Error': 'Invalid JSON request!'})
