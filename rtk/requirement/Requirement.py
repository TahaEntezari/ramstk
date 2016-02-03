#!/usr/bin/env python
"""
###############################
Requirement Package Data Module
###############################
"""

# -*- coding: utf-8 -*-
#
#       Requirement.py is part of The RTK Project
#
# All rights reserved.

# Import modules for localization support.
import gettext
import locale

# Import other RTK modules.
try:
    import Configuration as _conf
    import Utilities as _util
except ImportError:                         # pragma: no cover
    import rtk.Configuration as _conf
    import rtk.Utilities as _util

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2014 Andrew "weibullguy" Rowland'

try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class Model(object):
    """
    The Requirement data model contains the attributes and methods of a
    requirement.  A :py:class:`rtk.revision.Revision` will consist of one or
    more Requirements.  The attributes of a Requirement are:

    :ivar list lst_clear: list of answers to the Requirement clarity questions.
    :ivar list lst_complete: list of answers to the Requirement completeness
                             questions.
    :ivar list lst_consistent: list of answers to the Requirement consistency
                               questions.
    :ivar list lst_verifiable: list of answers to the Requirement verifiability
                               questions.
    :ivar int revision_id: the ID of the Revision the Requirement belongs to.
    :ivar int requirement_id: the ID of the Requirement.
    :ivar str description: noun description of the Requirement.
    :ivar str code: short code for the Requirement.
    :ivar str requirement_type: the type of Requirement.
    :ivar int priority: the priority of the Requirement.
    :ivar str specification: governing specification, if any, for the
                             Requirement.
    :ivar str page_number: applicable page number in the governing
                           specification.
    :ivar str figure_number: applicable figure number in the governing
                             specification.
    :ivar int derived: indicates whether or not the Requirement is derived.
    :ivar str owner: the owner of the Requirement.
    :ivar int validated: indicates whether or not the Requirement has been
                         validated.
    :ivar int validated_date: the date the Requirement was validated.
    :ivar int parent_id: the ID of the parent Requirement if the Requirement is
                         a derived Requirement.
    """

    def __init__(self):
        """
        Method to initialize a Requirement data model instance.
        """

        # Initialize public list attributes.
        self.lst_clear = []
        self.lst_complete = []
        self.lst_consistent = []
        self.lst_verifiable = []

        # Initialize public scalar attributes.
        self.revision_id = None
        self.requirement_id = None
        self.description = ''
        self.code = ''
        self.requirement_type = ''
        self.priority = 1
        self.specification = ''
        self.page_number = ''
        self.figure_number = ''
        self.derived = 0
        self.owner = ''
        self.validated = 0
        self.validated_date = 719163
        self.parent_id = -1

    def set_attributes(self, values):
        """
        Sets the Requirement data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        try:
            self.revision_id = int(values[0])
            self.requirement_id = int(values[1])
            self.description = str(values[2])
            self.code = str(values[3])
            self.requirement_type = str(values[4])
            self.priority = int(values[5])
            self.specification = str(values[6])
            self.page_number = str(values[7])
            self.figure_number = str(values[8])
            self.derived = int(values[9])
            self.owner = str(values[10])
            self.validated = int(values[11])
            self.validated_date = int(values[12])
            self.parent_id = int(values[13])
            self.lst_clear = self.unpack_values(values[14])
            self.lst_complete = self.unpack_values(values[15])
            self.lst_consistent = self.unpack_values(values[16])
            self.lst_verifiable = self.unpack_values(values[17])
        except IndexError as _err:
            _code = _util.error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except TypeError as _err:
            _code = _util.error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the Requirement data model attributes.

        :return: (self.revsion_id, self.requirement_id, self.description,
                  self.code, self.requirement_type, self.priority,
                  self.specification, self.page_number, self.figure_number,
                  self.derived, self.owner, self.validated,
                  self.validated_date, self.parent_id)
        :rtype: tuple
        """

        _values = (self.revision_id, self.requirement_id, self.description,
                   self.code, self.requirement_type, self.priority,
                   self.specification, self.page_number, self.figure_number,
                   self.derived, self.owner, self.validated,
                   self.validated_date, self.parent_id)

        return _values

    def pack_values(self, lstvalues):       # pylint: disable=R0201
        """
        Packs the clear, complete, consistent, and verifiable answers into a
        string for saving to the RTK Project database.

        :param list lstvalues: a list of 0's and 1's indicating the answer to
                               the set of clear, complete, consistent, or
                               verifiable questions.
        :return: _packed
        :rtype: str
        """

        _packed = ''
        for _value in lstvalues:
            _packed = _packed + str(_value)

        return _packed

    def unpack_values(self, strvalues):     # pylint: disable=R0201
        """
        Unpacks the clear, complete, consistent, and verifiable answers into a
        list of integers for displaying in the GUI.

        :param str strvalues: a string of 0's and 1's indicating the answer to
                              the set of clear, complete, consistent, or
                              verifiable questions.
        :return: _unpacked
        :rtype: list
        """

        _unpacked = []
        for __, _value in enumerate(strvalues):
            _unpacked.append(int(_value))

        return _unpacked


class Requirement(object):
    """
    The Requirement data controller provides an interface between the
    Requirement data model and an RTK view model.  A single Requirement
    controller can manage one or more Requirement data models.  The attributes
    of a Requirement data controller are:

    :ivar _dao: the :py:class:`rtk.dao.DAO.DAO` to use when communicating with
                the RTK Program database.
    :ivar _last_id: the last Requirement ID used.
    :ivar dicRequirements: Dictionary of the Requirement data models managed.
                           Key is the Requirement ID; value is a pointer to the
                           Requirement data model instance.
    """

    def __init__(self):
        """
        Initializes a Requirement data controller instance.
        """

        # Initialize private scalar attributes.
        self._dao = None
        self._last_id = None

        # Initialize public dictionary attributes.
        self.dicRequirements = {}

    def request_requirements(self, dao, revision_id):
        """
        Reads the RTK Project database and loads all the requirements
        associated with the selected Revision.  For each requirement returned:

        #. Retrieve the requirements from the RTK Project database.
        #. Create a Requirement data model instance.
        #. Set the attributes of the data model instance from the returned
           results.
        #. Add the instance to the dictionary of Requirements being managed
           by this controller.

        :param rtk.DAO dao: the Data Access object to use for communicating
                            with the RTK Project database.
        :param int revision_id: the Revision ID to select the requirements for.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        self._dao = dao

        self._last_id = self._dao.get_last_id('tbl_requirements')[0]

        # Select everything from the function table.
        _query = "SELECT * FROM tbl_requirements \
                  WHERE fld_revision_id={0:d} \
                  ORDER BY fld_parent_id".format(revision_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=False)

        try:
            _n_requirements = len(_results)
        except TypeError:
            _n_requirements = 0

        for i in range(_n_requirements):
            _requirement = Model()
            _requirement.set_attributes(_results[i])
            self.dicRequirements[_requirement.requirement_id] = _requirement

        return(_results, _error_code)

    def add_requirement(self, revision_id, parent_id=None):
        """
        Adds a new Requirement to the RTK Project for the selected Revision.

        :param int revision_id: the Revision ID to add the new Requirement(s).
        :keyword int parent_id: the Requirement ID of the parent requirement.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        # By default we add the new requirement as a top-level requirement.
        if parent_id is None:
            parent_id = -1

        _query = "INSERT INTO tbl_requirements \
                  (fld_revision_id, fld_parent_id) \
                  VALUES ({0:d}, {1:d})".format(revision_id, parent_id)
        (_results,
         _error_code,
         _requirement_id) = self._dao.execute(_query, commit=True)

        # If the new requirement was added successfully to the RTK Project
        # database:
        #   1. Retrieve the ID of the newly inserted requirement.
        #   2. Create a new Requirement model instance.
        #   3. Set the attributes of the new Requirement model instance.
        #   2. Add the new Requirement model to the controller dictionary.
        if _results:
            self._last_id = self._dao.get_last_id('tbl_requirements')[0]
            _requirement = Model()
            _requirement.set_attributes((revision_id, self._last_id, '', '',
                                         '', 1, '', '', '', 0, '', 0, 719163,
                                         parent_id))
            self.dicRequirements[_requirement.requirement_id] = _requirement

        return(_requirement, _error_code)

    def delete_requirement(self, requirement_id):
        """
        Deletes a Requirement from the RTK Project.

        :param int function_id: the Requirement ID to delete.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        # Delete all the child requirements, if any.
        _query = "DELETE FROM tbl_requirements \
                  WHERE fld_parent_id={0:d}".format(requirement_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        # Then delete the parent requirement.
        _query = "DELETE FROM tbl_requirements \
                  WHERE fld_requirement_id={0:d}".format(requirement_id)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)

        self.dicRequirements.pop(requirement_id)

        return(_results, _error_code)

    def copy_requirements(self, revision_id):
        """
        Method to copy a Requirement from the currently selected Revision to
        the new Revision.

        :param int revision_id: the ID of the newly created Revision.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        # Find the existing maximum Requirement ID already in the RTK Program
        # database and increment it by one.  If there are no existing
        # Requirements set the first Requirement ID to zero.
        _query = "SELECT MAX(fld_requirement_id) FROM tbl_requirements"
        (_requirement_id,
         _error_code, __) = self._dao.execute(_query, commit=False)

        if _requirement_id[0][0] is not None:
            _requirement_id = _requirement_id[0][0] + 1
        else:
            _requirement_id = 0

        # Copy the Requirement hierarchy for the new Revision.
        _dic_index_xref = {}
        _dic_index_xref[-1] = -1
        for _requirement in self.dicRequirements.values():
            _query = "INSERT INTO tbl_requirements \
                      (fld_revision_id, fld_requirement_id, \
                       fld_description, fld_code, fld_derived, \
                       fld_parent_id, fld_owner, fld_specification, \
                       fld_page_number, fld_figure_number) \
                      VALUES ({0:d}, {1:d}, '{2:s}', '{3:s}', {4:d}, \
                              {5:d}, '{6:s}', '{7:s}', '{8:s}', \
                              '{9:s}')".format(revision_id, _requirement_id,
                                               _requirement.description,
                                               _requirement.code,
                                               _requirement.derived,
                                               _requirement.parent_id,
                                               _requirement.owner,
                                               _requirement.specification,
                                               _requirement.page_number,
                                               _requirement.figure_number)
            (_results, _error_code, __) = self._dao.execute(_query,
                                                            commit=True)

            # Add the new Requirement to the requirements analysis table.
            _query = "INSERT INTO rtk_requirement_analysis \
                      (fld_requirement_id) \
                      VALUES ({0:d})".format(_requirement_id)
            (_results, _error_code, __) = self._dao.execute(_query,
                                                            commit=True)

            # Add an entry to the Requirement ID cross-reference dictionary for
            # for the newly added Requirement.
            _dic_index_xref[_requirement.requirement_id] = _requirement_id

            _requirement_id += 1

        # Update the parent IDs for the new Requirements using the index
        # cross-reference dictionary that was created when adding the new
        # Requirements.
        for _key in _dic_index_xref.keys():
            _query = "UPDATE tbl_requirements \
                      SET fld_parent_id={0:d} \
                      WHERE fld_parent_id={1:d} \
                      AND fld_revision_id={2:d}".format(_dic_index_xref[_key],
                                                        _key, revision_id)
            (_results, _error_code, __) = self._dao.execute(_query,
                                                            commit=True)

        return False

    def save_requirement(self, requirement_id):
        """
        Saves the Requirement attributes to the RTK Project database.

        :param int requirement_id: the ID of the requirement to save.
        :return: (_results, _error_code)
        :rtype: tuple
        """

        _requirement = self.dicRequirements[requirement_id]

        # Pack the answers to the analysis questions into a string for saving.
        _clear = _requirement.pack_values(_requirement.lst_clear)
        _complete = _requirement.pack_values(_requirement.lst_complete)
        _consistent = _requirement.pack_values(_requirement.lst_consistent)
        _verifiable = _requirement.pack_values(_requirement.lst_verifiable)

        _query = "UPDATE tbl_requirements \
                  SET fld_description='{1:s}', fld_code='{2:s}', \
                      fld_requirement_type='{3:s}', fld_priority={4:d}, \
                      fld_specification='{5:s}', fld_page_number='{6:s}', \
                      fld_figure_number='{7:s}', fld_derived={8:d}, \
                      fld_owner='{9:s}', fld_validated={10:d}, \
                      fld_validated_date={11:d}, fld_parent_id={12:d}, \
                      fld_clear='{13:s}', fld_complete='{14:s}', \
                      fld_consistent='{15:s}', fld_verifiable='{16:s}' \
                  WHERE fld_requirement_id={0:d}".format(
                      _requirement.requirement_id, _requirement.description,
                      _requirement.code, _requirement.requirement_type,
                      _requirement.priority, _requirement.specification,
                      _requirement.page_number, _requirement.figure_number,
                      _requirement.derived, _requirement.owner,
                      _requirement.validated, _requirement.validated_date,
                      _requirement.parent_id, _clear, _complete, _consistent,
                      _verifiable)
        (_results, _error_code, __) = self._dao.execute(_query, commit=True)
# TODO: Handle errors.
        return(_results, _error_code)

    def save_all_requirements(self):
        """
        Saves all Requirement data models managed by the controller.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        for _requirement in self.dicRequirements.values():
            (_results,
             _error_code) = self.save_requirement(_requirement.requirement_id)

        return False
