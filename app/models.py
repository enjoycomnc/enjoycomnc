from dataclasses import dataclass, field
from typing import List

@dataclass
class Supplier:
    id: int
    name: str

@dataclass
class Ingredient:
    id: int
    name: str
    unit: str
    price: float
    supplier_id: int
    stock: float = 0.0

@dataclass
class RecipeIngredient:
    ingredient_id: int
    quantity: float

@dataclass
class Recipe:
    id: int
    name: str
    description: str | None = None
    ingredients: List[RecipeIngredient] = field(default_factory=list)

@dataclass
class OrderItem:
    ingredient_id: int
    quantity: float

@dataclass
class Order:
    id: int
    supplier_id: int
    items: List[OrderItem] = field(default_factory=list)
    status: str = "created"
