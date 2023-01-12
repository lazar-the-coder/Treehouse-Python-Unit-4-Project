from models import Base, Product, session, engine
import csv
import datetime

def main():
    import_data()
    choice_process()

def import_data():
    with open('inventory.csv', newline='') as csvfile:
        productreader = csv.DictReader(csvfile)
        for row in productreader:
            item_adder([
                row['product_name'],
                row['product_price'],
                row['product_quantity'],
                row['date_updated']
                ])
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
            case 'q':
                running = False
                print('Alright, good bye')

def menu_choice():
    print('''
        \nInventory database
        \rv) View a single product's inventory
        \ra) Add a new product to the database
        \rb) Make a backup of the entire inventory
        \rq) Quit
        ''')
    while True:
        choice = input('What do you want to do?   ')
        if choice.lower() in ['v', 'a', 'b', 'q']:
            return choice.lower()
        else:
            print('Sorry, didn\'t understand. Please enter a valid choice.')

def view_item():
    min_id = session.query(Product.product_id).first()[0]
    max_id = session.query(Product.product_id).order_by(Product.product_id.desc()).first()[0]
    while True:
        choice = input(f'Choose a number between {min_id} and {max_id}, enter "q" to leave. ')
        if choice == 'q':
            return
        else:
            try:
                if int(choice) < min_id or int(choice) > max_id:
                    print(f'Please enter a number between {min_id} and {max_id}, enter "q" to leave. ')
                else:
                    item = session.query(Product).filter_by(product_id=choice).first()
                    date = item.date_updated.strftime('%B %d %Y')
                    print(f'{item.product_name} for ${item.product_price/100}, {item.product_quantity} in stock, last updated {date}')
                    cont = input('Press enter to continue')
                    return
            except ValueError:
                print ('Please enter a number or the letter q')

def add_item():
    while True:
        product_name = input('Enter product name: ')
        product_quantity = input('Enter product amount: ')
        product_price = input('Enter product price in dollars (ex. 13.40): ')
        product_date = datetime.date.today()
        try:
            item_adder([product_name, product_price, product_quantity, product_date])
        except ValueError:
            print('sorry, didn\'t understand what you entered.')
            try_again = input('Would you like to try again, or return to the main menu? (q to return, enter to try again) ')
            if try_again == 'q':
                return
        else:
            print('Added successfully')
            session.commit()
            return

def item_adder(item):
    item_name, price_before, quantity_before, date_before = item[0:]
    clean_quantity = int(quantity_before)
    if price_before[0] == '$':
        clean_price = round(float(price_before[1:]) * 100)
    else:
        clean_price = round(float(price_before[0:]) * 100)
    if type(date_before) == datetime.date:
        clean_date = date_before
    else:
        clean_date = (datetime.datetime.strptime(date_before, "%m/%d/%Y")).date()
    new_item = Product(
        product_name=item_name,
        product_quantity=clean_quantity,
        product_price=clean_price,
        date_updated=clean_date
        )
    if session.query(Product.product_name).filter_by(product_name=item_name).first():
        old_item = session.query(Product).filter_by(product_name=item_name).first()
        if old_item.date_updated <= clean_date:
            old_item.product_quantity = clean_quantity
            old_item.product_price = clean_price
            old_item.date_updated = clean_date
        else:
            pass
    else:
        session.add(new_item)

def backup_inventory():
    with open('backup.csv', 'w', newline='') as csvfile:
        fields = ['product_name', 'product_price', 'product_quantity', 'date_updated']
        writer = csv.DictWriter(csvfile, fieldnames = fields)
        writer.writeheader()
        for item in session.query(Product):
            writer.writerow({
                'product_name': item.product_name,
                'product_price': (f'${(item.product_price/100):.2f}'),
                'product_quantity': item.product_quantity,
                'date_updated': (item.date_updated.strftime("%#m/%#d/%Y"))
                })
    print('Inventory backed up successfully')
    cont = input('Press enter to continue')

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    main()