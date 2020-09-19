from ramstk.views.gtk3 import Gdk as Gdk, Gtk as Gtk
from ramstk.views.gtk3.widgets import RAMSTKCheckButton as RAMSTKCheckButton, RAMSTKComboBox as RAMSTKComboBox, RAMSTKEntry as RAMSTKEntry, RAMSTKFrame as RAMSTKFrame, RAMSTKPlot as RAMSTKPlot, RAMSTKScrolledWindow as RAMSTKScrolledWindow, RAMSTKTextView as RAMSTKTextView, RAMSTKTreeView as RAMSTKTreeView, do_make_label_group as do_make_label_group
from typing import Any, Dict, List, Union

class RAMSTKPanel(RAMSTKFrame):
    pltPlot: Any = ...
    tvwTreeView: Any = ...
    def __init__(self) -> None: ...
    def do_make_panel_fixed(self, **kwargs: Dict[str, Any]) -> None: ...
    def do_make_panel_plot(self) -> None: ...
    def do_make_panel_treeview(self) -> None: ...
    def on_cell_edit(self, cell: Gtk.CellRenderer, path: str, new_text: str, position: int, message: str) -> None: ...
    def on_changed_combo(self, combo: RAMSTKComboBox, index: int, message: str) -> Dict[Union[str, Any], Any]: ...
    def on_changed_text(self, entry: RAMSTKEntry, index: int, message: str) -> Dict[Union[str, Any], Any]: ...
    def on_edit(self, node_id: List[int], package: Dict[str, Any]) -> None: ...
    def on_focus_out(self, entry: object, __event: Gdk.EventFocus, index: int, message: str) -> Dict[Union[str, Any], Any]: ...
    def on_toggled(self, checkbutton: RAMSTKCheckButton, index: int, message: str) -> Dict[Union[str, Any], Any]: ...
