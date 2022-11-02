from kivymd.app import MDApp
from kivy.clock import Clock
from kivymd.uix.button import MDFlatButton, MDIconButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.widget import MDWidget
from kivy.properties import ColorProperty


class Keypad(MDGridLayout):

    def __init__(self, *args, **kwargs):
        super(Keypad, self).__init__(*args, **kwargs)
        Clock.schedule_once(self._init_keys)

    def _init_keys(self, dt):
        for i in range(1, 10):
            self.add_widget(TextKey(text=str(i)))

        self.add_widget(TextKey(text="C"))
        self.add_widget(TextKey(text="0"))
        self.add_widget(IconKey(icon="backspace-outline"))


class TextKey(MDFlatButton):
    key_color = ColorProperty((1, 0, 0, 1))

    def __init__(self, *args, **kwargs):
        super(TextKey, self).__init__(*args, **kwargs)
        self.rounded_button = True


class IconKey(MDIconButton):
    key_color = ColorProperty((1, 0, 0, 1))

    def __init__(self, *args, **kwargs):
        super(IconKey, self).__init__(*args, **kwargs)


class LockScreen(MDScreen):

    def __init__(self, *args, **kwargs):
        super(LockScreen, self).__init__(*args, **kwargs)
