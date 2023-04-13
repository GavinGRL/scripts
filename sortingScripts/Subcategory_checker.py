import csv
import os


class Checker:

    # * g-headsets over 150 go to high keyboard,mice,headset, 75-150 go to the auction pallet, under 75 go to low misc
    # * earbuds select go to a box, earbuds non-select go to a box
    # * mice over 75 go to high headsets, under 75 go to low misc
    # * phone/tablet cases go to own box
    # * keyboards over 150 go to high keyboard/mice/headset,
    # 75-150 go to the keyboards auction pallet, under 75 go to low misc
    # * bin routers gos in modems pallet, take from csv sheet that checks for these products

    def __init__(self, all_pallet_names, label_names, categories):
        pallet_names = all_pallet_names
        manifested_pallet_name = label_names
        category_names = categories
        self.sorting_specifics_folder = '../sorting_specifics/'
        return

    # TODO: finish function that finds what category the product belongs in
    def category_finder(self, name, price):

        if not self.keyboard(name, price) == "":
            return self.keyboard(name, price)

        elif not self.mice(name) == "":
            return self.mice(name)

        elif not self.earbuds(name) == "":
            return self.earbuds(name)

        elif not self.airpods(name) == "":
            return self.airpods(name)

        elif not self.headphones(name, price) == "":
            return self.headphones(name, price)

        elif not self.cpu_coolers(name) == "":
            return self.cpu_coolers(name)

        elif not self.modems(name, price) == "":
            return self.modems(name, price)

        return ''



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

