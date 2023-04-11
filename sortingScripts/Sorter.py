import csv
import os
import tkinter as tk
from tkinter import messagebox, Scrollbar, Canvas
from tkinter import ttk

import Subcategory_checker
import asinFinder

# TODO:[] Add a function to save what file you left off on

csv_file_location = "../csv_files/"
pallet_folder = "../pallets/"
truck_folder = "../truck_items/"
truck_items = ''
lpn = ''
label_names = [
    "over75", "under75", "keyboards_mice_under", "g_headphones_under",
    "earbuds_selected", "earbuds_not_selected", "modems"
]

# TODO:[] Update all_pallet_names to have all of the product categories sorted
all_pallet_names = ["over75", "under75", "keyboards_mice_g_headphones", "keyboards_mice_under", "g_headphones_under",
                    "earbuds_selected", "earbuds_not_selected", "modems", "Drawing Tablets/Portable Monitors",
                    "Graphics Cards", "Power Supplies", "Motherboards", "Ram", "SSD", "Cameras", "Audio Products",
                    "Gaming Systems", "NAS", "Hard Drives", "Mini Computers", "Watches", "Phone/Tablet Cases",
                    "Apple Accessories", "PCIE Cards", "Phones/Tablets", "Headphone", "Laptop"]

Categories = ["Miscellaneous", "Keyboard", "Mice", "Gaming Headphone", "Earbuds", "Modem", "Thermostat",
              "Drawing Tablet/Portable Monitor", "Graphics Card", "Power Supply", "Motherboard", "Ram",
              "Solid State Drive", "Camera", "Audio Product", " Gaming System", "NAS", "Hard Drive", "Mini Computer",
              "Smart Watch", "Case",
              "Apple Accessory", "PCIE Card", "Phone", "Tablet", "Headphone", "Laptop", "Chromebook", "Switch",
              "Docking Station",
              "Lock", "Router", "CPU", "Microphone", "CPU Cooler", "Monitor", "Desktop", "Keyboard Folio"]

file_name = {name: name for name in label_names}


def save_current_file_setup():
    with open(csv_file_location + "saved_files.csv", 'a', encoding='utf-8', newline='') as saved_file_file:
        saved_file_writer = csv.writer(saved_file_file)
        for name in file_name:
            row_values = [name, file_name[name]]
            saved_file_writer.writerow(row_values)
        saved_file_writer.writerow(['truck_items', truck_items])

    main_frame.quit()

    return


def load_saved_file_setup():
    # TODO:[] finish load file and implement
    with open(csv_file_location + "saved_files.csv", 'r', encoding='utf-8', newline='') as saved_file_file:
        return


def set_undefined():
    for name in label_names:
        labels[name].set(value=name.upper() + ": " + name + "_0")
        file_name[name] = (name + ".csv")


def file_creator(pallet_number, pallet_type):
    if label_names.__contains__(pallet_type):
        new_file_name = f"{pallet_type}_{pallet_number}.csv"
        if os.path.exists(new_file_name):
            messagebox.showerror(title="Not Valid", message=f"The file:{new_file_name} already exists")
            return
        file_name[pallet_type] = new_file_name + ".csv"
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


# TODO:[x] Update the csv file that is taken in and outputted to have the product category information 
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
                clear_fields()
                return
    # open input file and search for ASIN

    # * g-headsets over 150 go to high keyboard,mice,headset, 75-150 go to the auction pallet, under 75 go to low misc
    # * earbuds select go to a box, earbuds non-select go to a box
    # * mice over 75 go to high headsets, under 75 go to low misc
    # * phone/tablet cases go to own box
    # * keyboards over 150 go to high keyboard/mice/headset,
    # 75-150 go to the keyboards auction pallet, under 75 go to low misc
    # * bin routers gos in modems pallet, take from csv sheet that checks for these products
    if BOW(asin, lpn):
        return

    if not asin_found:
        row_val = asinFinder.asin_lookup(asin)  # [found_TF,name,price,upc]
        if not (row_val[0]):
            yesno = messagebox.askyesno(title="NO ASIN FOUND", message="Does this product have a UPC?")
            if yesno:
                upc_found_tf = ask_for_upc(lpn)
                if upc_found_tf:
                    return
                else:
                    ask_for_category(lpn)
                    return
            else:
                ask_for_category(lpn)
                return
            # if asinFinder found the asinD
        ask_for_asin_category(lpn, asin, row_val)
    return


def ask_for_asin_category(lpn, asin, row_val):
    ask_category_window = tk.Toplevel(root)
    ask_category_window.geometry("700x300")
    ask_category_frame = ttk.Frame(ask_category_window)
    ask_category_frame.grid(column=0, row=0, sticky='nsew')
    ask_category_frame.focus_set()
    # Create a label and entry widget for asin input
    title = ttk.Label(ask_category_frame, text="Title:")
    title.grid(column=0, row=0, padx=10, pady=10)

    title_name = ttk.Label(ask_category_frame, text=row_val[1])
    title_name.grid(column=1, row=0, padx=10, pady=10)

    price = ttk.Label(ask_category_frame, text="Price:")
    price.grid(column=0, row=1, padx=10, pady=10)

    price_name = ttk.Label(ask_category_frame, text=row_val[2])
    price_name.grid(column=1, row=1, padx=10, pady=10)

    category_entry_label = ttk.Label(ask_category_frame, text="Scan Category:")
    category_entry_label.grid(column=0, row=2, padx=10, pady=10)

    category_entry2 = ttk.Entry(ask_category_frame)
    category_entry2.grid(column=1, row=2, padx=10, pady=10)

    def submit():
        # row_val = [found_TF, name, price, upc]
        """submit: submits the upc entered"""
        category = category_entry2.get()
        ask_category_window.destroy()

        with open(csv_file_location + 'input.csv', 'a+', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            # input.csv = [category, Asin, UPC,ItemDesc,Total Price]
            row = [category, asin, row_val[3], row_val[1], row_val[2]]
            writer.writerow(row)
        return BOW(asin, lpn)

    submit_button = ttk.Button(ask_category_frame, text="Submit", command=submit())
    submit_button.grid(column=1, row=3, padx=10, pady=10)
    ask_category_frame.lift()
    category_entry2.focus()

    return


def BOW(asin, lpn):
    with open(csv_file_location + 'input.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Asin'] == asin:
                if row['Category'] == '':
                    change_category()

                asin_found = True
                # remove commas from item description and display title and price
                item_desc = row['ItemDesc'].replace(',', '')
                upc = row['UPC']
                price = float(row['Total Price'].replace(',', '').replace('$', ''))
                title_label_text.set("TITLE: {}".format(item_desc))
                price_label_text.set("PRICE: {}".format(price))
                asin_label_text.set("ASIN: {}".format(asin))
                # check if price is under or over $75 and write to respective CSV file
                category = Subcategory_checker.Checker.category_finder(asin)
                special_bin_tf = Subcategory_checker.Checker.special_bins_check(asin)
                # ? use subcategory_checker.py file to achieve this HERE

                # looks at price and subcategory_checker.py function to see if the item belongs in this pallet
                if price < 75 or special_bin_tf:
                    row_values = [lpn, upc, row['Asin'], item_desc, price, category]
                    file_writer(row_values, file_name['under75'])

                else:
                    # ? use subcategory_checker.py file to achieve this HERE
                    sorting_category_tf = Subcategory_checker.Checker.sorting_category_check(asin)

                    if sorting_category_tf:
                        # figure what pallet to put it into
                        if label_names.__contains__(category):
                            # pallet that is manifested
                            row_values = [lpn, upc, row['Asin'], item_desc, price, category]
                            file_writer(row_values, file_name[category])
                        else:
                            # pallet that is not manifested
                            row_values = [lpn, upc, asin, item_desc, price, category]
                            truckload_file_write(row_values)
                            pallet_label_text.set(f"PALLET: {category}")
                    else:
                        # this is the misc over 75 pallet
                        row_values = [lpn, upc, row['Asin'], item_desc, price]
                        file_writer(row_values, file_name['over75'])

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
    ask_for_category_window = tk.Toplevel(root)
    ask_for_category_window.geometry("350x120")
    ask_for_category_frame = ttk.Frame(ask_for_category_window)
    ask_for_category_frame.grid(column=0, row=0, sticky='nsew')
    ask_for_category_frame.focus_set()
    # Create a label and entry widget for asin input
    category_label = ttk.Label(ask_for_category_frame, text="Enter Category:")
    category_label.grid(column=0, row=0, padx=10, pady=10)
    category_entry = ttk.Entry(ask_for_category_frame)
    category_entry.grid(column=1, row=0, padx=10, pady=10)

    def submit_category():
        """submit: submits the upc entered"""
        category = category_entry.get()
        ask_for_category_window.destroy()

        return upc_asin_not_found(lpn, category)

    submit_button = ttk.Button(ask_for_category_frame, text="Submit", command=submit_category())
    submit_button.grid(column=1, row=1, padx=10, pady=10)
    ask_for_category_frame.lift()
    category_entry.focus()
    return


# If no ASIN or UPC
def upc_asin_not_found(lpn, category):
    row_values = [lpn, "N/A", "N/A", "N/A", "N/A", category]
    total_price = 0
    num_items = 0

    # If category is a manifest
    if category in label_names:
        # Find the average price of category
        with open(pallet_folder + file_name[category], 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                total_price += float(row[4].replace(',', '').replace('$', ''))
                num_items += 1

        avg_price_of_cat = total_price / num_items
        avg_price_string = f"${avg_price_of_cat}"

        # Set price to avg price, and set name to "Misc"
        row_values = [lpn, "N/A", "N/A", "MISC", avg_price_string, category]

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
    upc_found = False
    with open(csv_file_location + 'input.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['UPC'] == upc:
                upc_found = True
                item_desc = row['ItemDesc'].replace(',', '')
                asin = row['Asin']
                price = float(row['Total Price'].replace(',', '').replace('$', ''))
                title_label_text.set("TITLE: {}".format(item_desc))
                price_label_text.set("PRICE: {}".format(price))
                asin_label_text.set("ASIN: {}".format(asin))
                # check if price is under or over $75 and write to respective CSV file
                # checks the sub-category
                category = Subcategory_checker.Checker.category_finder(asin)
                special_bin_tf = Subcategory_checker.Checker.special_bins_check(asin)
                # ? use subcategory_checker.py file to achieve this HERE

                # looks at price and subcategory_checker.py function to see if the item belongs in this pallet
                if price < 75 & special_bin_tf:
                    row_values = [lpn, upc, row['Asin'], item_desc, price, category]
                    file_writer(row_values, file_name['under75'])
                else:
                    # ? use subcategory_checker.py file to achieve this HERE
                    sorting_category_tf = Subcategory_checker.Checker.sorting_category_check(asin)

                    if sorting_category_tf:
                        # figure what pallet to put it into
                        if label_names.__contains__(category):
                            # pallet that is manifested
                            row_values = [lpn, upc, row['Asin'], item_desc, price, category]
                            file_writer(row_values, file_name[category])
                        else:
                            # pallet that is not manifested
                            row_values = [lpn, upc, asin, item_desc, price, category]
                            truckload_file_write(row_values)
                            pallet_label_text.set(f"PALLET: {category}")
                    else:
                        # this is the misc over 75 pallet
                        row_values = [lpn, upc, row['Asin'], item_desc, price]
                        file_writer(row_values, file_name['over75'])
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
    # TODO:[] take the pallet_name and count it up one and set it to a new csv file
    tf_mistake = messagebox.askokcancel(title="Create New Box/Pallet",
                                        message=f"Are you sure you want to create a new Pallet/Box for: {pallet_name}")
    if tf_mistake:
        print(pallet_name)
        file_creator(pallet_name, -1)
    return


def undo():
    # remove from truckload.csv
    with open(truck_folder + truck_items, 'r') as truck_load, open('temp.csv', 'w', newline='') as output_file:
        reader = csv.reader(truck_load)
        writer = csv.writer(output_file)

        for row in reader:
            if row[0] == lpn:
                continue
            else:
                writer.writerow(row)

    os.remove(truck_items)
    os.rename('temp.csv', truck_items)

    # check if LPN is in any manifest files, if yes remove
    for name in file_name:
        with open(pallet_folder + file_name[name], 'r') as label_file, open('temp.csv', 'w', newline='') as output_file:
            reader = csv.reader(label_file)
            writer = csv.writer(output_file)

            for row in reader:
                if row[0] == lpn:
                    continue
                else:
                    writer.writerow(row)

        os.remove(file_name[name])
        os.rename('temp.csv', file_name[name])

    # go to not found in master.csv
    no_asin_funct()

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
    ask_for_upc_window = tk.Toplevel(root)
    ask_for_upc_window.geometry("350x120")
    ask_for_upc_frame = ttk.Frame(ask_for_upc_window)
    ask_for_upc_frame.grid(column=0, row=0, sticky='nsew')
    ask_for_upc_frame.focus_set()
    # Create a label and entry widget for asin input
    upc_label = ttk.Label(ask_for_upc_frame, text="Enter UPC:")
    upc_label.grid(column=0, row=0, padx=10, pady=10)
    upc_entry = ttk.Entry(ask_for_upc_frame)
    upc_entry.grid(column=1, row=0, padx=10, pady=10)

    def submit():
        """submit: submits the upc entered"""
        upc = upc_entry.get()
        ask_for_upc_window.destroy()

        return upc_search(lpn, upc)

    submit_button = ttk.Button(ask_for_upc_frame, text="Submit", command=submit)
    submit_button.grid(column=1, row=1, padx=10, pady=10)
    ask_for_upc_frame.lift()
    upc_entry.focus()


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
        truck_items = f"EL_Load_{truck_number}"
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

    def on_category_enter():
        # TODO:[x] if item has a category already it will change the category of the item that was previously scanned
        Subcategory_checker.Checker.set_category(change_category_entry2.get(), lpn) # TODO:[] make sure it gets the LPN
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
    directory = "./csv_files"

    def update_file_dropdown():
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


def no_asin_funct():
    """no_asin_funct: creates the new asin tab that takes in the lpn and the category it should go in"""
    no_asin_window = tk.Toplevel(root)
    no_asin_window.geometry("350x100")
    no_asin_frame = ttk.Frame(no_asin_window)
    no_asin_frame.grid(column=0, row=0, sticky='nsew')
    no_asin_frame.focus_set()
    # Create a label and entry widget for asin input
    asin_label = ttk.Label(no_asin_frame, text="Enter LPN:")
    asin_label.grid(column=0, row=0, padx=10, pady=10)
    lpn_entry2 = ttk.Entry(no_asin_frame)
    lpn_entry2.grid(column=1, row=0, padx=10, pady=10)

    def on_lpn_enter2(event):
        """on_lpn_enter2: checks if the lpn entry field is a lpn."""
        if lpn_entry2.get().startswith("L"):
            lpn = lpn_entry2.get()
            no_asin_window.destroy()
            yesno = messagebox.askyesno(title="NO ASIN FOUND", message="Does this product have a UPC?")

            if yesno:
                upc_found_tf = ask_for_upc(lpn)
                if upc_found_tf:
                    return

            ask_for_category(lpn)
            return
        else:
            lpn_entry2.delete(0, tk.END)
            lpn_entry2.focus()

    lpn_entry2.bind("<Return>", on_lpn_enter2)

    def submit():
        """submit: submits the asin and category location"""
        on_lpn_enter2()

    submit_button = ttk.Button(no_asin_frame, text="Submit", command=submit)
    submit_button.grid(column=1, row=2, padx=10, pady=10)
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

    set_undefined()

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
    root.mainloop()
