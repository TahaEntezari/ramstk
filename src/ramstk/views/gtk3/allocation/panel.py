# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.allocation.panel.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""GTK3 Allocation Panels."""

# Standard Library Imports
from typing import Any, Dict, List, Union

# Third Party Imports
import treelib
from pubsub import pub

# RAMSTK Package Imports
from ramstk.views.gtk3 import Gtk, _
from ramstk.views.gtk3.widgets import (
    RAMSTKComboBox,
    RAMSTKEntry,
    RAMSTKFixedPanel,
    RAMSTKTreePanel,
)


class AllocationGoalMethodPanel(RAMSTKFixedPanel):
    """Panel to display reliability Allocation goals and method."""

    # Define private dictionary class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _record_field = "hardware_id"
    _select_msg = "selected_allocation"
    _tag = "allocation"
    _title = _("Allocation Goals and Method")

    # Define public dictionary class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self):
        """Initialize an instance of the Allocation goals and method panel."""
        super().__init__()

        # Initialize widgets.
        self.cmbAllocationGoal: RAMSTKComboBox = RAMSTKComboBox()
        self.cmbAllocationMethod: RAMSTKComboBox = RAMSTKComboBox()
        self.txtHazardRateGoal: RAMSTKEntry = RAMSTKEntry()
        self.txtMTBFGoal: RAMSTKEntry = RAMSTKEntry()
        self.txtReliabilityGoal: RAMSTKEntry = RAMSTKEntry()

        # Initialize private dictionary instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.
        self._goal_id: int = 0
        self._on_edit_message = f"wvw_editing_{self._tag}"

        # Initialize public dictionary instance attributes.
        self.dic_attribute_widget_map = {
            "allocation_method_id": [
                10,
                self.cmbAllocationMethod,
                "changed",
                super().on_changed_combo,
                self._on_edit_message,
                0,
                {
                    "tooltip": _(
                        "Selects the method for allocating the reliability goal for "
                        "the selected hardware assembly."
                    ),
                },
                _("Select Allocation Method:"),
                "gint",
            ],
            "goal_measure_id": [
                5,
                self.cmbAllocationGoal,
                "changed",
                super().on_changed_combo,
                self._on_edit_message,
                0,
                {
                    "tooltip": _(
                        "Selects the goal measure for the selected hardware assembly."
                    ),
                },
                _("Select Goal Metric:"),
                "gint",
            ],
            "reliability_goal": [
                19,
                self.txtReliabilityGoal,
                "changed",
                super().on_changed_entry,
                self._on_edit_message,
                1.0,
                {
                    "tooltip": _(
                        "Displays the reliability goal for the selected hardware item."
                    ),
                    "width": 125,
                },
                _("R(t) Goal:"),
                "gfloat",
            ],
            "hazard_rate_goal": [
                7,
                self.txtHazardRateGoal,
                "changed",
                super().on_changed_entry,
                self._on_edit_message,
                0.0,
                {
                    "tooltip": _(
                        "Displays the hazard rate goal for the selected hardware item."
                    ),
                    "width": 125,
                },
                _("h(t) Goal:"),
                "gfloat",
            ],
            "mtbf_goal": [
                13,
                self.txtMTBFGoal,
                "changed",
                super().on_changed_entry,
                self._on_edit_message,
                0.0,
                {
                    "tooltip": _(
                        "Displays the MTBF goal for the selected hardware item."
                    ),
                    "width": 125,
                },
                _("MTBF Goal:"),
                "gfloat",
            ],
        }

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

        self.cmbAllocationMethod.connect("changed", self._on_method_changed)
        self.cmbAllocationGoal.connect("changed", self._on_goal_changed)

        # Subscribe to PyPubSub messages.

    def do_load_comboboxes(self) -> None:
        """Load the RAMSTKComboBox() widgets.

        :return: None
        :rtype: None
        """
        self.cmbAllocationGoal.do_load_combo(
            [[_("Reliability"), 0], [_("Hazard Rate"), 1], [_("MTBF"), 2]]
        )
        self.cmbAllocationMethod.do_load_combo(
            [
                [_("Equal Apportionment"), 0],
                [_("AGREE Apportionment"), 1],
                [_("ARINC Apportionment"), 2],
                [_("Feasibility of Objectives"), 3],
            ]
        )

    def _do_set_sensitive(self, attributes) -> None:
        """Set widget sensitivity as needed for the selected R(t) goal.

        :return: None
        :rtype: None
        """
        self.cmbAllocationGoal.set_sensitive(True)
        self.cmbAllocationGoal.do_update(
            attributes["goal_measure_id"], signal="changed"
        )
        self.cmbAllocationMethod.set_sensitive(True)
        self.cmbAllocationMethod.do_update(
            attributes["allocation_method_id"], signal="changed"
        )
        self.txtReliabilityGoal.set_sensitive(False)
        self.txtMTBFGoal.set_sensitive(False)
        self.txtHazardRateGoal.set_sensitive(False)

        if self._goal_id == 1:  # Expressed as reliability.
            self.txtReliabilityGoal.set_sensitive(True)
            self.txtReliabilityGoal.do_update(
                attributes["reliability_goal"],
                signal="changed",
            )
        elif self._goal_id == 2:  # Expressed as a hazard rate.
            self.txtHazardRateGoal.set_sensitive(True)
            self.txtHazardRateGoal.do_update(
                attributes["hazard_rate_goal"],
                signal="changed",
            )
        elif self._goal_id == 3:  # Expressed as an MTBF.
            self.txtMTBFGoal.set_sensitive(True)
            self.txtMTBFGoal.do_update(
                attributes["mtbf_goal"],
                signal="changed",
            )

    def _on_goal_changed(self, combo: RAMSTKComboBox) -> None:
        """Let others know when allocation goal combo changes.

        :param combo: the allocation goal type RAMSTKComboBox().
        :return: None
        :rtype: None
        """
        self._goal_id = combo.get_active()

    @staticmethod
    def _on_method_changed(combo: RAMSTKComboBox) -> None:
        """Let others know when allocation method combo changes.

        :param combo: the allocation calculation method RAMSTKComboBox().
        :return: None
        :rtype: None
        """
        pub.sendMessage(
            "succeed_change_allocation_method", method_id=combo.get_active()
        )


class AllocationTreePanel(RAMSTKTreePanel):
    """Panel to display reliability Allocation worksheet."""

    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _select_msg = "succeed_retrieve_allocations"
    _tag = "allocation"
    _title = _("Allocation Analysis")

    # Define public dictionary class attributes.

    # Define public dictionary list attributes.

    # Define public dictionary scalar attributes.

    def __init__(self):
        """Initialize an instance of the Allocation worksheet panel."""
        super().__init__()

        # Initialize private dictionary attributes.
        self._dic_hardware_attrs: Dict[int, List[Union[bool, float, int, str]]] = {}
        self._dic_reliability_attrs: Dict[int, List[Union[bool, float, int, str]]] = {}
        self._dic_row_loader = {
            "allocation": self.__do_load_allocation,
        }
        self._dic_visible_mask: Dict[int, Dict[str, str]] = {
            0: {
                "revision_id": False,
                "hardware_id": False,
                "name": True,
                "included": False,
                "n_sub_systems": False,
                "n_sub_elements": False,
                "mission_time": False,
                "duty_cycle": False,
                "int_factor": False,
                "soa_factor": False,
                "op_time_factor": False,
                "env_factor": False,
                "weight_factor": False,
                "percent_weight_factor": False,
                "hazard_rate_logistics": True,
                "hazard_rate_alloc": False,
                "mtbf_logistics": True,
                "mtbf_alloc": False,
                "reliability_logistics": True,
                "reliability_alloc": False,
                "availability_logistics": True,
                "availability_alloc": False,
            },
            1: {
                "revision_id": False,
                "hardware_id": False,
                "name": True,
                "included": True,
                "n_sub_systems": True,
                "n_sub_elements": False,
                "mission_time": True,
                "duty_cycle": False,
                "int_factor": False,
                "soa_factor": False,
                "op_time_factor": False,
                "env_factor": False,
                "weight_factor": False,
                "percent_weight_factor": False,
                "hazard_rate_logistics": True,
                "hazard_rate_alloc": True,
                "mtbf_logistics": True,
                "mtbf_alloc": True,
                "reliability_logistics": True,
                "reliability_alloc": True,
                "availability_logistics": True,
                "availability_alloc": True,
            },
            2: {
                "revision_id": False,
                "hardware_id": False,
                "name": True,
                "included": True,
                "n_sub_systems": True,
                "n_sub_elements": True,
                "mission_time": True,
                "duty_cycle": True,
                "int_factor": False,
                "soa_factor": False,
                "op_time_factor": False,
                "env_factor": False,
                "weight_factor": True,
                "percent_weight_factor": True,
                "hazard_rate_logistics": True,
                "hazard_rate_alloc": True,
                "mtbf_logistics": True,
                "mtbf_alloc": True,
                "reliability_logistics": True,
                "reliability_alloc": True,
                "availability_logistics": True,
                "availability_alloc": True,
            },
            3: {
                "revision_id": False,
                "hardware_id": False,
                "name": True,
                "included": True,
                "n_sub_systems": False,
                "n_sub_elements": False,
                "mission_time": False,
                "duty_cycle": False,
                "int_factor": False,
                "soa_factor": False,
                "op_time_factor": False,
                "env_factor": False,
                "weight_factor": True,
                "percent_weight_factor": False,
                "hazard_rate_logistics": True,
                "hazard_rate_alloc": True,
                "mtbf_logistics": True,
                "mtbf_alloc": True,
                "reliability_logistics": True,
                "reliability_alloc": True,
                "availability_logistics": True,
                "availability_alloc": True,
            },
            4: {
                "revision_id": False,
                "hardware_id": False,
                "name": True,
                "included": True,
                "n_sub_systems": False,
                "n_sub_elements": False,
                "mission_time": False,
                "duty_cycle": False,
                "int_factor": True,
                "soa_factor": True,
                "op_time_factor": True,
                "env_factor": True,
                "weight_factor": True,
                "percent_weight_factor": False,
                "hazard_rate_logistics": True,
                "hazard_rate_alloc": True,
                "mtbf_logistics": True,
                "mtbf_alloc": True,
                "reliability_logistics": True,
                "reliability_alloc": True,
                "availability_logistics": True,
                "availability_alloc": True,
            },
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._goal_id: int = 0
        self._method_id: int = 0
        self._on_edit_message: str = f"mvw_editing_{self._tag}"

        # Initialize public dictionary attributes.
        self.dic_attribute_widget_map = {
            "revision_id": [
                0,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Revision ID"),
                "gint",
            ],
            "hardware_id": [
                1,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Hardware ID"),
                "gint",
            ],
            "name": [
                2,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                "",
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Assembly"),
                "gchararray",
            ],
            "included": [
                3,
                Gtk.CellRendererToggle(),
                "toggled",
                super().on_cell_toggled,
                self._on_edit_message,
                1,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": False,
                },
                _("Included?"),
                "gint",
            ],
            "n_sub_systems": [
                4,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                1,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Number of Sub-Systems"),
                "gint",
            ],
            "n_sub_elements": [
                5,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                1,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Number of Sub-Elements"),
                "gint",
            ],
            "mission_time": [
                6,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                1,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Operating Time"),
                "gfloat",
            ],
            "duty_cycle": [
                7,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                1,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Duty Cycle"),
                "gfloat",
            ],
            "int_factor": [
                8,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                1,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Intricacy (1-10)"),
                "gint",
            ],
            "soa_factor": [
                9,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                1,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("State of the Art (1-10)"),
                "gint",
            ],
            "op_time_factor": [
                10,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                1,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Operating Time (1-10)"),
                "gint",
            ],
            "env_factor": [
                11,
                Gtk.CellRendererText(),
                "edited",
                super().on_cell_edit,
                self._on_edit_message,
                1,
                {
                    "bg_color": "#FFFFFF",
                    "editable": True,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Environment (1-10)"),
                "gint",
            ],
            "weight_factor": [
                12,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                1,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Weighting Factor"),
                "gfloat",
            ],
            "percent_weight_factor": [
                13,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                1,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Percent Weighting Factor"),
                "gfloat",
            ],
            "hazard_rate_logistics": [
                14,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Current Hazard Rate"),
                "gfloat",
            ],
            "hazard_rate_alloc": [
                15,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Allocated Failure Rate"),
                "gfloat",
            ],
            "mtbf_logistics": [
                16,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Current MTBF"),
                "gfloat",
            ],
            "mtbf_alloc": [
                17,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                0.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Allocation MTBF"),
                "gfloat",
            ],
            "reliability_logistics": [
                18,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                1.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Current Reliability"),
                "gfloat",
            ],
            "reliability_alloc": [
                19,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                1.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Allocated Reliability"),
                "gfloat",
            ],
            "availability_logistics": [
                20,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                1.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Current Availability"),
                "gfloat",
            ],
            "availability_alloc": [
                21,
                Gtk.CellRendererText(),
                "edited",
                None,
                self._on_edit_message,
                1.0,
                {
                    "bg_color": "#FFFFFF",
                    "editable": False,
                    "fg_color": "#000000",
                    "visible": True,
                },
                _("Allocation Availability"),
                "gfloat",
            ],
        }

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        super().do_set_properties()
        super().do_make_panel()
        super().do_set_callbacks()

        self.tvwTreeView.set_tooltip_text(
            _(
                "Displays the Allocation Analysis for the currently selected "
                "Hardware item."
            )
        )

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_load_panel, "succeed_calculate_allocation")
        pub.subscribe(self._do_set_hardware_attributes, "succeed_retrieve_hardwares")
        pub.subscribe(
            self._do_set_reliability_attributes, "succeed_retrieve_reliabilitys"
        )
        pub.subscribe(self._on_method_changed, "succeed_change_allocation_method")

    def _do_set_columns_visible(self) -> None:
        """Set editable columns based on the Allocation method selected.

        :return: None
        :rtype: None
        """
        self.tvwTreeView.visible = self._dic_visible_mask[self._method_id]
        self.tvwTreeView.do_set_visible_columns()

    def _do_set_hardware_attributes(self, tree: treelib.Tree) -> None:
        """Set the attributes when the hardware tree is retrieved.

        :param tree: the hardware treelib.Tree().
        :return: None
        :rtype: None
        """
        for _node in tree.all_nodes()[1:]:
            _hardware = _node.data["hardware"]
            self._dic_hardware_attrs[_hardware.hardware_id] = [
                _hardware.name,
            ]

    def _do_set_reliability_attributes(self, tree: treelib.Tree) -> None:
        """Set the attributes when the reliability tree is retrieved.

        :param tree: the reliability treelib.Tree().
        :return: None
        :rtype: None
        """
        for _node in tree.all_nodes()[1:]:
            _reliability = _node.data["reliability"]
            self._dic_reliability_attrs[_reliability.hardware_id] = [
                _reliability.hazard_rate_logistics,
                _reliability.mtbf_logistics,
                _reliability.reliability_logistics,
                _reliability.availability_logistics,
            ]

    def _on_method_changed(self, method_id: int) -> None:
        """Set method ID attributes when user changes the selection.

        :param method_id: the newly selected allocation method.
        :return: None
        :rtype: None
        """
        self._method_id = method_id
        self._do_set_columns_visible()

    def _on_row_change(self, selection: Gtk.TreeSelection) -> None:
        """Handle events for the Hardware package Module View RAMSTKTreeView().

        This method is called whenever a Hardware Module View RAMSTKTreeView()
        row is activated/changed.

        :param selection: the Hardware class Gtk.TreeSelection().
        :return: None
        """
        _attributes = super().on_row_change(selection)

        if _attributes:
            self._record_id = _attributes["hardware_id"]

            pub.sendMessage(
                "selected_allocation",
                attributes=_attributes,
            )
            pub.sendMessage(
                "request_get_allocation_attributes",
                node_id=self._record_id,
            )

    def __do_load_allocation(
        self, node: Any = "", row: Gtk.TreeIter = None
    ) -> Gtk.TreeIter:
        """Load the allocation RAMSTKTreeView().

        :param node: the treelib Node() with the mode data to load.
        :param row: the parent row of the mode to load into the hardware tree.
        :return: _new_row; the row that was just populated with hardware data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None

        _entity = node.data["allocation"]

        if not _entity.parent_id == 0:
            _model = self.tvwTreeView.get_model()

            try:
                _name = self._dic_hardware_attrs[_entity.hardware_id][0]
                _hr_logistics = self._dic_reliability_attrs[_entity.hardware_id][0]
                _mtbf_logistics = self._dic_reliability_attrs[_entity.hardware_id][1]
                _rel_logistics = self._dic_reliability_attrs[_entity.hardware_id][2]
                _avail_logistics = self._dic_reliability_attrs[_entity.hardware_id][3]
            except KeyError:
                _name = ""
                _hr_logistics = 0.0
                _mtbf_logistics = 0.0
                _rel_logistics = 1.0
                _avail_logistics = 1.0

            _attributes = [
                _entity.revision_id,
                _entity.hardware_id,
                _name,
                _entity.included,
                _entity.n_sub_systems,
                _entity.n_sub_elements,
                _entity.mission_time,
                _entity.duty_cycle,
                _entity.int_factor,
                _entity.soa_factor,
                _entity.op_time_factor,
                _entity.env_factor,
                _entity.weight_factor,
                _entity.percent_weight_factor,
                _hr_logistics,
                _entity.hazard_rate_alloc,
                _mtbf_logistics,
                _entity.mtbf_alloc,
                _rel_logistics,
                _entity.reliability_alloc,
                _avail_logistics,
                _entity.availability_alloc,
            ]

            try:
                _new_row = _model.append(row, _attributes)
            except (AttributeError, TypeError, ValueError):
                _new_row = None
                _message = _(
                    f"An error occurred when loading allocation record "
                    f"{str(node.identifier)} into the allocation list.  This might "
                    f"indicate it was missing it's data package, some of the data in "
                    f"the package was missing, or some of the data was the wrong "
                    f"type.  Row data was: {_attributes}"
                )
                pub.sendMessage(
                    "do_log_warning_msg",
                    logger_name="WARNING",
                    message=_message,
                )

        return _new_row
