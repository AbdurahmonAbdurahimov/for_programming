
def test_meal_composition():
    meal = {"name": "Rice Soup", "ingredients": {"rice": 100, "salt": 5}}
    assert "rice" in meal["ingredients"]
    assert meal["ingredients"]["salt"] == 5
