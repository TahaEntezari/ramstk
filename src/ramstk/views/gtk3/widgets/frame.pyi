# Stubs for ramstk.views.gtk3.widgets.frame (Python 3)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from .label import RAMSTKLabel
from ramstk.views.gtk3 import Gtk
from typing import Any

class RAMSTKFrame(Gtk.Frame):
    def __init__(self) -> None: ...
    def do_set_properties(self, **kwargs: Any) -> None: ...

    def add(self, _scrollwindow):
        pass
