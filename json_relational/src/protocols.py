
from json_relational.src.models import SQLIDManager, ChildAccumulator, KeyMapper
from typing import Dict, Any, List, Protocol


class IJsonRelationalContext(Protocol):
    sql_id_manager: SQLIDManager
    child_accumulator: ChildAccumulator
    key_mapper: KeyMapper

    def flatten(self, json_data: Any, depth: int, parent_info: tuple) -> Dict:
        ...

    def flatten_lines(self, json_lines: Any, is_json: bool) -> Dict:
        ...

    def add_key_mappings(self, mappings: Dict) -> Dict:
        ...
