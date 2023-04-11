import csv
import os


class Checker:
    def __init__(self, all_pallet_names, label_names, categories):
        pallet_names = all_pallet_names
        manifested_pallet_name = label_names
        category_names = categories
        return

    # TODO: Finish function that returns a boolean value based on if the product meets special rules for a bin item
    def special_bins_check(self, asin, title):
        return

    # TODO: finish function that returns a boolean value based on if it is a category that we sort into
    def sorting_category_check(self):
        return

    # TODO: finish function that finds what category the product belongs in
    def category_finder(self):
        return

    def set_category(self, category, lpn):
        # TODO:[] takes in the lpn and category and sets the LPN and asin to that new category
        return

    def keyboard(self, name, price):
        keyboard_key_words = ['keyboard']
        not_keyboard_key_words = ['iPad', 'Case', 'Laptop']
        if any(word in name for word in keyboard_key_words) and \
                not any(word in name for word in not_keyboard_key_words):
            if price < 150:
                return "keyboards_mice_under"
            else:
                return "keyboards_mice_g_headphones"

        return
