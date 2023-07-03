from config import users_list_url
import requests

response = requests.get(users_list_url)
users_list = response.text.split("\n")


