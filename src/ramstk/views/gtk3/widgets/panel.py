# pylint: disable=non-parent-init-called, too-many-public-methods, cyclic-import
# -*- coding: utf-8 -*-
#
#       ramstk.views.gtk3.widgets.panel.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""The RAMSTK GTK3 Panel Class."""

# Standard Library Imports
import inspect
from typing import Any, Callable, Dict, List, Union

# Third Party Imports
# pylint: disable=ungrouped-imports
# noinspection PyPackageValidations
import treelib
from pandas.plotting import register_matplotlib_converters
from pubsub import pub

# RAMSTK Package Imports
from ramstk.utilities import boolean_to_integer
from ramstk.views.gtk3 import Gtk, _

# RAMSTK Local Imports
from .button import RAMSTKCheckButton
from .combo import RAMSTKComboBox
from .entry import RAMSTKEntry, RAMSTKTextView
from .frame import RAMSTKFrame
from .label import RAMSTKLabel, do_make_label_group
from .plot import RAMSTKPlot
from .scrolledwindow import RAMSTKScrolledWindow
from .treeview import RAMSTKTreeView

register_matplotlib_converters()


class RAMSTKPanel(RAMSTKFrame):
    """The RAMSTKPanel class.

    The attributes of a RAMSTKPanel are:

    :cvar _record_field: the database table field that contains the record ID.
    :cvar _select_msg: the PyPubSub message the panel listens for to load values into
        it's attribute widgets.  Defaults to "selected_revision".
    :cvar _tag: the name of the tag in the table or view model tree.  This should be
        the same value as the _tag attribute for the table or view model the panel is
        used to display.
    :cvar _title: the title to display on the panel frame.

    :ivar _dic_row_loader: contains the methods used to load the row data
        into a RAMSTKTreeView() where the key is the name of the module and
        the value is the method.  This is necessary for those views that
        combine different tables such as the usage profile or FMEA.  Having
        different loader methods for each type of entity may be needed to
        load the data for each entity in the correct order.  Most work
        stream modules will simple use the do_load_row() method of this
        meta-class.  Example entries in this dict might be:

        'mission': self.__do_load_mission
        'function': super().do_load_row

    :ivar _parent_id: the ID of the parent entity for the selected work stream
        entity.  This is needed for hierarchical modules such as the
        function module.  For flat modules, this will always be zero.
    :ivar _record_id: the work stream module ID whose attributes
        this panel is displaying.

    :ivar dic_attribute_widget_map: a dict used to map model attributes to their
        respective display widgets.  The key is the name of the attribute in the record
        model and the value is a list containing the following information:

            * Position 0 is the (zero-based) index of the widget.
            * Position 1 is the widget used to display the attribute.  This can be a
                named instance of a widget (e.g., self.txtName) or a widget class from
                which an unnamed instance will be created
                (e.g., Gtk.CellRendererText()).
            * Position 2 is the signal emitted by the widget when it is updated/edited.
            * Position 3 is the callback method that emits the signal in position 2.
                Set this to None to make widget read-only.
            * Position 4 is the PyPubSub message published when the widget is updated.
            * Position 5 is the default value to display in the widget.
            * Position 6 is a dict containing the property values for the widget.
            * Position 7 is the text to use for the widget in position 1 label.  For
                RAMSTKTreeViews this will be the column heading.
            * Position 8 is the Gobject data type to display in the widget.

        For a fixed panel, dict entries should be in the order they should appear in
        the panel.
    :ivar fmt: the formatting string for displaying float values.
    """

    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _record_field: str = "revision_id"
    _select_msg: str = "selected_revision"
    _tag: str = ""
    _title: str = ""

    # Define public dict class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the RAMSTKPanel.

        :return: None
        :rtype: None
        """
        super().__init__()

        # Initialize private dict instance attributes.

        # Initialize private list instance attributes.
        self._lst_labels: List[str] = []
        self._lst_widgets: List[object] = []

        # Initialize private scalar instance attributes.
        self._parent_id: int = -1
        self._record_id: int = -1
        self._tree_loaded: bool = False

        # Initialize public dict instance attributes.
        self.dic_attribute_widget_map: Dict[str, List[Any]] = {}

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
        self.fmt: str = "{0:0.6}"
        self.tree: treelib.Tree = treelib.Tree()

        # Subscribe to PyPubSub messages.


class RAMSTKFixedPanel(RAMSTKPanel):
    """The RAMSTKFixedPanel class."""

    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.

    # Define public dict class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the RAMSTKFixedPanel.

        :return: None
        :rtype: None
        """
        super().__init__()

        # Initialize private dict instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.

        # Initialize public dict instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.
        self.on_edit_callback: str = f"wvw_editing_{self._tag}"

        # Subscribe to PyPubSub messages.
        pub.subscribe(
            self.do_clear_panel,
            "request_clear_views",
        )
        pub.subscribe(
            self.do_load_panel,
            self._select_msg,
        )
        pub.subscribe(
            self.on_edit,
            self.on_edit_callback,
        )

        # Generally used with panels that accept inputs and are, thus, editable.
        try:
            pub.subscribe(self._do_set_sensitive, f"succeed_get_{self._tag}_attributes")
        except AttributeError:
            pass

        # Generally used with panels that display results and are, thus, uneditable.
        try:
            pub.subscribe(self._do_load_entries, f"succeed_get_{self._tag}_attributes")
        except AttributeError:
            pass

    def do_clear_panel(self) -> None:
        """Clear the contents of the widgets on a fixed type panel.

        :return: None
        :rtype: None
        """
        for (
            __,  # pylint: disable=unused-variable
            _value,
        ) in self.dic_attribute_widget_map.items():
            _value[1].do_update(_value[4], signal=_value[2])

    def do_load_panel(
        self,
        attributes: Dict[str, Any],
    ) -> None:
        """Load data into the widgets on fixed type panel.

        :param attributes: the attributes dict for the selected item.
        :return: None
        """
        self._record_id = attributes[self._record_field]

        for _key, _value in self.dic_attribute_widget_map.items():
            _value[1].do_update(
                attributes.get(_key, _value[5]),
                signal=_value[2],
            )

        pub.sendMessage("request_set_cursor_active")

    def do_make_panel(self, **kwargs: Dict[str, Any]) -> None:
        """Create a panel with the labels and widgets on a Gtk.Fixed().

        :return: None
        :rtype: None
        """
        _justify = kwargs.get("justify", Gtk.Justification.RIGHT)

        # Extract the list of labels and associated widgets from the attribute-widget
        # map.
        _lst_labels = [x[1][7] for x in self.dic_attribute_widget_map.items()]
        _lst_widgets = [x[1][1] for x in self.dic_attribute_widget_map.items()]

        _fixed: Gtk.Fixed = Gtk.Fixed()

        _y_pos: int = 5
        # noinspection PyTypeChecker
        (_x_pos, _labels) = do_make_label_group(
            _lst_labels,
            bold=False,  # type: ignore
            justify=_justify,
            x_pos=5,  # type: ignore
            y_pos=5,  # type: ignore
        )
        for _idx, _label in enumerate(_labels):
            _fixed.put(_label, 5, _y_pos)

            _minimum: Gtk.Requisition = _lst_widgets[  # type: ignore
                _idx
            ].get_preferred_size()[0]
            if _minimum.height <= 0:
                _minimum.height = _lst_widgets[_idx].height  # type: ignore

            # RAMSTKTextViews are placed inside a scrollwindow so that's
            # what needs to be placed on the container.
            if isinstance(_lst_widgets[_idx], RAMSTKTextView):
                _fixed.put(
                    _lst_widgets[_idx].scrollwindow,  # type: ignore
                    _x_pos + 10,
                    _y_pos,
                )
                _y_pos += _minimum.height + 30
            elif isinstance(_lst_widgets[_idx], RAMSTKCheckButton):
                _fixed.put(_lst_widgets[_idx], _x_pos + 10, _y_pos)
                _y_pos += _minimum.height + 30
            else:
                _fixed.put(_lst_widgets[_idx], _x_pos + 10, _y_pos)
                _y_pos += _minimum.height + 5

        _scrollwindow: RAMSTKScrolledWindow = RAMSTKScrolledWindow(_fixed)

        self.add(_scrollwindow)

    def do_set_callbacks(self) -> None:
        """Set the callback methods for RAMSTKTreeView().

        :return: None
        """
        for (
            _key,
            _value,
        ) in self.dic_attribute_widget_map.items():
            _value[1].dic_handler_id[_value[2]] = _value[1].connect(
                _value[2],
                _value[3],
                _key,
                _value[4],
            )

    def do_set_properties(self, **kwargs: Any) -> None:
        """Set properties of the RAMSTKPanel() widgets.

        :return: None
        """
        super().do_set_properties(**{"bold": True, "title": self._title})

        for (
            __,  # pylint: disable=unused-variable
            _value,
        ) in self.dic_attribute_widget_map.items():
            _value[1].do_set_properties(**_value[6])

    def on_changed_combo(
        self, combo: RAMSTKComboBox, key: str, message: str
    ) -> Dict[Union[str, Any], Any]:
        """Retrieve changes made in RAMSTKComboBox() widgets.

        This method publishes the PyPubSub message that it is passed.  This
        is usually sufficient to ensure the attributes are updated by the
        datamanager.  This method also return a dict with {_key: _new_text}
        if this information is needed by the child class.

        :param combo: the RAMSTKComboBox() that called the method.
        :param key: the name in the class' Gtk.TreeModel() associated
            with the attribute from the calling Gtk.Widget().
        :param message: the PyPubSub message to publish.
        :return: {_key: _new_text}; the work stream module's attribute name
            and the new value from the RAMSTKComboBox().  The value {'': -1}
            will be returned when a KeyError or ValueError is raised by this
            method.
        """
        _key: str = ""
        _new_text: int = -1

        combo.handler_block(combo.dic_handler_id["changed"])

        try:
            _new_text = int(combo.get_active())

            # Only if something is selected should we send the message.
            # Otherwise attributes get updated to a value of -1 which isn't
            # correct.  And it sucks trying to figure out why, so leave the
            # conditional unless you have a more elegant (and there prolly
            # is) solution.
            if _new_text > -1:
                pub.sendMessage(
                    message,
                    node_id=self._record_id,
                    package={key: _new_text},
                )
        except (KeyError, ValueError):
            _method_name: str = inspect.currentframe().f_code.co_name  # type: ignore
            _error_msg = _(
                f"{_method_name}: An error occurred while editing {self._tag} data "
                f"for record ID {self._record_id} in the view.  Key {key} does not "
                f"exist in attribute dictionary."
            )
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )

        combo.handler_unblock(combo.dic_handler_id["changed"])

        return {_key: _new_text}

    def on_changed_entry(
        self, entry: RAMSTKEntry, key: str, message: str
    ) -> Dict[Union[str, Any], Any]:
        """Retrieve changes made in RAMSTKEntry() widgets.

        This method is called by:

            * RAMSTKEntry() 'changed' signal

        This method publishes the PyPubSub message that it is passed.  This
        is usually sufficient to ensure the attributes are updated by the
        datamanager.  This method also return a dict with {_key: _new_text}
        if this information is needed by the child class.

        :param entry: the RAMSTKEntry() that called the method.
        :param key: the name in the class' Gtk.TreeModel() associated
            with the data from the calling RAMSTKEntry() or RAMSTKTextView().
        :param message: the PyPubSub message to publish.
        :return: {_key: _new_text}; the child module attribute name and the
            new value from the RAMSTKEntry() or RAMSTKTextView(). The value
            {'': ''} will be returned when a KeyError or ValueError is raised
            by this method.
        :rtype: dict
        """
        try:
            _handler_id = entry.dic_handler_id["changed"]
        except KeyError:
            _handler_id = entry.dic_handler_id["value-changed"]

        entry.handler_block(_handler_id)

        _package: Dict[str, Any] = self.__do_read_text(
            entry, key, self.dic_attribute_widget_map[key][8]
        )

        entry.handler_unblock(_handler_id)

        pub.sendMessage(message, node_id=self._record_id, package=_package)

        return _package

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def on_changed_textview(
        self, buffer: Gtk.TextBuffer, key: str, message: str, textview: RAMSTKTextView
    ) -> Dict[Union[str, Any], Any]:
        """Retrieve changes made in RAMSTKTextView() widgets.

        This method is called by:

            * Gtk.TextBuffer() 'changed' signal

        :param buffer: the Gtk.TextBuffer() calling this method.  This
            parameter is unused in this method.
        :param key: the name in the class' Gtk.TreeModel() associated
            with the data from the calling RAMSTKTextView().
        :param message: the PyPubSub message to broadcast.
        :param textview: the RAMSTKTextView() calling this method.
        :return: {_key: _new_text}; the child module attribute name and the
            new value from the RAMSTKTextView(). The value {'': ''} will be
            returned when a KeyError or ValueError is raised by this method.
        """
        textview.handler_block(textview.dic_handler_id["changed"])

        _package: Dict[str, Any] = self.__do_read_text(
            textview, key, self.dic_attribute_widget_map[key][8]
        )

        textview.handler_unblock(textview.dic_handler_id["changed"])

        pub.sendMessage(message, node_id=[self._record_id, -1], package=_package)

        return _package

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def on_edit(self, node_id: List[int], package: Dict[str, Any]) -> None:
        """Update the panel's Gtk.Widgets() when attributes are changed.

        This method is used to update a RAMSTKPanel() containing a
        Gtk.Fixed() populated with widgets [generally the work view]
        whenever a module view RAMSTKTreeView() is edited.  It is used to keep
        the data displayed in-sync.

        A dict 'package' is sent when a module view RAMSTKTreeView() is
        edited/changed.

            `package` key: `package` value

        corresponds to:

            database field name: database field new value

        The key in the 'package' is used to find the value in
        _dic_attribute_updater corresponding to the data being changed.
        Position 0 of the _dic_attribute_updater value list is the method
        used to update the widget and position 1 is the name of the signal
        to block during the update.

        :param node_id: the list of IDs of the work stream module item
            being edited.  This unused parameter is part of the PyPubSub
            message data package that this method responds to so it must
            remain in the argument list.
        :param package: a dict containing the attribute name as key and
            the new attribute value as the value.
        :return: None
        """
        _method_name: str = inspect.currentframe().f_code.co_name  # type: ignore
        [[_key, _value]] = package.items()

        try:
            _signal = self.dic_attribute_widget_map[_key][2]
            _function = self.dic_attribute_widget_map[_key][3]
            _function(_value, _signal)  # type: ignore
        except KeyError:
            _error_msg = _(
                "{2}: An error occurred while updating {1} data for record "
                "ID {0} in the view.  No key {3} in dic_attribute_widget_map."
            ).format(self._record_id, self._tag, _method_name, _key)
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )
        except TypeError:
            _error_msg = _(
                "{2}: An error occurred while updating {1} data for record "
                "ID {0} in the view.  Data for key {3} is the wrong "
                "type."
            ).format(self._record_id, self._tag, _method_name, _key)
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )

    def on_toggled(
        self, checkbutton: RAMSTKCheckButton, key: str, message: str
    ) -> Dict[Union[str, Any], Any]:
        """Retrieve changes made in RAMSTKCheckButton() widgets.

        :param checkbutton: the RAMSTKCheckButton() that was toggled.
        :param key: the name in the class' Gtk.TreeModel() associated
            with the data from the calling RAMSTKCheckButton().
        :param message: the PyPubSub message to broadcast.
        :return: {_key: _new_text}; the child module attribute name and the
            new value from the RAMSTKEntry() or RAMSTKTextView(). The value
            {'': -1} will be returned when a KeyError is raised by this method.
        """
        _new_text: int = -1

        try:
            _new_text = int(checkbutton.get_active())
            checkbutton.do_update(_new_text, signal="toggled")

            pub.sendMessage(
                message,
                node_id=[self._record_id, -1, ""],
                package={key: _new_text},
            )
        except KeyError:
            _method_name: str = inspect.currentframe().f_code.co_name  # type: ignore
            _error_msg = _(
                f"{_method_name}: An error occurred while updating {self._tag} data "
                f"for record ID {self._record_id} in the view.  Key {key} does not "
                f"exist in attribute dictionary."
            )
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )

        return {key: _new_text}

    def __do_read_text(
        self, entry: RAMSTKEntry, key: str, datatype: str
    ) -> Dict[str, Any]:
        """Read the text in a RAMSTKEntry() or Gtk.TextBuffer().

        :param entry: the RAMSTKEntry() or Gtk.TextBuffer() to read.
        :param key: the key for the entry to be read.
        :return: {_key, _new_text}; a dict containing the attribute key and
            the new value (text) for that key.
        """
        _new_text: Any = ""

        try:
            if str(datatype) == "gfloat":
                _new_text = float(entry.do_get_text())
            elif str(datatype) == "gint":
                _new_text = int(entry.do_get_text())
            elif str(datatype) == "gchararray":
                _new_text = str(entry.do_get_text())
        except (KeyError, ValueError):
            _method_name: str = inspect.currentframe().f_code.co_name  # type: ignore
            _error_msg = _(
                f"{_method_name}: An error occurred while reading {self._tag} data for "
                f"record ID {self._record_id} in the view.  Key {key} does not exist "
                f"in attribute dictionary."
            )
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )

        return {key: _new_text}


class RAMSTKPlotPanel(RAMSTKPanel):
    """The RAMSTKPlotPanel class.

    The attributes of a RAMSTKPlotPanel are:

    :ivar pltPlot: a RAMSTPlot() for the panels that embed a plot.
    """

    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.

    # Define public dict class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the RAMSTKPlotPanel.

        :return: None
        :rtype: None
        """
        super().__init__()

        # Initialize widgets.
        self.pltPlot: RAMSTKPlot = RAMSTKPlot()

        # Initialize private dict instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.

        # Initialize public dict instance attributes.

        # Initialize public list instance attributes.
        self.lst_axis_labels: List[str] = [_("abscissa"), _("ordinate")]
        self.lst_legend: List[str] = []

        # Initialize public scalar instance attributes.
        self.plot_title: str = ""

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_clear_panel, "request_clear_views")

    def do_clear_panel(self) -> None:
        """Clear the contents of the RAMSTKPlot on a plot type panel.

        :return: None
        :rtype: None
        """
        self.pltPlot.axis.cla()
        self.pltPlot.figure.clf()
        self.pltPlot.plot.draw()

    def do_load_panel(self) -> None:
        """Load data into the RAMSTKPlot on a plot type panel.

        :return: None
        :rtype: None
        """
        self.pltPlot.do_make_title(self.plot_title)
        self.pltPlot.do_make_labels(
            self.lst_axis_labels[1], x_pos=-0.5, y_pos=0, set_x=False
        )

        self.pltPlot.do_make_legend(self.lst_legend)
        self.pltPlot.figure.canvas.draw()

    def do_make_panel(self) -> None:
        """Create a panel with a RAMSTKPlot().

        :return: None
        :rtype: None
        """
        _scrollwindow: Gtk.ScrolledWindow = Gtk.ScrolledWindow()
        _scrollwindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        _scrollwindow.add(self.pltPlot.canvas)

        self.add(_scrollwindow)

    def do_set_callbacks(self) -> None:
        """Set the callback methods for RAMSTKTreeView().

        :return: None
        """

    def do_set_properties(self, **kwargs: Any) -> None:
        """Set properties of the RAMSTKPanel() widgets.

        :return: None
        """
        super().do_set_properties(**{"bold": True, "title": self._title})


class RAMSTKTreePanel(RAMSTKPanel):
    """The RAMSTKTreePanel class.

    The attributes of a RAMSTKTreePanel are:

    :ivar tvwTreeView: a RAMSTKTreeView() for the panels that embed a
        treeview.
    """

    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.

    # Define public dict class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self) -> None:
        """Initialize an instance of the RAMSTKTreePanel.

        :return: None
        :rtype: None
        """
        super().__init__()

        # Initialize widgets.
        self.tvwTreeView: RAMSTKTreeView = RAMSTKTreeView()

        # Initialize private dict instance attributes.
        self._dic_row_loader: Dict[str, Callable] = {}

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.

        # Initialize public dict instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(self.do_clear_panel, "request_clear_views")
        # pub.subscribe(self.do_load_panel, "succeed_insert_{}".format(self._tag))
        pub.subscribe(self.do_refresh_tree, f"lvw_editing_{self._tag}")
        pub.subscribe(self.do_refresh_tree, f"mvw_editing_{self._tag}")
        pub.subscribe(self.do_refresh_tree, f"wvw_editing_{self._tag}")
        pub.subscribe(self.on_delete_treerow, f"succeed_delete_{self._tag}")
        if self._select_msg is not None:
            pub.subscribe(self.do_load_panel, self._select_msg)

    def do_clear_panel(self) -> None:
        """Clear the contents of the RAMSTKTreeView on a tree type panel.

        :return: None
        :rtype: None
        """
        _model = self.tvwTreeView.get_model()
        try:
            _model.clear()
        except AttributeError:
            pass

    def do_load_panel(self, tree: treelib.Tree) -> None:
        """Load data into the RAMSTKTreeView on a tree type panel.

        :param tree: the treelib Tree containing the module to load.
        :return: None
        """
        _model = self.tvwTreeView.get_model()
        _model.clear()

        try:
            _row = None
            for _node in tree.all_nodes()[1:]:
                _row = self._dic_row_loader[_node.tag](_node, _row)
            self.tvwTreeView.expand_all()
            _row = _model.get_iter_first()
            if _row is not None:
                self.tvwTreeView.selection.select_iter(_row)
                self.show_all()
        except TypeError:
            _method_name: str = inspect.currentframe().f_code.co_name  # type: ignore
            _error_msg = _(
                "{2}: An error occurred while loading {1} data for Record "
                "ID {0} into the view.  One or more values from the "
                "database was the wrong type for the column it was trying to "
                "load."
            ).format(self._record_id, self._tag, _method_name)
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )
        except ValueError:
            _method_name = inspect.currentframe().f_code.co_name  # type: ignore
            _error_msg = _(
                "{2}: An error occurred while loading {1:s} data for Record "
                "ID {0:d} into the view.  One or more values from the "
                "database was missing."
            ).format(self._record_id, self._tag, _method_name)
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )

    def do_load_treerow(self, node: treelib.Node, row: Gtk.TreeIter) -> Gtk.TreeIter:
        """Load a row into the RAMSTKTreeView().

        :param node: the treelib Node() with the data to load.
        :param row: the parent row of the row to load.
        :return: _new_row; the row that was just populated with data.
        :rtype: :class:`Gtk.TreeIter`
        """
        _new_row = None
        _data: List[Any] = []

        try:
            # pylint: disable=unused-variable
            [[__, _entity]] = node.data.items()
            _attributes = _entity.get_attributes()
            _model = self.tvwTreeView.get_model()
            for _key, _pos in self.tvwTreeView.position.items():
                _data.insert(_pos, _attributes[_key])

            _new_row = _model.append(row, _data)
        except (AttributeError, TypeError, ValueError) as _error:
            _method_name: str = inspect.currentframe().f_code.co_name  # type: ignore
            _error_msg = (
                f"{_method_name}: An error occurred when loading "
                f"{self._tag} {node.identifier}.  This might indicate it was missing "
                f"it's data package, some of the data in the package was missing, or "
                f"some of the data was the wrong type.  Row data was: {_data}.  Error "
                f"was: {_error}."
            )
            pub.sendMessage(
                "do_log_warning_msg",
                logger_name="WARNING",
                message=_error_msg,
            )
            _new_row = None

        return _new_row

    def do_make_panel(self) -> None:
        """Create a panel with a RAMSTKTreeView().

        :return: None
        """
        self._lst_widgets.append(self.tvwTreeView)

        self.tvwTreeView.widgets = {
            _key: _value[1] for _key, _value in self.dic_attribute_widget_map.items()
        }
        self.tvwTreeView.editable = {
            _key: _value[6]["editable"]
            for _key, _value in self.dic_attribute_widget_map.items()
        }
        self.tvwTreeView.visible = {
            _key: _value[6]["visible"]
            for _key, _value in self.dic_attribute_widget_map.items()
        }
        self.tvwTreeView.datatypes = {
            _key: _value[8] for _key, _value in self.dic_attribute_widget_map.items()
        }

        _scrollwindow: Gtk.ScrolledWindow = Gtk.ScrolledWindow()
        _scrollwindow.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        _scrollwindow.add(self.tvwTreeView)

        self.add(_scrollwindow)

    def do_make_treeview(self, **kwargs: Dict[str, Any]) -> None:
        """Make the RAMSTKTreeView() instance for this panel.

        :return: None
        :rtype: None
        """
        _bg_color: str = kwargs.get("bg_color", "#FFFFFF")  # type: ignore
        _fg_color: str = kwargs.get("fg_color", "#000000")  # type: ignore
        _fmt_file: str = kwargs.get("fmt_file", "")  # type: ignore

        self.tvwTreeView.do_parse_format(_fmt_file)
        self.tvwTreeView.do_make_model()

        for _key, _value in self.dic_attribute_widget_map.items():
            self.tvwTreeView.widgets[_key] = _value[1]
            try:
                self.tvwTreeView.headings[_key] = _value[7]
            except IndexError:
                pass

        self.tvwTreeView.do_make_columns(
            colors={"bg_color": _bg_color, "fg_color": _fg_color}
        )

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def do_refresh_tree(self, node_id: List, package: Dict[str, Any]) -> None:
        """Update the module view RAMSTKTreeView() with attribute changes.

        This method is used to update a RAMSTKPanel() containing a
        RAMSTKTreeView() [generally the module view] whenever a work view
        widget is edited.  It is used to keep the data displayed in-sync.

        A dict 'package' is sent when a workview widget is edited/changed.

            `package` key: `package` value

        corresponds to:

            database field name: database field new value

        The key in the 'package' is used to find the value in
        _dic_attribute_updater corresponding to the data being changed.
        Position 2 of the _dic_attribute_updater value list is the nominal
        position in the RAMSTKTreeView() containing the same attribute data
        as the one being changed.

        :param node_id: unused in this method.
        :param package: the key:value for the data being updated.
        :return: None
        """
        [[_key, _value]] = package.items()

        try:
            _position = self.tvwTreeView.position[_key]

            _model, _row = self.tvwTreeView.get_selection().get_selected()
            _model.set(_row, _position, _value)
        except KeyError:
            _method_name: str = inspect.currentframe().f_code.co_name  # type: ignore
            _error_msg = _(
                "{2}: An error occurred while refreshing {1} data for Record "
                "ID {0} in the view.  Key {3} does not exist in "
                "attribute dictionary."
            ).format(self._record_id, self._tag, _method_name, _key)
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )
        except TypeError:
            _method_name: str = inspect.currentframe().f_code.co_name  # type: ignore
            _error_msg = _(
                "{2}: An error occurred while refreshing {1} data for Record "
                "ID {0} in the view.  Data {4} for {3} is the wrong "
                "type."
            ).format(self._record_id, self._tag, _method_name, _key, _value)
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )

    def do_set_callbacks(self) -> None:
        """Set the callback methods for RAMSTKTreeView().

        :return: None
        """
        self.tvwTreeView.dic_handler_id["changed"] = self.tvwTreeView.selection.connect(
            "changed", self._on_row_change
        )

        for _key, _value in self.dic_attribute_widget_map.items():
            try:
                if _value[3] is not None:
                    _value[1].connect(_value[2], _value[3], _key, _value[4])
            except KeyError:
                print(self._tag, type(_value))

    def do_set_cell_callbacks(self, message: str, columns: List[str]) -> None:
        """Set the callback methods for RAMSTKTreeView() cells.

        :param message: the PyPubSub message to broadcast on a
            successful edit.
        :param columns: the list of column numbers whose cells should
            have a callback function assigned.
        :return: None
        """
        for _key in columns:
            _cell = self.tvwTreeView.get_column(
                self.tvwTreeView.position[_key]
            ).get_cells()
            try:
                _cell[0].connect(
                    "edited",
                    self.on_cell_edit,
                    self.tvwTreeView.position[_key],
                    message,
                )
            except TypeError:
                _cell[0].connect(
                    "toggled",
                    self.on_cell_toggled,
                    self.tvwTreeView.position[_key],
                    message,
                )

    def do_set_headings(self) -> None:
        """Set the treeview headings depending on the selected row.

        It's used when the tree displays an aggregation of models such as
        the FMEA or PoF.  This method applies the appropriate headings when
        a row is selected.

        :return: None
        :rtype: None
        """
        _columns = self.tvwTreeView.get_columns()
        i = 0
        for _key in self.tvwTreeView.headings:
            _label = RAMSTKLabel(
                "<span weight='bold'>" + self.tvwTreeView.headings[_key] + "</span>"
            )
            _label.do_set_properties(
                height=-1, justify=Gtk.Justification.CENTER, wrap=True
            )
            _label.show_all()
            _columns[i].set_widget(_label)
            _columns[i].set_visible(self.tvwTreeView.visible[_key])

            i += 1

    def do_set_properties(self, **kwargs: Any) -> None:
        """Set properties of the RAMSTKPanel() widgets.

        :return: None
        """
        super().do_set_properties(**{"bold": True, "title": self._title})

        self.tvwTreeView.set_enable_tree_lines(True)
        self.tvwTreeView.set_grid_lines(Gtk.TreeViewGridLines.BOTH)
        self.tvwTreeView.set_level_indentation(2)
        self.tvwTreeView.set_rubber_banding(True)

    def on_cell_edit(
        self,
        cell: Gtk.CellRenderer,
        path: str,
        new_text: str,
        position: int,
        message: str,
    ) -> None:
        """Handle edits of the RAMSTKTreeview() in a treeview panel.

        :param cell: the Gtk.CellRenderer() that was edited.
        :param path: the RAMSTKTreeView() path of the Gtk.CellRenderer()
            that was edited.
        :param new_text: the new text in the edited Gtk.CellRenderer().
        :param position: the column position of the edited
            Gtk.CellRenderer().
        :param message: the PyPubSub message to publish.
        :return: None
        """
        try:
            _keys = list(self.tvwTreeView.position.keys())
            _vals = list(self.tvwTreeView.position.values())
            _col = _keys[_vals.index(position)]
            _key = self.tvwTreeView.position[_col]
            _position = self.tvwTreeView.position[_col]

            _new_text = self.tvwTreeView.do_edit_cell(cell, path, new_text, _position)
            pub.sendMessage(
                message,
                node_id=[self._record_id, ""],
                package={_key: _new_text},
            )
        except KeyError:
            _method_name: str = inspect.currentframe().f_code.co_name  # type: ignore
            _error_msg = _(
                "{2}: An error occurred while editing {1} data for record "
                "ID {0} in the view.  One or more keys could not be found in "
                "the attribute dictionary."
            ).format(self._record_id, self._tag, _method_name)
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )

    # pylint: disable=unused-argument
    def on_cell_toggled(
        self, cell: Gtk.CellRenderer, path: str, position: int, message: str
    ) -> None:
        """Handle edits of the FMEA Work View RAMSTKTreeview() toggle cells.

        :param cell: the Gtk.CellRenderer() that was toggled.
        :param path: the RAMSTKTreeView() path of the Gtk.CellRenderer()
            that was toggled.
        :param position: the column position of the toggled
            Gtk.CellRenderer().
        :param message: the PyPubSub message to publish.
        :return: None
        :rtype: None
        """
        _new_text = boolean_to_integer(cell.get_active())

        try:
            _keys = list(self.tvwTreeView.position.keys())
            _vals = list(self.tvwTreeView.position.values())
            _col = _keys[_vals.index(position)]
            _key = self.tvwTreeView.position[_col]

            if not self.tvwTreeView.do_edit_cell(cell, path, _new_text, position):
                pub.sendMessage(
                    message, node_id=[self._record_id, ""], package={_key: _new_text}
                )
        except KeyError:
            _method_name: str = inspect.currentframe().f_code.co_name  # type: ignore
            _error_msg = _(
                "{2}: An error occurred while editing {1} data for record "
                "ID {0} in the view.  One or more keys could not be found in "
                "the attribute dictionary."
            ).format(self._record_id, self._tag, _method_name)
            pub.sendMessage(
                "do_log_debug",
                logger_name="DEBUG",
                message=_error_msg,
            )

    # pylint: disable=unused-argument
    # noinspection PyUnusedLocal
    def on_delete_treerow(self, tree: treelib.Tree) -> None:
        """Update the RAMSTKTreeView after deleting a line item.

        :param tree: the treelib Tree() containing the workflow module data.
        :return: None
        """
        _model, _row = self.tvwTreeView.selection.get_selected()
        _model.remove(_row)

        _row = _model.get_iter_first()
        if _row is not None:
            self.tvwTreeView.selection.select_iter(_row)
            self.show_all()

        pub.sendMessage("request_set_cursor_active")

    def on_insert(self, data: Any) -> None:
        """Add row to module view for newly added work stream element.

        :param data: the data package for the work stream element to add.
        :return: None
        """
        _model, _row = self.tvwTreeView.selection.get_selected()

        # When inserting a child record, the selected row becomes the parent
        # row.
        if self._record_id == self._parent_id:
            _prow = _row
        # When inserting a sibling record, use the parent of the selected
        # row.
        else:
            _prow = _model.iter_parent(_row)

        self.tvwTreeView.do_insert_row(data, _prow)

        pub.sendMessage("request_set_cursor_active")

    def on_row_change(self, selection: Gtk.TreeSelection) -> Dict[str, Any]:
        """Get the attributes for the newly selected row.

        :param selection: the Gtk.TreeSelection() for the new row.
        :return: _attributes; the dict of attributes and value for the item
            in the selected row.  The key is the attribute name, the value is
            the attribute value.  Pulling them from the RAMSTKTreeView()
            ensures uncommitted changes are always selected.
        """
        selection.handler_block(self.tvwTreeView.dic_handler_id["changed"])

        _attributes: Dict[str, Any] = {}

        _model, _row = selection.get_selected()
        if _row is not None:
            for (
                _key,
                __,  # pylint: disable=unused-variable
            ) in self.dic_attribute_widget_map.items():
                _attributes[_key] = _model.get_value(
                    _row,
                    self.tvwTreeView.position[_key],
                )

        selection.handler_unblock(self.tvwTreeView.dic_handler_id["changed"])

        return _attributes
