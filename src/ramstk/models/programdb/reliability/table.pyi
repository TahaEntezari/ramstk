# Standard Library Imports
from typing import Any, Dict

# RAMSTK Package Imports
from ramstk.analyses import dormancy as dormancy
from ramstk.analyses.statistics import exponential as exponential
from ramstk.analyses.statistics import lognormal as lognormal
from ramstk.analyses.statistics import normal as normal
from ramstk.analyses.statistics import weibull as weibull
from ramstk.models import RAMSTKBaseTable as RAMSTKBaseTable
from ramstk.models import RAMSTKReliabilityRecord as RAMSTKReliabilityRecord

class RAMSTKReliabilityTable(RAMSTKBaseTable):
    _db_id_colname: str
    _db_tablename: str
    _select_msg: str
    _tag: str
    _lst_id_columns: Any
    _record: Any
    pkey: str
    def __init__(self, **kwargs: Dict[Any, Any]) -> None: ...
    def do_get_new_record(self, attributes: Dict[str, Any]) -> object: ...
    def do_calculate_hazard_rate_active(
        self,
        node_id: int,
        duty_cycle: float,
        quantity: int,
        multiplier: float,
        time: float = ...,
    ) -> None: ...
    def do_calculate_hazard_rate_dormant(
        self,
        node_id: int,
        category_id: int,
        subcategory_id: int,
        env_active: int,
        env_dormant: int,
    ) -> None: ...
    def do_calculate_hazard_rate_logistics(self, node_id: int) -> None: ...
    def do_calculate_hazard_rate_mission(
        self, node_id: int, duty_cycle: float
    ) -> None: ...
    def do_calculate_mtbf(self, node_id: int, multiplier: float) -> None: ...
    def do_calculate_reliability(self, node_id: int, time: float) -> None: ...
