import numpy as np


class OrderedCategoryEncoder:
    def __init__(self):
        self.categories_: list[str] = None  # pyright: ignore
        self.category_map: dict[str:int] = None  # pyright: ignore
        self.inverse_category_map: dict[int:str] = None  # pyright: ignore

    def fit(self, ordered_categories: list[str]):
        self.categories_ = ordered_categories
        self.category_map = {
            category: i + 1 for i, category in enumerate(ordered_categories)
        }
        self.inverse_category_map = {
            i + 1: category for i, category in enumerate(ordered_categories)
        }

    def transform(self, values: list[str]) -> np.array:  # pyright: ignore
        if set(values) - set(self.category_map):
            for value in values:
                if value not in self.category_map:
                    print(f"'{value}' was not in the fit data")
            raise ValueError("New category found, cannot transform")

        return np.array([self.category_map[value] for value in values])

    def inverse_transform(self, values: list[int]) -> np.array:  # pyright: ignore
        if set(values) - set(self.inverse_category_map):
            for value in values:
                if value not in self.inverse_category_map:
                    print(f"'{value}' was not in the fit data")
            raise ValueError("New category found, cannot transform")

        return np.array([self.inverse_category_map[value] for value in values])
