from typing import Dict, Any, List
from json_relational.src.protocols import IJsonRelationalContext


class FlatteningStrategy:
    def flatten(self, data, depth, parent_info, context):
        raise NotImplementedError


class DictFlattener(FlatteningStrategy):
    def flatten(self, d, depth, parent_info, context: IJsonRelationalContext):
        flat_object = {"sql_id": parent_info[1]}

        for child_key, value in d.items():
            mapped_key = context.key_mapper.get_mapped_key(child_key)
            if isinstance(value, dict):
                flattened = [context.flatten(
                    value, depth + 1, context.sql_id_manager.get_sql_info(mapped_key))]
                context.child_accumulator.process_children(
                    mapped_key, flattened, parent_info, context.sql_id_manager)
            elif isinstance(value, list):
                flattened = context.flatten(
                    value, depth + 1, context.sql_id_manager.get_sql_info(mapped_key))
                context.child_accumulator.process_children(
                    mapped_key, flattened, parent_info, context.sql_id_manager)
            else:
                flat_object[mapped_key] = value

        return flat_object


class ListFlattener(FlatteningStrategy):
    def flatten(self, lst, depth, parent_info, context):
        items = []
        for item in lst:
            wrapped_item = {parent_info[0]: item} if not isinstance(
                item, (dict, list)) else item
            flattened = context.flatten(wrapped_item, depth + 1, parent_info)
            items.append(flattened)

        return items
