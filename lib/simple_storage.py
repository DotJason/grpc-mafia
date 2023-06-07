"""
Simple key-value storage by auto-incrementing id
"""


class SimpleStorage:
    def __init__(self):
        self.storage = {}
        self.next_id = 0

    def add(self, obj):
        obj_id = self.next_id
        self.next_id += 1

        self.storage[obj_id] = obj
        return obj_id

    def __getitem__(self, obj_id):
        return self.storage[obj_id]

    def remove(self, obj_id):
        self.storage.pop(obj_id)
