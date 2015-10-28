#!/usr/bin/env python
"""
###################################################
Hardware.Component.Relay Package Solid State Module
###################################################
"""

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'

# -*- coding: utf-8 -*-
#
#       rtk.hardware.component.relay.SolidState.py is part of the RTK Project
#
# All rights reserved.

import gettext
import locale

try:
    import configuration as _conf
    from hardware.component.relay.Relay import Model as Relay
except ImportError:                         # pragma: no cover
    import rtk.configuration as _conf
    from rtk.hardware.component.relay.Relay import Model as Relay

# Add localization support.
try:
    locale.setlocale(locale.LC_ALL, _conf.LOCALE)
except locale.Error:                        # pragma: no cover
    locale.setlocale(locale.LC_ALL, '')

_ = gettext.gettext


class SolidState(Relay):
    """
    The SolidState Relay data model contains the attributes and methods of a
    SolidState Relay component.  The attributes of a SolidState Relay are:

    :cvar subcategory: default value: 65

    Hazard Rate Models:
        # MIL-HDBK-217F, section 13.2.
    """

    # MIL-HDK-217F hazard rate calculation variables.
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    _lst_piQ = [1.0, 4.0]
    _lst_piE = [1.0, 3.0, 12.0, 6.0, 17.0, 12.0, 19.0, 21.0, 32.0, 23.0, 0.4,
                12.0, 33.0, 590.0]
    _lst_lambdab_count = [[0.40, 1.2, 4.8, 2.4, 6.8, 4.8, 7.6, 8.4, 13.0, 9.2,
                           0.16, 4.8, 13.0, 240.0],
                          [0.50, 1.5, 6.0, 3.0, 8.5, 5.0, 9.5, 11.0, 16.0,
                           12.0, 0.20, 5.0, 17.0, 300.0]]
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----

    subcategory = 65

    def __init__(self):
        """
        Initialize an SolidState Relay data model instance.
        """

        super(SolidState, self).__init__()

    def calculate(self):
        """
        Calculates the hazard rate for the Mechanical Relay data model.

        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """

        self.hazard_rate_model = {}

        if self.hazard_rate_type == 1:
            self.hazard_rate_model['equation'] = 'lambdab * piQ'

            # Set the base hazard rate for the model.
            self.base_hr = self._lst_lambdab_count[self.construction - 1][self.environment_active - 1]
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the quality pi factor for the model.
            self.piQ = self._lst_piQ[self.quality - 1]
            self.hazard_rate_model['piQ'] = self.piQ

        elif self.hazard_rate_type == 2:
            self.hazard_rate_model['equation'] = 'lambdab * piQ * piE'

            # Set the base hazard rate for the model.
            if self.construction == 1:
                self.base_hr = 0.4
            else:
                self.base_hr = 0.5
            self.hazard_rate_model['lambdab'] = self.base_hr

            # Set the quality factor for the model.
            self.piQ = self._lst_piQ[self.quality - 1]
            self.hazard_rate_model['piQ'] = self.piQ

            # Set the environment factor for the model.
            self.piE = self._lst_piE[self.environment_active - 1]
            self.hazard_rate_model['piE'] = self.piE

        return Relay.calculate(self)
