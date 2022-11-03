from kivy.clock import Clock
from kivy.properties import (BooleanProperty, ColorProperty, NumericProperty,
                             ObjectProperty, OptionProperty, StringProperty)
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDIconButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.widget import MDWidget


class Keypad(MDGridLayout):

    def __init__(self, *args, **kwargs):
        super(Keypad, self).__init__(*args, **kwargs)
        Clock.schedule_once(self._init_keys)

    def _init_keys(self, dt):
        for i in range(1, 10):
            self.add_widget(TextKey(text=str(i),
                                    on_release=self.num_key_press))

        self.add_widget(TextKey(text="C", on_release=self.clear_key_press))
        self.add_widget(TextKey(text="0", on_release=self.num_key_press))
        self.add_widget(
            IconKey(icon="backspace-outline",
                    on_release=self.backspace_key_press))

    def num_key_press(self, *args):
        pass

    def clear_key_press(self, *args):
        pass

    def backspace_key_press(self, *args):
        pass


class TextKey(MDFlatButton):
    key_color = ColorProperty((1, 0, 0, 1))

    def __init__(self, *args, **kwargs):
        super(TextKey, self).__init__(*args, **kwargs)
        self.rounded_button = True


class IconKey(MDIconButton):
    key_color = ColorProperty((1, 0, 0, 1))

    def __init__(self, *args, **kwargs):
        super(IconKey, self).__init__(*args, **kwargs)


class PasswordEntry(MDBoxLayout):
    pass_length = NumericProperty(4)

    def __init__(self, *args, **kwargs):
        super(PasswordEntry, self).__init__(*args, **kwargs)
        Clock.schedule_once(self._init_components)

    def _init_components(self, dt):
        for i in range(self.pass_length):
            self.add_widget(PasswordEntryDot())


class PasswordEntryDot(MDWidget):
    enabled = BooleanProperty(False)

    def __init__(self, *args, **kwargs):
        super(PasswordEntryDot, self).__init__(*args, **kwargs)


class LockScreen(MDScreen):
    _pass_entry = ObjectProperty(None)

    pass_length = NumericProperty(6)
    next_screen_name = StringProperty()
    correct_password = StringProperty()
    mode = OptionProperty("signin", options=["signin", "signup"])

    _entered_pass = StringProperty("")

    def __init__(self, *args, **kwargs):
        super(LockScreen, self).__init__(*args, **kwargs)

    def on__entered_pass(self, *args):
        password = args[1]
        password_length = len(password)
        children_list = list(reversed(self._pass_entry.children))

        for index, child in enumerate(children_list):
            if index < password_length:
                child.enabled = True
            else:
                child.enabled = False

    def pass_validate(self):
        print(self._entered_pass, self.correct_password)

        return self._entered_pass == self.correct_password

    def switch_to_next_screen(self):
        if self.next_screen_name:
            self.parent.current = self.next_screen_name
        else:
            self.parent.current = self.parent.next()

    def num_key_press(self, obj):
        entered_pass_length = len(self._entered_pass)
        if entered_pass_length == self.pass_length - 1:
            self._entered_pass += obj.text
            matched = self.pass_validate()
            if matched:
                self.switch_to_next_screen()
            self.clear_pass()
        elif entered_pass_length < self.pass_length:
            self._entered_pass += obj.text

    def clear_pass(self, *args):
        self._entered_pass = ""

    def backspace_key_press(self, obj):
        self._entered_pass = self._entered_pass[:-1]
