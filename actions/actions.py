from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


def levenshtein_distance(s, t):
    m, n = len(s), len(t)
    if m < n:
        s, t = t, s
        m, n = n, m
    d = [list(range(n + 1))] + [[i] + [0] * n for i in range(1, m + 1)]
    for j in range(1, n + 1):
        for i in range(1, m + 1):
            if s[i - 1] == t[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                d[i][j] = min(d[i - 1][j], d[i][j - 1], d[i - 1][j - 1]) + 1
    return d[m][n]

def compute_similarity(input_string, reference_string):
    distance = levenshtein_distance(input_string, reference_string)
    max_length = max(len(input_string), len(reference_string))
    similarity = 1 - (distance / max_length)
    return similarity

input_string = "Geeksforgeeks"
reference_string = "Geeks4geeks"
similarity = compute_similarity(input_string, reference_string)
print(similarity)



# load response file

import json

# Open and read the JSON file
with open('./ecommerce_data/ecommerce.json', 'r') as file:
    product_details = json.load(file)


class ExtractPhoneEntity(Action):

    def name(self) -> Text:
        return "action_extract_phone_name_entity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        product_name_entity = next(tracker.get_latest_entity_values('product_name'), None)

        print(product_name_entity)
        
        if(product_name_entity):
            product_details_keys = product_details['product_details']
            final_key_score=0
            final_key = ""
            for key in product_details_keys:
                score = compute_similarity(key, product_name_entity)
                if(score>final_key_score):
                    final_key_score=score
                    final_key = key
            
            final_response = product_details['product_details'][final_key]
                    
            dispatcher.utter_message(text=f"{final_response}")

        else:
            dispatcher.utter_message(text=f"Sorry, could not detect phone name")

        return []



class OrderStatus(Action):

    def name(self) -> Text:
        return "action_extract_email_address"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        email_address = next(tracker.get_latest_entity_values('email_adress'), None)
        print(email_address)
        if(email_address):
            dispatcher.utter_message(text=f"I see an order Id: #WB9834895, under your email address given. Can you please confirm you want know status about this address")

        else:
            dispatcher.utter_message(text=f"Sorry, could not detect phone name")

        return []


class ChangeAddress(Action):

    def name(self) -> Text:
        return "action_extract_email_address_for_address"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        email_address = next(tracker.get_latest_entity_values('email_adress'), None)
        print(email_address)
        if(email_address):
            dispatcher.utter_message(text=f"Thank You for sharing your email address, Your email addres is {email_address}")
            dispatcher.utter_message(text=f"Please provide your new address to update.")

        else:
            dispatcher.utter_message(text=f"Sorry, could not detect phone name")

        return []
    


    
class UpdateAddress(Action):

    def name(self) -> Text:
        return "action_update_address"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        address = next(tracker.get_latest_entity_values('address'), None)
        print(address)
        if(address):
            dispatcher.utter_message(text=f"Thank You for sharing your new address, We have updated your address")
            dispatcher.utter_message(text=f"Here is your new shipping address : {address}")

        else:
            dispatcher.utter_message(text=f"Sorry, could not detect phone name")

        return []