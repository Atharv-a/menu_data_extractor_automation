from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

def create_menu(data, restaurant):
    response = model.generate_content(f"Use the data given below to make a menu for restaurant with name {restaurant}, if some data does not make sense then either leave it out or make changes to it. Do not give feedback in the end."+data)
    print(response.text)