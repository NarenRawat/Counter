from kivy.metrics import dp
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen


class MadeByImage(Image):

    def __init__(self, *args, **kwargs):
        super(MadeByImage, self).__init__(*args, **kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if touch.is_double_tap:
                touch.grab(self)
            elif touch.is_triple_tap:
                if (self.parent.top * 0.6) < self.center_y < self.parent.top:
                    MDApp.get_running_app().change_root_screen("lock_screen")
                    self.y = self.parent.y + dp(10)
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.center_y += touch.dpos[1]
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
        return super().on_touch_up(touch)


class InfoScreen(MDScreen):

    def __init__(self, *args, **kwargs):
        super(InfoScreen, self).__init__(*args, **kwargs)
