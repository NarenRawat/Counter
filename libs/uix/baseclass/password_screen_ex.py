from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivymd.app import MDApp
from kivy.metrics import dp
from kivy.properties import (NumericProperty, ObjectProperty, StringProperty,
                             BooleanProperty, ColorProperty, BoundedNumericProperty)
from kivymd.uix.button import (MDFlatButton, MDIconButton, MDRoundFlatButton)
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.behaviors import ToggleButtonBehavior
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

kv = """
<PasswordScreen>:
    # _keypad_grid: _keypad_grid
    _pass_layout: _pass_layout

    keys_color: (1, 0, 0, 1)

    MDLabel:
        id: main_label
        halign: 'center'
        adaptive_height: True
        pos_hint: {'center_x': 0.5, 'top': 0.95}
        text: root.top_text
        bold: True
        font_size: root.top_text_size
        theme_text_color: "Custom"
        text_color: root.top_text_color

    MDBoxLayout:
        orientation: 'vertical'
        size_hint: 1, 1
        pos_hint: {'center_x': 0.5, 'y': 0.1}
        adaptive_height: True
        padding: 0, 0, 0, dp(20)
        spacing: dp(50)

        MDBoxLayout:
            id: _pass_layout
            adaptive_size: True
            orientation: "horizontal"
            spacing: dp(10)
            # md_bg_color: 1, 0, 0, 1
            pos_hint: {'center_x': 0.5}


        Keypad:
            pos_hint: {'center_x': 0.5}
            num_press: root._key_press
            backspace_press: root.backspace_press
            clear_press: root.clear_press
            keys_color: root.keys_color

<Keypad>:
    cols: 3
    adaptive_size: True
    spacing: dp(15)

<TextKey>:
    font_size: "50sp"
    bold: True
    halign: 'center'
    size_hint: None, None

    
<EntryField>:
    canvas.before:
        Color:
            rgba:(*self.underline_color[:3], 1 if self.state == "down" else 0.3)
        Line:
            width: dp(1.2)
            points: [(self.x, self.y), (self.right, self.y)]

    halign: 'center'
    theme_text_color: 'Custom'
    text_color: (*self.entry_text_color[:3], 1 if self.state == "down" else 0.3)
    size_hint: None, None
    size: self.texture_size

<TextKey>:
    canvas:
        Color:
            rgba: self.key_color
        Line:
            width: dp(1.2)
            circle: (self.center_x, self.center_y, self.width / 2)
            close: True

    theme_text_color: "Custom"
    text_color: self.key_color
    ripple_color: self.key_color

<IconKey>:
    theme_icon_color: "Custom"
    icon_color: self.key_color
    ripple_color: self.key_color

"""


class Keypad(MDGridLayout):
    keys_color = ColorProperty()

    def __init__(self, *args, **kwargs):
        super(Keypad, self).__init__(*args, **kwargs)
        self._text_size = dp(40)
        Clock.schedule_once(self._init_keys)

    def _init_keys(self, dt):
        for i in range(1, 10):
            self.add_widget(
                TextKey(text=str(i),
                        on_press=self.num_press,
                        font_size=self._text_size,
                        key_color=self.keys_color))
        self.add_widget(
            TextKey(text="C",
                    font_size=self._text_size,
                    on_press=self.clear_press,
                    key_color=self.keys_color))
        self.add_widget(
            TextKey(text="0",
                    font_size=self._text_size,
                    on_press=self.num_press,
                    key_color=self.keys_color))
        self.add_widget(
            IconKey(icon="backspace-outline",
                    icon_size=self._text_size,
                    rounded_button=True,
                    on_press=self.backspace_press,
                    key_color=self.keys_color))

    def num_press(self, *args):
        pass

    def clear_press(self, *args):
        pass

    def backspace_press(self, *args):
        pass


class TextKey(MDFlatButton):
    # key_color = ColorProperty(MDApp.get_running_app().theme_cls.primary_color)
    key_color = ColorProperty((1, 0, 0, 1))

    def __init__(self, *args, **kwargs):
        super(TextKey, self).__init__(*args, **kwargs)
        self.rounded_button = True


class IconKey(MDIconButton):
    key_color = ColorProperty((1, 0, 0, 1))

    def __init__(self, *args, **kwargs):
        super(IconKey, self).__init__(*args, **kwargs)


class EntryField(ToggleButtonBehavior, MDLabel):
    underline_color = ColorProperty()
    entry_text_color = ColorProperty()

    def __init__(self, *args, **kwargs):
        super(EntryField, self).__init__(*args, **kwargs)
        self.width = dp(14)
        self.height = dp(30)


class PasswordScreen(MDScreen):
    # app = MDApp.get_running_app()

    next_screen_name = StringProperty()

    top_text = StringProperty("Log In")
    top_text_color = ColorProperty((1, 0, 0, 1))
    top_text_size = NumericProperty(dp(35))

    entry_field_underline_color = ColorProperty((1, 0, 0, 1))
    entry_field_text_color = ColorProperty((1, 0, 0, 1))
    entry_field_alpha = BoundedNumericProperty(0.3, min=0, max=1)

    pass_length = NumericProperty(4)

    keys_color = ColorProperty((1, 0, 0, 1))

    _entered_pass = StringProperty()
    _pass_layout = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super(PasswordScreen, self).__init__(*args, **kwargs)
        Builder.load_string(kv)
        Clock.schedule_once(self.init_components)

    def init_components(self, dt):
        self.init_pass_layout()

    def init_pass_layout(self):
        for i in range(self.pass_length):
            lbl = EntryField()
            lbl.font_size = dp(25)
            lbl.underline_color = self.entry_field_underline_color
            lbl.entry_text_color = self.entry_field_text_color
            lbl.group = "pass"
            if i == 0:
                lbl.state = "down"
            self._pass_layout.add_widget(lbl)

    def on__entered_pass(self, *args):
        children_list = list(reversed(self._pass_layout.children))
        password = args[1]

        for index, child in enumerate(children_list):

            if len(password) > index:
                char = password[index]
                child.text = char
                child.size = child.texture_size
            else:
                char = " "
                child.text = char

        for index, child in enumerate(children_list):
            if index == len(password):
                children_list[len(password)].state = "down"
            else:
                children_list[index].state = "normal"

    def _key_press(self, obj):
        if len(self._entered_pass) < self.pass_length:
            self._entered_pass += obj.text

    def backspace_press(self, obj):
        self._entered_pass = self._entered_pass[:-1]

    def clear_press(self, obj):
        self._entered_pass = ""
