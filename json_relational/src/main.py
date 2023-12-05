from typing import Protocol, Dict, Any
from json_relational.src.models import SQLIDManager, ChildAccumulator, KeyMapper
from json_relational.src.flatten_strategies import DictFlattener, ListFlattener
import json


class JsonRelational:
    def __init__(self, root_name='log', max_depth=10):
        self.root_name = root_name
        self.max_depth = max_depth
        self.sql_id_manager = SQLIDManager()
        self.child_accumulator = ChildAccumulator()
        self.key_mapper = KeyMapper()
        self.strategies = {
            dict: DictFlattener(),
            list: ListFlattener()
        }

    def flatten(self, json_data, depth=0, parent_info=None):
        if depth > self.max_depth:
            return json_data

        parent_info = parent_info or (
            self.root_name, self.sql_id_manager.increment_sql_id(self.root_name))

        strategy = self.strategies.get(type(json_data))
        if strategy:
            return strategy.flatten(json_data, depth, parent_info, self)
        else:
            return json_data

    def flatten_json(self, json_data):
        results = []
        result = self.flatten(json_data)
        results.append(result)

        self.child_accumulator.accumulated_children[self.root_name] = results
        return {
            self.root_name: results,
            **self.child_accumulator.accumulated_children,
            "mappings": self.child_accumulator.mappings
        }

    def flatten_lines(self, json_lines, is_json=False):
        results = []
        json_lines = json_lines if is_json else json_lines.splitlines()
        for line in json_lines:
            if not line:
                continue
            line = line if is_json else json.loads(line)
            result = self.flatten(line)
            results.append(result)

        self.child_accumulator.accumulated_children[self.root_name] = results
        return {
            self.root_name: results,
            **self.child_accumulator.accumulated_children,
            "mappings": self.child_accumulator.mappings
        }

    def add_key_mappings(self, mappings):
        self.key_mapper.add_key_mappings(mappings)

    def _flatten_dict(self, d, depth, parent_info):
        parent_info = parent_info or (
            self.root_name, self.sql_id_manager.increment_sql_id(self.root_name))
        flat_object = {"sql_id": parent_info[1]}

        for child_key, value in d.items():
            mapped_key = self.key_mapper.get_mapped_key(child_key)
            if isinstance(value, (dict, list)):
                flattened = self.flatten(
                    value, depth + 1, self.sql_id_manager.get_sql_info(mapped_key))
                self.child_accumulator.process_children(
                    mapped_key, flattened, parent_info, self.sql_id_manager)
            else:
                flat_object[mapped_key] = value

        return flat_object

    def _flatten_list(self, lst, depth, parent_info):
        parent_info = parent_info or (
            self.root_name, self.sql_id_manager.increment_sql_id(self.root_name))

        items = []
        for item in lst:
            if not isinstance(item, (dict, list)):
                wrapped_item = {parent_info[0]: item}
            else:
                wrapped_item = item

            flattened = self.flatten(wrapped_item, depth + 1, parent_info)
            items.append(flattened)

        return items
