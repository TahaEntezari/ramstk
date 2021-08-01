# -*- coding: utf-8 -*-
#
#       ramstk.controllers.options.datamanager.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Options Package Data Model."""

# Standard Library Imports
from typing import Any, Dict, List

# Third Party Imports
from pubsub import pub

# RAMSTK Package Imports
from ramstk.controllers import RAMSTKDataManager
from ramstk.models.commondb import RAMSTKSiteInfo


class DataManager(RAMSTKDataManager):
    """Contain the attributes and methods of the Option data manager."""

    # Define private dict class attributes.

    # Define private list class attributes.

    # Define private scalar class attributes.
    _db_id_colname = "fld_site_id"
    _db_tablename = "ramstk_site_info"
    _tag = "option"

    # Define public dict class attributes.

    # Define public list class attributes.

    # Define public scalar class attributes.

    def __init__(self, **kwargs) -> None:
        """Initialize a Options data manager instance."""
        RAMSTKDataManager.__init__(self, **kwargs)

        # Initialize private dictionary attributes.
        self._pkey: Dict[str, List[str]] = {
            "option": ["site_id"],
        }

        # Initialize private list attributes.

        # Initialize private scalar attributes.
        self._site_id: int = 0

        # Initialize public dictionary attributes.

        # Initialize public list attributes.

        # Initialize public scalar attributes.

        # Subscribe to PyPubSub messages.
        pub.subscribe(super().do_get_attributes, "request_get_option_attributes")
        pub.subscribe(super().do_set_attributes, "request_set_option_attributes")
        pub.subscribe(super().do_update, "request_update_option")

    def do_select_all(self, attributes: Dict[str, Any]) -> None:
        """Retrieve all the Options data from the RAMSTK Program database.

        :param attributes: the RAMSTK option attributes for the
            selected Site.
        :return: None
        :rtype: None
        """
        self._site_id = attributes["site_id"]

        for _node in self.tree.children(self.tree.root):
            self.tree.remove_node(_node.identifier)

        # noinspection PyUnresolvedReferences
        for _option in self.dao.do_select_all(
            RAMSTKSiteInfo,
            key=["site_id"],
            value=[self._site_id],
            order=RAMSTKSiteInfo.site_id,
        ):

            self.tree.create_node(
                tag="option",
                identifier=_option.site_id,
                parent=self._root,
                data={"option": _option},
            )

        pub.sendMessage(
            "succeed_retrieve_options",
            tree=self.tree,
        )
