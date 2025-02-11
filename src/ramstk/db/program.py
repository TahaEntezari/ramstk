# -*- coding: utf-8 -*-
#
#       ramstk.db.program.py is part of The RAMSTK Project
#
# All rights reserved.
# Copyright since 2007 Doyle "weibullguy" Rowland doyle.rowland <AT> reliaqual <DOT> com
"""RAMSTK Program Database Model."""

# Third Party Imports
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session

# RAMSTK Package Imports
from ramstk.models import (
    RAMSTKActionRecord,
    RAMSTKAllocationRecord,
    RAMSTKCauseRecord,
    RAMSTKControlRecord,
    RAMSTKDesignElectricRecord,
    RAMSTKDesignMechanicRecord,
    RAMSTKEnvironmentRecord,
    RAMSTKFailureDefinitionRecord,
    RAMSTKFunctionRecord,
    RAMSTKHardwareRecord,
    RAMSTKHazardRecord,
    RAMSTKMechanismRecord,
    RAMSTKMilHdbk217FRecord,
    RAMSTKMissionPhaseRecord,
    RAMSTKMissionRecord,
    RAMSTKModeRecord,
    RAMSTKNSWCRecord,
    RAMSTKOpLoadRecord,
    RAMSTKOpStressRecord,
    RAMSTKProgramInfoRecord,
    RAMSTKProgramStatusRecord,
    RAMSTKReliabilityRecord,
    RAMSTKRequirementRecord,
    RAMSTKRevisionRecord,
    RAMSTKSimilarItemRecord,
    RAMSTKStakeholderRecord,
    RAMSTKTestMethodRecord,
    RAMSTKValidationRecord,
)


def do_make_programdb_tables(engine: Engine) -> None:
    """Create all the tables in the RAMSTK Program database.

    :param engine: the SQLAlchemy database engine to use to create the program
        database tables.
    :type engine: :class:`sqlalchemy.engine.Engine`
    :return: None
    :rtype: None
    """
    RAMSTKRevisionRecord.__table__.create(bind=engine)
    RAMSTKProgramInfoRecord.__table__.create(bind=engine)
    RAMSTKProgramStatusRecord.__table__.create(bind=engine)
    RAMSTKMissionRecord.__table__.create(bind=engine)
    RAMSTKMissionPhaseRecord.__table__.create(bind=engine)
    RAMSTKEnvironmentRecord.__table__.create(bind=engine)
    RAMSTKFailureDefinitionRecord.__table__.create(bind=engine)

    RAMSTKFunctionRecord.__table__.create(bind=engine)
    RAMSTKHazardRecord.__table__.create(bind=engine)

    RAMSTKRequirementRecord.__table__.create(bind=engine)
    RAMSTKStakeholderRecord.__table__.create(bind=engine)

    RAMSTKHardwareRecord.__table__.create(bind=engine)
    RAMSTKAllocationRecord.__table__.create(bind=engine)
    RAMSTKDesignElectricRecord.__table__.create(bind=engine)
    RAMSTKDesignMechanicRecord.__table__.create(bind=engine)
    RAMSTKMilHdbk217FRecord.__table__.create(bind=engine)
    RAMSTKNSWCRecord.__table__.create(bind=engine)
    RAMSTKReliabilityRecord.__table__.create(bind=engine)
    RAMSTKSimilarItemRecord.__table__.create(bind=engine)
    RAMSTKModeRecord.__table__.create(bind=engine)
    RAMSTKMechanismRecord.__table__.create(bind=engine)
    RAMSTKCauseRecord.__table__.create(bind=engine)
    RAMSTKActionRecord.__table__.create(bind=engine)
    RAMSTKControlRecord.__table__.create(bind=engine)
    RAMSTKOpLoadRecord.__table__.create(bind=engine)
    RAMSTKOpStressRecord.__table__.create(bind=engine)
    RAMSTKTestMethodRecord.__table__.create(bind=engine)

    RAMSTKValidationRecord.__table__.create(bind=engine)


def do_create_program_db(engine: Engine, session: scoped_session) -> None:
    """Create and initialize a RAMSTK Program database.

    :param engine: the SQLAlchemy Engine connected to the database.
    :type engine: :class:`sqlalchemy.engine.Engine`
    :param session: the SQLAlchemy session to use when creating the database.
    :type session: :class:`sqlalchemy.orm.Session`
    :return: None
    :rtype: None
    """
    do_make_programdb_tables(engine)

    _record = RAMSTKProgramInfoRecord()
    session.add(_record)

    _revision = RAMSTKRevisionRecord()
    session.add(_revision)
    session.commit()

    _mission = RAMSTKMissionRecord()
    _mission.revision_id = _revision.revision_id
    session.add(_mission)
    session.commit()

    _record = RAMSTKProgramStatusRecord()
    _record.revision_id = _revision.revision_id
    session.add(_record)

    session.commit()
