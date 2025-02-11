# Standard Library Imports
from typing import Any, Dict, List

# RAMSTK Package Imports
from ramstk.configuration import RAMSTKUserConfiguration as RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.views.gtk3 import Gtk as Gtk
from ramstk.views.gtk3 import _ as _
from ramstk.views.gtk3.widgets import RAMSTKListView as RAMSTKListView
from ramstk.views.gtk3.widgets import RAMSTKPanel as RAMSTKPanel

# RAMSTK Local Imports
from . import FailureDefinitionTreePanel as FailureDefinitionTreePanel

class FailureDefinitionListView(RAMSTKListView):
    _tag: str
    _tablabel: str
    _tabtooltip: str
    _lst_mnu_labels: List[str]
    _lst_tooltips: List[str]
    _pnlPanel: RAMSTKPanel
    def __init__(
        self, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager
    ) -> None: ...
    def _do_request_delete(self, __button: Gtk.ToolButton) -> None: ...
    _record_id: int
    def _do_set_record_id(self, attributes: Dict[str, Any]) -> None: ...
    def __make_ui(self) -> None: ...
