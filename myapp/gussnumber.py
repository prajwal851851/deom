import random

def number_gussing_game():
    print("BYE")
   
guss=random.randint(0,10)

attempts=0

while True:
    try:
        number=int (input("enter a number between 1 tp 10 : "))
        
    except ValueError():
        print("enter a valid number!!")
    
        
        continue
    attempts +=1
    if guss>number:
        print("your guss is not correct try again")
    elif guss<number:
        print("your guss is not correct try again")
    else:
        print(f" congrulations your guss number is {guss} in {attempts} attempts")
        break
        

number_gussing_game()    



def find_second_last():
    numbers=[1,4,6,7,4,5,3]
    if len(numbers)<2:
        return None
    
    

def clean_inventory_data(products):
    seen_products = set()
    cleaned_list = []
    
    for item in products:
        # Step 1: Normalize and clean individual fields
        
        # Clean the name: strip whitespaces and convert to Title Case
        clean_name = item["name"].strip().title()
        
        # Clean the price: strip "$" if present and convert to float
        raw_price = item["price"]
        if isinstance(raw_price, str):
            clean_price = float(raw_price.replace("$", "").strip())
        else:
            clean_price = float(raw_price)
            
        # Clean the stock: default to 0 if None
        clean_stock = item["stock"] if item["stock"] is not None else 0
        
        # Create a unique tuple representation to check for absolute duplicates
        product_signature = (clean_name, clean_price, clean_stock)
        
        # Step 2: Deduplicate using a set
        if product_signature not in seen_products:
            seen_products.add(product_signature)
            cleaned_list.append({
                "name": clean_name,
                "price": clean_price,
                "stock": clean_stock
            })
            
    # Step 3: Sort the final cleaned list alphabetically by product name
    cleaned_list.sort(key=lambda x: x["name"])
    
    return cleaned_list

# --- Testing the Function ---
raw_products = [
    {"name": "  leather jacket ", "price": "$120.00", "stock": 15},
    {"name": "running shoes", "price": 85.50, "stock": None},
    {"name": "leather jacket ", "price": "$120.00", "stock": 15}, 
    {"name": "wireless HEADPHONES", "price": "$59.99", "stock": 42},
    {"name": "running shoes", "price": 85.50, "stock": None}       
]

import pprint
print("Cleaned Inventory:")
pprint.pprint(clean_inventory_data(raw_products))
    

    
    
    
    
