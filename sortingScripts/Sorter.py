import csv
import os
import tkinter as tk
from tkinter import messagebox,Scrollbar, Canvas
from tkinter import ttk
from ttkthemes import ThemedTk
import Subcategory_checker
import asinFinder

#TODO:[] Add a function to save what file you left off on
#TODO:[] Lookup UPC searching API and if that would work for category

truck_number = ''
truck_items = ''
label_names = [
    "over75", "under75","keyboards_mice_g_headphones", "keyboards_mice_under", "g_headphones_under",
    "earbuds_selected", "earbuds_not_selected", "modems"
]

#TODO:[x] Update all_pallet_names to have all of the product catigories sorted
all_pallet_names = ["over75", "under75","keyboards_mice_g_headphones", "keyboards_mice_under", "g_headphones_under",
    "earbuds_selected", "earbuds_not_selected", "modems","Drawing Tablets/Portable Monitors","Graphics Cards",
    "Power Supplies","Motherboards","Ram","SSD","Cameras","Audio Products","Gaming Systems","NAS","Hard Drives",
    "Mini Computers","Watches","Phone/Tablet Cases","Apple Accessories","PCIE Cards","Phones/Tablets", "Headphone","Laptop",]

Categories = ["Miscellaneous","Keyboard", "Mice", "Gaming Headphone","Earbuds", "Modem","Thermostat",
    "Drawing Tablet/Portable Monitor","Graphics Card","Power Supply","Motherboard","Ram",
    "Solid State Drive","Camera","Audio Product","Gaming System","NAS","Hard Drive","Mini Computer","Smart Watch","Case",
    "Apple Accessory","PCIE Card","Phone","Tablet", "Headphone","Laptop","Chromebook","Switch","Docking Station",
    "Lock","Router","CPU","Microphone","CPU Cooler","Monitor","Desktop","Keyboard Folio"]

file_name = {name: name for name in label_names}

def set_undefined():
    for name in label_names:
        labels[name].set(value=name.upper() + ": "+name+"_0")
        print(file_name[name])

def file_creator(pallet_number, pallet_type):
    if label_names.__contains__(pallet_type):
        new_file_name = f"{pallet_type}_{pallet_number}.csv"
        if os.path.exists(new_file_name):
            messagebox.showerror(title="Not Valid",message=f"The file:{new_file_name} already exists")
            return
        file_name[pallet_type] = new_file_name+".csv"
        print(file_name[pallet_type])
        labels[pallet_type].set(value=pallet_type.upper() + ": "+new_file_name)
    else:
        messagebox.showerror(title="Not Valid",message="This file name is not valid")
    return

def file_changer(found_file_name,pallet_type):
    file_name[pallet_type] = found_file_name
    labels[pallet_type].set(value=pallet_type.upper() + ": "+found_file_name)
    
    #messagebox.showerror(title="NO FILE",message="This file does not exist")
        
    return


#TODO:[x] Update the csv file that is taken in and outputted to have the product category information 
def search_asin(*args):
    global title_label, price_label, asin_label, pallet_label
    for name in label_names:
        #! Fix this, does not work correctly in currect state
        if labels[name].get == name + '_0':
            messagebox.showerror(title="No Pallet Selected",message="Please select pallets")
            return
    
    os.system('cls' if os.name == 'nt' else 'clear')
    asin = asin_entry.get()
    lpn = lpn_entry.get()
    asin_found = False
    with open('KnownBinItems','r',encoding='utf-8') as csvfile:
         reader = csv.DictReader(csvfile)
         for row in reader:
             if row["Asin"] == asin:
                asin_found = True
                item_desc = row['ItemDesc'].replace(',', '')
                upc = row['UPC']
                price = float(row['Total Price'].replace(',', '').replace('$', ''))
                title_label_text.set("TITLE: {}".format(item_desc))
                price_label_text.set("PRICE: {}".format(price))
                asin_label_text.set("ASIN: {}".format(asin))
                category = Subcategory_checker.checker.category_finder(asin)
                with open(file_name['under75'], 'a', encoding='utf-8', newline='') as under_75_file,\
                    open(truck_items,'a', encoding='utf-8', newline='') as truck_items_file:
                    under_75_writer = csv.writer(under_75_file)
                    #! Find what category the product is and put it below in the Misc section
                    row_values = [lpn, upc,row['Asin'], item_desc, price,category]
                    under_75_writer.writerow(row_values)
                    truckload_file_write(row_values)
                    pallet_label_text.set("PALLET: Under 75")
                clear_fields()
                return
    # open input file and search for ASIN
    
    #* g-headsets over 150 go to high keyboard,mice,headset, 75-150 go to the auction pallet, under 75 go to low misc
    #* earbuds select go to a box, earbuds non-select go to a box
    #* mice over 75 go to high headsets, under 75 go to low misc
    #* phone/tablet cases go to own box
    #* keyboards over 150 go to high keyboard/mice/headset, 75-150 go to the keyboards auction pallet, under 75 go to low misc
    #* bin routers gos in modems pallet, take from csv sheet that checks for these products
    #TODO:[x] Impliment the system to change truckloads and csv file for all in that truckload
    
    
    with open('input.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Asin'] == asin:
                asin_found = True
                # remove commas from item description and display title and price
                item_desc = row['ItemDesc'].replace(',', '')
                upc = row['UPC']
                price = float(row['Total Price'].replace(',', '').replace('$', ''))
                title_label_text.set("TITLE: {}".format(item_desc))
                price_label_text.set("PRICE: {}".format(price))
                asin_label_text.set("ASIN: {}".format(asin))
                # check if price is under or over $75 and write to respective CSV file
                #TODO:[x] Have a separate class called here to check if the asin product belongs to a specific box, check all_pallet_names  
                #checks the sub-category
                category = Subcategory_checker.checker.category_finder(asin)
                special_bin_tf = Subcategory_checker.checker.special_bins_check(asin)
                #? use subcategory_checker.py file to achive this HERE
                
                #looks at price and subcategory_checker.py fuction to see if the item belongs in this pallet
                if price < 75 & special_bin_tf:
                    with open(file_name['under75'], 'a', encoding='utf-8', newline='') as under_75_file:
                        under_75_writer = csv.writer(under_75_file)
                        
                        row_values = [lpn,upc, row['Asin'], item_desc, price,category]
                        under_75_writer.writerow(row_values)
                        truckload_file_write(row_values)
                        pallet_label_text.set("PALLET: Under 75") 
                    
                else:
                    #TODO:[x] Make a function to return if the item is misc or if it belongs in a certain box
                    #? use subcategory_checker.py file to achive this HERE
                    sorting_category_tf = Subcategory_checker.checker.sorting_category_check(asin)
                    
                    if sorting_category_tf:
                        #figureout what pallet to put it into
                        if label_names.__contains__(category):
                            with open(file_name[category], 'a', encoding='utf-8', newline='') as cat_file:
                                cat_file_writer = csv.writer(cat_file)
                                row_values = [lpn, upc,row['Asin'], item_desc, price,category]
                                truckload_file_write(row_values)
                                cat_file_writer.writerow(row_values)
                                pallet_label_text.set(f"PALLET: {category}") 
                        else:
                            row_values = [lpn,asin,upc, item_desc, price,category]
                            truckload_file_write(row_values)
                            pallet_label_text.set(f"PALLET: {category}") 
                                
                    else:
                        #this is the misc over 75 pallet
                        with open(file_name['over75'], 'a', encoding='utf-8', newline='') as over_75_file:
                            over_75_writer = csv.writer(over_75_file)
                            row_values = [lpn, upc,row['Asin'], item_desc, price]
                            truckload_file_write(row_values)
                            over_75_writer.writerow(row_values)
                            pallet_label_text.set("PALLET: Over 75")
                    
                clear_fields()
                return
            
    #TODO:[] If asin is not found, it should search the internet for the information
    if not asin_found:
        row_val = asinFinder.asin_lookup(asin) #[found_TF,name,price,upc]
        if not(row_val[0]):
            yesno = messagebox.askyesno(title="NO ASIN FOUND",message="Does this product have a UPC?")
            #TODO:[x] Get UPC from user
            if yesno:
                upc_found_tf = ask_for_upc(lpn)
                if upc_found_tf:
                    return
            #TODO:[] if upc is not given/not found, what to do
            #TODO:[] Scan Category gui 
        else:
            #if asinFinder found the asin
            
            with open(file_name[category], 'a', encoding='utf-8', newline='') as cat_file:
                cat_file_writer = csv.writer(cat_file)
                row_values = [lpn, upc,row['Asin'], item_desc, price,category]
                truckload_file_write(row_values)
                cat_file_writer.writerow(row_values)
                pallet_label_text.set(f"PALLET: {category}") 
            
            
        #! Most of this code below will NOT be reused  
        #? need something like this twice I think, once for if the item has no upc and another for if the UPC is not found
        #? (might do something else with it like call set_product_to_category)
        title_label_text.set("TITLE: N/A")
        price_label_text.set("PRICE: N/A")
        asin_label_text.set("ASIN: {}".format(asin))
        with open(under75, 'a', encoding='utf-8', newline='') as under_75_file, \
            open(over75, 'a', encoding='utf-8', newline='') as over_75_file:
            under_75_writer = csv.writer(under_75_file)
            over_75_writer = csv.writer(over_75_file)
            if yesno:
                row_values = [lpn, asin, "N/A", "N/A"]
                over_75_writer.writerow(row_values)
                truckload_file_write(row_values)
                pallet_label_text.set("PALLET: over 75")
                
            else:
                row_values = [lpn, asin, "N/A", "N/A"]
                under_75_writer.writerow(row_values)
                truckload_file_write(row_values)
                pallet_label_text.set("PALLET: under 75")
    return

def truckload_file_write(row_values):
    with open(truck_items,'a', encoding='utf-8', newline='') as truck_items_file:
        truck_items_writer = csv.writer(truck_items_file)
        truck_items_writer.writerow(row_values)

#TODO:[] Write the new asin to the input file if it finds the information using the UPC
def upc_search(lpn,upc):
    upc_found = False
    with open('input.csv', 'r', encoding='utf-8') as csvfile:
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
                #TODO:[x] Have a separate class called here to check if the asin product belongs to a specific box, check all_pallet_names  
                #checks the sub-category
                category = Subcategory_checker.checker.category_finder(asin)
                special_bin_tf = Subcategory_checker.checker.special_bins_check(asin)
                #? use subcategory_checker.py file to achive this HERE
                
                #looks at price and subcategory_checker.py fuction to see if the item belongs in this pallet
                if price < 75 & special_bin_tf:
                    with open(file_name['under75'], 'a', encoding='utf-8', newline='') as under_75_file:
                        under_75_writer = csv.writer(under_75_file)
                        row_values = [lpn, row['Asin'],upc, item_desc, price,category]
                        truckload_file_write(row_values)
                        under_75_writer.writerow(row_values)
                        pallet_label_text.set("PALLET: Under 75") 
                    
                else:
                    #TODO:[x] Make a function to return if the item is misc or if it belongs in a certain box
                    #? use subcategory_checker.py file to achive this HERE
                    sorting_category_tf = Subcategory_checker.checker.sorting_category_check(asin)
                    
                    if sorting_category_tf:
                        #figureout what pallet to put it into
                        if label_names.__contains__(category):
                            with open(file_name[category], 'a', encoding='utf-8', newline='') as cat_file:
                                cat_file_writer = csv.writer(cat_file)
                                row_values = [lpn,asin,upc, item_desc, price,category]
                                truckload_file_write(row_values)
                                cat_file_writer.writerow(row_values)
                                pallet_label_text.set(f"PALLET: {category}") 
                        else:
                            row_values = [lpn,asin,upc, item_desc, price,category]
                            truckload_file_write(row_values)
                            pallet_label_text.set(f"PALLET: {category}") 
                    else:
                        #this is the misc over 75 pallet
                        with open(file_name['over75'], 'a', encoding='utf-8', newline='') as over_75_file:
                            over_75_writer = csv.writer(over_75_file)
                            row_values = [lpn, asin,upc, item_desc, price,category]
                            truckload_file_write(row_values)
                            over_75_writer.writerow(row_values)
                            pallet_label_text.set("PALLET: Over 75")
                    
                clear_fields()
    return upc_found               

def set_product_to_category(lpn):
    #TODO:[] make this take in a category and automatically set that product to the given category 
    #TODO:[x] make it ask for UPC to see if we can find the product
    #? Do i need this method if I am putting in separate classes for all of the csv files needed
    yesno = messagebox.askyesno(title="NO ASIN FOUND",message="Does this product have a UPC?")
    
    if yesno:
        #TODO:[x] Get UPC from user
        upc_found_tf = ask_for_upc(lpn)
        if upc_found_tf:
            return
        else:
            row_values = [lpn,"N/A","N/A","N/A","N/A",category_name]
    else:
        row_values = [lpn,"N/A","N/A","N/A","N/A",category_name]
    
            
    return
    
def complete_pallet(pallet_name):
    #TODO:[] take the pallet_name and count it up one and set it to a new csv file
    tf_mistake = messagebox.askokcancel(title="Create New Box/Pallet",message=f"Are you sure you want to create a new Pallet/Box for: {pallet_name}")
    if tf_mistake:
        print(pallet_name)
        file_creator(pallet_name,-1)
    return

def undo():
    #TODO:[] make this so when the undo button is pressed it will undo the last function, wether that be hitting complete on the complete_pallet or scanned the wrong product or scanned the wrong category when no asin was found
    return


def clear_fields():
    """clear_fields: clears the asin and lpn entry fields in the gui"""
    asin_entry.delete(0, tk.END)
    lpn_entry.delete(0, tk.END)

def on_asin_enter(*args):
    """on_asin_enter: checks if the asin entry field is an asin"""
    if asin_entry.get().startswith("B"):
        lpn_entry.focus()
    else:
        asin_entry.delete(0, tk.END)
        asin_entry.focus
    
def on_lpn_enter(*args):
    """on_lpn_enter: checks if the lpn entry field is an lpn and calls search_asin function."""
    if lpn_entry.get().startswith("L"):
        search_asin() #searches 
        asin_entry.focus()
    else:
        lpn_entry.delete(0, tk.END)
        lpn_entry.focus
        
def ask_for_upc(lpn):
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
        #TODO:[] Fix to make this work like a submit button
        upc = upc_entry.get()
        ask_for_upc_window.destroy()
        
        return upc_search(lpn,upc)

    submit_button = ttk.Button(ask_for_upc_frame, text="Submit", command=submit)
    submit_button.grid(column=1, row=1, padx=10, pady=10)
    ask_for_upc_frame.lift()
    upc_entry.focus()

def open_options():
    """open_options: Creates the New Pallet GUI screen and the logic behind it. Creates two tabs 'New Pallet'
     and 'Change Pallet' in which you can either create a new pallet by selecting a new type of pallet and 
     setting the new pallet number or pick from a an existing pallet that is in the same directory as this code"""
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
        file_creator(pallet_number_var,pallet_type_var)

    submit_button = ttk.Button(tab1, text="Submit", command=submit_options)
    submit_button.grid(column=1, row=2, padx=10, pady=10)

    # create "Existing Pallet" tab
    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text="Existing Pallet")
    directory = "./csv_files"

    def update_file_dropdown(*args):
        """update_file_dropdown: Updates the file dropdown in the Existing Pallet tab to reflect the selected pallet type"""
        selected_filetype = filetype_dropdown.get()
        # filter the list of CSV files based on the selected file type
        csv_files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith('.csv') and f.startswith(selected_filetype)]
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
        file_changer(selected_file,pallet_type)

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
    
    def on_lpn_enter2(*args):
        """on_lpn_enter2: checks if the lpn entry field is an lpn."""
        if lpn_entry2.get().startswith("L"):
            set_product_to_category(lpn_entry2.get())
            no_asin_window.destroy()
        else:
            lpn_entry2.delete(0, tk.END)
            lpn_entry2.focus() 
    
    
    lpn_entry2.bind("<Return>", on_lpn_enter2) 
    

    def submit():
        """submit: submits the asin and category location"""
        #TODO:[x] Fix to make this work like a submit button
        on_lpn_enter2()

    submit_button = ttk.Button(no_asin_frame, text="Submit", command=submit)
    submit_button.grid(column=1, row=2, padx=10, pady=10)
    no_asin_frame.lift()
    lpn_entry2.focus()

#'fold' is just so i can collapse this section of code for my own sake, can be taken out later
fold = True
if fold:
    root = tk.Tk()
    root.title("ASIN Search")
    root.attributes('-fullscreen', False)
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

    style = ttk.Style()
    style.configure("TLabel", font=("Helvetica", 18))  # Adjust the font size for labels
    style.configure("TEntry", font=("Helvetica", 18))  # Adjust the font size for entry fields
    style.configure("TButton", font=("Helvetica", 18))  # Adjust the font size for buttons
    style.configure("TCombobox", font=("Helvetica", 18))  # Adjust the font size for comboboxes
    style.configure("TNotebook.Tab", font=("Helvetica", 18))  # Adjust the font size for notebook tabs

    # create frames
    label_frame = ttk.Frame(main_frame, padding=10, relief="groove")
    label_frame.grid(column=0, row=5, rowspan=10, padx=10, pady=10,columnspan=3,sticky='w')
    # create labels and entry fields
    asin_label = ttk.Label(main_frame, text="Enter ASIN:")
    asin_label.grid(column=0, row=0, padx=10, pady=10)
    # create a scrolling frame
    label3_frame = ttk.Frame(main_frame, padding=10, relief="groove", borderwidth=2, width=600, height=600)
    label3_frame.grid(column=5, row=0, rowspan=80, padx=10, pady=10, sticky='w')

    canvas = Canvas(label3_frame, width=850, height=1500)  
    scrollable_frame = ttk.Frame(canvas, width=850, height=1500)
    scrollbar = Scrollbar(label3_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    labels = {name: tk.StringVar(value="") for name in label_names}


    def complete_pallet_callback(item_name):
        return lambda: complete_pallet(item_name)
    new_items = [(item[0], tk.StringVar(value="")) for item in labels]
    for i, (item_name, item_label) in enumerate(labels.items()):

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

    #TODO:[] Create field to submit a new truckload number and have it displayed at the top
    
    title_label = ttk.Label(label_frame, textvariable=title_label_text,anchor="w", width=fixed_width)
    title_label.grid(column=0, row=0, padx=5, pady=5,columnspan=15,sticky='w')

    price_label = ttk.Label(label_frame, textvariable=price_label_text,anchor="w", width=fixed_width)
    price_label.grid(column=0, row=1, padx=5, pady=5,columnspan=15,sticky='w')

    asin_label = ttk.Label(label_frame, textvariable=asin_label_text,anchor="w", width=fixed_width)
    asin_label.grid(column=0, row=2, padx=5, pady=5,columnspan=15,sticky='w')

    pallet_label = ttk.Label(label_frame, textvariable=pallet_label_text, width=fixed_width, font=("Helvetica", 18),relief="solid")
    pallet_label.grid(column=2, row=4, padx=5, pady=50,columnspan=35)

    asin_entry = ttk.Entry(main_frame, font=font)
    asin_entry.grid(column=1, row=0, padx=10, pady=10)
    asin_entry.bind("<Return>", on_asin_enter)

    lpn_label = ttk.Label(main_frame, text="Enter LPN:")
    lpn_label.grid(column=0, row=1, padx=10, pady=10)

    lpn_entry = ttk.Entry(main_frame,font=font)
    lpn_entry.grid(column=1, row=1, padx=10, pady=10)
    lpn_entry.bind("<Return>", on_lpn_enter)

    search_button = ttk.Button(main_frame, text="Search", command=search_asin)
    search_button.grid(column=2, row=0, padx=10, pady=10)

    options_button = ttk.Button(main_frame, text="Change Pallet", command=open_options)
    options_button.grid(column=2, row=1, padx=10, pady=10)

    no_asin_button = ttk.Button(main_frame, text="No ASIN", command=no_asin_funct)
    no_asin_button.grid(column=2, row=2, padx=10, pady=10)

    quit_button = ttk.Button(main_frame, text="Quit", command=main_frame.quit)
    quit_button.grid(column=2, row=3, padx=10, pady=10)


    title_label_text.set("TITLE:")
    price_label_text.set("PRICE:")
    asin_label_text.set("ASIN:")
    pallet_label_text.set("PALLET:")

    root.mainloop()