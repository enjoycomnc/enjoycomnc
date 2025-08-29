import unittest
from app import services
from app.models import RecipeIngredient, OrderItem

class TestKitchenFlow(unittest.TestCase):
    def test_basic_flow(self):
        supplier = services.create_supplier("Prime")
        ingredient = services.create_ingredient("Tomato", "kg", 1.5, supplier.id)
        recipe = services.create_recipe(
            "Tomato Salad",
            "Simple salad",
            [RecipeIngredient(ingredient.id, 0.5)],
        )
        order = services.create_order(
            supplier.id, [OrderItem(ingredient.id, 10)]
        )
        services.receive_order(order.id)
        self.assertEqual(services.list_ingredients()[0].stock, 10)

if __name__ == "__main__":
    unittest.main()
