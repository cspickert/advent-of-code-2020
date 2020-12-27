from base import BaseSolution


class Solution(BaseSolution):
    def load_data(self, input):
        return [
            (
                set(line.split("(")[0].strip().split()),
                set(line.split("(")[1].strip(")")[9:].split(", ")),
            )
            for line in input.splitlines()
        ]

    def part1(self, data):
        all_allergens = set()
        all_ingredients = set()

        for ingredients, allergens in data:
            all_allergens.update(allergens)
            all_ingredients.update(ingredients)

        possible_allergens = {
            ingredient: set(all_allergens) for ingredient in all_ingredients
        }

        for ingredient in possible_allergens:
            for ingredient_list, allergen_list in data:
                if ingredient not in ingredient_list:
                    possible_allergens[ingredient] -= allergen_list

        non_allergens = {
            ingredient
            for ingredient in possible_allergens
            if not possible_allergens[ingredient]
        }

        return sum(
            ingredient in ingredient_list
            for ingredient in non_allergens
            for ingredient_list, _ in data
        )
