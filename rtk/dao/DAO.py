# -*- coding: utf-8 -*-
#
#       rtk.dao.DAO.py is part of The RTK Project
#
# All rights reserved.
# Copyright 2007 - 2017 Andrew Rowland andrew.rowland <AT> reliaqual <DOT> com
"""Data Access Object (DAO) Package."""

import gettext

from sqlalchemy import create_engine, exc, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database

# Import other RTK modules.
import rtk.dao.RTKCommonDB

# Import tables objects for the RTK Common database.
from .RTKUser import RTKUser
from .RTKGroup import RTKGroup
from .RTKEnviron import RTKEnviron
from .RTKModel import RTKModel
from .RTKType import RTKType
from .RTKCategory import RTKCategory
from .RTKSubCategory import RTKSubCategory
from .RTKPhase import RTKPhase
from .RTKDistribution import RTKDistribution
from .RTKManufacturer import RTKManufacturer
from .RTKUnit import RTKUnit
from .RTKMethod import RTKMethod
from .RTKCriticality import RTKCriticality
from .RTKRPN import RTKRPN
from .RTKLevel import RTKLevel
from .RTKApplication import RTKApplication
from .RTKHazards import RTKHazards
from .RTKStakeholders import RTKStakeholders
from .RTKStatus import RTKStatus
from .RTKCondition import RTKCondition
from .RTKFailureMode import RTKFailureMode
from .RTKMeasurement import RTKMeasurement
from .RTKLoadHistory import RTKLoadHistory

# Import RTK Program database table objects.
from .RTKAction import RTKAction
from .RTKAllocation import RTKAllocation
from .RTKCause import RTKCause
from .RTKControl import RTKControl
from .RTKDesignElectric import RTKDesignElectric
from .RTKDesignMechanic import RTKDesignMechanic
from .RTKEnvironment import RTKEnvironment
from .RTKFailureDefinition import RTKFailureDefinition
from .RTKFunction import RTKFunction
from .RTKGrowthTest import RTKGrowthTest
from .RTKHardware import RTKHardware
from .RTKHazardAnalysis import RTKHazardAnalysis
from .RTKIncident import RTKIncident
from .RTKIncidentAction import RTKIncidentAction
from .RTKIncidentDetail import RTKIncidentDetail
from .RTKMatrix import RTKMatrix
from .RTKMechanism import RTKMechanism
from .RTKMilHdbkF import RTKMilHdbkF
from .RTKMission import RTKMission
from .RTKMissionPhase import RTKMissionPhase
from .RTKMode import RTKMode
from .RTKNSWC import RTKNSWC
from .RTKOpLoad import RTKOpLoad
from .RTKOpStress import RTKOpStress
from .RTKProgramInfo import RTKProgramInfo
from .RTKProgramStatus import RTKProgramStatus
from .RTKReliability import RTKReliability
from .RTKRequirement import RTKRequirement
from .RTKRevision import RTKRevision
from .RTKSimilarItem import RTKSimilarItem
from .RTKSoftware import RTKSoftware
from .RTKSoftwareDevelopment import RTKSoftwareDevelopment
from .RTKSoftwareReview import RTKSoftwareReview
from .RTKSoftwareTest import RTKSoftwareTest
from .RTKStakeholder import RTKStakeholder
from .RTKSurvival import RTKSurvival
from .RTKSurvivalData import RTKSurvivalData
from .RTKTest import RTKTest
from .RTKTestMethod import RTKTestMethod
from .RTKValidation import RTKValidation

RTK_BASE = declarative_base()

# Add localization support.
_ = gettext.gettext

__author__ = 'Andrew Rowland'
__email__ = 'andrew.rowland@reliaqual.com'
__organization__ = 'ReliaQual Associates, LLC'
__copyright__ = 'Copyright 2007 - 2015 Andrew "weibullguy" Rowland'


class DAO(object):
    """This is the data access controller class."""

    RTK_SESSION = sessionmaker()

    # Define public class scalar attributes.
    engine = None
    metadata = None
    session = None

    def __init__(self):
        """Initialize an instance of the DAO controller."""

        # Initialize private dictionary instance attributes.

        # Initialize private list instance attributes.

        # Initialize private scalar instance attributes.

        # Initialize public dictionary instance attributes.

        # Initialize public list instance attributes.

        # Initialize public scalar instance attributes.

    def db_connect(self, database):
        """
        Connect to the database using settings from the configuration file.

        :param str database: the absolute path to the database to connect to.
        :return: False if successful, True if an error occurs.
        :rtype: bool
        """
        self.engine = create_engine(database, echo=False)
        self.metadata = MetaData(self.engine)

        self.session = self.RTK_SESSION(
            bind=self.engine,
            autoflush=True,
            autocommit=False,
            expire_on_commit=False)

        return False

    def _db_table_create(self, table):
        """
        Check if the passed table exists and create it if not.

        :param table: the table to check for.
        :return: False if successful or True if an error is encountered.
        :rtype: bool
        """
        _return = False

        if not self.engine.dialect.has_table(self.engine.connect(),
                                             str(table)):
            table.create(bind=self.engine)

        return _return

    def db_create_program(self, database):
        """
        Create a new RTK Program database.

        :param str database: the RFC1738 URL path to the database to connect
                             with.
        :return: False if successful or True if an error occurs.
        :rtype: bool
        """
        try:
            create_database(database)
        except IOError:
            return True

        self._db_table_create(RTKProgramInfo.__table__)
        self._db_table_create(RTKProgramStatus.__table__)

        self._db_table_create(RTKRevision.__table__)
        _revision = RTKRevision()
        _revision.revision_id = 1
        _revision.description = _(u"Test Revision")
        self.db_add([
            _revision,
        ], self.session)
        self.session.commit()

        self._db_table_create(RTKMission.__table__)
        _mission = RTKMission()
        _mission.revision_id = _revision.revision_id
        _mission.mission_id = 1
        _mission.description = _(u"Test Mission")
        self.db_add([
            _mission,
        ], self.session)
        self.session.commit()

        self._db_table_create(RTKMissionPhase.__table__)
        _phase = RTKMissionPhase()
        _phase.mission_id = _mission.mission_id
        _phase.phase_id = 1
        _phase.description = _(u"Test Mission Phase 1")
        self.db_add([
            _phase,
        ], self.session)
        self.session.commit()

        self._db_table_create(RTKEnvironment.__table__)
        self._db_table_create(RTKFailureDefinition.__table__)

        self._db_table_create(RTKFunction.__table__)
        self._db_table_create(RTKMode.__table__)
        self._db_table_create(RTKControl.__table__)
        self._db_table_create(RTKAction.__table__)
        _dic_rows = {}
        for i in [1, 2, 3]:
            _function = RTKFunction()
            _function.revision_id = _revision.revision_id
            _function.function_code = "FUNC-000{0:d}".format(i)
            self.db_add([_function], self.session)

            _mode = RTKMode()
            _mode.function_id = _function.function_id
            _mode.hardware_id = -1
            _mode.description = (
                "Test Functional Failure Mode #{0:d}").format(i)
            self.db_add([
                _mode,
            ], self.session)
            _control = RTKControl()
            _control.mode_id = _mode.mode_id
            _control.cause_id = -1
            _control.description = (
                "Test Functional FMEA Control #{0:d}").format(i)
            _action = RTKAction()
            _action.mode_id = _mode.mode_id
            _action.cause_id = -1
            _action.action_recommended = ("Test Functional FMEA Recommended "
                                          "Action #{0:d}").format(i)
            self.db_add([_control, _action], self.session)
            _dic_rows[i] = _function.function_id

        self._db_table_create(RTKRequirement.__table__)
        self._db_table_create(RTKStakeholder.__table__)
        self._db_table_create(RTKMatrix.__table__)

        # Create tables for Hardware analyses.
        self._db_table_create(RTKHardware.__table__)
        self._db_table_create(RTKReliability.__table__)
        self._db_table_create(RTKMilHdbkF.__table__)
        self._db_table_create(RTKNSWC.__table__)
        self._db_table_create(RTKDesignElectric.__table__)
        self._db_table_create(RTKDesignMechanic.__table__)

        _system = RTKHardware()
        _system.revision_id = _revision.revision_id
        _system.hardware_id = 1
        _system.description = "Test System"
        _system.ref_des = "S1"
        _system.comp_ref_des = "S1"
        self.db_add([
            _system,
        ], self.session)
        self.session.commit()

        self._db_table_create(RTKAllocation.__table__)
        self._db_table_create(RTKSimilarItem.__table__)
        self._db_table_create(RTKHazardAnalysis.__table__)
        self._db_table_create(RTKMechanism.__table__)
        self._db_table_create(RTKCause.__table__)
        self._db_table_create(RTKOpLoad.__table__)
        self._db_table_create(RTKOpStress.__table__)
        self._db_table_create(RTKTestMethod.__table__)
        _reliability = RTKReliability()
        _reliability.hardware_id = _system.hardware_id
        _mil_hdbk_217 = RTKMilHdbkF()
        _mil_hdbk_217.hardware_id = _system.hardware_id
        _design_electric = RTKDesignElectric()
        _design_electric.hardware_id = _system.hardware_id
        _design_mechanic = RTKDesignMechanic()
        _design_mechanic.hardware_id = _system.hardware_id
        _allocation = RTKAllocation()
        _allocation.revision_id = _revision.revision_id
        _allocation.hardware_id = _system.hardware_id
        _allocation.parent_id = 0
        _similaritem = RTKSimilarItem()
        _similaritem.revision_id = _revision.revision_id
        _similaritem.hardware_id = _system.hardware_id
        _similaritem.parent_id = 0
        _hazardanalysis = RTKHazardAnalysis()
        _hazardanalysis.revision_id = _revision.revision_id
        _hazardanalysis.hardware_id = _system.hardware_id
        _mode = RTKMode()
        _mode.function_id = -1
        _mode.hardware_id = _system.hardware_id
        _mode.description = 'System Test Failure Mode'
        self.db_add([
            _reliability, _mil_hdbk_217, _design_electric, _design_mechanic,
            _allocation, _similaritem, _hazardanalysis, _mode
        ], self.session)

        # Build a Hardware FMEA for the system.
        _mechanism = RTKMechanism()
        _mechanism.mode_id = _mode.mode_id
        _mechanism.description = 'Test Failure Mechanism #1'
        self.db_add([_mechanism], self.session)
        _cause = RTKCause()
        _cause.mechanism_id = _mechanism.mechanism_id
        _cause.description = 'Test Failure Cause #1'
        self.db_add([_cause], self.session)
        _control = RTKControl()
        _control.mode_id = -1
        _control.cause_id = _cause.cause_id
        _control.description = 'Test FMEA Control #1'
        _action = RTKAction()
        _action.mode_id = -1
        _action.cause_id = _cause.cause_id
        _action.action_recommended = 'Test FMEA Recommended Action #1'

        # Build the PoF for the system.
        _opload = RTKOpLoad()
        _opload.mechanism_id = _mechanism.mechanism_id
        _opload.description = 'Test Operating Load'
        self.db_add([_control, _action, _opload], self.session)
        _opstress = RTKOpStress()
        _opstress.load_id = _opload.load_id
        _opstress.description = 'Test Operating Stress'
        self.db_add([_opstress], self.session)
        _testmethod = RTKTestMethod()
        _testmethod.stress_id = _opstress.stress_id
        _testmethod.description = 'Test Test Method'
        self.db_add([_testmethod], self.session)

        _dic_cols = {1: _system.hardware_id}
        for i in [1, 2, 3, 4]:
            _subsystem = RTKHardware()
            _subsystem.revision_id = _revision.revision_id
            _subsystem.hardware_id = i + 1
            _subsystem.parent_id = _system.hardware_id
            _subsystem.ref_des = "SS{0:d}".format(i)
            _subsystem.comp_ref_des = "S1:SS{0:d}".format(i)
            _subsystem.description = "Test Sub-System {0:d}".format(i)
            self.db_add([
                _subsystem,
            ], self.session)
            _dic_cols[i + 1] = _subsystem.hardware_id

            if i == 1:
                for j in [5, 6, 7]:
                    _assembly = RTKHardware()
                    _assembly.revision_id = _revision.revision_id
                    _assembly.hardware_id = j + 1
                    _assembly.parent_id = _subsystem.hardware_id
                    _assembly.ref_des = "A{0:d}".format(j - 4)
                    _assembly.comp_ref_des = "S1:SS1:A{0:d}".format(j - 4)
                    _assembly.description = "Test Assembly {0:d}".format(j - 4)
                    self.db_add([
                        _assembly,
                    ], self.session)
                    _dic_cols[j + 1] = _assembly.hardware_id
        self.session.commit()

        for i in [1, 2, 3, 4]:
            _allocation = RTKAllocation()
            _allocation.revision_id = _revision.revision_id
            _allocation.hardware_id = i + 1
            _allocation.parent_id = _system.hardware_id
            _similaritem = RTKSimilarItem()
            _similaritem.revision_id = _revision.revision_id
            _similaritem.hardware_id = i + 1
            _similaritem.parent_id = _system.hardware_id
            _hazardanalysis = RTKHazardAnalysis()
            _hazardanalysis.revision_id = _revision.revision_id
            _hazardanalysis.hardware_id = i + 1
            _reliability = RTKReliability()
            _reliability.hardware_id = i + 1
            _mil_hdbk_217 = RTKMilHdbkF()
            _mil_hdbk_217.hardware_id = i + 1
            _design_electric = RTKDesignElectric()
            _design_electric.hardware_id = i + 1
            _design_mechanic = RTKDesignMechanic()
            _design_mechanic.hardware_id = i + 1
            self.db_add([
                _allocation, _similaritem, _hazardanalysis, _reliability,
                _mil_hdbk_217, _design_electric, _design_mechanic
            ], self.session)

        for i in [5, 6, 7]:
            _allocation = RTKAllocation()
            _allocation.revision_id = _revision.revision_id
            _allocation.hardware_id = i + 1
            _allocation.parent_id = 2
            _similaritem = RTKSimilarItem()
            _similaritem.revision_id = _revision.revision_id
            _similaritem.hardware_id = i + 1
            _similaritem.parent_id = 2
            _hazardanalysis = RTKHazardAnalysis()
            _hazardanalysis.revision_id = _revision.revision_id
            _hazardanalysis.hardware_id = i + 1

            _reliability = RTKReliability()
            _reliability.hardware_id = i + 1
            _mil_hdbk_217 = RTKMilHdbkF()
            _mil_hdbk_217.hardware_id = i + 1
            _design_electric = RTKDesignElectric()
            _design_electric.hardware_id = i + 1
            _design_mechanic = RTKDesignMechanic()
            _design_mechanic.hardware_id = i + 1
            self.db_add([
                _allocation, _similaritem, _hazardanalysis, _reliability,
                _mil_hdbk_217, _design_electric, _design_mechanic
            ], self.session)

        self.session.commit()

        for _ckey in _dic_cols:
            for _rkey in _dic_rows:
                _matrix = RTKMatrix()
                _matrix.revision_id = _revision.revision_id
                _matrix.matrix_id = 1
                _matrix.matrix_type = 'fnctn_hrdwr'
                _matrix.column_id = _ckey
                _matrix.column_item_id = _dic_cols[_ckey]
                _matrix.row_id = _ckey
                _matrix.row_item_id = _dic_rows[_rkey]
                self.db_add([_matrix], self.session)
        self.session.commit()

        # Create tables for Software analyses.
        self._db_table_create(RTKSoftware.__table__)
        self._db_table_create(RTKSoftwareDevelopment.__table__)
        self._db_table_create(RTKSoftwareReview.__table__)
        self._db_table_create(RTKSoftwareTest.__table__)

        # Create tables for Incidents.
        self._db_table_create(RTKIncident.__table__)
        self._db_table_create(RTKIncidentAction.__table__)
        self._db_table_create(RTKIncidentDetail.__table__)

        # Create table for Testing.
        self._db_table_create(RTKTest.__table__)

        # Create tables for Survival Analysis.
        self._db_table_create(RTKSurvival.__table__)
        self._db_table_create(RTKSurvivalData.__table__)

        # Create table for Verification and Validation.
        self._db_table_create(RTKValidation.__table__)

        return False

    @staticmethod
    def db_add(item, session):
        """
        Add a new item to the RTK Program database.

        :param item: the object to add to the RTK Program database.
        :param session: the SQLAlchemy scoped_session instance used to
                        communicate with the RTK Program database.
        :type session: :py:class:`sqlalchemy.orm.scoped_session`
        :return: (_error_code, _Msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = "RTK SUCCESS: Adding one or more items to the RTK Program " \
               "database."
        # TODO: Determine if the add_many option can work with Foreign Keys.
        for _item in item:
            try:
                session.add(_item)
                session.commit()
            except (exc.SQLAlchemyError, exc.DBAPIError) as error:
                print error
                session.rollback()
                _error_code = 1003
                _msg = "RTK ERROR: Adding one or more items to the RTK " \
                       "Program database."

        return _error_code, _msg

    @staticmethod
    def db_update(session):
        """
        Update the RTK Program database with any pending changes.

        :param session: the SQLAlchemy scoped_session instance used to
                        communicate with the RTK Program database.
        :type session: :py:class:`sqlalchemy.orm.scoped_session`
        :return: (_error_code, _Msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = "RTK SUCCESS: Updating the RTK Program database."

        try:
            session.commit()
        except (exc.SQLAlchemyError, exc.DBAPIError) as error:
            print error
            session.rollback()
            _error_code = 1004
            _msg = "RTK ERROR: Updating the RTK Program database."

        return _error_code, _msg

    @staticmethod
    def db_delete(item, session):
        """
        Delete a record from the RTK Program database.

        :param item: the item to remove from the RTK Program database.
        :type item: Object()
        :param session: the SQLAlchemy scoped_session instance used to
                        communicate with the RTK Program database.
        :type session: :py:class:`sqlalchemy.orm.scoped_session`
        :return: (_error_code, _Msg); the error code and associated error
                                      message.
        :rtype: (int, str)
        """
        _error_code = 0
        _msg = "RTK SUCCESS: Deleting an item from the RTK Program database."

        try:
            session.delete(item)
            session.commit()
        except (exc.SQLAlchemyError, exc.DBAPIError) as error:
            print error
            session.rollback()
            _error_code = 1005
            _msg = "RTK ERROR: Deleting an item from the RTK Program database."

        return _error_code, _msg

    @staticmethod
    def db_query(query, session=None):
        """
        Execute an SQL query against the connected database.

        :param str query: the SQL query string to execute
        :param session: the SQLAlchemy scoped_session instance used to
                        communicate with the RTK Program database.
        :type session: :class:`sqlalchemy.orm.scoped_session`
        :return:
        :rtype: str
        """
        return session.execute(query)

    @property
    def db_last_id(self):
        """
        Retrieve the value of the last ID column from a table in the database.

        :return: _last_id; the last value of the ID column.
        :rtype: int
        """
        _last_id = 0
        # TODO: Write the db_last_id method if needed, else remove from file.
        return _last_id
