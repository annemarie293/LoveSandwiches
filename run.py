import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get Sales figures input from user. Loop repeats until data is validated
    """
    while True:
        print("Please enter sales data from the last market")
        print("Data should be 6 numbers, separated by commas")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here:")

        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is validated")
            break
    return sales_data


def validate_data(values):
    """
    Inside the Try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there arent exactly 6 values
    """

    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"6 values exactly required, you provided {len(values)} values"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again")
        return False

    return True


def update_worksheet(sheet, data):
    """
    Recieves a list of integers and appends as a new row
    to the relevant worksheet
    """
    print(f"Updating {sheet} worksheet...\n")
    update_worksheet = SHEET.worksheet(sheet)
    update_worksheet.append_row(data)
    print(f"{sheet} worksheet is updated.\n")


def calculate_surplus_data(sales_row):
    """
    Calculates daily surplus:
    daily stock - daily sales
    """
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    stock_row = [int(num) for num in stock_row]
    surplus_data = []
    for stock, sale in zip(stock_row, sales_row):
        surplus = stock-sale
        surplus_data.append(surplus)
    return surplus_data


def get_last_5_entries_sales():
    """
    collect the last 5 entries from a column of data for all sandwich
    Returns the data as a list of lists of integers
    """
    sales = SHEET.worksheet("sales")
    
    columns =[]
    for ind in range(1,7):
        column = sales.col_values(ind)
        column = [int(num) for num in column[-5:]]
        columns.append(column)
    
    return columns

def main():
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet("sales", sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet("surplus", new_surplus_data)


print("Welcome to Love Sandwiches Data automation! \n")
#main()
sales_columns =get_last_5_entries_sales()

