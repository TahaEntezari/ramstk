from ramstk.controllers import RAMSTKDataManager as RAMSTKDataManager
from ramstk.exceptions import DataAccessError as DataAccessError
from ramstk.models.programdb import RAMSTKFailureDefinition as RAMSTKFailureDefinition
from typing import Any, Dict, List

class DataManager(RAMSTKDataManager):
    _tag: str = ...
    def __init__(self, **kwargs: Dict[Any, Any]) -> None: ...
    last_id: Any = ...
    def _do_delete_failure_definition(self, node_id: int) -> None: ...
    def _do_get_attributes(self, node_id: int, table: str) -> None: ...
    def do_get_tree(self) -> None: ...
    def do_insert_failure_definition(self) -> None: ...
    _revision_id: Any = ...
    def do_select_all(self, attributes: Dict[str, Any]) -> None: ...
    def do_set_all_attributes(self, attributes: Dict[str, Any]) -> None: ...
    def do_set_attributes(self, node_id: List, package: Dict[str, Any]) -> None: ...
    def do_update(self, node_id: int) -> None: ...
