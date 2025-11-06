from starlette import status

class APIException(Exception):

    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)

    @classmethod
    def from_exception(cls, exc: Exception):
        if isinstance(exc, KeyError):
            return cls(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"요청한 리소스를 찾을 수 없습니다 (키: {exc})"
            )

        elif isinstance(exc, ValueError):
            return cls(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"잘못된 값이 입력되었습니다: {exc}"
            )

        else:
            return cls(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"서버 내부 오류가 발생했습니다: {exc}"
            )