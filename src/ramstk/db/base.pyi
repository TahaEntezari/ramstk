# Standard Library Imports
from typing import Any, Dict, List, TextIO, Tuple

# Third Party Imports
from sqlalchemy.engine import Engine
from sqlalchemy.orm import query as query
from sqlalchemy.orm import scoped_session

# RAMSTK Package Imports
from ramstk.exceptions import DataAccessError as DataAccessError

def do_create_program_db(database: Dict[str, str], sql_file: TextIO) -> None: ...
def do_open_session(database: str) -> Tuple[Engine, scoped_session]: ...

class BaseDatabase:
    cxnargs: Dict[str, str] = ...
    engine: Engine = ...
    session: scoped_session = ...
    database: str = ...
    sqlstatements: Dict[str, str] = ...
    def __init__(self) -> None: ...
    def do_connect(self, database: Dict) -> None: ...
    def do_delete(self, item: object) -> None: ...
    def do_disconnect(self) -> None: ...
    def do_insert(self, record: object) -> None: ...
    def do_insert_many(self, records: List[object]) -> None: ...
    def do_select_all(self, table: Any, **kwargs: Any) -> query.Query: ...
    def do_update(self, record: object = ...) -> None: ...
    def get_database_list(self, database: Dict[str, str]) -> List: ...
    def get_last_id(self, table: str, id_column: str) -> Any: ...
