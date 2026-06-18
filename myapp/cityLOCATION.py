import webbrowser

def find_city_in_google_map(city_name):
    google_earth_url=f"https://earth.google.com/web/search/{city_name}"
    
    webbrowser.open(google_earth_url)
    
    
city_name=input("enter your city : ")
find_city_in_google_map(city_name)
    
    #grammar correction 
    
"""from textblob import TextBlob

def correct_grammar(text):
    blob=TextBlob(text)
    corrected_text=str(blob.correct())
    return corrected_text
    
text=input(f"enter your text : ")
corrected_text=correct_grammar(text)
print(f"corrected:{corrected_text}")    
    """

#mouse moving bot

"""import pyautogui as pag
import random
import time

while True:
    x=random.randint(600,700)
    y=random.randint(200,600)
    pag.moveTo(x,y,1)
    time.sleep(200)"""
    