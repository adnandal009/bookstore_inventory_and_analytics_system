
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class Bookstore:
    def __init__(self, author=None, title=None, price=None, genre=None, quantity=None, data_inventory=None, data_sales=None):
        self.author = author
        self.title = title
        self.price = price
        self.quantity = quantity
        self.genre = genre
        self.data_inventory = data_inventory
        self.data_sales = data_sales

    def add_book(self):
        try:
            print()
            print("="*10)
            print("== Add a Book ==")
            print("="*10)
            print()

            title = input("Enter Title of Book : ").lower()
            author = input("Enter Author Name  : ")
            genre = input("Enter Genre Of Book : ")
            price = int(input("Enter Price of Book : "))
            quantity = int(input("Enter Quantity of Book : "))

            print(f"Title: {title}\nAuthor: {author}\nPrice: {price}\nQuantity: {quantity}")

            new_entry = {
                'Title': title,
                'Author': author,
                'Genre': genre,
                'Price': price,
                'Quantity': quantity
            }

            self.data_inventory = pd.concat(
                [self.data_inventory, pd.DataFrame([new_entry])],
                ignore_index=True
            )

            self.data_inventory.to_csv('inventory.csv', index=False)
            print("\nBook Added Successfully !!")
            print(self.data_inventory.tail(1))

        except:
            print("Something Went Wrong !!")

    def update_inventory(self):
        try:
            print()
            print("="*10)
            print("== Update Inventory ==")
            print("="*10)

            title_up = input("Enter Book Name For Updating Inventory : ").lower()
            quantity_up = int(input("Enter New Quantity of Your Book : "))

            if title_up in self.data_inventory['Title'].values:
                self.data_inventory.loc[
                    self.data_inventory['Title'] == title_up, 'Quantity'
                ] = quantity_up

                self.data_inventory.to_csv('inventory.csv', index=False)
                print(f"Quantity of {title_up} Updated Successfully !!")
            else:
                print("Please Enter Valid Book Name !!")

        except:
            print("Something Went Wrong !!")

    def record_sale(self, title, quantity):
        pass

    def generate_report(self):
        try:
            while True:
                print()
                print("="*10)
                print("== Generate Report ==")
                print("="*10)
                print("1. Total Sales By Genre")
                print("2. Total Sales By Author")
                print("3. Monthly Sales Trends")
                print("4. Revenue Share By Genre")
                print("5. Price and Sales Volume Heatmap")
                print("6. Back To Main Menu")
                print("="*10)

                ch = int(input("Enter Your Choice : "))

                data = pd.merge(self.data_sales, self.data_inventory, on='Title')

                if ch == 1:
                    print("== Total Sales By Genre ==")

                    genre_sales = data.groupby('Genre')['Quantity Sold'].sum()

                    sns.barplot(x=genre_sales.index, y=genre_sales.values)
                    plt.title("Total Sales By Genre")
                    plt.xlabel("Genre")
                    plt.ylabel("Books Sold")
                    plt.show()

                elif ch == 2:
                    print("== Total Sales By Author ==")

                    author_sales = data.groupby('Author')['Quantity Sold'].sum()

                    sns.barplot(x=author_sales.index, y=author_sales.values)
                    plt.title("Total Sales By Author")
                    plt.xlabel("Author")
                    plt.ylabel("Books Sold")
                    plt.xticks(rotation=45)
                    plt.show()

                elif ch == 3:
                    print("== Monthly Sales Trends ==")

                    data['Date'] = pd.to_datetime(data['Date'])
                    data['Month'] = data['Date'].dt.to_period('M').astype(str)

                    monthly_sales = data.groupby('Month')['Total Revenue'].sum()

                    plt.plot(monthly_sales.index, monthly_sales.values, marker='o')
                    plt.title("Monthly Sales Trends")
                    plt.xlabel("Month")
                    plt.ylabel("Total Revenue")
                    plt.show()

                elif ch == 4:
                    print("== Revenue Share By Genre ==")

                    genre_revenue = data.groupby('Genre')['Total Revenue'].sum()

                    plt.pie(genre_revenue.values, labels=genre_revenue.index,
                            autopct='%1.1f%%')
                    plt.title("Revenue Share By Genre")
                    plt.show()

                elif ch == 5:
                    print("== Price and Sales Volume Heatmap ==")

                    book_sales = data.groupby('Title')['Quantity Sold'].sum().reset_index()

                    book_price = self.data_inventory[['Title', 'Price']]

                    heatmap_data = pd.merge(book_price, book_sales, on='Title')

                    correlation = heatmap_data[['Price', 'Quantity Sold']].corr()

                    sns.heatmap(correlation, annot=True, cmap='coolwarm')
                    plt.title("Price and Sales Volume Correlation")
                    plt.show()

                elif ch == 6:
                    break

                else:
                    print("Please Enter Valid Choice !!")

        except:
            print("Something Went Wrong !!")

    def sales_analysis(self):
        try:
            while True:
                print()
                print("="*10)
                print("== Sales Analysis ==")
                print("="*10)
                print("1. Total Revenue")
                print("2. Top selling Books")
                print("3. Sales Trends and Genre")
                print("4. Book With Lowest Sales")
                print("5. Back To Main Menu")
                print("="*10)

                ch = int(input("Enter Your Choice : "))

                if ch == 1:
                    print("="*10)

                    total_revenue = self.data_sales['Total Revenue'].sum()
                    print(f"Total Revenue : {total_revenue}")

                    print("="*10)

                elif ch == 2:
                    print("="*10)
                    print("== Top Selling Books ==")

                    top_sell = self.data_sales.groupby('Title')['Quantity Sold'].sum()
                    print(top_sell)

                    print("="*10)

                elif ch == 3:
                    print("="*10)
                    print("== Sales Trends and Genre ==")

                    self.data_sales['Date'] = pd.to_datetime(self.data_sales['Date'])
                    sales_trend = self.data_sales.groupby('Date')['Total Revenue'].sum()
                    print(sales_trend)

                    print("="*10)

                elif ch == 4:
                    print()
                    print("="*10)

                    lowest_sell = self.data_sales.groupby('Title')['Quantity Sold'].sum()
                    lowest_sell = lowest_sell.sort_values()

                    print(lowest_sell)
                    print()
                    print("Book With Lowest Sales :")
                    print(lowest_sell.idxmin())

                    print("="*10)

                elif ch == 5:
                    print("Going Back To Main Menu...")
                    break

                else:
                    print("Invalid Choice")

        except:
            print("Something Went Wrong !!")

    def load_data(self):
        try:
            while True:
                print()
                print("="*10)
                print("== Data Loading and Data Cleaning ==")
                print("="*10)
                print()
                print("1. Load Data Sets")
                print("2. Clean Data")
                print("3. First 5 Rows")
                print("4. Data Info")
                print("5. Back to Main Menu")

                ch = int(input("Enter Your Choice : "))

                if ch == 1:
                    print()
                    print("="*10)
                    print("== Load Dataset ==")
                    print("="*10)

                    self.data_inventory = pd.read_csv('inventory.csv')
                    self.data_sales = pd.read_csv('sales.csv')

                    print("DataSets Loaded Successfully !!")

                elif ch == 2:
                    if self.data_inventory is None or self.data_sales is None:
                        print("Please Load Dataset First")

                    else:
                        print("== Data Cleaning ==")
                        print("1. Check For Missing Values")
                        print("2. Fill Missing Values With 0")
                        print("3. Drop Rows With Missing Values")

                        ch2 = int(input("Enter Your Choice : "))

                        if ch2 == 1:
                            print("Inventory Missing Values")
                            print(self.data_inventory.isna().sum())

                            print("Sales Missing Values")
                            print(self.data_sales.isna().sum())

                        elif ch2 == 2:
                            self.data_inventory = self.data_inventory.fillna(0)
                            self.data_sales = self.data_sales.fillna(0)

                            print("Missing Values Filled Successfully !!")

                        elif ch2 == 3:
                            self.data_inventory = self.data_inventory.dropna()
                            self.data_sales = self.data_sales.dropna()

                            print("Missing Rows Removed Successfully !!")

                        else:
                            print("Invalid Choice")

                        self.data_inventory.to_csv('inventory.csv', index=False)
                        self.data_sales.to_csv('sales.csv', index=False)

                elif ch == 3:
                    if self.data_inventory is not None and self.data_sales is not None:
                        print(self.data_inventory.head())
                        print(self.data_sales.head())
                    else:
                        print("Please Load Dataset First")

                elif ch == 4:
                    if self.data_inventory is not None and self.data_sales is not None:
                        self.data_inventory.info()
                        self.data_sales.info()
                    else:
                        print("Please Load Dataset First")

                elif ch == 5:
                    print("Going Back to Main Menu")
                    break

                else:
                    print("Invalid Choice")

        except:
            print("Something Went Wrong !!")

    def main_menu(self):
        while True:
            print("===== Bookstore Inventory and Analytics System =====")
            print("1. Data Loading and Data Cleaning")
            print("2. Adding New Book")
            print("3. Updating Inventory")
            print("4. Generate Report With Data Visualization")
            print("5. Sales Analysis")
            print("6. Exit")

            choice = int(input("Enter Your Choice : "))

            if choice == 1:
                self.load_data()

            elif choice == 2:
                self.add_book()

            elif choice == 3:
                self.update_inventory()

            elif choice == 4:
                self.generate_report()

            elif choice == 5:
                self.sales_analysis()

            elif choice == 6:
                print("Exiting from Program GoodBye !")
                break

            else:
                print("Invalid Choice")


obj = Bookstore()
obj.main_menu()
