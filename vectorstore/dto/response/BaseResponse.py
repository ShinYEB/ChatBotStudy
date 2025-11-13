from pydantic.generics import GenericModel
from typing import TypeVar, Generic, Optional, List
from starlette import status

T = TypeVar('T')

class BaseResponse(GenericModel, Generic[T]):
    status: str = status.HTTP_200_OK
    message: Optional[str] = None
    data: Optional[T] = None