from ramstk.configuration import RAMSTKUserConfiguration as RAMSTKUserConfiguration
from ramstk.logger import RAMSTKLogManager as RAMSTKLogManager
from ramstk.utilities import integer_to_boolean as integer_to_boolean, string_to_boolean as string_to_boolean
from ramstk.views.gtk3 import GObject as GObject, Gdk as Gdk, Gtk as Gtk
from ramstk.views.gtk3.widgets import RAMSTKBaseView as RAMSTKBaseView, RAMSTKComboBox as RAMSTKComboBox, RAMSTKEntry as RAMSTKEntry, RAMSTKFrame as RAMSTKFrame, RAMSTKLabel as RAMSTKLabel, RAMSTKScrolledWindow as RAMSTKScrolledWindow, do_make_buttonbox as do_make_buttonbox, do_make_column as do_make_column, do_make_label_group as do_make_label_group, do_make_text_cell as do_make_text_cell, do_make_toggle_cell as do_make_toggle_cell, do_set_cell_properties as do_set_cell_properties
from typing import Any

class EditPreferences(Gtk.Window, RAMSTKBaseView):
    btnConfDir: Any = ...
    btnDataDir: Any = ...
    btnIconDir: Any = ...
    btnLogDir: Any = ...
    cmbModuleBookTabPosition: Any = ...
    cmbWorkBookTabPosition: Any = ...
    cmbListBookTabPosition: Any = ...
    cmbReportSize: Any = ...
    txtFRMultiplier: Any = ...
    txtDecimalPlaces: Any = ...
    txtMissionTime: Any = ...
    cmbFormatFiles: Any = ...
    tvwFormatFile: Any = ...
    btnRevisionBGColor: Any = ...
    btnRevisionFGColor: Any = ...
    btnFunctionBGColor: Any = ...
    btnFunctionFGColor: Any = ...
    btnRequirementsBGColor: Any = ...
    btnRequirementsFGColor: Any = ...
    btnHardwareBGColor: Any = ...
    btnHardwareFGColor: Any = ...
    btnSoftwareBGColor: Any = ...
    btnSoftwareFGColor: Any = ...
    btnValidationBGColor: Any = ...
    btnValidationFGColor: Any = ...
    btnIncidentBGColor: Any = ...
    btnIncidentFGColor: Any = ...
    btnTestingBGColor: Any = ...
    btnTestingFGColor: Any = ...
    def __init__(self, __widget: Gtk.ImageMenuItem, configuration: RAMSTKUserConfiguration, logger: RAMSTKLogManager, parent: object) -> None: ...
