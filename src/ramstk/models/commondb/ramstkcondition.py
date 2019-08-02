# * coding: utf8 *
#
#       ramstk.dao.commondb.RAMSTKCondition.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright 2007  2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTKCondition Table Module."""

# Third Party Imports
from sqlalchemy import Column, Integer, String

# RAMSTK Package Imports
from ramstk import RAMSTK_BASE
from ramstk.Utilities import none_to_default


class RAMSTKCondition(RAMSTK_BASE):
    """Class to represent the table ramstk_condition in RAMSTK Common database."""

    __defaults__ = {
        'description': 'Condition Description',
        'condition_type': ''
    }
    __tablename__ = 'ramstk_condition'
    __table_args__ = {'extend_existing': True}

    condition_id = Column(
        'fld_condition_id',
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    description = Column('fld_description', String(512), default=__defaults__['description'])
    condition_type = Column('fld_condition_type', String(256), default=__defaults__['condition_type'])

    def get_attributes(self):
        """
        Retrieve current values of the RAMSTKCondition data model attributes.

        :return: {condition_id, description, condition_type} pairs
        :rtype: dict
        """
        _attributes = {
            'condition_id': self.condition_id,
            'description': self.description,
            'condition_type': self.condition_type,
        }

        return _attributes

    def set_attributes(self, attributes):
        """
        Set one or more RAMSTKCondition attributes.

        .. note:: you should pop the condition ID entries from the attributes
            dict before passing it to this method.

        :param dict attributes: dict of key:value pairs to assign to the
            instance attributes.
        :return: None
        :rtype: None
        :raise: AttributeError if passed an attribute key that doesn't exist as
            a table field.
        """
        for _key in attributes:
            getattr(self, _key)
            setattr(self, _key,
                    none_to_default(attributes[_key], self.__defaults__[_key]))
