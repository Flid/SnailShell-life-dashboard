from kivy.uix.screenmanager import Screen

from ..base import PluginBase


class HomeScreen(Screen):
    pass


class Plugin(PluginBase):
    kv_files = [
        'uix/home_screen.kv',
    ]
    screens = []

    def load_screens(self):
        home_screen = HomeScreen()
        home_screen.name = 'home'
        self.screens.append(home_screen)
        self.root_screen_name = home_screen.name
