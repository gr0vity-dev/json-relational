import hashlib


class SQLIDManager:
    def __init__(self):
        self.sql_id_counters = {}

    def increment_sql_id(self, type_name):
        self.sql_id_counters[type_name] = self.sql_id_counters.get(
            type_name, 0) + 1
        return self.sql_id_counters[type_name]

    def get_sql_info(self, type_name):
        return (type_name, self.sql_id_counters.get(type_name, 1))


class ChildAccumulator:
    def __init__(self, sql_id_manager):
        self.sql_id_manager = sql_id_manager
        self.accumulated_children = {}
        self.mappings = []
        self.child_hash_to_sql_id = {}
        self.pinned_root = None

    def set_pinned_root(self, pinned_root):
        self.pinned_root = pinned_root

    def add_new_child(self, key, child, child_hash, parent):
        sql_id = self.sql_id_manager.increment_sql_id(key)
        self.child_hash_to_sql_id[child_hash] = sql_id
        child["sql_id"] = sql_id
        self.accumulated_children.setdefault(key, []).append(child)
        self.add_mapping(parent, key, sql_id)

    def add_mapping(self, parent, key, link_sql_id):
        if self.pinned_root:
            parent = self.sql_id_manager.get_sql_info(self.pinned_root)
        self.mappings.append({
            "main_type": parent[0],
            "main_sql_id": parent[1],
            "link_type": key,
            "link_sql_id": link_sql_id
        })

    def process_children(self, key, child_items, parent):

        for child in child_items:
            self._process_child(key, child, parent)

    def _process_child(self, key, child, parent):
        child_hash = self.hash_dict(key, child)
        if child_hash not in self.child_hash_to_sql_id:
            self.add_new_child(key, child, child_hash, parent)
        else:
            self.add_mapping(
                parent, key, self.child_hash_to_sql_id[child_hash])

    def hash_dict(self, key, d):
        assert isinstance(d, dict)
        d_filtered = {k: v for k, v in d.items() if k != 'sql_id'}
        d_string = str(key) + str(sorted(d_filtered.items()))
        return hashlib.md5(d_string.encode()).hexdigest()


class KeyMapper:
    def __init__(self):
        self.key_mappings = {}

    def add_key_mappings(self, mappings):
        self.key_mappings.update(mappings)

    def get_mapped_key(self, key):
        return self.key_mappings.get(key, key)
