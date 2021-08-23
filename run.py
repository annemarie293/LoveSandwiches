import gspread
from google.oauth2.service_account import Credentials

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
    Get Sales figures input from the user
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

def update_sales_worksheet(data):
    """
    Update Sales worksheet in Google sheets, add new row with user input Sales data
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Worksheet is updated.\n")

data = get_sales_data()
print(data)
sales_data = [int(num) for num in data]
print(sales_data)
update_sales_worksheet(sales_data)
