# Standard Library Imports
from typing import Any, Dict, List, Tuple

# Third Party Imports
import treelib

# RAMSTK Package Imports
from ramstk.configuration import RAMSTK_CONTROL_TYPES as RAMSTK_CONTROL_TYPES
from ramstk.configuration import RAMSTK_CRITICALITY as RAMSTK_CRITICALITY
from ramstk.configuration import (
    RAMSTK_FAILURE_PROBABILITY as RAMSTK_FAILURE_PROBABILITY
)
from ramstk.configuration import (
    RAMSTKUserConfiguration as RAMSTKUserConfiguration
)
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.views.gtk3 import GdkPixbuf as GdkPixbuf
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.assistants import AddControlAction as AddControlAction
from ramstk.views.gtk3.widgets import RAMSTKCheckButton as RAMSTKCheckButton
from ramstk.views.gtk3.widgets import RAMSTKLabel as RAMSTKLabel
from ramstk.views.gtk3.widgets import RAMSTKPanel as RAMSTKPanel
from ramstk.views.gtk3.widgets import RAMSTKTextView as RAMSTKTextView
from ramstk.views.gtk3.widgets import RAMSTKWorkView as RAMSTKWorkView

def do_request_insert(attributes: Dict[str, Any], level: str,
                      parent_id: str) -> None:
    ...


def get_indenture_level(record_id: str) -> str:
    ...


class MethodPanel(RAMSTKPanel):
    _dic_attribute_keys: Any = ...
    _lst_labels: Any = ...
    chkCriticality: Any = ...
    chkRPN: Any = ...
    txtItemCriticality: Any = ...
    _lst_widgets: Any = ...

    def __init__(self) -> None:
        ...

    def _do_clear_panel(self) -> None:
        ...

    def _do_load_panel(self, item_criticality: Dict[str, float]) -> None:
        ...

    def __do_set_callbacks(self) -> None:
        ...

    def __do_set_properties(self) -> None:
        ...


class FMEAPanel(RAMSTKPanel):
    _dic_column_masks: Dict[str, List[bool]] = ...
    _dic_headings: Any = ...
    _module: str = ...
    _dic_attribute_keys: Any = ...
    _dic_mission_phases: Any = ...
    _dic_row_loader: Any = ...
    _lst_fmea_data: Any = ...
    _lst_missions: Any = ...
    _title: Any = ...
    dic_action_category: Any = ...
    dic_action_status: Any = ...
    dic_detection: Any = ...
    dic_icons: Any = ...
    dic_occurrence: Any = ...
    dic_severity: Any = ...
    dic_users: Any = ...

    def __init__(self) -> None:
        ...

    def do_load_combobox(self) -> None:
        ...

    def do_set_callbacks(self) -> None:
        ...

    def _on_delete_insert_fmea(self, node_id: int, tree: treelib.Tree) -> None:
        ...

    _record_id: Any = ...

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        ...

    def __do_get_mission(self, entity: object) -> None:
        ...

    def __do_get_rpn_names(self, entity: object) -> Tuple[str, str, str, str]:
        ...

    def __do_get_rpn_values(self, position: int, name: str) -> int:
        ...

    def __do_load_action(self, node: treelib.Node,
                         row: Gtk.TreeIter) -> Gtk.TreeIter:
        ...

    def __do_load_action_category(self) -> None:
        ...

    def __do_load_cause(self, node: treelib.Node,
                        row: Gtk.TreeIter) -> Gtk.TreeIter:
        ...

    def __do_load_control(self, node: treelib.Node,
                          row: Gtk.TreeIter) -> Gtk.TreeIter:
        ...

    def __do_load_control_type(self) -> None:
        ...

    def __do_load_failure_probability(self) -> None:
        ...

    def __do_load_mechanism(self, node: treelib.Node,
                            row: Gtk.TreeIter) -> Gtk.TreeIter:
        ...

    def __do_load_missions(self, attributes: treelib.Tree) -> None:
        ...

    def __do_load_mission_phases(self, mission: str) -> None:
        ...

    def __do_load_mode(self, node: treelib.Node,
                       row: Gtk.TreeIter) -> Gtk.TreeIter:
        ...

    def __do_load_rpn_detection(self) -> None:
        ...

    def __do_load_rpn_occurrence(self) -> None:
        ...

    def __do_load_rpn_severity(self) -> None:
        ...

    def __do_load_severity_class(self) -> None:
        ...

    def __do_load_status(self) -> None:
        ...

    def __do_load_users(self) -> None:
        ...

    def __do_set_properties(self) -> None:
        ...

    def __on_cell_edit(self, cell: Gtk.CellRenderer, path: str, new_text: Any,
                       position: int) -> None:
        ...


class FMEA(RAMSTKWorkView):
    _module: str = ...
    _pixbuf: bool = ...
    _tablabel: str = ...
    _tabtooltip: str = ...
    _lst_callbacks: Any = ...
    _lst_icons: Any = ...
    _lst_mnu_labels: Any = ...
    _lst_tooltips: Any = ...
    _item_hazard_rate: float = ...
    _pnlMethods: Any = ...
    _pnlPanel: Any = ...

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        ...

    def _do_request_calculate(self, __button: Gtk.ToolButton) -> None:
        ...

    def _do_request_delete(self, __button: Gtk.ToolButton) -> None:
        ...

    def _do_request_insert_child(self, __button: Gtk.ToolButton) -> None:
        ...

    def _do_request_insert_sibling(self, __button: Gtk.ToolButton) -> None:
        ...

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        ...

    def _do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        ...

    _parent_id: Any = ...

    def _do_set_parent(self, attributes: Dict[str, Any]) -> None:
        ...

    def _on_get_hardware_attributes(self, attributes: Dict[str, Any]) -> None:
        ...

    def __do_set_callbacks(self) -> None:
        ...

    def __make_ui(self) -> None:
        ...

    def __on_request_insert_control_action(self) -> str:
        ...
