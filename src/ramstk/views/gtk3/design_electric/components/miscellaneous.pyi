# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel

class MiscDesignElectricInputPanel(RAMSTKFixedPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: str
    cmbApplication: RAMSTKComboBox
    cmbQuality: RAMSTKComboBox
    cmbType: RAMSTKComboBox
    txtFrequency: RAMSTKEntry
    txtUtilization: RAMSTKEntry
    _duty_cycle: float
    _hazard_rate_method_id: int
    _quality_id: int
    dic_attribute_widget_map: Dict[str, List[Any]]
    category_id: int
    subcategory_id: int
    def __init__(self) -> None: ...
    def do_load_comboboxes(self, subcategory_id: int) -> None: ...
    def _do_load_panel(self, attributes: Dict[str, Any]) -> None: ...
    def _do_set_hardware_attributes(self, attributes: Dict[str, Any]) -> None: ...
    def _do_set_reliability_attributes(self, attributes: Dict[str, Any]) -> None: ...
    def _do_set_sensitive(self, attributes: Dict[str, Any]) -> None: ...
    def __do_load_crystal(self, attributes: Dict[str, Any]) -> None: ...
    def __do_load_filter(self, attributes: Dict[str, Any]) -> None: ...
    def __do_load_lamp(self, attributes: Dict[str, Any]) -> None: ...
    def __do_set_crystal_sensitive(self, attributes: Dict[str, Any]) -> None: ...
    def __do_set_lamp_sensitive(self, attributes: Dict[str, Any]) -> None: ...
