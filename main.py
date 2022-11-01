import os

from kivy.core.window import Window
from kivymd.app import MDApp

from libs.uix.baseclass.root import Root

KV_DIR = os.path.join("libs", "uix", "kv")


class CounterApp(MDApp):

    def __init__(self, **kwargs):
        super(CounterApp, self).__init__(**kwargs)
        self.title = "Counter"
        self.load_all_kv_files(KV_DIR)
        Window.bind(on_keyboard=self.key_input)

    def build(self):
        return Root()

    def key_input(self, window, key, scancode, codepoint, modifier):
        if key == 27:  # 27 key = escape
            return True

    def on_pause(self):
        return True

    def change_root_screen(self, screen_name):
        self.root.current = screen_name


if __name__ == "__main__":
    CounterApp().run()
