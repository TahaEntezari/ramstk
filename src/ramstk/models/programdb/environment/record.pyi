# Standard Library Imports
from typing import Any

# Third Party Imports
from sqlalchemy.orm import relationship

# RAMSTK Package Imports
from ramstk.db import RAMSTK_BASE as RAMSTK_BASE
from ramstk.models import RAMSTKBaseRecord as RAMSTKBaseRecord

class RAMSTKEnvironmentRecord(RAMSTK_BASE, RAMSTKBaseRecord):
    __defaults__: Any
    __tablename__: str
    __table_args__: Any
    revision_id: Any
    mission_id: Any
    phase_id: Any
    environment_id: Any
    name: Any
    units: Any
    minimum: Any
    maximum: Any
    mean: Any
    variance: Any
    ramp_rate: Any
    low_dwell_time: Any
    high_dwell_time: Any
    phase: relationship
    is_mission: bool
    is_phase: bool
    is_env: bool
    def get_attributes(self): ...
