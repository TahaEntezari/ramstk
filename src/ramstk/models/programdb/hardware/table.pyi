# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.models import RAMSTKBaseTable as RAMSTKBaseTable
from ramstk.models import RAMSTKHardwareRecord as RAMSTKHardwareRecord

class RAMSTKHardwareTable(RAMSTKBaseTable):
    _db_id_colname: str
    _db_tablename: str
    _select_msg: str
    _tag: str
    _lst_id_columns: Any
    _record: Any
    pkey: str
    def __init__(self, **kwargs: Dict[Any, Any]) -> None: ...
    def do_get_new_record(self, attributes: Dict[str, Any]) -> object: ...
    def do_calculate_cost(self, node_id: int) -> float: ...
    def do_calculate_part_count(self, node_id: int) -> int: ...
    def do_make_composite_ref_des(self, node_id: int = ...) -> None: ...
