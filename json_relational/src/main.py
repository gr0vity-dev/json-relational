from json_relational.src.models import SQLIDManager, ChildAccumulator, KeyMapper
from json_relational.src.flatten_strategies import DictFlattener, ListFlattener
import json


class JsonRelational:
    def __init__(self, root_name='log', max_depth=10, pin_root=False):
        self.root_name = root_name
        self.max_depth = max_depth
        self.sql_id_manager = SQLIDManager()
        self.child_accumulator = ChildAccumulator(
            pinned_root=root_name) if pin_root else ChildAccumulator()
        self.key_mapper = KeyMapper()
        self.strategies = {
            dict: DictFlattener(),
            list: ListFlattener()
        }

    @staticmethod
    def read_text(file_path, encoding='utf-8'):
        with open(file_path, 'r', encoding=encoding) as file:
            return file.read()

    @staticmethod
    def read_json(file_path, encoding='utf-8'):
        with open(file_path, 'r', encoding=encoding) as file:
            return json.load(file)

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
        if isinstance(json_data, list):
            return self.flatten_lines(json_data, is_json=True)

        results = [self.flatten(json_data)]
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
