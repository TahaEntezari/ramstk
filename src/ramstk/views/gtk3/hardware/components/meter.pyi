from .panels import RAMSTKAssessmentInputPanel as RAMSTKAssessmentInputPanel, RAMSTKAssessmentResultPanel as RAMSTKAssessmentResultPanel
from ramstk.views.gtk3.widgets import RAMSTKComboBox as RAMSTKComboBox, RAMSTKEntry as RAMSTKEntry
from typing import Any

class AssessmentInputPanel(RAMSTKAssessmentInputPanel):
    cmbApplication: Any = ...
    cmbType: Any = ...
    def __init__(self) -> None: ...
    def do_load_comboboxes(self, subcategory_id: int) -> None: ...

class AssessmentResultPanel(RAMSTKAssessmentResultPanel):
    txtPiA: Any = ...
    txtPiF: Any = ...
    txtPiT: Any = ...
    def __init__(self) -> None: ...
