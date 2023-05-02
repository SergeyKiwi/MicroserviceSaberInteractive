import uvicorn
from src.config import IP, PORT

if __name__ == "__main__":
    uvicorn.run("src.app:app", host=IP, port=PORT, reload=True)
