from fastapi import FastAPI

from dto.request.ChatRequest import ChatRequest
from dto.response.BaseResponse import BaseResponse
from service.chatbotService import generate
from exception.APIException import APIException
from exception.ExceptionHandler import api_exception_handler

app = FastAPI()
app.add_exception_handler(APIException, api_exception_handler)

@app.get("/health")
def health():
    return True

@app.post("/chat",
          response_model=BaseResponse)
def chat(request: ChatRequest):
    try:
        return BaseResponse(
            message="success",
            data={"answer" : generate(request.prompt)}
        )
    except Exception as e:
        raise APIException.from_exception(e)

