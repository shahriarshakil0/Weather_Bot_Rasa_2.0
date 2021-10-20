# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List

# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher


# class ActionHelloWorld(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello World!")

#         return []
from typing import Any, Text, Dict, List
from datetime import datetime

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from .weather import weather
import requests

class ActionWeather(Action):

    def name(self) -> Text:
        return "action_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            city = tracker.get_slot('location')
            temperature = round(weather(city)['main']['temp']-273.15)
            print("this is city",city)
            desc = weather(city)['weather'][0]['description']
            hum = weather(city)['main']['humidity']
            wind_spd = weather(city)['wind']['speed']

            response = f"The current temperature at {city} is {temperature} degree Celsius. Weather is {desc}. The humidity is {hum}% and wind speed is {wind_spd}kph"
            dispatcher.utter_message(response)

        except:
            dispatcher.utter_message("I can't understand your location. Please try again.")

        return [SlotSet('location', city)]

from rasa_sdk.events import AllSlotsReset

class ActionHelloWorld(Action):

     def name(self) -> Text:
            return "action_clear"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #  dispatcher.utter_message("Do you want to know about another city")

         return [AllSlotsReset()]
