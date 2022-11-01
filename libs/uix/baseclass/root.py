import json
from os import path

from kivy.clock import Clock
from kivymd.uix.screenmanager import MDScreenManager


class Root(MDScreenManager):

    def __init__(self, *args, **kwargs):
        super(Root, self).__init__(*args, **kwargs)
        Clock.schedule_once(self.add_screens)

    def add_screens(self, delta):
        with open(path.join("json", "root_screens.json")) as file:
            screens = json.load(file)

        for screen_name in screens.keys():
            screen_details = screens[screen_name]
            exec(screen_details["import"])
            screen_object = eval(screen_details["object"])
            screen_object.name = screen_name
            self.add_widget(screen_object)
