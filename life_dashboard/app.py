from kivy.app import App
from kivy.logger import Logger as log
from kivy.uix.screenmanager import ScreenManager

from life_dashboard.plugins.base import (
    after_load_plugins,
    load_plugin_kv_files,
    load_plugin_screens,
    load_plugins
)
from life_dashboard.settings import HOME_PLUGIN_NAME


class LifeDashboardApp(App):
    def __init__(self, *args, **kwargs):
        self.plugins = load_plugins()
        self.home_plugin = self.plugins[HOME_PLUGIN_NAME]
        self.screens = {}

        super().__init__(*args, **kwargs)

    def load_kv(self, *args, **kwargs):
        load_plugin_kv_files(self.plugins)
        after_load_plugins(self.plugins)

    def _register_screens(self, manager):
        for plugin in self.plugins.values():
            for screen in getattr(plugin, 'screens', []):
                self.screens[screen.name] = screen
                manager.add_widget(screen)

    def build(self):
        import pdb; pdb.set_trace()
        #self.sm = ScreenManager()

        #load_plugin_screens(self.plugins)

        self._register_screens(self.sm)
        self.sm.current = self.home_plugin.root_screen_name
        return self.sm

    def on_stop(self):
        log.info('Stopping app...')
