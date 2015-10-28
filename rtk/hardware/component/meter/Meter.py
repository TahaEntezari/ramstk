#!/usr/bin/env python
"""
#############################################
Hardware.Component.Meter Package Meter Module
#############################################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.meter.Meter.py is part of the RTK Project
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
    elif 'invalid literal for int() with base 10' in message[0]:   # Type error
        _error_code = 10
    elif 'index out of range' in message[0]:   # Index error
        _error_code = 40
    else:                                   # Unhandled error
        print message
        _error_code = 1000                  # pragma: no cover

    return _error_code


class Model(Component):
    """
    The Meter data model contains the attributes and methods of a Meter
    component.  The attributes of an Meter are:

    :cvar category: default value: 9

    :ivar application: default value: 0
    :ivar base_hr: default value: 0.0
    :ivar reason: default value: ""
    :ivar piE: default value: 0.0

    Hazard Rate Models:
        # MIL-HDBK-217F, sections 12.3 and 18.1.
    """

    category = 9

    def __init__(self):
        """
        Initialize an Meter data model instance.
        """

        super(Model, self).__init__()

        # Initialize public list attributes.
        self.lst_derate_criteria = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]

        # Initialize public scalar attributes.
        self.application = 0                # Application index.
        self.base_hr = 0.0                  # Base hazard rate.
        self.reason = ""                    # Overstress reason.
        self.piE = 0.0                      # Environment pi factor.

    def set_attributes(self, values):
        """
        Sets the Meter data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Component.set_attributes(self, values[:96])

        try:
            self.base_hr = float(values[96])
            self.piE = float(values[97])
            self.application = int(values[116])
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
        Retrieves the current values of the Meter data model
        attributes.

        :return: (base_hr, piE, application, reason)
        :rtype: tuple
        """

        _values = Component.get_attributes(self)

        _values = _values + (self.base_hr, self.piE, self.application,
                             self.reason)

        return _values

    def calculate(self):
        """
        Calculates the hazard rate for the Meter data model.

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

        # Calculate operating point ratios.
        self.current_ratio = self.operating_current / self.rated_current
        self.voltage_ratio = self.operating_voltage / self.rated_voltage
        self.power_ratio = self.operating_power / self.rated_power

        return False


class ElapsedTime(Model):
    """
    The Elapsed Time Meter data model contains the attributes and methods of an
    Elapsed Time Meter component.  The attributes of an Elapsed Time Meter are:

    :cvar subcategory: default value: 77

    :ivar application: default value: 0
    :ivar base_hr: default value: 0.0
    :ivar reason: default value: ""
    :ivar piE: default value: 0.0

    Hazard Rate Models:
        # MIL-HDBK-217F, sections 12.3.
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_lambdab = [20.0, 30.0, 80.0]
    _lst_piE = [1.0, 2.0, 12.0, 7.0, 18.0, 5.0, 8.0, 16.0, 25.0, 26.0, 0.5,
                14.0, 38.0, 0.0]
    _lst_lambdab_count = [[10.0, 20.0, 120.0, 70.0, 180.0, 50.0, 80.0, 160.0,
                           250.0, 260.0, 5.0, 140.0, 380.0, 0.0],
                          [15.0, 30.0, 180.0, 105.0, 270.0, 75.0, 120.0, 240.0,
                           375.0, 390.0, 7.5, 210.0, 570.0, 0.0],
                          [40.0, 80.0, 480.0, 280.0, 720.0, 200.0, 320.0,
                           640.0, 1000.0, 1040.0, 20.0, 560.0, 1520.0, 0.0]]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 1

    def __init__(self):
        """
        Initialize an Elapsed Time Meter data model instance.
        """

        super(ElapsedTime, self).__init__()

        # Initialize public scalar attributes.
        self.piT = 0.0                      # Temperature stress pi factor.

    def set_attributes(self, values):
        """
        Sets the Elapsed Time Meter data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Model.set_attributes(self, values)

        try:
            self.piT = float(values[98])
        except IndexError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the Elapsed Time Meter data model
        attributes.

        :return: (piT)
        :rtype: tuple
        """

        _values = Model.get_attributes(self)

        _values = _values + (self.piT,)

        return _values

    def calculate(self):
        """
        Calculates the hazard rate for the Elapsed Time Meter data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab'

            # Base hazard rate.
            try:
                self._lambdab_count = self._lst_lambdab_count[self.application - 1]
            except AttributeError:
                # TODO: Handle attribute error.
                return True

        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piT * piE'

            # Set the model's base hazard rate.
            self.base_hr = self._lst_lambdab[self.application - 1]
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the model's environmental correction factor.
            self.piE = self._lst_piE[self.environment_active - 1]
            self.hazard_rate_model['piE'] = self.piE

            # Set the model's temperature stress factor.
            _temp = self.temperature_active / self.max_rated_temperature
            if _temp >= 0.0 and _temp <= 0.5:
                self.piT = 0.5
            elif _temp > 0.5 and _temp <= 0.6:  # pragma: no cover
                self.piT = 0.6
            elif _temp > 0.6 and _temp <= 0.8:  # pragma: no cover
                self.piT = 0.8
            elif _temp > 0.8:                   # pragma: no cover
                self.piT = 1.0
            self.hazard_rate_model['piT'] = self.piT

        return Model.calculate(self)


class Panel(Model):
    """
    The Panel Meter data model contains the attributes and methods of an
    Panel Meter component.  The attributes of an Panel Meter are:

    :cvar subcategory: default value: 78

    :ivar quality: default value: 0
    :ivar q_override: default value: 0.0
    :ivar function: default value: 0
    :ivar piA: default value: 0.0
    :ivar piF: default value: 0.0
    :ivar piQ: default value: 0.0

    Hazard Rate Models:
        # MIL-HDBK-217F, sections 18.1.
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piE = [1.0, 4.0, 25.0, 12.0, 35.0, 28.0, 42.0, 58.0, 73.0, 60.0, 1.1,
                60.0, 0.0, 0.0]
    _lst_piQ = [1.0, 3.4]
    _lst_lambdab_count = [[0.09, 0.36, 2.3, 1.1, 3.2, 2.5, 3.8, 5.2, 6.6, 5.4,
                           0.099, 5.4, 0.0, 0.0],
                          [0.15, 0.81, 2.8, 1.8, 5.4, 4.3, 6.4, 8.9, 11.0, 9.2,
                           0.17, 9.2, 0.0, 0.0]]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 2

    def __init__(self):
        """
        Initialize a Panel Meter data model instance.
        """

        super(Panel, self).__init__()

        # Initialize public scalar attributes.
        self.quality = 0
        self.q_override = 0.0
        self.function = 0
        self.piA = 0.0
        self.piF = 0.0
        self.piQ = 0.0

    def set_attributes(self, values):
        """
        Sets the Panel Meter data model attributes.

        :param tuple values: tuple of values to assign to the instance
                             attributes.
        :return: (_code, _msg); the error code and error message.
        :rtype: tuple
        """

        _code = 0
        _msg = ''

        (_code, _msg) = Model.set_attributes(self, values)

        try:
            self.q_override = float(values[98])
            self.piA = float(values[99])
            self.piF = float(values[100])
            self.piQ = float(values[101])
            self.quality = int(values[117])
            self.function = int(values[118])
        except IndexError as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Insufficient input values."
        except(TypeError, ValueError) as _err:
            _code = _error_handler(_err.args)
            _msg = "ERROR: Converting one or more inputs to correct data type."

        return(_code, _msg)

    def get_attributes(self):
        """
        Retrieves the current values of the Panel Meter data model
        attributes.

        :return: (quality, function, q_override, piA, piF, piQ)
        :rtype: tuple
        """

        _values = Model.get_attributes(self)

        _values = _values + (self.quality, self.function, self.q_override,
                             self.piA, self.piF, self.piQ)

        return _values

    def calculate(self):
        """
        Calculates the hazard rate for the Panel Meter data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab'

            # Base hazard rate.
            try:
                self._lambdab_count = self._lst_lambdab_count[self.application - 1]
            except AttributeError:
                # TODO: Handle attribute error.
                return True

        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piA * piF * piQ * piE'

            # Set the model's base hazard rate.
            self.base_hr = 0.09
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the model's application factor.
            if self.application == 1:
                self.piA = 1.0
            else:
                self.piA = 1.7
            self.hazard_rate_model['piA'] = self.piA

            # Set the model's function factor.
            if self.function < 3:
                self.piF = 1.0
            else:
                self.piF = 2.8
            self.hazard_rate_model['piF'] = self.piF

            # Set the model's quality correction factor.
            self.piQ = self._lst_piQ[self.quality - 1]
            self.hazard_rate_model['piQ'] = self.piQ

            # Set the model's environmental correction factor.
            self.piE = self._lst_piE[self.environment_active - 1]
            self.hazard_rate_model['piE'] = self.piE

        return Model.calculate(self)
