# Standard Library Imports
from typing import Any

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKCheckButton as RAMSTKCheckButton
from ramstk.views.gtk3.widgets import RAMSTKEntry as RAMSTKEntry
from ramstk.views.gtk3.widgets import RAMSTKFixedPanel as RAMSTKFixedPanel
from ramstk.views.gtk3.widgets import RAMSTKTextView as RAMSTKTextView
from ramstk.views.gtk3.widgets import RAMSTKTreePanel as RAMSTKTreePanel

class FunctionTreePanel(RAMSTKTreePanel):
    _select_msg: str
    _tag: str
    _title: Any
    _type: str
    _dic_row_loader: Any
    dic_attribute_widget_map: Any
    def __init__(self) -> None: ...
    def _on_module_switch(self, module: str = ...) -> None: ...
    _record_id: Any
    _parent_id: Any
    def _on_row_change(self, selection: Gtk.TreeSelection) -> None: ...

class FunctionGeneralDataPanel(RAMSTKFixedPanel):
    _record_field: str
    _select_msg: str
    _tag: str
    _title: Any
    _type: str
    chkSafetyCritical: Any
    txtCode: Any
    txtName: Any
    txtRemarks: Any
    dic_attribute_widget_map: Any
    def __init__(self) -> None: ...
