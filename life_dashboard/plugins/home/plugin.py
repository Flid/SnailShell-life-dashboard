from ..base import PluginBase
from kivy.uix.screenmanager import Screen


class HomeScreen(Screen):
    pass#name = 'home'


class Plugin(PluginBase):
    kv_files = [
        'uix/home_screen.kv',
    ]
    screens = []

    def on_import(self, name):
        """
        Called right after the class is imported.
        """

    def on_load(self):
        """
        Called when all plugins are imported already,
        it's just another round of initialization.
        """

    def load_screens(self):
        home_screen = HomeScreen()
        home_screen.name = 'home'
        self.screens.append(home_screen)
        self.root_screen_name = home_screen.name
