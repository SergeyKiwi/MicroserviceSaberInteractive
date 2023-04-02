import uvicorn
from settings import *

if __name__ == "__main__":
    uvicorn.run("app:app", host=IP, port=PORT, reload=True)
