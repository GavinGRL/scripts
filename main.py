import csv
import os
import tkinter as tk
from tkinter import messagebox,Scrollbar, Canvas
from tkinter import ttk
from ttkthemes import ThemedTk
global under75,over75,gaming_headphones_over,\
    gaming_headphones_under,earbuds_selected,\
    earbuds_not_selected,keyboards_mice,\
    no_asin,all_scanned

under75 = ''
over75 = ''
gaming_headphones_over = ''
gaming_headphones_under = ''
earbuds_selected = ''
earbuds_not_selected = ''
keyboards_mice = ''
no_asin = ''
all_scanned = ''

pallet_names_list = [under75,over75,gaming_headphones_over,
    gaming_headphones_under,earbuds_selected,
    earbuds_not_selected,keyboards_mice,
    no_asin,all_scanned]

for i in range(len(pallet_names_list)):
    pallet_names_list[i] = 'undefined'

def file_creator(pallet_number, pallet_type):
    global under75, over75, over75_label, under75_label
    file_name = f"{pallet_type}_{pallet_number}.csv"
    if os.path.exists(file_name):
        messagebox.showerror(title="Not Valid",message=f"The file:{file_name} already exists")
    elif 'over' in pallet_type:
        over75 = file_name
        over75_label.set(f"over 75: {file_name}")
    elif 'under' in pallet_type:
        under75 = file_name
        under75_label.set(f"under 75: {file_name}")
    else:
        messagebox.showerror(title="Not Valid",message="This file name is not valid")
        
    return

def file_changer(file_name):
    global under75, over75, over75_label, under75_label
    if 'over' in file_name:
        over75 = file_name
        over75_label.set(f"over 75: {file_name}")
    elif 'under' in file_name:
        under75 = file_name
        under75_label.set(f"under 75: {file_name}")
    else:
        messagebox.showerror(title="NO FILE",message="This file does not exist")
        
    return

def search_asin(*args):
    global over75, under75, title_label, price_label, asin_label, pallet_label
    for i in range(len(pallet_names_list)):
        if pallet_names_list[i] == 'undefined':
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
                price = float(row['Total Price'].replace(',', '').replace('$', ''))
                title_label_text.set("TITLE: {}".format(item_desc))
                price_label_text.set("PRICE: {}".format(price))
                asin_label_text.set("ASIN: {}".format(asin))
                with open(under75, 'a', encoding='utf-8', newline='') as under_75_file:
                    under_75_writer = csv.writer(under_75_file)
                    row_values = [lpn, row['Asin'], item_desc, price]
                    under_75_writer.writerow(row_values)
                    pallet_label_text.set("PALLET: Under 75")
                clear_fields()
                return
    # open input file and search for ASIN
    with open('input.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Asin'] == asin:
                asin_found = True
                # remove commas from item description and display title and price
                item_desc = row['ItemDesc'].replace(',', '')
                price = float(row['Total Price'].replace(',', '').replace('$', ''))
                title_label_text.set("TITLE: {}".format(item_desc))
                price_label_text.set("PRICE: {}".format(price))
                asin_label_text.set("ASIN: {}".format(asin))
                # check if price is under or over $75 and write to respective CSV file
                
                #CHANGE FINE NAMES HERE, MAKE SURE TO CHANGE THE ONES IN ASIN_NOTFOUND
                with open(under75, 'a', encoding='utf-8', newline='') as under_75_file:
                        
                    under_75_writer = csv.writer(under_75_file)
                    over_75_writer = csv.writer(over_75_file)
                    if price < 75:
                        row_values = [lpn, row['Asin'], item_desc, price]
                        under_75_writer.writerow(row_values)
                        pallet_label_text.set("PALLET: under 75")
                        
                    else:
                        row_values = [lpn, row['Asin'], item_desc, price]
                        over_75_writer.writerow(row_values)
                        pallet_label_text.set("PALLET: over 75")
                        
                clear_fields()
                return            
    if not asin_found:
        # if ASIN is not found, show error message
        yesno = messagebox.askyesno(title="NO ASIN FOUND",message="Is this item more then $75?")
        
        title_label_text.set("TITLE: N/A")
        price_label_text.set("PRICE: N/A")
        asin_label_text.set("ASIN: {}".format(asin))
        #CHANGE FILE NAMES HERE
        with open(under75, 'a', encoding='utf-8', newline='') as under_75_file, \
            open(over75, 'a', encoding='utf-8', newline='') as over_75_file:
            under_75_writer = csv.writer(under_75_file)
            over_75_writer = csv.writer(over_75_file)
            if yesno:
                row_values = [lpn, asin, "N/A", "N/A"]
                over_75_writer.writerow(row_values)
                pallet_label_text.set("PALLET: over 75")
                
            else:
                row_values = [lpn, asin, "N/A", "N/A"]
                under_75_writer.writerow(row_values)
                pallet_label_text.set("PALLET: under 75")
                
    
    return

def clear_fields():
    asin_entry.delete(0, tk.END)
    lpn_entry.delete(0, tk.END)

def on_asin_enter(*args):
    if asin_entry.get().startswith("B"):
        lpn_entry.focus()
    else:
        asin_entry.delete(0, tk.END)
        asin_entry.focus
    

def on_lpn_enter(*args):
    if lpn_entry.get().startswith("L"):
        search_asin()
        asin_entry.focus()
    else:
        lpn_entry.delete(0, tk.END)
        lpn_entry.focus

def open_options():
    options_window = tk.Toplevel(root)
    options_window.title("Change Pallet")
    options_window.geometry("500x200")
    font = ("Helvetica", 18)

    dropdown_values = ['under_75','over_75','Gaming_Headphones_over','Gaming_Headphones_under',
                        'earbuds_selected','earbuds_not_selected',
                        'keyboards_mice','no_asin','all_scanned']

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
                                      values=dropdown_values, 
                                      state="readonly", 
                                      font=font)
    quantity_dropdown.grid(column=1, row=1, padx=10, pady=10)

    # create submit button
    def submit_options():
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
                                    values=dropdown_values,
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
        selected_file = file_var.get()
        file_changer(selected_file)

    file_button = ttk.Button(tab2, text="Submit", command=submit_file)
    file_button.grid(column=1, row=2, padx=10, pady=10)

    notebook.pack(expand=1, fill="both")

def no_asin_funct():
    no_asin_window = tk.Toplevel(root)
    no_asin_window.geometry("400x200")
    no_asin_frame = ttk.Frame(no_asin_window)
    no_asin_frame.grid(column=0, row=0, sticky='nsew')
    no_asin_frame.focus_set()
    # Create a label and entry widget for asin input
    asin_label = ttk.Label(no_asin_frame, text="Enter LPN:")
    asin_label.grid(column=0, row=0, padx=10, pady=10)
    lpn_entry2 = ttk.Entry(no_asin_frame)
    lpn_entry2.grid(column=1, row=0, padx=10, pady=10)
      

    # Create a label and dropdown menu for selection
    category_label = ttk.Label(no_asin_frame, text="Scan Item Place:")
    category_label.grid(column=0, row=1, padx=10, pady=10)
    category_entry = ttk.Entry(no_asin_frame)
    category_entry.grid(column=1, row=1, padx=10, pady=10)
    
    def on_asin_enter2(*args):
        if lpn_entry2.get().startswith("L"):
            category_entry.focus()
        else:
            lpn_entry2.delete(0, tk.END)
            lpn_entry2.focus() 
    def on_cat_enter(*args):
        if category_entry.get().startswith("LPN"):
            category_entry.delete(0, tk.END)
            category_entry.focus() 
        else:
            set_product_to_category(category_entry.get())
            no_asin_window.destroy()
    
    lpn_entry2.bind("<Return>", on_asin_enter2) 
    category_entry.bind("<Return>", on_cat_enter) 

    # Create a button to submit the asin and selected item
    def submit():
        lpn = lpn_entry2.get()
        item = category_entry.get()
        print(f"LPN: {lpn}\nSelected item: {item}")

    submit_button = ttk.Button(no_asin_frame, text="Submit", command=submit)
    submit_button.grid(column=1, row=2, padx=10, pady=10)
    no_asin_frame.lift()
    lpn_entry2.focus()
    
def set_product_to_category(pallet_name):
    #TODO make this take in a category and automatically set that product to the given catqgory csv file
    print(pallet_name)
    return
    
def complete_pallet(pallet_name):
    #TODO take the pallet_name and count it up one and set it to a new csv file
    print(pallet_name)
    return

def undo():
    #TODO make this so when the undo button is pressed it will undo the last function, wether that be hitting complete
    #on the complete_pallet or scanned the wrong product or scanned the wrong catigory when no asin was found
    return

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

    canvas = Canvas(label3_frame, width=800, height=1500)  
    scrollable_frame = ttk.Frame(canvas, width=800, height=1500)
    scrollbar = Scrollbar(label3_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    over75_label = tk.StringVar(value="")
    under75_label = tk.StringVar(value="")
    gaming_headphones_over125_label = tk.StringVar(value="")
    gaming_headphones_under125_label = tk.StringVar(value="")
    earbuds_selected_label = tk.StringVar(value="")
    earbuds_not_selected_label = tk.StringVar(value="")
    keyboards_mice_label = tk.StringVar(value="")
    no_asin_label = tk.StringVar(value="")
    all_scanned_label = tk.StringVar(value="")
    routers_switches_label = tk.StringVar(value="")
    docking_stations_label = tk.StringVar(value="")
    apple_accessories_label = tk.StringVar(value="")
    laptops_surfaces_label = tk.StringVar(value="")
    drawing_tablets_portable_monitors_label = tk.StringVar(value="")
    modems_label = tk.StringVar(value="")
    power_supplies_label = tk.StringVar(value="")
    motherboards_label = tk.StringVar(value="")
    graphics_cards_label = tk.StringVar(value="")
    cpu_coolers_label = tk.StringVar(value="")
    phones_tablets_label = tk.StringVar(value="")
    ram_label = tk.StringVar(value="")
    pcie_cards_label = tk.StringVar(value="")
    phone_tablet_cases_label = tk.StringVar(value="")
    watches_label = tk.StringVar(value="")
    ssd_label = tk.StringVar(value="")
    nas_label = tk.StringVar(value="")
    hard_drives_label = tk.StringVar(value="")
    mini_computers_label = tk.StringVar(value="")
    cameras_label = tk.StringVar(value="")
    cpu_label = tk.StringVar(value="")
    audio_devices_label = tk.StringVar(value="")
    gaming_systems_label = tk.StringVar(value="")
    headphones_label = tk.StringVar(value="")

    items = [('over_pallet', over75_label),
            ('under_pallet', under75_label),
            ('gaming_headphones_over', gaming_headphones_over125_label),
            ('gaming_headphones_under', gaming_headphones_under125_label),
            ('earbuds_selected', earbuds_selected_label),
            ('earbuds_not_selected', earbuds_not_selected_label),
            ('keyboards_mice', keyboards_mice_label),
            ('routers_switches', routers_switches_label),
            ('docking_stations', docking_stations_label),
            ('apple_accessories', apple_accessories_label),
            ('laptops_surfaces', laptops_surfaces_label),
            ('drawing_tablets_portable_monitors', drawing_tablets_portable_monitors_label),
            ('modems', modems_label),
            ('power_supplies', power_supplies_label),
            ('motherboards', motherboards_label),
            ('graphics_cards', graphics_cards_label),
            ('cpu_coolers', cpu_coolers_label),
            ('phones_tablets', phones_tablets_label),
            ('ram', ram_label),
            ('pcie_cards', pcie_cards_label),
            ('phone_tablet_cases', phone_tablet_cases_label),
            ('watches', watches_label),
            ('ssd', ssd_label),
            ('nas', nas_label),
            ('hard_drives', hard_drives_label),
            ('mini_computers', mini_computers_label),
            ('cameras', cameras_label),
            ('cpu', cpu_label),
            ('audio_devices', audio_devices_label),
            ('gaming_systems', gaming_systems_label),
            ('headphones', headphones_label),
            ('no_asin', no_asin_label),
            ('all_scanned', all_scanned_label)]

    def complete_pallet_callback(item_name):
        return lambda: complete_pallet(item_name)
    new_items = [(item[0], tk.StringVar(value="")) for item in items]
    for i, (item_name, item_label) in enumerate(items):

        button = ttk.Button(scrollable_frame, text="Complete", command=complete_pallet_callback(item_name))
        button.grid(column=0, row=i, padx=1, pady=1, sticky='w')
        
        label = ttk.Label(scrollable_frame, textvariable=item_label)
        label.grid(column=1, row=i, padx=1, pady=1, sticky='w')

    over75_label.set("Over 75: NONE SELECTED")
    under75_label.set("Under 75: NONE SELECTED")
    gaming_headphones_over125_label.set("Gaming\nHeadphones Over: NONE SELECTED")
    gaming_headphones_under125_label.set("Gaming\nHeadphones Under: NONE SELECTED")
    earbuds_selected_label.set("Selected Earbuds: NONE SELECTED")
    earbuds_not_selected_label.set("Other Earbuds: NONE SELECTED")
    keyboards_mice_label.set("Keyboards Mice: NONE SELECTED")
    no_asin_label.set("No asin: NONE SELECTED")
    all_scanned_label.set("All Scanned: NONE SELECTED")
    routers_switches_label.set("Routers/Switches: NONE SELECTED")
    docking_stations_label.set("Docking Stations: NONE SELECTED")
    apple_accessories_label.set("Apple Accessories: NONE SELECTED")
    laptops_surfaces_label.set("Laptops/Surface: NONE SELECTED")
    drawing_tablets_portable_monitors_label.set("Drawing/\nPortable Monitors: NONE SELECTED")
    modems_label.set("Modems: NONE SELECTED")
    power_supplies_label.set("Power Supplies: NONE SELECTED")
    motherboards_label.set("Motherboards: NONE SELECTED")
    graphics_cards_label.set("Graphics Cards: NONE SELECTED")
    cpu_coolers_label.set("CPU Coolers: NONE SELECTED")
    phones_tablets_label.set("Phones/Tablets: NONE SELECTED")
    ram_label.set("RAM: NONE SELECTED")
    pcie_cards_label.set("PCIE Cards: NONE SELECTED")
    phone_tablet_cases_label.set("Cases Phone/Tablets: NONE SELECTED")
    watches_label.set("Watches: NONE SELECTED")
    ssd_label.set("SSD: NONE SELECTED")
    nas_label.set("NAS: NONE SELECTED")
    hard_drives_label.set("Hard Drives: NONE SELECTED")
    mini_computers_label.set("Mini Computers: NONE SELECTED")
    cameras_label.set("Web/Security Cams: NONE SELECTED")
    cpu_label.set("CPUs: NONE SELECTED")
    audio_devices_label.set("Audio Devices: NONE SELECTED")
    gaming_systems_label.set("Gaming Systems: NONE SELECTED")
    headphones_label.set("Headphones: NONE SELECTED")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))


    # add labels to label_frame
    fixed_width = 45

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