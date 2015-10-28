#!/usr/bin/env python
"""
#######################################################
Hardware.Component.Connection Package Connection Module
#######################################################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.connection.Connection.py is part of the RTK
#       Project
#
# All rights reserved.

import gettext
import locale

try:
    import calculations as _calc
    import configuration as _conf
    from hardware.component.Component import Model as Component
except ImportError:                         # pragma: no cover
    import rtk.calculations as _calc
    import rtk.configuration as _conf
    from rtk.hardware.component.Component import Model as Component

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


def _error_handler(message):
    """
    Converts string errors to integer error codes.

    :param str message: the message to convert to an error code.
    :return: _err_code
    :rtype: int
    """

    if 'argument must be a string or a number' in message[0]:   # Type error
        _error_code = 10
    elif 'index out of range' in message[0]:   # Index error
        _error_code = 40
    else:                                   # Unhandled error
        _error_code = 1000                  # pragma: no cover

    return _error_code


class Model(Component):
    """
    The Connection data model contains the attributes and methods of a
    connection component.  The attributes of a Connection are:

    :cvar category: default value: 8

    :ivar base_hr: default value: 0.0
    :ivar reason: default value: ""
    :ivar piE: default value: 0.0

    Hazard Rate Models:
        # MIL-HDBK-217F, sections 15, 16, and 17.
    """

    category = 8

    def __init__(self):
        """
        Initialize a Connection data model instance.
        """

        super(Model, self).__init__()

        # Initialize public list attributes.
        self.lst_derate_criteria = [[0.7, 0.7, 0.0], [0.9, 0.9, 0.0]]

        # Initialize public scalar attributes.
        self.quality = 0                    # Quality level.
        self.q_override = 0.0
        self.base_hr = 0.0                  # Base hazard rate.
        self.reason = ""                    # Overstress reason.
        self.piQ = 1.0                      # Quality pi factor.
        self.piE = 0.0                      # Environment pi factor.

    def set_attributes(self, values):
        """
        Sets the Connection data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Component.set_attributes(self, values[:96])

        try:
            self.q_override = float(values[96])
            self.base_hr = float(values[97])
            self.piQ = float(values[98])
            self.piE = float(values[99])
            self.quality = int(values[116])
            # TODO: Add field to rtk_stress to hold overstress reason.
            self.reason = ''
        except IndexError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the Connection data model attributes.

        :return: (q_override, base_hr, piQ, piE, quality, reason)
        :rtype: tuple
        """

        _values = Component.get_attributes(self)

        _values = _values + (self.q_override, self.base_hr, self.piQ, self.piE,
                             self.quality, self.reason)

        return _values

    def calculate(self):
        """
        Calculates the hazard rate for the Connection data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        if self.hazard_rate_type == 1:
            # Base hazard rate.
            try:
                self.hazard_rate_model['lambdab'] = \
                    self._lambdab_count[self.environment_active - 1]
            except AttributeError:
                # TODO: Handle attribute error.
                return True

            # Quality correction factor.
            try:
                self.hazard_rate_model['piQ'] = self.piQ
            except AttributeError:
                # TODO: Handle attribute error.
                return True

        elif self.hazard_rate_type == 2:
            # Set the model's base hazard rate.
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the model's environmental correction factor.
            self.hazard_rate_model['piE'] = self.piE

        # Calculate component active hazard rate.
        self.hazard_rate_active = _calc.calculate_part(self.hazard_rate_model)
        self.hazard_rate_active = (self.hazard_rate_active + \
                                   self.add_adj_factor) * \
                                  (self.duty_cycle / 100.0) * \
                                  self.mult_adj_factor * self.quantity
        self.hazard_rate_active = self.hazard_rate_active / _conf.FRMULT

        # Calculate overstresses.
        self._overstressed()

        # Calculate operating point ratios.
        self.current_ratio = self.operating_current / self.rated_current
        self.voltage_ratio = self.operating_voltage / self.rated_voltage
        self.power_ratio = self.operating_power / self.rated_power

        return False

    def _overstressed(self):
        """
        Determines whether the Connection is overstressed based on it's rated
        values and operating environment.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        _reason_num = 1
        _harsh = True

        self.overstress = False

        # If the active environment is Benign Ground, Fixed Ground,
        # Sheltered Naval, or Space Flight it is NOT harsh.
        if self.environment_active in [1, 2, 4, 11]:
            _harsh = False

        if _harsh:
            if self.operating_voltage > 0.7 * self.rated_voltage:
                self.overstress = True
                self.reason = self.reason + str(_reason_num) + \
                    _(u". Operating voltage > 70% rated voltage.\n")
                _reason_num += 1
            if self.operating_current > 0.7 * self.rated_current:
                self.overstress = True
                self.reason = self.reason + str(_reason_num) + \
                    _(u". Operating current > 70% rated current.\n")
                _reason_num += 1
            if (self.temperature_rise + self.temperature_active -
                    self.max_rated_temperature) < 25:
                self.overstress = True
                self.reason = self.reason + str(_reason_num) + \
                    _(u". Operating temperature within 25.0C of maximum rated "
                      u"temperature.\n")
                _reason_num += 1
        else:
            if self.operating_voltage > 0.9 * self.rated_voltage:
                self.overstress = True
                self.reason = self.reason + str(_reason_num) + \
                    _(u". Operating voltage > 90% rated voltage.\n")
                _reason_num += 1
            if self.operating_current > 0.9 * self.rated_current:
                self.overstress = True
                self.reason = self.reason + str(_reason_num) + \
                    _(u". Operating current > 90% rated current.\n")
                _reason_num += 1

        return False
