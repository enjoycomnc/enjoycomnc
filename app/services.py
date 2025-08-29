from app.models import Supplier, Ingredient, Recipe, RecipeIngredient, Order, OrderItem
from app.storage import STORAGE
from typing import List

# Suppliers

def create_supplier(name: str) -> Supplier:
    data = STORAGE.add('suppliers', {'name': name})
    return Supplier(**data)

def list_suppliers() -> List[Supplier]:
    return [Supplier(**s) for s in STORAGE.suppliers.values()]

# Ingredients

def create_ingredient(name: str, unit: str, price: float, supplier_id: int, stock: float = 0.0) -> Ingredient:
    if supplier_id not in STORAGE.suppliers:
        raise ValueError("Supplier does not exist")
    data = STORAGE.add('ingredients', {
        'name': name,
        'unit': unit,
        'price': price,
        'supplier_id': supplier_id,
        'stock': stock,
    })
    return Ingredient(**data)

def list_ingredients() -> List[Ingredient]:
    return [Ingredient(**i) for i in STORAGE.ingredients.values()]

# Recipes

def create_recipe(name: str, description: str | None, ingredients: List[RecipeIngredient]) -> Recipe:
    for item in ingredients:
        if item.ingredient_id not in STORAGE.ingredients:
            raise ValueError(f"Ingredient {item.ingredient_id} missing")
    data = STORAGE.add('recipes', {
        'name': name,
        'description': description,
        'ingredients': [item.__dict__ for item in ingredients],
    })
    return Recipe(id=data['id'], name=name, description=description, ingredients=ingredients)

def list_recipes() -> List[Recipe]:
    recipes = []
    for r in STORAGE.recipes.values():
        ing = [RecipeIngredient(**ri) for ri in r['ingredients']]
        recipes.append(Recipe(id=r['id'], name=r['name'], description=r['description'], ingredients=ing))
    return recipes

# Orders

def create_order(supplier_id: int, items: List[OrderItem]) -> Order:
    if supplier_id not in STORAGE.suppliers:
        raise ValueError("Supplier does not exist")
    for item in items:
        if item.ingredient_id not in STORAGE.ingredients:
            raise ValueError(f"Ingredient {item.ingredient_id} missing")
    data = STORAGE.add('orders', {
        'supplier_id': supplier_id,
        'items': [i.__dict__ for i in items],
        'status': 'created'
    })
    return Order(id=data['id'], supplier_id=supplier_id, items=items, status='created')

def list_orders() -> List[Order]:
    orders = []
    for o in STORAGE.orders.values():
        items = [OrderItem(**oi) for oi in o['items']]
        orders.append(Order(id=o['id'], supplier_id=o['supplier_id'], items=items, status=o['status']))
    return orders

def receive_order(order_id: int) -> Order:
    order = STORAGE.orders.get(order_id)
    if not order:
        raise ValueError("Order not found")
    if order['status'] == 'received':
        raise ValueError("Order already received")
    for item in order['items']:
        STORAGE.ingredients[item['ingredient_id']]['stock'] += item['quantity']
    order['status'] = 'received'
    items = [OrderItem(**oi) for oi in order['items']]
    return Order(id=order_id, supplier_id=order['supplier_id'], items=items, status=order['status'])
