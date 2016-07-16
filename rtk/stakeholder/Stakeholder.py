#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.stakeholder.Stakeholder.py is part of The RTK Project
#
# All rights reserved.

"""
###############################
Stakeholder Package Data Module
###############################
"""

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import Configuration
    import Utilities
except ImportError:                         # pragma: no cover
    import rtk.Configuration as Configuration
    import rtk.Utilities as Utilities


__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, Configuration.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Model(object):
    """
    The Stakeholder data model contains the attributes and methods of a
    stakeholder input.  A :py :class:`rtk.requirement.Requirement` will consist
    of one or more Stakeholder inputs.  The attributes of a Stakeholder are:

    :ivar list lst_user_floats: default value: [0.0, 0.0, 0.0, 0.0, 0.0]

    :ivar int revision_id: the ID of the :py:class:`rtk.revision.Revision` the
                           Stakeholder input is associated with.
    :ivar int input_id: the ID of the Stakeholder input.
    :ivar str stakeholder: the stakeholder providing the input.
    :ivar str description: the description of the Stakeholder input.
    :ivar str group: the affinity group the Stakeholder input belongs to.
    :ivar int priority: the priority of implementing the Stakeholder input.
    :ivar int customer_rank: the customer ranking of the Stakeholder input.
    :ivar int planned_rank: the planned custmer ranking of the Stakeholder
                            input.
    :ivar float improvement: the calculated improvement factor for the
                             Stakeholder input.
    :ivar float overall_weight: the weighting of the Stakeholder input relative
                                to all the other Stakeholder inputs.
    :ivar str requirement: the requirement that encompasses the Stakeholder
                           input.
    """

    def __init__(self):
        """
        Method to initialize a Stakeholder data model instance.
        """

        # Define private dict attributes.

        # Define private list attributes.

        # Define private scalar attributes.

        # Define public dict attributes.

        # Define public list attributes.
        self.lst_user_floats = [1.0, 1.0, 1.0, 1.0, 1.0]

        # Define public scalar attributes.

        self.revision_id = None
        self.input_id = None
        self.stakeholder = ''
        self.description = ''
        self.group = ''
        self.priority = 1
        self.customer_rank = 1
        self.planned_rank = 3
        self.improvement = 1.0
        self.overall_weight = 0.0
        self.requirement = ''

    def set_attributes(self, values):
        """
        Method to set the Stakeholder data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        try:
            self.revision_id = int(values[0])
            self.input_id = int(values[1])
            self.stakeholder = str(values[2])
            self.description = str(values[3])
            self.group = str(values[4])
            self.priority = int(values[5])
            self.customer_rank = int(values[6])
            self.planned_rank = int(values[7])
            self.improvement = float(values[8])
            self.overall_weight = float(values[9])
            self.requirement = str(values[10])
            self.lst_user_floats[0] = float(values[11])
            self.lst_user_floats[1] = float(values[12])
            self.lst_user_floats[2] = float(values[13])
            self.lst_user_floats[3] = float(values[14])
            self.lst_user_floats[4] = float(values[15])
        except IndexError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = Utilities.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Method to retrieve the current values of the Stakeholder data model
        attributes.


        :return: (revision_id, input_id, stakeholder, description, group,
                  priority, customer_rank, planned_rank, improvement,
                  overall_weight, requirement, lst_user_floats[0],
                  lst_user_floats[1], lst_user_floats[2], lst_user_floats[3],
                  lst_user_floats[4])
        :rtype: tuple
        """

        _values = (self.revision_id, self.input_id, self.stakeholder,
                   self.description, self.group, self.priority,
                   self.customer_rank, self.planned_rank, self.improvement,
                   self.overall_weight, self.requirement,
                   self.lst_user_floats[0], self.lst_user_floats[1],
                   self.lst_user_floats[2], self.lst_user_floats[3],
                   self.lst_user_floats[4])

        return _values

    def calculate_weight(self):
        """
        Method to calculate the improvement factor and overall weighting of a
        Stakeholder input.

        :return: False if successful or True if an error is encountered.
        :rtype: boolean
        """

        self.improvement = 1.0 + 0.2 * (self.planned_rank - self.customer_rank)
        self.overall_weight = float(self.priority) * self.improvement * \
                              self.lst_user_floats[0] * \
                              self.lst_user_floats[1] * \
                              self.lst_user_floats[2] * \
                              self.lst_user_floats[3] * self.lst_user_floats[4]

        return False


class Stakeholder(object):
    """
    The Stakeholder data controller provides an interface between the
    Stakeholder data model and an RTK view model.  A single Stakeholder
    controller can manage one or more Stakeholder data models.  The attributes
    of a Stakeholder data controller are:

    :ivar _dao: the :py:class:`rtk.dao.DAO.DAO` to use when communicating with
                the RTK Project database.
    :ivar int _last_id: the last Stakeholder ID used.
    :ivar dict dicStakeholders: Dictionary of the Stakeholder data models
                                managed.  Key is the Stakeholder ID; value is a
                                pointer to the Stakeholder data model instance.

    """

    def __init__(self):
        """
        Method to initialize a Stakeholder data controller instance.
        """

        # Define private dictionary attributes.

        # Define private list attributes.

        # Define private scalar attributes.
        self._last_id = None

        # Initialize public dictionary attributes.
        self.dicStakeholders = {}

        # Initialize public list attributes.

        # Initialize public scalar attributes.
        self.dao = None

    def request_inputs(self, revision_id):
        """
        Method to read the RTK Project database and load all the stakeholder
        inputs associated with the selected Revision.  For each stakeholder
        input returned:

        #. Retrieve the inputs from the RTK Project database.
        #. Create a Stakeholder data model instance.
        #. Set the attributes of the data model instance from the returned
           results.
        #. Add the instance to the dictionary of Stakeholders being managed
           by this controller.

        :param int revision_id: the Revision ID to select the stakeholders for.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        self._last_id = self.dao.get_last_id('tbl_stakeholder_input')[0]

        # Select everything from the function table.
        _query = "SELECT * FROM tbl_stakeholder_input \
                  WHERE fld_revision_id={0:d}".format(revision_id)
        (_results, _error_code, __) = self.dao.execute(_query, commit=False)

        try:
            _n_stakeholders = len(_results)
        except TypeError:
            _n_stakeholders = 0

        for i in range(_n_stakeholders):
            _stakeholder = Model()
            _stakeholder.set_attributes(_results[i])
            self.dicStakeholders[_stakeholder.input_id] = _stakeholder

        return(_results, _error_code)

    def add_input(self, revision_id):
        """
        Method to add a new Stakeholder input to the RTK Project for the
        selected Revision.

        :param int revision_id: the Revision ID to add the new Stakeholder(s).
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _query = "INSERT INTO tbl_stakeholder_input \
                  (fld_revision_id) \
                  VALUES ({0:d})".format(revision_id)
        (_results,
         _error_code,
         _stakeholder_id) = self.dao.execute(_query, commit=True)

        # If the new stakeholder was added successfully to the RTK Project
        # database:
        #   1. Retrieve the ID of the newly inserted stakeholder.
        #   2. Create a new Stakeholder model instance.
        #   3. Set the attributes of the new Stakeholder model instance.
        #   4. Add the new Stakeholder model to the controller dictionary.
        if _results:
            self._last_id = self.dao.get_last_id('tbl_stakeholder_input')[0]
            _stakeholder = Model()
            _stakeholder.set_attributes((revision_id, self._last_id, '', '',
                                         '', 1, 1, 3, 1.0, 0.0))
            self.dicStakeholders[_stakeholder.input_id] = _stakeholder

        return(_stakeholder, _error_code)

    def delete_input(self, input_id):
        """
        Method to delete a Stakeholder input from the RTK Project database.

        :param int input_id: the Stakeholder input ID to delete.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        # Then delete the parent stakeholder.
        _query = "DELETE FROM tbl_stakeholder_input \
                  WHERE fld_input_id={0:d}".format(input_id)
        (_results, _error_code, __) = self.dao.execute(_query, commit=True)

        self.dicStakeholders.pop(input_id)

        return(_results, _error_code)

    def save_input(self, input_id):
        """
        Method to save the Stakeholder attributes to the RTK Project database.


        :param int input_id: the ID of the stakeholder input to save.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _input = self.dicStakeholders[input_id]

        _query = "UPDATE tbl_stakeholder_input \
                  SET fld_stakeholder='{1:s}', fld_description='{2:s}', \
                      fld_group='{3:s}', fld_priority={4:d}, \
                      fld_customer_rank={5:d}, fld_planned_rank={6:d}, \
                      fld_improvement={7:f}, fld_overall_weight={8:f}, \
                      fld_requirement='{9:s}', fld_user_float_1={10:f}, \
                      fld_user_float_2={11:f}, fld_user_float_3={12:f}, \
                      fld_user_float_4={13:f}, fld_user_float_5={14:f} \
                  WHERE fld_input_id={0:d}".format(
                      _input.input_id, _input.stakeholder,
                      _input.description, _input.group, _input.priority,
                      _input.customer_rank, _input.planned_rank,
                      _input.improvement, _input.overall_weight,
                      _input.requirement, _input.lst_user_floats[0],
                      _input.lst_user_floats[1], _input.lst_user_floats[2],
                      _input.lst_user_floats[3], _input.lst_user_floats[4])
        (_results, _error_code, __) = self.dao.execute(_query, commit=True)

        return(_results, _error_code)

    def save_all_inputs(self):
        """
        Method to save all Stakeholder data models managed by the controller.


        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        for _input in self.dicStakeholders.values():
            (_results,
             _error_code) = self.save_input(_input.input_id)

        return False

    def calculate_stakeholder(self, input_id):
        """
        Method to request the model calculate the Stakeholder input.


        :param int input_id: the Stakholder ID to calculate.
        :return: (improvement, overall_weight)
        :rtype: tuple
        """

        _stakeholder = self.dicStakeholders[input_id]
        _stakeholder.calculate_weight()

        return(_stakeholder.improvement, _stakeholder.overall_weight)
