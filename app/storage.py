from typing import Dict

class InMemoryStorage:
    def __init__(self):
        self.suppliers: Dict[int, dict] = {}
        self.ingredients: Dict[int, dict] = {}
        self.recipes: Dict[int, dict] = {}
        self.orders: Dict[int, dict] = {}
        self._counters = {
            'suppliers': 0,
            'ingredients': 0,
            'recipes': 0,
            'orders': 0,
        }

    def _next_id(self, table: str) -> int:
        self._counters[table] += 1
        return self._counters[table]

    def add(self, table: str, data: dict) -> dict:
        new_id = self._next_id(table)
        data['id'] = new_id
        getattr(self, table)[new_id] = data
        return data

STORAGE = InMemoryStorage()
