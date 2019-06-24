# -*- coding: utf-8 -*-
#
#       ramstk.analyses.prediction.Connection.py is part of the RAMSTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Doyle Rowland doyle.rowland <AT> reliaqual <DOT> com
"""Connection Reliability Calculations Module."""

# Standard Library Imports
from math import exp

PART_COUNT_217F_LAMBDA_B = {
    1: {
        1: [
            0.011, 0.14, 0.11, 0.069, 0.20, 0.058, 0.098, 0.23, 0.34, 0.37,
            0.0054, 0.16, 0.42, 6.8,
        ],
        2: [
            0.012, 0.015, 0.13, 0.075, 0.21, 0.06, 0.1, 0.22, 0.32, 0.38,
            0.0061, 0.18, 0.54, 7.3,
        ],
    },
    2: [
        0.0054, 0.021, 0.055, 0.035, 0.10, 0.059, 0.11, 0.085, 0.16, 0.19,
        0.0027, 0.078, 0.21, 3.4,
    ],
    3: [
        0.0019, 0.0058, 0.027, 0.012, 0.035, 0.015, 0.023, 0.021, 0.025,
        0.048, 0.00097, 0.027, 0.070, 1.3,
    ],
    4: [
        0.053, 0.11, 0.37, 0.69, 0.27, 0.27, 0.43, 0.85, 1.5, 1.0, 0.027,
        0.53, 1.4, 27.0,
    ],
    5: {
        1: [
            0.0026, 0.0052, 0.018, 0.010, 0.029, 0.010, 0.016, 0.016,
            0.021, 0.042, 0.0013, 0.023, 0.062, 1.1,
        ],
        2: [
            0.00014, 0.00028, 0.00096, 0.00056, 0.0015, 0.00056, 0.00084,
            0.00084, 0.0011, 0.0022, 0.00007, 0.0013, 0.0034, 0.059,
        ],
        3: [
            0.00026, 0.00052, 0.0018, 0.0010, 0.0029, 0.0010, 0.0016,
            0.0016, 0.0021, 0.0042, 0.00013, 0.0023, 0.0062, 0.11,
        ],
        4: [
            0.000050, 0.000100, 0.000350, 0.000200, 0.000550, 0.000200,
            0.000300, 0.000300, 0.000400, 0.000800, 0.000025, 0.000450,
            0.001200, 0.021000,
        ],
        5: [
            0.0000035, 0.000007, 0.000025, 0.000014, 0.000039, 0.000014,
            0.000021, 0.000021, 0.000028, 0.000056, 0.0000018, 0.000031,
            0.000084, 0.0015,
        ],
        6: [
            0.00012, 0.00024, 0.00084, 0.00048, 0.0013, 0.00048, 0.00072,
            0.00072, 0.00096, 0.0019, 0.00005, 0.0011, 0.0029, 0.050,
        ],
        7: [
            0.000069, 0.000138, 0.000483, 0.000276, 0.000759, 0.000276,
            0.000414, 0.000414, 0.000552, 0.001104, 0.000035, 0.000621,
            0.001656, 0.02898,
        ],
    },
}
PART_STRESS_217F_LAMBDA_B = {
    3: 0.00042,
    4: [0.000041, 0.00026],
    5: [0.0026, 0.00014, 0.00026, 0.00005, 0.0000035, 0.00012, 0.000069],
}
PI_E = {
    1: {
        1: [
            1.0, 1.0, 8.0, 5.0, 13.0, 3.0, 5.0, 8.0, 12.0, 19.0, 0.5, 10.0,
            27.0, 490.0,
        ],
        2: [
            2.0, 5.0, 21.0, 10.0, 27.0, 12.0, 18.0, 17.0, 25.0, 37.0, 0.8,
            20.0, 54.0, 970.0,
        ],
    },
    2: {
        1: [
            1.0, 3.0, 8.0, 5.0, 13.0, 6.0, 11.0, 6.0, 11.0, 19.0, 0.5,
            10.0, 27.0, 490.0,
        ],
        2: [
            2.0, 7.0, 17.0, 10.0, 26.0, 14.0, 22.0, 14.0, 22.0, 37.0, 0.8,
            20.0, 54.0, 970.0,
        ],
    },
    3: [
        1.0, 3.0, 14.0, 6.0, 18.0, 8.0, 12.0, 11.0, 13.0, 25.0, 0.5, 14.0,
        36.0, 650.0,
    ],
    4: [
        1.0, 2.0, 7.0, 5.0, 13.0, 5.0, 8.0, 16.0, 28.0, 19.0, 0.5, 10.0,
        27.0, 500.0,
    ],
    5: [
        1.0, 2.0, 7.0, 4.0, 11.0, 4.0, 6.0, 6.0, 8.0, 16.0, 0.5, 9.0, 24.0,
        420.0,
    ],
}
PI_K = [1.0, 1.5, 2.0, 3.0, 4.0]
REF_TEMPS = {1: 473.0, 2: 423.0, 3: 373.0, 4: 358.0}


def _calculate_mil_hdbk_217f_part_count_lambda_b(attributes):
    r"""
    Calculate the parts count base hazard rate (lambda b) from MIL-HDBK-217F.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    count method.  The dictionary PART_COUNT_217F_LAMBDA_B contains the
    MIL-HDBK-217F parts count base hazard rates.  Keys are for
    PART_COUNT_217F_LAMBDA_B are:

        #. subcategory_id
        #. type id; if the connection subcategory is NOT type dependent, then
            the second key will be zero.

    Current subcategory IDs are:

    +----------------+-------------------------------+-----------------+
    | Subcategory \  |           Connection \        | MIL-HDBK-217F \ |
    |       ID       |              Style            |    Section      |
    +================+===============================+=================+
    |        1       | Circular, Rack and Panel, \   |       15.1      |
    |                | Coaxial, Triaxial             |                 |
    +----------------+-------------------------------+-----------------+
    |        2       | PCB/PWA Edge                  |       15.2      |
    +----------------+-------------------------------+-----------------+
    |        3       | IC Socket                     |       15.3      |
    +----------------+-------------------------------+-----------------+
    |        4       | Plated Through Hole (PTH)     |       16.1      |
    +----------------+-------------------------------+-----------------+
    |        5       | Non-PTH                       |       17.1      |
    +----------------+-------------------------------+-----------------+

    These keys return a list of base hazard rates.  The hazard rate to use is
    selected from the list depending on the active environment.

    :param dict attributes: the attributes for the connection being calculated.
    :return: attributes; the keyword argument (hardware attribute) dictionary
        with updated values and the error message, if any.
    :rtype: dict
    """
    try:
        if attributes['subcategory_id'] in [1, 5]:
            _lst_base_hr = PART_COUNT_217F_LAMBDA_B[
                attributes['subcategory_id']
            ][
                attributes['type_id']
            ]
        else:
            _lst_base_hr = PART_COUNT_217F_LAMBDA_B[
                attributes['subcategory_id']
            ]
    except KeyError:
        _lst_base_hr = [0.0]

    try:
        attributes['lambda_b'] = _lst_base_hr[
            attributes['environment_active_id'] - 1
        ]
    except IndexError:
        attributes['lambda_b'] = 0.0

    return attributes


def _calculate_mil_hdbk_217f_part_stress_lambda_b(attributes):
    """
    Calculate the part stress base hazard rate (lambda b) from MIL-HDBK-217F.

    This function calculates the MIL-HDBK-217F hazard rate using the parts
    stress method.

    :param dict attributes: the attributes for the connection being calculated.
    :return: attributes; the keyword argument (hardware attribute) dictionary
        with updated values and the error message, if any.
    :rtype: dict
    """
    # Reference temperature is used to calculate base hazard rate for
    # circular/rack and panel connectors.  To get the reference temperature
    # dictionary key, we quesry the key dictionary in which the first key is
    # the connector type ID, second key is the specification ID.  The insert
    # material ID is the index in the list returned.
    _dic_keys = {
        1: {
            1: [2, 2, 2, 2, 2, 2],
            2: [2, 2, 2, 2, 2, 2],
            3: [1, 1, 1, 2, 2, 2, 2, 2, 2],
            4: [1, 1, 1, 2, 2, 2, 2, 2, 2],
            5: [1, 1, 1, 2, 2, 2, 2, 2, 2],
        },
        2: {
            1: [2, 2, 2, 2, 2, 2, 4, 4, 4],
            2: [1, 1, 1, 2, 2, 2, 2, 2, 2, 4, 4, 4],
            3: [1, 1, 1, 2, 2, 2, 2, 2, 2],
            4: [1, 1, 1, 2, 2, 2, 2, 2, 2],
            5: [2, 2, 2, 2, 2, 2],
            6: [2, 2, 2, 2, 2, 2],
        },
        3: {
            1: [2, 2, 2, 2, 2, 2, 4, 4, 4],
            2: [2, 2, 2, 2, 2, 2, 4, 4, 4],
        },
        4: {
            1: [3, 3],
            2: [3, 3],
            3: [3, 3],
            4: [3, 3],
            5: [3, 3],
            6: [3, 3],
            7: [3, 3],
            8: [3, 3, 2, 2, 2, 2, 2, 2],
        },
        5: {
            1: [3, 3, 2, 2, 2, 2, 2, 2],
        },
    }
    # Factors are used to calculate base hazard rate for circular/rack and
    # panel connectors.  Key is from dictionary above (1 - 4) or contact
    # gauge (22 - 12).
    _dic_factors = {
        1: {
            1: [0.2, -1592.0, 5.36],
            2: [0.431, -2073.6, 4.66],
            3: [0.19, -1298.0, 4.25],
            4: [0.77, -1528.8, 4.72],
            12: 0.1,
            16: 0.274,
            20: 0.64,
            22: 0.989,
        },
        2: {
            20: 0.64,
            22: 0.989,
            26: 2.1,
        },
    }
    _contact_temp = (
        attributes['temperature_active']
        + attributes['temperature_rise'] + 273.0
    )
    if attributes['subcategory_id'] == 1:
        _key = _dic_keys[attributes['type_id']][
            attributes[
                'specification_id'
            ]
        ][attributes['insert_id'] - 1]
        _ref_temp = REF_TEMPS[_key]
        _f0 = _dic_factors[attributes['subcategory_id']][_key][0]
        _f1 = _dic_factors[attributes['subcategory_id']][_key][1]
        _f2 = _dic_factors[attributes['subcategory_id']][_key][2]
    elif attributes['subcategory_id'] == 2:
        _ref_temp = 423.0
        _f0 = 0.216
        _f1 = -2073.6
        _f2 = 4.66
    elif attributes['subcategory_id'] == 3:
        _contact_temp = 0.0
        _ref_temp = 1.0
        _f0 = 0.00042
        _f1 = 0.0
        _f2 = 1.0

    if attributes['subcategory_id'] in [4, 5]:
        attributes['lambda_b'] = PART_STRESS_217F_LAMBDA_B[
            attributes['subcategory_id']
        ][
            attributes['type_id'] - 1
        ]
    elif attributes['subcategory_id'] == 3:
        attributes['lambda_b'] = 0.00042
    else:
        attributes['lambda_b'] = _f0 * exp(
            (_f1 / _contact_temp)
            + (_contact_temp / _ref_temp)**_f2,
        )

    return attributes


def _calculate_insert_temperature(attributes):
    """
    Calculate the insert temperature.

    :param dict attributes: the attributes for the connection being calculated.
    """
    # First key is subcategory ID, second key is contact gauge.
    _dic_factors = {
        1: {
            12: 0.1,
            16: 0.274,
            20: 0.64,
            22: 0.989,
        },
        2: {
            20: 0.64,
            22: 0.989,
            26: 2.1,
        },
    }

    try:
        _fo = _dic_factors[attributes['subcategory_id']][
            attributes[
                'contact_gauge'
            ]
        ]
    except KeyError:
        _fo = 1.0
    attributes['temperature_rise'] = (
        _fo * attributes['current_operating']**1.85
    )

    return attributes


def _do_check_variables(attributes):
    """
    Check calculation variable to ensure they are all greater than zero.

    All variables are checked regardless of whether they'll be used in the
    calculation for the connection type which is why a WARKING message is
    issued rather than an ERROR message.

    :param dict attributes: the attributes for the connection being calculated.
    :return: _msg; a message indicating all the variables that are less than or
        equal to zero in value.
    :rtype: str
    """
    _msg = ''

    if attributes['lambda_b'] <= 0.0:
        _msg = _msg + 'RAMSTK WARNING: Base hazard rate is 0.0 when ' \
            'calculating connection, hardware ID: ' \
            '{0:d}.\n'.format(attributes['hardware_id'])

    if attributes['piQ'] <= 0.0:
        _msg = _msg + 'RAMSTK WARNING: piQ is 0.0 when calculating ' \
            'connection, hardware ID: {0:d}.\n'.format(
                attributes['hardware_id'],
            )

    if attributes['hazard_rate_method_id'] == 2:
        if attributes['piC'] <= 0.0:
            _msg = _msg + 'RAMSTK WARNING: piC is 0.0 when calculating ' \
                'connection, hardware ID: {0:d}.\n'.format(
                    attributes['hardware_id'],
                )
        if attributes['piE'] <= 0.0:
            _msg = _msg + 'RAMSTK WARNING: piE is 0.0 when calculating ' \
                'connection, hardware ID: {0:d}.\n'.format(
                    attributes['hardware_id'],
                )
        if attributes['piK'] <= 0.0:
            _msg = _msg + 'RAMSTK WARNING: piK is 0.0 when calculating ' \
                'connection, hardware ID: {0:d}.\n'.format(
                    attributes['hardware_id'],
                )
        if attributes['piP'] <= 0.0:
            _msg = _msg + 'RAMSTK WARNING: piP is 0.0 when calculating ' \
                'connection, hardware ID: {0:d}.\n'.format(
                    attributes['hardware_id'],
                )

    return _msg


def _get_environment_factor(attributes):
    """
    Retrieve the environment factor (piE).

    :param dict attributes: the attributes dictionary of the connection being
        calculated.
    :return: attributes; the attributes dictionary updated with pi_E.
    :rtype: dict
    """
    if attributes['subcategory_id'] in [1, 2]:
        attributes['piE'] = PI_E[attributes['subcategory_id']][
            attributes[
                'quality_id'
            ]
        ][attributes['environment_active_id'] - 1]
    else:
        attributes['piE'] = PI_E[attributes['subcategory_id']][
            attributes['environment_active_id'] - 1
        ]

    return attributes


def _get_mate_unmate_factor(attributes):
    """
    Retrieve the mating/unmating factor (piK).

    :param dict attributes: the attributes dictionary of the connection being
        calculated.
    :return: attributes; the attributes dictionary updated with pi_E.
    :rtype: dict
    """
    if attributes['n_cycles'] <= 0.05:
        attributes['piK'] = PI_K[0]
    elif 0.05 < attributes['n_cycles'] <= 0.5:
        attributes['piK'] = PI_K[1]
    elif 0.5 < attributes['n_cycles'] <= 5.0:
        attributes['piK'] = PI_K[2]
    elif 5.0 < attributes['n_cycles'] <= 50.0:
        attributes['piK'] = PI_K[3]
    else:
        attributes['piK'] = PI_K[4]

    return attributes


def calculate_217f_part_count(**attributes):
    """
    Calculate the part count hazard rate for a connection.

    :param dict attributes: the attributes for the connection being calculated.
    :return: (attributes, _msg); the keyword argument (hardware attribute)
             dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    attributes = _calculate_mil_hdbk_217f_part_count_lambda_b(attributes)
    _msg = _do_check_variables(attributes)

    attributes['hazard_rate_active'] = (
        attributes['lambda_b'] * attributes['piQ']
    )

    return attributes, _msg


def calculate_217f_part_stress(**attributes):
    """
    Calculate the part stress hazard rate for a connection.

    This function calculates the MIL-HDBK-217F hazard rate using the part
    stress method.

    :param dict attributes: the attributes for the connection being calculated.
    :return: (attributes, _msg); the keyword argument (hardware attribute)
        dictionary with updated values and the error message, if any.
    :rtype: (dict, str)
    """
    attributes = _calculate_insert_temperature(attributes)
    attributes = _calculate_mil_hdbk_217f_part_stress_lambda_b(attributes)
    attributes = _get_environment_factor(attributes)
    attributes = _get_mate_unmate_factor(attributes)

    # Determine active pins factor.
    if attributes['subcategory_id'] in [1, 2, 3]:
        attributes['piP'] = exp(
            ((attributes['n_active_pins'] - 1) / 10.0)**0.51064,
        )

    # Determine the complexity factor (piC) for PTH connections.
    if attributes['subcategory_id'] == 4:
        if attributes['n_circuit_planes'] > 2:
            attributes['piC'] = 0.65 * attributes['n_circuit_planes']**0.63
        else:
            attributes['piC'] = 1.0

    _msg = _do_check_variables(attributes)

    # Calculate the active hazard rate.
    attributes[
        'hazard_rate_active'
    ] = attributes['lambda_b'] * attributes['piE']
    if attributes['subcategory_id'] == 3:
        attributes[
            'hazard_rate_active'
        ] = attributes['hazard_rate_active'] * attributes['piP']
    elif attributes['subcategory_id'] == 4:
        attributes[
            'hazard_rate_active'
        ] = attributes['hazard_rate_active'] * (
            attributes['n_wave_soldered'] * attributes['piC']
            + attributes['n_hand_soldered'] * (attributes['piC'] + 13.0)
        ) * attributes['piQ']
    elif attributes['subcategory_id'] == 5:
        attributes[
            'hazard_rate_active'
        ] = attributes['hazard_rate_active'] * attributes['piQ']
    else:
        attributes[
            'hazard_rate_active'
        ] = (
            attributes['hazard_rate_active'] * attributes['piK']
            * attributes['piP']
        )

    return attributes, _msg
