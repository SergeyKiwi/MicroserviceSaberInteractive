import uvicorn
from src.settings import *

if __name__ == "__main__":
    uvicorn.run("src.app:app", host=IP, port=PORT, reload=True)
