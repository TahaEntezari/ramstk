# Standard Library Imports
from typing import Any, Dict, Tuple

# RAMSTK Package Imports
from ramstk.models import RAMSTKBaseTable

class RAMSTKAllocationTable(RAMSTKBaseTable):
    _db_id_colname: str
    _db_tablename: str
    _select_msg: str
    _tag: str
    _system_hazard_rate: float
    _lst_id_columns: Any
    _node_hazard_rate: float
    _record: Any
    pkey: str
    def __init__(self, **kwargs: Dict[str, Any]) -> None: ...
    _parent_id: Any
    def do_get_new_record(self, attributes: Dict[str, Any]) -> object: ...
    def do_calculate_allocation_goals(self, node_id: int) -> None: ...
    def do_calculate_agree_allocation(
        self, node_id: int, duty_cycle: float
    ) -> None: ...
    def do_calculate_arinc_allocation(self, node_id: int) -> None: ...
    def do_calculate_equal_allocation(self, node_id: int) -> None: ...
    def do_calculate_foo_allocation(self, node_id: int) -> None: ...
    def _do_calculate_agree_total_elements(self, node_id: int) -> Tuple[int, int]: ...
    def _do_calculate_foo_cumulative_weight(self, node_id: int) -> int: ...
