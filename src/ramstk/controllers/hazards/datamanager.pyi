from ramstk.controllers import RAMSTKDataManager as RAMSTKDataManager
from ramstk.exceptions import DataAccessError as DataAccessError
from ramstk.models.programdb import RAMSTKHazardAnalysis as RAMSTKHazardAnalysis
from typing import Any, Dict

class DataManager(RAMSTKDataManager):
    _tag: str = ...
    _pkey: Any = ...
    _last_id: Any = ...
    def __init__(self, **kwargs: Dict[Any, Any]) -> None: ...
    def do_get_tree(self) -> None: ...
    _revision_id: Any = ...
    last_id: Any = ...
    def do_select_all(self, attributes: Dict[str, Any]) -> None: ...
    def do_update(self, node_id: int) -> None: ...
    def _do_delete_hazard(self, node_id: int) -> None: ...
    def _do_insert_hazard(self, parent_id: int=...) -> None: ...
