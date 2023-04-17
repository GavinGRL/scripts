import csv
import os
import time
import tkinter as tk
from tkinter import messagebox, Scrollbar, Canvas
from tkinter import ttk
import re
import Subcategory_checker
import asinFinder

csv_file_location = "../csv_files/"
pallet_folder = "../pallets/"
truck_folder = "../truck_items/"
completed_pallet_folder = "../completed_pallets/"
truck_items = ''
lpn = ''
label_names = [
    "over75", "under75", "keyboards_mice_auction", "g_headphones_auction",
    "other_earbuds", "Modems", "cpu_coolers"]

# TODO:[] Update all_pallet_names to have all of the product categories sorted
all_pallet_names = ["over75", "under75", "keyboards/mice/gaming headset", "keyboards_mice_auction", "g_headphones_auction",
                    "earbuds_to_test", "other_earbuds", "Modems", "Drawing Tablets/Portable Monitors",
                    "Graphics Cards", "Power Supplies", "Motherboards", "Ram", "SSD", "Cameras", "Audio Products",
                    "Gaming Systems", "NAS", "Hard Drives", "Mini Computers", "Watches", "Phone/Tablet Cases",
                    "Apple Accessories", "PCIE Cards", "Phones/Tablets", "Headphones", "Laptop", "Airpods",
                    "CPU", "cpu_coolers", "Docking Stations", "Routers/Switches", "Bulk"]

sorting_categories = ["keyboards/mice/gaming headset", "keyboards_mice_auction", "g_headphones_auction",
                      "earbuds_to_test", "other_earbuds", "Modems", "Drawing Tablets/Portable Monitors",
                      "Graphics Cards", "Power Supplies", "Motherboards", "Ram", "SSD", "Cameras", "Audio Products",
                      "Gaming Systems", "NAS", "Hard Drives", "Mini Computers", "Watches", "Phone/Tablet Cases",
                      "Apple Accessories", "PCIE Cards", "Phones/Tablets", "Headphones", "Laptop", "Airpods",
                      "CPU", "cpu_coolers","Docking Stations","Routers/Switches","Bulk"]

file_name = {name: name for name in label_names}


def save_current_file_setup():
    os.remove(csv_file_location + "saved_files.csv")

    with open(csv_file_location + "saved_files.csv", 'a', encoding='utf-8', newline='') as saved_file_file:
        saved_file_writer = csv.writer(saved_file_file)
        for name in file_name:
            row_values = [name, file_name[name]]
            saved_file_writer.writerow(row_values)
        saved_file_writer.writerow(['truck_items', truck_items])

    main_frame.quit()

    return


def load_file_setup():
    global truck_items
    with open(csv_file_location + "saved_files.csv", 'r', encoding='utf-8', newline='') as saved_file_file:
        saved_file_reader = csv.reader(saved_file_file)

        for row in saved_file_reader:
            if len(row) == 2:  # Check if the row has exactly two values
                name, new_file_name = row
                if name == 'truck_items':
                    truck_items = new_file_name
                else:
                    file_name[name] = new_file_name

        for name in label_names:
            labels[name].set(value=name.upper() + ": " + file_name[name])
        truck_items_label_text.set(value=truck_items)

    return


def set_undefined():
    for name in label_names:
        labels[name].set(value=name.upper() + ": " + name + "_0")
        file_name[name] = (name + ".csv")


# computes the average price of a pallet file, then sets all MISC items to that average price
def compute_misc_avg(pallet_type):
    if os.path.exists(pallet_folder + file_name[pallet_type]):
        print("PATH EXISTS")
        # find the average price while skipping over temp items
        with open(pallet_folder + file_name[pallet_type], 'r', encoding='utf-8') as f, open(pallet_folder + 'temp.csv',
                                                                                            'w',
                                                                                            encoding='utf-8') as temp:
            reader = csv.reader(f)
            writer = csv.writer(temp)

            # calculate average price
            total_price = 0
            num_items = 0
            for row in reader:
                if not row[4] == 'temp_price':
                    total_price += float(row[4])
                    num_items += 1
            avg_price_cat = total_price / num_items
            # reset reader to look at top of file
            f.seek(0)

            # write updated rows to temp file
            for row in reader:
                if not row[3] == 'MISC':
                    writer.writerow(row)
                else:
                    row[4] = avg_price_cat
                    writer.writerow(row)

        os.remove(pallet_folder + file_name[pallet_type])
        os.rename(pallet_folder + "temp.csv", completed_pallet_folder + file_name[pallet_type])
    else:
        print("PATH DOES NOT EXIST")


def file_creator(pallet_number, pallet_type):
    compute_misc_avg(pallet_type)

    if pallet_number == -1:
        match = re.search(r"(\d+)\.csv$", file_name[pallet_type])
        if match:
            pallet_number = int(match.group(1)) + 1
        else:
            messagebox.showerror(title="Not Valid", message=f"Your request could not be completed")

    if label_names.__contains__(pallet_type):
        new_file_name = f"{pallet_type}_{pallet_number}.csv"
        if os.path.exists(new_file_name):
            messagebox.showerror(title="Not Valid", message=f"The file:{new_file_name} already exists")
            return
        file_name[pallet_type] = new_file_name
        print(file_name[pallet_type])
        labels[pallet_type].set(value=pallet_type.upper() + ": " + new_file_name)
    else:
        messagebox.showerror(title="Not Valid", message="This file name is not valid")
    return


def file_changer(found_file_name, pallet_type):
    file_name[pallet_type] = found_file_name
    labels[pallet_type].set(value=pallet_type.upper() + ": " + found_file_name)

    # messagebox.showerror(title="NO FILE",message="This file does not exist")

    return


def search_asin():
    global title_label, price_label, asin_label, pallet_label, lpn
    for name in label_names:
        # ! Fix this, does not work correctly in current state
        if labels[name].get == name + '_0':
            messagebox.showerror(title="No Pallet Selected", message="Please select pallets")
            return

    os.system('cls' if os.name == 'nt' else 'clear')
    asin = asin_entry.get()
    lpn = lpn_entry.get()
    asin_found = False
    with open(csv_file_location + 'KnownBinItems.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["Asin"] == asin:
                item_desc = row['ItemDesc'].replace(',', '')
                upc = row['UPC']
                price = float(row['Total Price'].replace(',', '').replace('$', ''))
                title_label_text.set("TITLE: {}".format(item_desc))
                price_label_text.set("PRICE: {}".format(price))
                asin_label_text.set("ASIN: {}".format(asin))
                category = Subcategory_checker.Checker.category_finder(asin)
                row_values = [lpn, upc, row['Asin'], item_desc, price, category]
                file_writer(row_values, file_name['under75'])
                pallet_label_text.set('PALLET: Under 75')
                set_input_file_category('under75', asin, upc, item_desc, price)
                clear_fields()
                return
    # open input file and search for ASIN

    if BOW(asin, lpn):
        return
    else:
        row_val = asinFinder.asin_lookup(asin)  # [found_TF,name,price,upc]
        if not (row_val[0]):
            set_product_to_category(lpn)
            # if asinFinder found the asinD
        price = row_val[2]
        name = row_val[1]
        upc = row_val[3]

        ask_for_asin_category(False, lpn, asin, upc, name, price)
    return


def ask_for_asin_category(tf_already_in, lpn, asin, upc, name, price):
    ask_category_window = tk.Toplevel(root)
    ask_category_window.geometry("1000x250")
    ask_category_frame = ttk.Frame(ask_category_window)
    ask_category_frame.grid(column=0, row=0, sticky='nsew')
    ask_category_frame.focus_set()
    # Create a label and entry widget for asin input
    title = ttk.Label(ask_category_frame, text="Title:")
    title.grid(column=0, row=0, padx=10, pady=10)

    title_name = ttk.Label(ask_category_frame, text=name[:60])
    title_name.grid(column=1, row=0, padx=10, pady=10, sticky='w')

    given_price = ttk.Label(ask_category_frame, text="Price:")
    given_price.grid(column=0, row=1, padx=10, pady=10)

    price_name = ttk.Label(ask_category_frame, text=price)
    price_name.grid(column=1, row=1, padx=10, pady=10, sticky='w')

    category_entry_label = ttk.Label(ask_category_frame, text="Scan Category:")
    category_entry_label.grid(column=0, row=2, padx=10, pady=10)

    category_entry2 = ttk.Entry(ask_category_frame)
    category_entry2.grid(column=1, row=2, padx=10, pady=10)

    def submit():
        # row_val = [found_TF, name, price, upc]
        """submit: submits the upc entered"""
        category = category_entry2.get()
        ask_category_window.destroy()
        if tf_already_in:
            # Open the CSV file in write mode and create a csv.writer object

            with open(csv_file_location + 'input.csv', 'r', encoding='utf-8') as input_file, open(
                    csv_file_location + 'temp.csv', 'w', encoding='utf-8',
                    newline='') as output:
                reader = csv.reader(input_file)
                writer = csv.writer(output)

                for row in reader:
                    if row[1] == asin:
                        new_row = [category, asin, upc, name, price]
                        writer.writerow(new_row)
                    else:
                        writer.writerow(row)

            os.remove(csv_file_location + 'input.csv')
            os.rename(csv_file_location + 'temp.csv', csv_file_location + 'input.csv')

        else:
            with open(csv_file_location + 'input.csv', 'a+', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                # input.csv = [category, Asin, UPC,ItemDesc,Total Price]
                row = [category, asin, upc, name, price]
                writer.writerow(row)
        return BOW(asin, lpn)

    submit_button = ttk.Button(ask_category_frame, text="Submit", command=submit)
    submit_button.grid(column=1, row=3, padx=10, pady=10)
    ask_category_frame.lift()
    category_entry2.focus()

    return


def set_input_file_category(category, asin, upc, name, price):
    # TODO:[x] make work, deletes all data in input.csv
    with open(csv_file_location + 'input.csv', 'r', encoding='utf-8') as input_file, \
            open(csv_file_location + 'temp.csv', 'w', encoding='utf-8', newline='') as output:
        reader = csv.reader(input_file)
        writer = csv.writer(output)

        for row in reader:
            if row[1] == asin:
                new_row = [category, asin, upc, name, price]
                writer.writerow(new_row)
            else:
                writer.writerow(row)

    # no need to close the file explicitly
    # the "with" statement will take care of it

    os.remove(csv_file_location + 'input.csv')
    os.rename(csv_file_location + 'temp.csv', csv_file_location + 'input.csv')

    return


def BOW(asin, lpn):
    asin_found = False
    sub_cat = Subcategory_checker.Checker(all_pallet_names, label_names, sorting_categories)
    with open(csv_file_location + 'input.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Asin'] == asin:
                asin_found = True
                # remove commas from item description and display title and price
                asin = row['Asin']
                item_desc = row['ItemDesc'].replace(',', '')
                upc = row['UPC']

                price = float(row['Total Price'].replace(',', '').replace('$', ''))
                title_label_text.set("TITLE: {}".format(item_desc))
                price_label_text.set("PRICE: {}".format(price))
                asin_label_text.set("ASIN: {}".format(asin))
                if price < 75 and sub_cat.modems(item_desc, price) == "":
                    row_values = [lpn, upc, asin, item_desc, price, 'under75']
                    file_writer(row_values, file_name['under75'])
                    pallet_label_text.set('PALLET: Under 75')
                    set_input_file_category('under75', asin, upc, item_desc, price)

                else:
                    csvfile.close()
                    category_of_item = sub_cat.category_finder(item_desc, price)
                    if not category_of_item == '':
                        set_input_file_category(category_of_item, asin, upc, item_desc, price)
                    with open(csv_file_location + 'input.csv', 'r', encoding='utf-8') as csvfile2:
                        reader2 = csv.DictReader(csvfile2)
                        for row2 in reader2:
                            if row2['Asin'] == asin:
                                if row2['Category'] == '':
                                    tf_already_in = True
                                    ask_for_asin_category(tf_already_in, lpn, asin, upc, item_desc, price)
                                    return asin_found
                                else:
                                    category = row2['Category']
                                    if sorting_categories.__contains__(category):
                                        # figure what pallet to put it into
                                        if label_names.__contains__(category):
                                            # pallet that is manifested
                                            row_values = [lpn, upc, asin, item_desc, price, category]
                                            file_writer(row_values, file_name[category])
                                        else:
                                            # pallet that is not manifested
                                            row_values = [lpn, upc, asin, item_desc, price, category]
                                            truckload_file_write(row_values)
                                        pallet_label_text.set(f"PALLET: {category}")

                                    else:
                                        # this is the misc over 75 pallet
                                        row_values = [lpn, upc, asin, item_desc, price, category]
                                        file_writer(row_values, file_name['over75'])
                                        pallet_label_text.set('PALLET: Over 75')
                                    clear_fields()
                                    return asin_found

                clear_fields()
    return asin_found


def file_writer(row_values, file_name_writer):
    """row_values = lpn, upc, ASIN, item_desc, price, category"""
    with open(pallet_folder + file_name_writer, 'a', encoding='utf-8', newline='') as write_file:
        write_file_writer = csv.writer(write_file)
        write_file_writer.writerow(row_values)
        truckload_file_write(row_values)
    return


def ask_for_category(lpn):
    def submit_category():
        """submit: submits the upc entered"""
        category.set(category_entry.get())
        ask_for_category_window.destroy()
        upc_asin_not_found(lpn, category.get())  # Call upc_asin_not_found here

    root = tk.Tk()  # Create the root window
    ask_for_category_window = tk.Toplevel(root)
    ask_for_category_window.geometry("350x120")
    ask_for_category_frame = ttk.Frame(ask_for_category_window)
    ask_for_category_frame.grid(column=0, row=0, sticky='nsew')
    ask_for_category_frame.focus_set()

    # Create a label and entry widget for category input
    category_label = ttk.Label(ask_for_category_frame, text="Enter Category:")
    category_label.grid(column=0, row=0, padx=10, pady=10)
    category_entry = ttk.Entry(ask_for_category_frame)
    category_entry.grid(column=1, row=0, padx=10, pady=10)

    category = tk.StringVar()  # Create a StringVar to store the value of the category

    submit_button = ttk.Button(ask_for_category_frame, text="Submit", command=submit_category)
    submit_button.grid(column=1, row=1, padx=10, pady=10)
    root.withdraw()  # Hide the root window
    ask_for_category_window.mainloop()  # Start the event loop

    return


# If no ASIN or UPC
def upc_asin_not_found(lpn, category):
    row_values = [lpn, "N/A", "N/A", "N/A", "N/A", category]
    total_price = 0
    num_items = 0

    # If category is a manifest
    if category in label_names:

        # Set price to avg price, and set name to "Misc"
        row_values = [lpn, "N/A", "N/A", "MISC", "temp_price", category]

        # Add to category manifest and truckload
        file_writer(row_values, file_name[category])

    # If category is not a manifest, add to truckload
    else:
        truckload_file_write(row_values)
    pallet_label_text.set(f"PALLET: {category}")

    return


def truckload_file_write(row_values):
    with open(truck_folder + truck_items, 'a', encoding='utf-8', newline='') as truck_items_file:
        truck_items_writer = csv.writer(truck_items_file)
        truck_items_writer.writerow(row_values)


def upc_search(lpn, upc):
    sub_cat = Subcategory_checker.Checker(all_pallet_names, label_names, sorting_categories)
    upc_found = False
    with open(csv_file_location + 'input.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['UPC'] == upc:
                upc_found = True
                # remove commas from item description and display title and price
                asin = row['Asin']
                item_desc = row['ItemDesc'].replace(',', '')
                upc = row['UPC']

                price = float(row['Total Price'].replace(',', '').replace('$', ''))
                title_label_text.set("TITLE: {}".format(item_desc))
                price_label_text.set("PRICE: {}".format(price))
                asin_label_text.set("ASIN: {}".format(asin))
                if price < 75 and sub_cat.modems(item_desc, price) == "":
                    row_values = [lpn, upc, asin, item_desc, price, 'under75']
                    file_writer(row_values, file_name['under75'])
                    pallet_label_text.set('PALLET: Under 75')
                    set_input_file_category('under75', asin, upc, item_desc, price)

                else:
                    csvfile.close()
                    category_of_item = sub_cat.category_finder(item_desc, price)
                    if not category_of_item == '':
                        set_input_file_category(category_of_item, asin, upc, item_desc, price)
                    with open(csv_file_location + 'input.csv', 'r', encoding='utf-8') as csvfile2:
                        reader2 = csv.DictReader(csvfile2)
                        for row2 in reader2:
                            if row2['Asin'] == asin:
                                if row2['Category'] == '':
                                    tf_already_in = True
                                    ask_for_asin_category(tf_already_in, lpn, asin, upc, item_desc, price)
                                    return upc_found
                                else:
                                    category = row2['Category']
                                    if sorting_categories.__contains__(category):
                                        # figure what pallet to put it into
                                        if label_names.__contains__(category):
                                            # pallet that is manifested
                                            row_values = [lpn, upc, asin, item_desc, price, category]
                                            file_writer(row_values, file_name[category])
                                        else:
                                            # pallet that is not manifested
                                            row_values = [lpn, upc, asin, item_desc, price, category]
                                            truckload_file_write(row_values)
                                        pallet_label_text.set(f"PALLET: {category}")

                                    else:
                                        # this is the misc over 75 pallet
                                        row_values = [lpn, upc, asin, item_desc, price, category]
                                        file_writer(row_values, file_name['over75'])
                                        pallet_label_text.set('PALLET: Over 75')
                                    clear_fields()
                                    return upc_found

                clear_fields()
    return upc_found


def set_product_to_category(lpn):
    yesno = messagebox.askyesno(title="NO ASIN FOUND", message="Does this product have a UPC?")

    if yesno:
        upc_found_tf = ask_for_upc(lpn)
        if upc_found_tf:
            return

    ask_for_category(lpn)
    return


def complete_pallet(pallet_name):
    tf_mistake = messagebox.askokcancel(title="Create New Box/Pallet",
                                        message=f"Are you sure you want to create a new Pallet/Box for: {pallet_name}")
    if tf_mistake:
        print(pallet_name)
        file_creator(-1, pallet_name)
    return


def undo():
    # remove from truckload.csv
    with open(truck_folder + truck_items, 'r', encoding='utf-8') as truck_load, open(truck_folder + 'temp.csv', 'w',
                                                                                     newline='',
                                                                                     encoding='utf-8') as output_file:
        reader = csv.reader(truck_load)
        writer = csv.writer(output_file)

        for row in reader:
            if row[0] == lpn:
                continue
            else:
                writer.writerow(row)

    os.remove(truck_folder + truck_items)
    os.rename(truck_folder + 'temp.csv', truck_folder + truck_items)

    # check if LPN is in any manifest files, if yes remove
    for name in file_name:
        file_path = pallet_folder + file_name[name]
        if not os.path.isfile(file_path):
            continue
        with open(file_path, 'r', encoding='utf-8') as label_file, open(pallet_folder + 'temp.csv', 'w',
                                                                        newline='', encoding='utf-8') as output_file:
            reader = csv.reader(label_file)
            writer = csv.writer(output_file)

            for row in reader:
                if row[0] == lpn:
                    continue
                else:
                    writer.writerow(row)

        os.remove(pallet_folder + file_name[name])
        os.rename(pallet_folder + 'temp.csv', pallet_folder + file_name[name])

    # go to not found in master.csv
    set_product_to_category(lpn)

    return


def clear_fields():
    """clear_fields: clears the asin and lpn entry fields in the gui"""
    asin_entry.delete(0, tk.END)
    lpn_entry.delete(0, tk.END)


def on_asin_enter(event):
    """on_asin_enter: checks if the asin entry field is an asin"""
    if asin_entry.get().startswith("B"):
        lpn_entry.focus()
    else:
        asin_entry.delete(0, tk.END)


def on_lpn_enter(event):
    """on_lpn_enter: checks if the lpn entry field is a lpn and calls search_asin function."""
    if lpn_entry.get().startswith("L"):
        search_asin()  # searches
        asin_entry.focus()
    else:
        lpn_entry.delete(0, tk.END)


def ask_for_upc(lpn):
    """
    @rtype: upc_search(lpn, upc) true or false after hitting submit
    """
    def submit():
        """submit: submits the upc entered"""
        upc.set(upc_entry.get())
        ask_for_upc_window.destroy()

    root = tk.Tk()
    ask_for_upc_window = tk.Toplevel(root)
    ask_for_upc_window.geometry("350x120")
    ask_for_upc_frame = ttk.Frame(ask_for_upc_window)
    ask_for_upc_frame.grid(column=0, row=0, sticky='nsew')
    ask_for_upc_frame.focus_set()

    upc_label = ttk.Label(ask_for_upc_frame, text="Enter UPC:")
    upc_label.grid(column=0, row=0, padx=10, pady=10)
    upc_entry = ttk.Entry(ask_for_upc_frame)
    upc_entry.grid(column=1, row=0, padx=10, pady=10)

    upc = tk.StringVar()

    submit_button = ttk.Button(ask_for_upc_frame, text="Submit", command=submit)
    submit_button.grid(column=1, row=1, padx=10, pady=10)

    root.withdraw()
    ask_for_upc_window.wait_window(ask_for_upc_window)

    return upc_search(lpn, upc.get())



def change_truck_file():
    change_truck_file_window = tk.Toplevel(root)
    change_truck_file_window.geometry("420x120")
    change_truck_file_frame = ttk.Frame(change_truck_file_window)
    change_truck_file_frame.grid(column=0, row=0, sticky='nsew')
    change_truck_file_frame.focus_set()
    # Create a label and entry widget for asin input
    truck_number_label = ttk.Label(change_truck_file_frame, text="Enter Truck Number:")
    truck_number_label.grid(column=0, row=0, padx=10, pady=10)
    truck_number_entry = ttk.Entry(change_truck_file_frame)
    truck_number_entry.grid(column=1, row=0, padx=10, pady=10)

    def submit():
        global truck_items
        """Submit: Submits the Truck Number"""
        truck_number = truck_number_entry.get()
        truck_items = f"EL_Load_{truck_number}.csv"
        truck_items_label_text.set(f"TRUCK FILE: {truck_items}")
        change_truck_file_window.destroy()

        return

    submit_button = ttk.Button(change_truck_file_frame, text="Submit", command=submit)
    submit_button.grid(column=1, row=1, padx=10, pady=10)
    change_truck_file_frame.lift()
    truck_number_entry.focus()


def change_category():
    """no_asin_funct: creates the new asin tab that takes in the lpn and the category it should go in"""
    change_category_window = tk.Toplevel(root)
    change_category_window.geometry("350x100")
    change_category_frame = ttk.Frame(change_category_window)
    change_category_frame.grid(column=0, row=0, sticky='nsew')
    change_category_frame.focus_set()
    # Create a label and entry widget for asin input
    change_category_label2 = ttk.Label(change_category_frame, text="Scan Category:")
    change_category_label2.grid(column=0, row=0, padx=10, pady=10)
    change_category_entry2 = ttk.Entry(change_category_frame)
    change_category_entry2.grid(column=1, row=0, padx=10, pady=10)

    import os

    def on_category_enter():

        category = change_category_entry2.get()
        asin = re.sub(r'^ASIN: ', '', asin_label_text.get())
        upc = ''
        price = ''
        product_name = ''
        old_category = ''

        # Changes the category of the product in the truck load file
        temp_file = truck_folder + 'temp.csv'
        with open(truck_folder + truck_items, 'r', newline='', encoding='utf-8') as truck_load, open(temp_file, 'w',
                                                                                                     newline='',
                                                                                                     encoding='utf-8') as temp_truck:
            reader = csv.reader(truck_load)
            writer = csv.writer(temp_truck)
            for row in reader:
                if row[0] == lpn:
                    old_category = row[5]
                    updated_row = [lpn, row[1], asin, row[3], row[4], category]
                    upc = row[1]
                    product_name = row[3]
                    price = row[4]
                    writer.writerow(updated_row)
                else:
                    writer.writerow(row)

        # Close both truck_load and temp_truck files
        truck_load.close()
        temp_truck.close()

        os.remove(truck_folder + truck_items)
        os.rename(temp_file, truck_folder + truck_items)
        # Changes the category of the product in the input file
        temp_file = csv_file_location + 'temp.csv'
        with open(csv_file_location + 'input.csv', 'r', newline='', encoding='utf-8') as input_file, open(temp_file,
                                                                                                          'w',
                                                                                                          newline='',
                                                                                                          encoding='utf-8') as temp_input:
            reader = csv.reader(input_file)
            writer = csv.writer(temp_input)
            for row in reader:
                if row[1] == asin:
                    row = [category, asin, upc, product_name, price]
                writer.writerow(row)

        os.remove(csv_file_location + 'input.csv')
        os.rename(temp_file, csv_file_location + 'input.csv')

        # Removes the row the product was on for the given file
        for name in file_name:
            file_path = pallet_folder + file_name[name]
            if not os.path.isfile(file_path):
                continue
            temp_file = pallet_folder + 'temp.csv'
            with open(file_path, 'r', newline='', encoding='utf-8') as label_file, open(temp_file, 'w', newline='',
                                                                                        encoding='utf-8') as temp_label:
                reader = csv.reader(label_file)
                writer = csv.writer(temp_label)
                for row in reader:
                    if row[0] == lpn:
                        # Remove the old entry only if the old category is different from the new one
                        if old_category != category:
                            continue
                        row = [lpn, upc, asin, product_name, price, category]
                    writer.writerow(row)

            os.remove(file_path)
            os.rename(temp_file, file_path)

        # Sets the new category in the new file
        if label_names.__contains__(category):
            with open(pallet_folder + file_name[category], 'a', encoding='utf-8', newline='') as write_file:
                write_file_writer = csv.writer(write_file)
                row_values = [lpn, upc, asin, product_name, price, category]
                write_file_writer.writerow(row_values)

        pallet_label_text.set(f"PALLET: {category}")
        change_category_window.destroy()
        return

    change_category_entry2.bind("<Return>", on_category_enter)

    def submit():
        """submit: submits the asin and category location"""
        on_category_enter()

    submit_button = ttk.Button(change_category_frame, text="Submit", command=submit)
    submit_button.grid(column=1, row=2, padx=10, pady=10)
    change_category_frame.lift()
    change_category_entry2.focus()

    return


def open_options():
    """open_options: Creates the New Pallet GUI screen and the logic behind it. Creates two tabs 'New Pallet'
     and 'Change Pallet' in which you can either create a new pallet by selecting a new type of pallet and
     setting the new pallet number or pick from an existing pallet that is in the same directory as this code"""
    options_window = tk.Toplevel(root)
    options_window.title("Change Pallet")
    options_window.geometry("500x200")
    font = ("Helvetica", 18)

    # create Notebook widget with two tabs
    notebook = ttk.Notebook(options_window)

    # create "New Pallet" tab
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="New Pallet")

    # create widgets for "New Pallet" tab
    number_label = ttk.Label(tab1, text="Enter number:")
    number_label.grid(column=0, row=0, padx=10, pady=10)

    pallet_number = ttk.Entry(tab1, font=font)
    pallet_number.grid(column=1, row=0, padx=10, pady=10)

    # create dropdown menu for quantity selection
    pallet_type = tk.StringVar(value="None")
    quantity_label = ttk.Label(tab1, text="Select Type:")
    quantity_label.grid(column=0, row=1, padx=10, pady=10)
    quantity_dropdown = ttk.Combobox(tab1, textvariable=pallet_type,
                                     values=label_names,
                                     state="readonly",
                                     font=font)
    quantity_dropdown.grid(column=1, row=1, padx=10, pady=10)

    # create submit button
    def submit_options():
        """submit_options: grabs pallet number and type to create a new pallet"""
        pallet_number_var = pallet_number.get()
        pallet_type_var = pallet_type.get()
        file_creator(pallet_number_var, pallet_type_var)

    submit_button = ttk.Button(tab1, text="Submit", command=submit_options)
    submit_button.grid(column=1, row=2, padx=10, pady=10)

    # create "Existing Pallet" tab
    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text="Existing Pallet")
    directory = pallet_folder

    def update_file_dropdown(event):
        """update_file_dropdown: Updates the file dropdown in the Existing Pallet tab to reflect the selected pallet
        type"""
        selected_filetype = filetype_dropdown.get()
        # filter the list of CSV files based on the selected file type
        csv_files = [f for f in os.listdir(directory) if
                     os.path.isfile(os.path.join(directory, f)) and f.endswith('.csv') and f.startswith(
                         selected_filetype)]
        file_dropdown['values'] = csv_files
        file_dropdown.set("None")

    # create StringVar variables for the selected file type and file
    file_var = tk.StringVar(value="None")
    file_var2 = tk.StringVar(value="None")

    # create a label and dropdown for the file type
    filetype_label = ttk.Label(tab2, text="Select file type:")
    filetype_label.grid(column=0, row=0, padx=10, pady=10)

    filetype_dropdown = ttk.Combobox(tab2, textvariable=file_var2,
                                     values=label_names,
                                     font=font, state="readonly")
    filetype_dropdown.grid(column=1, row=0, padx=10, pady=10)

    # bind the update_file_dropdown function to the file type dropdown
    filetype_dropdown.bind("<<ComboboxSelected>>", update_file_dropdown)

    # create a label and dropdown for the file
    file_label = ttk.Label(tab2, text="Select file:")
    file_label.grid(column=0, row=1, padx=10, pady=10)

    file_dropdown = ttk.Combobox(tab2, textvariable=file_var, font=font, state="readonly")
    file_dropdown.grid(column=1, row=1, padx=10, pady=10)

    # create submit button for file and quantity selection
    def submit_file():
        """submit_file: takes the file that was selected and sets it so the user can populate it"""
        selected_file = file_dropdown.get()
        pallet_type = filetype_dropdown.get()
        file_changer(selected_file, pallet_type)

    file_button = ttk.Button(tab2, text="Submit", command=submit_file)
    file_button.grid(column=1, row=2, padx=10, pady=10)

    notebook.pack(expand=1, fill="both")


"""def undone():
    # TODO[]: set_product_to_category(lpn)?
    yesno = messagebox.askyesno(title="NO ASIN FOUND", message="Does this product have a UPC?")

    if yesno:
        upc_found_tf = ask_for_upc(lpn)
        if upc_found_tf:
            return
    else:
        ask_for_category(lpn)
        return"""


def no_asin_funct():
    """no_asin_funct: creates the new asin tab that takes in the lpn."""

    def on_lpn_enter2(event=None):
        """on_lpn_enter2: checks if the lpn entry field is a lpn."""
        if lpn_entry2.get().startswith("L"):
            set_product_to_category(lpn_entry2.get())
            no_asin_window.destroy()
        else:
            lpn_entry2.delete(0, tk.END)
            lpn_entry2.focus()

    root = tk.Tk()  # You need to create the root window, unless you have it defined elsewhere
    no_asin_window = tk.Toplevel(root)
    no_asin_window.geometry("350x100")
    no_asin_frame = ttk.Frame(no_asin_window)
    no_asin_frame.grid(column=0, row=0, sticky='nsew')
    no_asin_frame.focus_set()

    # Create a label and entry widget for LPN input
    asin_label = ttk.Label(no_asin_frame, text="Enter LPN:")
    asin_label.grid(column=0, row=0, padx=10, pady=10)
    lpn_entry2 = ttk.Entry(no_asin_frame)
    lpn_entry2.grid(column=1, row=0, padx=10, pady=10)

    lpn_entry2.bind("<Return>", on_lpn_enter2)

    def submit():
        """submit: submits the LPN"""
        on_lpn_enter2()

    submit_button = ttk.Button(no_asin_frame, text="Submit", command=submit)
    submit_button.grid(column=1, row=1, padx=10, pady=10)
    root.withdraw()  # Hide the root window
    no_asin_frame.lift()
    lpn_entry2.focus()


# 'fold' is just so I can collapse this section of code for my own sake, can be taken out later
fold = True
if fold:
    root = tk.Tk()
    root.title("ASIN Search")
    root.attributes('-fullscreen', True)
    font = ("Helvetica", 18)
    # Create main_frame to hold all other widgets
    main_frame = ttk.Frame(root)
    main_frame.grid(column=0, row=0, sticky='nsew')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    for i in range(20):
        main_frame.columnconfigure(i, weight=1)
        main_frame.rowconfigure(i, weight=1)

    title_label_text = tk.StringVar(value="")
    price_label_text = tk.StringVar(value="")
    asin_label_text = tk.StringVar(value="")
    pallet_label_text = tk.StringVar(value="")
    truck_items_label_text = tk.StringVar(value="")

    style = ttk.Style()
    style.configure("TLabel", font=("Helvetica", 18))  # Adjust the font size for labels
    style.configure("TEntry", font=("Helvetica", 18))  # Adjust the font size for entry fields
    style.configure("TButton", font=("Helvetica", 18))  # Adjust the font size for buttons
    style.configure("TCombobox", font=("Helvetica", 18))  # Adjust the font size for combo boxes
    style.configure("TNotebook.Tab", font=("Helvetica", 18))  # Adjust the font size for notebook tabs

    # create frames
    label_frame = ttk.Frame(main_frame, padding=10, relief="groove")
    label_frame.grid(column=0, row=4, rowspan=10, padx=10, pady=10, columnspan=3, sticky='w')
    # create labels and entry fields
    asin_label = ttk.Label(main_frame, text="Enter ASIN:")
    asin_label.grid(column=0, row=0, padx=10, pady=10)
    # create a scrolling frame
    label3_frame = ttk.Frame(main_frame, padding=10, relief="groove", borderwidth=2)
    label3_frame.grid(column=5, row=1, rowspan=80, padx=10, pady=10, sticky='w')

    truck_items_frame = ttk.Frame(main_frame, padding=10, relief="groove", borderwidth=2, width=850)
    truck_items_frame.grid(column=5, row=0, padx=10, pady=10, sticky='w')

    canvas = Canvas(label3_frame, width=850, height=800)
    scrollable_frame = ttk.Frame(canvas, width=850, height=800)
    scrollbar = Scrollbar(label3_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    labels = {name: tk.StringVar(value="") for name in label_names}


    def complete_pallet_callback(item_name_callback):
        return lambda: complete_pallet(item_name_callback)


    new_items = [(item[0], tk.StringVar(value="")) for item in labels]
    for i, (item_name, item_label) in enumerate(labels.items(), start=1):
        button = ttk.Button(
            scrollable_frame,
            text="Complete",
            command=complete_pallet_callback(item_name)
        )
        button.grid(column=0, row=i, padx=1, pady=1, sticky='w')

        label = ttk.Label(scrollable_frame, textvariable=item_label)
        label.grid(column=1, row=i, padx=1, pady=1, sticky='w')

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # add labels to label_frame
    fixed_width = 45

    truck_name_label = ttk.Label(truck_items_frame, textvariable=truck_items_label_text)
    truck_name_label.grid(column=1, row=0, padx=10, pady=10, sticky='w')

    change_truck_button = ttk.Button(truck_items_frame, text="Change Truck", command=change_truck_file)
    change_truck_button.grid(column=0, row=0, padx=10, pady=10)

    title_label = ttk.Label(label_frame, textvariable=title_label_text, anchor="w", width=fixed_width)
    title_label.grid(column=0, row=0, padx=5, pady=5, columnspan=15, sticky='w')

    price_label = ttk.Label(label_frame, textvariable=price_label_text, anchor="w", width=fixed_width)
    price_label.grid(column=0, row=1, padx=5, pady=5, columnspan=15, sticky='w')

    asin_label = ttk.Label(label_frame, textvariable=asin_label_text, anchor="w", width=fixed_width)
    asin_label.grid(column=0, row=2, padx=5, pady=5, columnspan=15, sticky='w')

    pallet_label = ttk.Label(label_frame, textvariable=pallet_label_text, width=fixed_width, font=("Helvetica", 18),
                             relief="solid")
    pallet_label.grid(column=0, row=4, padx=5, pady=50, columnspan=35)

    undo_button = ttk.Button(label_frame, text="Undo/Wrong Item", command=undo)
    undo_button.grid(column=0, row=5, padx=1, pady=1)

    change_category_button = ttk.Button(label_frame, text="Change Category", command=change_category)
    change_category_button.grid(column=1, row=5, padx=1, pady=1)

    asin_entry = ttk.Entry(main_frame, font=font)
    asin_entry.grid(column=1, row=0, padx=5, pady=5)
    asin_entry.bind("<Return>", on_asin_enter)

    lpn_label = ttk.Label(main_frame, text="Enter LPN:")
    lpn_label.grid(column=0, row=1, padx=5, pady=5)

    lpn_entry = ttk.Entry(main_frame, font=font)
    lpn_entry.grid(column=1, row=1, padx=5, pady=5)
    lpn_entry.bind("<Return>", on_lpn_enter)

    search_button = ttk.Button(main_frame, text="Search", command=search_asin)
    search_button.grid(column=2, row=0, padx=1, pady=1)

    options_button = ttk.Button(main_frame, text="Change Pallet", command=open_options)
    options_button.grid(column=2, row=1, padx=1, pady=1)

    no_asin_button = ttk.Button(main_frame, text="No ASIN", command=no_asin_funct)
    no_asin_button.grid(column=2, row=2, padx=1, pady=1)

    quit_button = ttk.Button(main_frame, text="Quit", command=save_current_file_setup)
    quit_button.grid(column=2, row=3, padx=1, pady=1)

    title_label_text.set("TITLE:")
    price_label_text.set("PRICE:")
    asin_label_text.set("ASIN:")
    pallet_label_text.set("PALLET:")
    truck_items_label_text.set("TRUCK FILE:")
    load_file_setup()
    root.mainloop()

