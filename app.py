from ast import Try
from models import Base, Product, session, engine
import csv
import datetime


#import the contense of inventory.csv
#add the data into the database.
#create a menu for selection

def main():
    import_data()
    choice_process()

def import_data():
    with open('inventory.csv', newline='') as csvfile:
        productreader = csv.reader(csvfile, delimiter='|')
        rows = list(productreader)
        for row in rows[1:]:
            item_adder(row[0].split(','))
    session.commit()

def choice_process():
    running = True
    while running:
        choice = menu_choice()
        match choice:
            case 'v':
                view_item()
            case 'a':
                add_item()
            case 'b':
                backup_inventory()

def menu_choice():
    print('''
        \nInventory database
        \rv) View an Item
        \ra) Add an Item
        \rb) Backup Inventory''')
    while True:
        choice = input('What do you want to do?   ')
        if choice.lower() in ['v', 'a', 'b']:
            return choice.lower()
        else:
            print('Sorry, didn\'t understand. Please enter a valid choice.')

def view_item():
    for item in session.query(Product):
        print(f'{item.product_name} {item.product_quantity} {(item.product_price/100)} {item.date_updated}')


def add_item():
    product_name = input('Enter product name: ')
    product_quantity = input('Enter product amount: ')
    product_price = input('Enter product price in dollars (ex. $13.40): ')
    product_date = input('Enter product update date (format. MM/DD/YYYY): ')
    try:
        item_adder([product_name, product_quantity, product_price, product_date])
    except ValueError:
        print('sorry, didn\'t understand what you entered.')
    else:
        session.commit()

def item_adder(item):
    print(item)
    item_name, price_before, quantity_before, date_before = item[0:]
    clean_quantity = int(quantity_before)
    if price_before[0] == '$':
        clean_price = int(float(price_before[1:]) * 100)
    else:
        clean_price = int(float(price_before[0:]) * 100)
    clean_date = datetime.datetime.strptime(date_before, "%m/%d/%Y")
    new_item = Product(
        product_name=item_name,
        product_quantity=clean_quantity,
        product_price=clean_price,
        date_updated=clean_date
        )
    session.add(new_item)

def backup_inventory():
    pass

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    main()