from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import bing
from bing import WebDriverException

app = FastAPI()


class ChatRequest(BaseModel):
    question: str


@app.get("/")
def read_root():
    return {"result": "Welcome"}


@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        answer = bing.bot(req.question)
    except WebDriverException as e:
        raise HTTPException(status_code=500, detail=f"Bot error WebDriverException: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bot error: {e}")

    return {"result": answer}
