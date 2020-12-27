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
        return sum(
            ingredient in ingredient_list
            for ingredient in self.find_non_allergens(data)
            for ingredient_list, _ in data
        )

    def part2(self, data):
        return self.find_allergens(data)

    def find_non_allergens(self, data):
        return {
            ingredient
            for ingredient, allergens in self.find_possible_allergens(data).items()
            if not allergens
        }

    def find_allergens(self, data):
        mapping = dict(
            (ingredient, allergens)
            for ingredient, allergens in self.find_possible_allergens(data).items()
            if allergens
        )
        while True:
            updated = False
            for ingredient, allergens in mapping.items():
                if len(allergens) == 1:
                    for other_ingredient in mapping:
                        if other_ingredient != ingredient and mapping[
                            other_ingredient
                        ].intersection(allergens):
                            mapping[other_ingredient] -= allergens
                            updated = True
            if not updated:
                break
        mapping = {
            allergen: ingredient
            for ingredient in mapping
            for allergen in mapping[ingredient]
        }
        return ",".join(mapping[allergen] for allergen in sorted(mapping))

    def find_possible_allergens(self, data):
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

        return possible_allergens
