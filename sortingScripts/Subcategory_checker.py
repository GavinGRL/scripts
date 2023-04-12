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
        return False

    # TODO: finish function that finds what category the product belongs in
    def category_finder(self):

        return

    def keyboard(self, name, price):
        keyboard_key_words = ['keyboard']
        not_keyboard_key_words = ['iPad', 'Case', 'Laptop','Magic Keyboard']
        if any(word in name for word in keyboard_key_words) and \
                not any(word in name for word in not_keyboard_key_words):
            if price < 150:
                return "keyboards_mice_under"
            else:
                return "keyboards_mice_g_headphones"

        return

    def airpods(self, name, price, asin):
        asin_list = [ 'B07PXGQC1Q', 'B0BDHB9Y8H', 'B09JQL3NWT', 'B07H6QCGGZ', 'B08PZDSP2Z', 'B08PZJ8FZ8', 'B08PZD76NP',
                      'B08PZJN7BD', 'B08PZHYWJS', 'B07ZPC9QD4', 'B07PXGQC1Q', 'B09JQMJHXY', 'B0BDHWDR12', 'B07731Y1CC',
                      'B01MQWUXZS', 'B07PYLT6DN']

        return

    #wifi 5, escept synology

