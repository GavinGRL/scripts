import csv

# GLDesc,CategoryCode,CategoryDesc,SubcatCode,SubcatDesc,Asin,UPC,ItemDesc
categories = {}
with open('categories.csv', newline='', encoding='utf-8') as categories_file:
    reader = csv.DictReader(categories_file)
    for row in reader:
        categories[row['Asin']] = {
            'CategoryCode': row['CategoryCode'],
            'CategoryDesc': row['CategoryDesc'],
            'SubcatCode': row['SubcatCode'],
            'SubcatDesc': row['SubcatDesc']
        }

# GLDesc,Asin,UPC,ItemDesc,Units,Total Price
rows_with_categories = []
with open('items.csv', newline='', encoding='utf-8') as items_file:
    reader = csv.DictReader(items_file)
    for row in reader:
        asin = row['Asin']
        if asin in categories:
            row['CategoryCode'] = categories[asin]['CategoryCode']
            row['CategoryDesc'] = categories[asin]['CategoryDesc']
            row['SubcatCode'] = categories[asin]['SubcatCode']
            row['SubcatDesc'] = categories[asin]['SubcatDesc']
        else:
            row['CategoryCode'] = 'n/a'
            row['CategoryDesc'] = 'n/a'
            row['SubcatCode'] = 'n/a'
            row['SubcatDesc'] = 'n/a'
        rows_with_categories.append(row)

#GLDesc,CategoryCode,CategoryDesc,SubcatCode,SubcatDesc,Asin,UPC,ItemDesc,Units,Total Price
with open('items_with_categories.csv', 'w', newline='', encoding='utf-8') as output_file:
    fieldnames = ['GLDesc', 'CategoryCode', 'CategoryDesc', 'SubcatCode', 'SubcatDesc', 'Asin', 'UPC', 'ItemDesc', 'Units', 'Total Price']
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows_with_categories)
