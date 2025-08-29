"""Petit exemple d'utilisation du module de gestion."""
from app import services
from app.models import RecipeIngredient, OrderItem

if __name__ == "__main__":
    supplier = services.create_supplier("Prime")
    ingredient = services.create_ingredient("Tomate", "kg", 1.5, supplier.id)
    recipe = services.create_recipe("Salade de tomates", None, [RecipeIngredient(ingredient.id, 0.5)])
    order = services.create_order(supplier.id, [OrderItem(ingredient.id, 10)])
    services.receive_order(order.id)
    print("Stock de l'ingrédient:", services.list_ingredients()[0].stock)
