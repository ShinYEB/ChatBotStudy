from fastapi import FastAPI

from dto.response.BaseResponse import BaseResponse
from exception.APIException import APIException
from exception.ExceptionHandler import api_exception_handler
from service.RetrieverService import build, split
app = FastAPI()
app.add_exception_handler(APIException, api_exception_handler)

@app.get("/health")
def health():
    return True

@app.get("/build",
          response_model=BaseResponse)
def building():
    try:
        return BaseResponse(
            message="success",
            data={"answer" : build()}
        )
    except Exception as e:
        raise APIException.from_exception(e)

@app.get("/split")
def splitting():
    try:
        return BaseResponse(
            message="success",
            data={"answer": split()}
        )
    except Exception as e:
        raise APIException.from_exception(e)

