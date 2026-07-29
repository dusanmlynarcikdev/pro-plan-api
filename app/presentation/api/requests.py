from pydantic import ConfigDict

from app.presentation.api.responses import BaseResponse


class BaseRequest(BaseResponse):
    model_config = ConfigDict(str_min_length=1, str_strip_whitespace=True)
