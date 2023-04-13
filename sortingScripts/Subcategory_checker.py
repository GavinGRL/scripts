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
        name = name.upper()
        keyboard_key_words = ['KEYBOARD']
        not_keyboard_key_words = ['IPAD', 'CASE', 'LAPTOP', 'MAGIC KEYBOARD']
        if any(word in name for word in keyboard_key_words) and \
                not any(word in name for word in not_keyboard_key_words):
            if price < 150:
                return "keyboards_mice_under"
            else:
                return "keyboards_mice_g_headphones"

        return ""

    def mice(self, name):
        name = name.upper()
        mice_words = ['MOUSE']
        not_mice_words = ['TABLET', 'DESKTOP', 'COMPUTER']
        if any(word in name for word in mice_words) and not any(word in name for word in not_mice_words):
            return "keyboards_mice_g_headphones"
        else:
            return ""

    def earbuds(self, name):
        name = name.upper()
        earbuds_file = self.sorting_specifics_folder
        earbud_words = ['EARBUD', 'EARPHONE', 'IN-EAR']
        not_earbud_words = ['POCKETALKER', 'AIRPODS', 'RADIO', 'WALKIE TALKIE']

        if any(word in name for word in earbud_words) and not any(word in name for word in not_earbud_words):
            with open(earbuds_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)

                for row in reader:

                    if row[0] in name:
                        return "earbuds_selected"
                    else:
                        return "earbuds_not_selected"
        else:
            return ""

    def airpods(self, name):
        name = name.upper()
        airpod_words = ["AIRPOD"]
        not_airpod_words = ["BELKIN"]

        if any(word in name for word in airpod_words) and not any(word in name for word in not_airpod_words):
            return "AirPods"
        else:
            return ""

    def headphones(self, name, price):
        name = name.upper()
        headphone_words = ["GAMING HEADPHONE"]
        not_headphone_words = ["APPLE"]

        if any(word in name for word in headphone_words):
            if(price > 150):
                return "keyboard_mice_g_headphones"
            else:
                return "g_headphones_under"
        else:
            return ""

    def cpu_coolers(self, name):
        name = name.upper()
        cpu_cooler_words = ["CPU COOLER", "CPU LIQUID COOLER", "RADIATOR"]
        not_cpu_cooler_words = ["CASE"]

        if any(word in name for word in cpu_cooler_words) and not any(word in name for word in not_cpu_cooler_words):
            return "cpu_coolers"
        else:
            return ""

    def modems(self, name, price):  # Modem, DOCSIS, WIFI 5, NOT Synology, and Routers under 75
        name = name.upper()
        router_words = ['ROUTER']
        modem_words = ["MODEM", "DOCSIS", "WIFI 5", "WI-FI 5"]
        not_modem_words = ["SYNOLOGY"]

        if any(word in name for word in router_words) and price < 75 \
                or any(word in name for word in modem_words) and not any(word in name for word in not_modem_words):
            return "modems"
        else:
            return ""
