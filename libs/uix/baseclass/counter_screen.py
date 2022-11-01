from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty
from kivymd.app import MDApp


class CounterScreen(MDScreen):
    count = StringProperty("0")

    def __init__(self, *args, **kwargs):
        super(CounterScreen, self).__init__(*args, **kwargs)
        self.app = MDApp.get_running_app()

    def increase_count(self):
        self.count = str(int(self.count) + 1)

    def decrease_count(self):
        self.count = str(int(self.count) - 1)

    def reset_count_zero(self):
        self.count = "0"
