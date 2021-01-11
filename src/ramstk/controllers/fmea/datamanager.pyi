# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager as RAMSTKDataManager
from ramstk.exceptions import DataAccessError as DataAccessError
from ramstk.models.programdb import RAMSTKAction as RAMSTKAction
from ramstk.models.programdb import RAMSTKCause as RAMSTKCause
from ramstk.models.programdb import RAMSTKControl as RAMSTKControl
from ramstk.models.programdb import RAMSTKMechanism as RAMSTKMechanism
from ramstk.models.programdb import RAMSTKMode as RAMSTKMode

class DataManager(RAMSTKDataManager):
    _tag: str = ...
    _root: int = ...
    _pkey: Any = ...
    _is_functional: Any = ...
    _parent_id: int = ...
    last_id: Any = ...

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        ...

    def do_get_tree(self) -> None:
        ...

    _revision_id: Any = ...

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        ...

    def do_update(self, node_id: int) -> None:
        ...

    def _add_cause_node(self, cause: RAMSTKCause, parent_id: str) -> None:
        ...

    def _add_mode_node(self, mode: RAMSTKMode) -> None:
        ...

    def _do_delete(self, node_id: int) -> None:
        ...

    def _do_insert_action(self, parent_id: str) -> None:
        ...

    def _do_insert_cause(self, parent_id: str) -> None:
        ...

    def _do_insert_control(self, parent_id: str) -> None:
        ...

    def _do_insert_mechanism(self, mode_id: str) -> None:
        ...

    def _do_insert_mode(self) -> None:
        ...

    def _do_select_all_action(self, parent_id: str) -> None:
        ...

    def _do_select_all_cause(self, parent_id: str) -> None:
        ...

    def _do_select_all_control(self, parent_id: str) -> None:
        ...

    def _do_select_all_functional_fmea(self) -> None:
        ...

    def _do_select_all_hardware_fmea(self) -> None:
        ...

    def _do_select_all_mechanism(self, mode_id: int) -> None:
        ...
