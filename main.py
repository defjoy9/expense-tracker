import argparse
import csv
import os
import datetime
from tempfile import NamedTemporaryFile
import shutil

def manage_db(database_path, header):
    if not os.path.exists(database_path):
        os.mknod(database_path)

        with open(database_path, mode='w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(header)

def last_id(database_path):
    with open(database_path, mode="r",newline='') as csvfile:
        reader = csv.reader(csvfile)
        last_id = 0
        for row in reader:
            last_id = row[0]
        if last_id == "ID" or last_id == None:
            last_id = 0
    return last_id

def add(database_path,description, amount):
    date_now = datetime.datetime.now().strftime("%Y-%m-%d")
    id = last_id()
    id = int(id) + 1
    with open(database_path, mode="a", newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([id,date_now, description, amount])
    return print(f"Expense added successfully (ID:{id})")

def update(database_path,header,id,description,amount):
    date_now = datetime.datetime.now().strftime("%Y-%m-%d")
    tempfile = NamedTemporaryFile(mode='w', delete=False)
    
    with open(database_path, 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=header)
        writer = csv.DictWriter(tempfile, fieldnames=header)

        for row in reader:
            if str(row['ID']) == id:
                row['Date'],row['Description'],row['Amount'] = date_now, description, amount
            row = {'ID': row['ID'], 'Date': row['Date'], 'Description': row['Description'], 'Amount': row['Amount']}
            writer.writerow(row)
    shutil.move(tempfile.name, database_path)
    print("Expense updated successfully")

def delete(database_path, header, id):
    tempfile = NamedTemporaryFile(mode='w', delete=False)

    with open(database_path, mode='r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=header)
        writer = csv.DictWriter(tempfile, fieldnames=header)

        for row in reader:
            if row['ID'] != id:
                new_row = row
                writer.writerow(new_row)
    shutil.move(tempfile.name, database_path)
    print(f"Expense of ID {id} sucessfully deleted")

def summary(database_path,header,month=None):
    total = 0
    
    with open(database_path, mode='r') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=header)

        for row in reader:
            amount = row['Amount']
            if month == None:
                if amount != "Amount":
                    total += float(amount)
                months = "everything"
            else:
                date = datetime.datetime.strptime(row["Date"],"%Y-%m-%d").date()
                if date.month == month:
                    total += float(amount)
                months = date.strftime("%B")
    return print(f"Total expenses for {months}: ${total:.2f}")

def list_csv(database_path,header):
    with open(database_path, mode='r') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=header)
        justify = 12
        for row in reader:
            print(row['ID'].ljust(3," "), row['Date'].ljust(justify," "),row['Description'].ljust(justify," "),row['Amount'].ljust(justify," "))

def main():
    database_path = "database.csv"
    header = ["ID","Date","Description","Amount"]
    manage_db(database_path,header)
    parser = argparse.ArgumentParser(
                        prog='Expense-tracker',
                        description='Application that manages your finances',
                        epilog='made by defjoy9')
    parser.add_argument('action')
    parser.add_argument('--description')    
    parser.add_argument("--amount")
    parser.add_argument("--id")
    parser.add_argument("--month")

    args = parser.parse_args()

    if args.action == "add":
        add(database_path,args.description, args.amount)
    elif args.action == "update":
        update(database_path, header, args.id, args.description, args.amount)
    elif args.action == "delete":
        delete(database_path, header, args.id)
    elif args.action == "summary":
        summary(database_path, header, args.month)
    elif args.action == "list":
        list_csv(database_path,header)

if __name__ == "__main__":
    main()