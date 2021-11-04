from __future__ import annotations
from typing import (
    Union,
    Iterator,
    # Type, List, Dict,
    # Mapping,
    TypeVar,
    Protocol,
    Generic,
    runtime_checkable,
    TYPE_CHECKING,
)

import json
import base64

StateDict = Union[dict[str, Union[int, str]], bytes]

if TYPE_CHECKING:
    class JSONArray(list[JSON], Protocol):  # type: ignore
        __class__: type[list[JSON]]  # type: ignore

    class JSONObject(dict[str, JSON], Protocol):  # type: ignore
        __class__: type[dict[str, JSON]]  # type: ignore

    JSON = Union[None, float, str, JSONArray, JSONObject]



T = TypeVar('T')


@runtime_checkable
class RangersModule(Protocol):

    def __save_state__(self) -> JSON:
        ...

    def __restore_state__(self, data: JSON) -> None:
        ...

    def __on_turn_code__(self) -> None:
        ...

    def __on_dialogbegin_code__(self) -> None:
        ...

    def __on_act_code__(self) -> None:
        ...

class MasterMod(RangersModule):
    modules: dict[str, RangersModule]

    def __init__(self) -> None:
        self.modules = {}

    def __save_state__(self) -> str:
        data = {}
        for module_name, module in self.modules.items():
            try:
                module_data = module.__save_state__()
                module_s = json.dumps(module_data)
                module_d = module_s.encode(encoding='utf-8', errors='xmlcharrefreplace')
                module_b = base64.b64encode(module_d)
                module_c = module_b.decode()

                # module_name = module.name
                data[module_name] = module_c
            except:
                pass

        data_s = json.dumps(data)
        data_d = data_s.encode(encoding='utf-8', errors='xmlcharrefreplace')
        data_b = base64.b64encode(data_d)
        data_c = data_b.decode()

        return data_c

    def __restore_state__(self, data: str) -> None:  # type: ignore[override]
        data_b = data.encode()
        data_d = base64.b64decode(data_b)
        data_s = data_d.decode(encoding='utf-8', errors='xmlcharrefreplace')
        data = json.loads(data_s)

        for module_name, module in self.modules.items():
            try:
                ...
            except:
                pass




