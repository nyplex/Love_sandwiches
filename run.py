import gspread 
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')



def get_sales_data():
    """
    Get sales figures input from the user
    """
    
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")
        
        data_str = input("Enter data here: ")
        sales_data = data_str.split(",")
        
        
        if validate_data(sales_data):
            print("Data is valid")
            break

    return sales_data


def validate_data(values):
    """[Insisde the Try, converts all string values into integers. Raises ValueError if the strings cannot be converted into int, or if there aren't exactly 6 values.]

    Args:
        values ([string]): [array of values]

    Raises:
        ValueError: [if values length != 6]

    Returns:
        [bool]: [return True if data is valid]
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values requried, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again. \n")
        return False
        
    return True
    

def calculate_surplus_data(sales_row):
    """[Compare sales with stock and calculate the surplus for each item ttype. The surplus value is defined a the sales figures substracted from the stock:
        -Positive surplus indicates waste
        -Negative surplus indactes extra made when stock was sold out.
    ]

    Args:
        sales_row ([list]): [sales provided by user]

    Returns:
        [list]: [surplus data]
    """
    
    print("Calculating surplus data... \n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data


def update_worksheet(data, worksheet):
    """[Receive a list of values to be inserted into a worksheet. Update the relevant worsheet with the data provided.]

    Args:
        data ([list]): [list of value to be insert into the worksheet.]
        worksheet ([string]): [name of the worksheet to update.]
    """
    
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully.\n")



def main():
    """[Run all program functions]
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")

print("Welcome to Love Sandwiches")
main()