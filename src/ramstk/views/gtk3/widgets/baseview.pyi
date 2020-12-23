# Standard Library Imports
from typing import Any, Dict, List, Tuple

# Third Party Imports
import pandas as pd
import treelib

# RAMSTK Package Imports
from ramstk.configuration import (
    RAMSTKUserConfiguration as RAMSTKUserConfiguration
)
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.views.gtk3 import Gdk as Gdk
from ramstk.views.gtk3 import GObject as GObject
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _

# RAMSTK Local Imports
from .button import do_make_buttonbox as do_make_buttonbox
from .dialog import RAMSTKMessageDialog as RAMSTKMessageDialog
from .label import RAMSTKLabel as RAMSTKLabel
from .matrixview import RAMSTKMatrixView as RAMSTKMatrixView
from .panel import RAMSTKPanel as RAMSTKPanel
from .treeview import RAMSTKTreeView as RAMSTKTreeView

class RAMSTKBaseView(Gtk.HBox):
    _pixbuf: bool = ...
    dic_tab_position: Any = ...
    RAMSTK_USER_CONFIGURATION: RAMSTKUserConfiguration = ...
    RAMSTK_LOGGER: Any = ...
    _dic_icons: Any = ...
    _lst_callbacks: Any = ...
    _lst_icons: Any = ...
    _lst_mnu_labels: Any = ...
    _lst_tooltips: Any = ...
    _lst_col_order: Any = ...
    _lst_handler_id: Any = ...
    _lst_layouts: Any = ...
    _img_tab: Any = ...
    _mission_time: Any = ...
    _notebook: Any = ...
    _parent_id: int = ...
    _pnlPanel: Any = ...
    _record_id: int = ...
    _revision_id: int = ...
    _tree_loaded: bool = ...
    treeview: Any = ...
    fmt: Any = ...
    hbx_tab_label: Any = ...

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        ...

    def do_request_delete(self, __button: Gtk.ToolButton) -> None:
        ...

    def __set_callbacks(self) -> None:
        ...

    def __set_icons(self) -> Dict[str, str]:
        ...

    def _make_treeview(self) -> RAMSTKTreeView:
        ...

    def do_embed_matrixview_panel(self) -> None:
        ...

    def do_embed_treeview_panel(self) -> None:
        ...

    def do_expand_tree(self) -> None:
        ...

    def do_get_headings(self, level: str) -> List:
        ...

    def do_load_row(self, attributes: Dict[str, Any]) -> None:
        ...

    def do_make_layout(self) -> None:
        ...

    def do_make_layout_lr(self) -> Gtk.HPaned:
        ...

    def do_make_layout_lrr(self) -> Tuple[Gtk.HPaned, Gtk.VPaned]:
        ...

    def do_make_layout_llr(self) -> Tuple[Gtk.HPaned, Gtk.VPaned]:
        ...

    def do_make_layout_llrr(self) -> Tuple[Gtk.VPaned, Gtk.VPaned]:
        ...

    def do_raise_dialog(self, **kwargs: Any) -> RAMSTKMessageDialog:
        ...

    def do_refresh_tree(self, node_id: List, package: Dict[str, Any]) -> None:
        ...

    def do_request_insert(self, **kwargs: Any) -> None:
        ...

    def do_request_insert_child(self, __button: Gtk.ToolButton) -> Any:
        ...

    def do_request_insert_sibling(self, __button: Gtk.ToolButton) -> Any:
        ...

    def do_request_update(self, __button: Gtk.ToolButton) -> None:
        ...

    def do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        ...

    def do_set_cursor(self, cursor: Gdk.CursorType) -> None:
        ...

    def do_set_cursor_active(self, tree: treelib.Tree = ...) -> None:
        ...

    def do_set_cursor_active_on_fail(self, error_message: str = ...) -> None:
        ...

    def do_set_cursor_busy(self) -> None:
        ...

    def make_tab_label(self, **kwargs: Dict[str, Any]) -> None:
        ...

    def make_toolbuttons(self, **kwargs: Dict[str, Any]) -> None:
        ...

    def on_button_press(self, __treeview: RAMSTKTreeView,
                        event: Gdk.EventButton) -> None:
        ...

    def on_delete(self, node_id: int, tree: treelib.Tree) -> None:
        ...

    def on_insert(self, node_id: int = ..., tree: treelib.Tree = ...) -> None:
        ...

    def on_row_change(self, selection: Gtk.TreeSelection) -> Dict[str, Any]:
        ...

    def on_select_revision(self, attributes: Dict[str, Any]) -> None:
        ...


class RAMSTKListView(RAMSTKBaseView):
    matrixview: Any = ...
    tab_label: Any = ...

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        ...

    def _do_request_update(self, __button: Gtk.ToolButton) -> None:
        ...

    def do_request_update_all(self, __button: Gtk.ToolButton) -> None:
        ...

    def do_load_matrix(self, matrix_type: str, matrix: pd.DataFrame) -> None:
        ...

    def make_ui(self) -> None:
        ...


class RAMSTKModuleView(RAMSTKBaseView):
    _dic_key_index: Any = ...

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        ...

    def make_ui(self) -> None:
        ...


class RAMSTKWorkView(RAMSTKBaseView):
    _lst_widgets: Any = ...

    def __init__(self, configuration: RAMSTKUserConfiguration,
                 logger: RAMSTKLogManager) -> None:
        ...

    def do_clear_tree(self) -> None:
        ...

    def on_edit(self, node_id: List[int], package: Dict[str, Any]) -> None:
        ...
