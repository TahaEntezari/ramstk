#!/usr/bin/env python -O
"""
This is the test class for testing Stakeholder module algorithms and models.
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2014 Andrew "Weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       TestStakeholder.py is part of The RTK Project
#
# All rights reserved.

import unittest
from nose.plugins.attrib import attr

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(dirname(__file__))) + "/rtk")

import dao.DAO as _dao
from stakeholder.Stakeholder import Model, Stakeholder


class TestStakeholderModel(unittest.TestCase):
    """
    Class for testing the Stakeholder data model class.
    """

    def setUp(self):
        """
        Setup the test fixture for the Stakeholder class.
        """

        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

        self.DUT = Model()

    @attr(all=True, unit=True)
    def test_stakeholder_create(self):
        """
        (TestStakeholder) __init__ should return a Stakeholder model
        """

        self.assertTrue(isinstance(self.DUT, Model))

        self.assertEqual(self.DUT.lst_user_floats, [1.0, 1.0, 1.0, 1.0, 1.0])
        self.assertEqual(self.DUT.revision_id, None)
        self.assertEqual(self.DUT.input_id, None)
        self.assertEqual(self.DUT.stakeholder, '')
        self.assertEqual(self.DUT.description, '')
        self.assertEqual(self.DUT.group, '')
        self.assertEqual(self.DUT.priority, 1)
        self.assertEqual(self.DUT.customer_rank, 1)
        self.assertEqual(self.DUT.planned_rank, 3)
        self.assertEqual(self.DUT.improvement, 1.0)
        self.assertEqual(self.DUT.overall_weight, 0.0)
        self.assertEqual(self.DUT.requirement, '')

    @attr(all=True, unit=True)
    def test_stakeholder_set_attributes(self):
        """
        (TestStakeholder) set_attributes should return a 0 error code on success
        """

        _values = (0, 0, 'Stakeholder', 'Description', 'Affinity Group', 2,
                   4, 2, 1.6, 1.2, 'Requirement', 1.0, 2.0, 3.0, 4.0, 5.0)
        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 0)

    @attr(all=True, unit=True)
    def test_stakeholder_set_attributes_wrong_type(self):
        """
        (TestStakeholder) set_attributes should return a 10 error code when passed a wrong data type
        """

        _values = (0, 0, 'Stakeholder', 'Description', 'Affinity Group', 2,
                   4, 2, 1.6, 1.2, 'Requirement', 1.0, None, 3.0, 4.0, 5.0)
        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 10)

    @attr(all=True, unit=True)
    def test_stakeholder_set_attributes_missing_index(self):
        """
        (TestStakeholder) set_attributes should return a 40 error code when too few items are passed
        """

        _values = (0, 0, 'Stakeholder', 'Affinity Group', 2, 4, 2, 1.6, 1.2,
                   1.0, 2.0, 3.0, 4.0, 5.0)
        (_error_code,
         _error_msg) = self.DUT.set_attributes(_values)
        self.assertEqual(_error_code, 40)

    @attr(all=True, unit=True)
    def test_stakeholder_get_attributes(self):
        """
        (TestStakeholder) get_attributes should return a tuple of attribute values
        """

        self.assertEqual(self.DUT.get_attributes(),
                         (None, None, '', '', '', 1, 1, 3, 1.0, 0.0, '',
                          1.0, 1.0, 1.0, 1.0, 1.0))

    @attr(all=True, unit=True)
    def test_sanity(self):
        """
        (TestStakeholder) get_attributes(set_attributes(values)) == values
        """

        _values = (0, 0, 'Stakeholder', 'Description', 'Affinity Group', 2,
                   4, 2, 1.6, 1.2, 'Requirement', 1.0, 2.0, 3.0, 4.0, 5.0)

        self.DUT.set_attributes(_values)
        _result = self.DUT.get_attributes()
        self.assertEqual(_result, _values)

    @attr(all=True, unit=True)
    def test_calculate_weight(self):
        """
        (TestStakeholder) calculate_weight returns False on success and calculate values are correct
        """

        _values = (0, 0, 'Stakeholder', 'Description', 'Affinity Group', 2,
                   4, 2, 1.6, 1.2, 1, 1.0, 2.0, 3.0, 4.0, 5.0)
        self.DUT.set_attributes(_values)
        self.assertFalse(self.DUT.calculate_weight())
        self.assertEqual(self.DUT.improvement, 0.6)
        self.assertEqual(self.DUT.overall_weight, 144.0)


class TestStakeholderController(unittest.TestCase):
    """
    Class for testing the Stakeholder data controller class.
    """

    def setUp(self):
        """
        Sets up the test fixture for the Stakeholder class.
        """

        _database = '/home/andrew/projects/RTKTestDB.rtk'
        self._dao = _dao(_database)

        self.DUT = Stakeholder()

    @attr(all=True, unit=True)
    def test_controller_create(self):
        """
        (TestStakeholder) __init__ should create a Stakeholder data controller
        """

        self.assertTrue(isinstance(self.DUT, Stakeholder))
        self.assertEqual(self.DUT._dao, None)
        self.assertEqual(self.DUT._last_id, None)
        self.assertEqual(self.DUT.dicStakeholders, {})

    @attr(all=True, integration=True)
    def test_request_inputs(self):
        """
        (TestStakeholder) request_inputs should return 0 on success
        """

        self.assertEqual(self.DUT.request_inputs(self._dao, 0)[1], 0)
# TODO: Test that method fails when no Stakeholder inputs exist in database.
    @attr(all=True, integration=True)
    def test_add_input(self):
        """
        (TestStakeholder) add_input returns 0 on success and new Stakeholder data model added to dictionary
        """

        self.assertEqual(self.DUT.request_inputs(self._dao, 0)[1], 0)
        (_results,
         _error_code) = self.DUT.add_input(0)

        self.assertTrue(isinstance(self.DUT.dicStakeholders[self.DUT._last_id],
                                   Model))
        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_delete_input(self):
        """
        (TestStakeholder) delete_input returns 0 on success
        """

        self.assertEqual(self.DUT.request_inputs(self._dao, 0)[1], 0)
        (_results,
         _error_code) = self.DUT.delete_input(self.DUT._last_id)

        self.assertTrue(_results)
        self.assertEqual(_error_code, 0)

    @attr(all=True, integration=True)
    def test_save_input(self):
        """
        (TestStakeholder) save_input returns (True, 0) on success
        """

        self.DUT.request_inputs(self._dao, 0)
        self.assertEqual(self.DUT.save_input(1), (True, 0))

    @attr(all=True, integration=True)
    def test_save_all_inputs(self):
        """
        (TestStakeholder) save_all_inputs returns False on success
        """

        self.DUT.request_inputs(self._dao, 0)
        self.assertFalse(self.DUT.save_all_inputs())

    @attr(all=True, integration=True)
    def test_calculate_stakeholder(self):
        """
        (TestStakeholder) calculate_stakeholder returns 0 on success
        """

        self.DUT.request_inputs(self._dao, 0)
        self.assertEqual(self.DUT.calculate_stakeholder(1), (1.0, 1.0))
