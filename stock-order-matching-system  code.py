import uuid
import json
import sys

user_profiles = {}
buy_orders = []
sell_orders = []

def record_transaction(asset_symbol, number_of_orders, execution_price, buying_profile_id, selling_profile_id):
    with open("execution_log.txt", "a") as log_file:
        log_entry = {
            "asset_symbol": asset_symbol,
            "number_of_orders": number_of_orders,
            "execution_price": execution_price,
            "buying_profile_id": buying_profile_id,
            "selling_profile_id": selling_profile_id
        }
        log_file.write(json.dumps(log_entry) + "\n")
        
class UserProfile:
    def __init__(self, given_name, family_name, email_address):
        self.id = str(uuid.uuid4())
        self.given_name = given_name
        self.family_name = family_name
        self.email_address = email_address
        user_profiles[self.id] = self
        
class BuyOrder:
    def __init__(self, asset_symbol, order_price, quantity, profile_id):
        self.asset_symbol = asset_symbol
        self.order_price = order_price
        self.quantity = quantity
        self.profile_id = profile_id
        buy_orders.append(self)
        evaluate_orders()
        
class SellOrder:
    def __init__(self, asset_symbol, order_price, quantity, profile_id):
        self.asset_symbol = asset_symbol
        self.order_price = order_price
        self.quantity = quantity
        self.profile_id = profile_id
        sell_orders.append(self)
        evaluate_orders()
        
def register_user():
    given_name = input("Enter your first name: ")
    family_name = input("Enter your last name: ")
    email_address = input("Enter your email address: ")
    new_user = UserProfile(given_name, family_name, email_address)
    print(f"Account created successfully! Your User ID is {new_user.id}")

def place_buy_order():
    profile_id = input("Enter your User ID: ")
    if profile_id not in user_profiles:
        print("Invalid User ID. Please create an account first.")
        return
    asset_symbol = input("Enter the stock name: ")
    order_price = float(input("Enter the bidding price: "))
    quantity = int(input("Enter the amount: "))
    BuyOrder(asset_symbol, order_price, quantity, profile_id)
    print("Bid placed successfully!")

def place_sell_order():
    profile_id = input("Enter your User ID: ")
    if profile_id not in user_profiles:
        print("Invalid User ID. Please create an account first.")
        return
    asset_symbol = input("Enter the stock name: ")
    order_price = float(input("Enter the asking price: "))
    quantity = int(input("Enter the amount: "))
    SellOrder(asset_symbol, order_price, quantity, profile_id)
    print("Ask placed successfully!")

def terminate_application():
    print("Exiting the program. Goodbye!")
    sys.exit()

def display_main_interface():
    command_actions = {
        'a': register_user,
        'b': place_buy_order,
        'c': place_sell_order,
        'd': terminate_application,
    }

    while True:
        print("\nMain Menu")
        print("a. Create an account")
        print("b. Make a bidding")
        print("c. Make an asking")
        print("d. Exit the program")
        user_selection = input("Choose an option (a/b/c/d): ").lower()
        action = command_actions.get(user_selection, lambda: print("Invalid option. Please try again."))
        action()

def process_exact_match(buy_order, sell_order):
    print(f"{buy_order.quantity} order(s) successfully executed at {buy_order.order_price}")
    record_transaction(buy_order.asset_symbol, buy_order.quantity, buy_order.order_price, buy_order.profile_id, sell_order.profile_id)
    buy_orders.remove(buy_order)
    sell_orders.remove(sell_order)

def process_partial_buy(buy_order, sell_order):
    print(f"{buy_order.quantity} order(s) successfully executed at {buy_order.order_price}")
    record_transaction(buy_order.asset_symbol, buy_order.quantity, buy_order.order_price, buy_order.profile_id, sell_order.profile_id)
    sell_order.quantity -= buy_order.quantity
    buy_orders.remove(buy_order)

def process_partial_sell(buy_order, sell_order):
    print(f"{sell_order.quantity} order(s) successfully executed at {buy_order.order_price}")
    record_transaction(buy_order.asset_symbol, sell_order.quantity, buy_order.order_price, buy_order.profile_id, sell_order.profile_id)
    buy_order.quantity -= sell_order.quantity
    sell_orders.remove(sell_order)

def evaluate_orders():
    for buy_order in buy_orders[:]:  
        for sell_order in sell_orders[:]:  
            if buy_order.asset_symbol == sell_order.asset_symbol and buy_order.order_price >= sell_order.order_price:
                quantity_comparison = (buy_order.quantity > sell_order.quantity) - (buy_order.quantity < sell_order.quantity)
                actions = {
                    0: lambda: process_exact_match(buy_order, sell_order),
                    -1: lambda: process_partial_buy(buy_order, sell_order),
                    1: lambda: process_partial_sell(buy_order, sell_order)
                }
                actions[quantity_comparison]()
                break
            
if __name__ == "__main__":
    display_main_interface()
