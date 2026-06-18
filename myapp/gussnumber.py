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
    
    
    
