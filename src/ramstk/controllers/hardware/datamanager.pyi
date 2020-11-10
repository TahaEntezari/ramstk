# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager as RAMSTKDataManager
from ramstk.exceptions import DataAccessError as DataAccessError
from ramstk.models.programdb import RAMSTKNSWC as RAMSTKNSWC
from ramstk.models.programdb import RAMSTKAllocation as RAMSTKAllocation
from ramstk.models.programdb import (
    RAMSTKDesignElectric as RAMSTKDesignElectric
)
from ramstk.models.programdb import (
    RAMSTKDesignMechanic as RAMSTKDesignMechanic
)
from ramstk.models.programdb import RAMSTKHardware as RAMSTKHardware
from ramstk.models.programdb import RAMSTKMilHdbkF as RAMSTKMilHdbkF
from ramstk.models.programdb import RAMSTKReliability as RAMSTKReliability
from ramstk.models.programdb import RAMSTKSimilarItem as RAMSTKSimilarItem

class DataManager(RAMSTKDataManager):
    _tag: str = ...
    _root: int = ...
    _pkey: Any = ...

    def __init__(self, **kwargs: Dict[str, Any]) -> None:
        ...

    def do_get_tree(self) -> None:
        ...

    _revision_id: Any = ...
    last_id: Any = ...

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        ...

    def do_update(self, node_id: int) -> None:
        ...

    def _do_delete_hardware(self, node_id: int) -> None:
        ...

    def _do_get_all_attributes(self, node_id: int) -> None:
        ...

    def _do_insert_hardware(self, parent_id: int, part: int) -> None:
        ...

    def _do_make_composite_ref_des(self, node_id: int = ...) -> None:
        ...

    def _do_set_all_attributes(self, attributes: Dict[str, Any]) -> None:
        ...
