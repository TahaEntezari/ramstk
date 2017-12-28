#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.capacitor.Capacitor.py is part of the RTK
#       Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Capacitor Package."""

import Configuration
import Utilities

lst_derate_criteria = [[0.6, 0.6, 0.0], [0.9, 0.9, 0.0]]
category = 4

def calculate_part(self):
    """
    Calculate the hazard rate for the Capacitor data model.

    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    # Quality correction factor.
    try:
        self.piQ = self._piQ[self.quality - 1]
    except AttributeError:
        # TODO: Handle attribute error.
        return True
    self.hazard_rate_model['piQ'] = self.piQ

    if self.hazard_rate_type == 1:
        # Base hazard rate.
        self.hazard_rate_model['lambdab'] = \
            self._lambdab_count[self.environment_active - 1]

    elif self.hazard_rate_type == 2:
        # Set the model's base hazard rate.
        self.base_hr = self.hazard_rate_model['lambdab']

        # Set the model's environmental correction factor.
        try:
            self.piE = self._piE[self.environment_active - 1]
        except AttributeError:
            # TODO: Handle attribute error.
            return True
        self.hazard_rate_model['piE'] = self.piE

    # Calculate component active hazard rate.
    _keys = self.hazard_rate_model.keys()
    _values = self.hazard_rate_model.values()

    for i in range(len(_keys)):
        vars()[_keys[i]] = _values[i]

    self.hazard_rate_active = eval(self.hazard_rate_model['equation'])
    self.hazard_rate_active = (self.hazard_rate_active +
                               self.add_adj_factor) * \
                              (self.duty_cycle / 100.0) * \
                              self.mult_adj_factor * self.quantity
    self.hazard_rate_active = self.hazard_rate_active / \
                              Configuration.FRMULT

    # Calculate overstresses.
    self._overstressed()

    # Calculate operating point ratios.
    self.current_ratio = self.operating_current / self.rated_current
    self.voltage_ratio = (self.operating_voltage + self.acvapplied) / \
                         self.rated_voltage
    self.power_ratio = self.operating_power / self.rated_power

    return False

def _overstressed(self):
    """
    Determine whether the Capacitor is overstressed.

    This determination is based on it's rated values and operating environment.

    :return: False if successful or True if an error is encountered.
    :rtype: bool
    """

    _reason_num = 1
    _reason = ''

    _harsh = True

    self.overstress = False

    # If the active environment is Benign Ground, Fixed Ground,
    # Sheltered Naval, or Space Flight it is NOT harsh.
    if self.environment_active in [1, 2, 4, 11]:
        _harsh = False

    if _harsh:
        if self.operating_voltage > 0.60 * self.rated_voltage:
            self.overstress = True
            _reason = _reason + str(_reason_num) + \
                            _(u". Operating voltage > 60% rated voltage.\n")
            _reason_num += 1
        if self.max_rated_temperature - self.temperature_active <= 10.0:
            self.overstress = True
            _reason = _reason + str(_reason_num) + \
                            _(u". Operating temperature within 10.0C of "
                            u"maximum rated temperature.\n")
            _reason_num += 1
    else:
        if self.operating_voltage > 0.90 * self.rated_voltage:
            self.overstress = True
            _reason = _reason + str(_reason_num) + \
                            _(u". Operating voltage > 90% rated voltage.\n")
            _reason_num += 1

    self.reason = _reason

    return False
