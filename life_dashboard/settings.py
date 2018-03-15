import os

MASTER_HOST = os.environ['MASTER_HOST']
RABBITMQ_USER = os.environ['RABBITMQ_USER']
RABBITMQ_PASSWORD = os.environ['RABBITMQ_PASSWORD']
RABBITMQ_PORT = int(os.environ['RABBITMQ_PORT'])


PLUGIN_ENV_VAR_PREFIX = 'LIFE_DASHBOARD_PLUGIN_'

HOME_PLUGIN_NAME = 'home'
COMMANDS_LISTENER_PLUGIN_NAME = 'commans_listener'

DEFAULT_PLUGINS = {
    HOME_PLUGIN_NAME.upper(): 'life_dashboard.plugins.home',
    COMMANDS_LISTENER_PLUGIN_NAME.upper(): 'life_dashboard.plugins.commands_listener',
}

KIVY_BORDERLESS = int(os.environ.get('KIVY_BORDERLESS', 1))
KIVY_FULLSCREEN = int(os.environ.get('KIVY_FULLSCREEN', 0))
KIVY_SCREEN_WIDTH = int(os.environ.get('KIVY_SCREEN_WIDTH', 800))
KIVY_SCREEN_HEIGHT = int(os.environ.get('KIVY_SCREEN_HEIGHT', 480))
KIVY_SCREEN_POS_X = int(os.environ.get('KIVY_SCREEN_POS_X', 0))
KIVY_SCREEN_POS_Y = int(os.environ.get('KIVY_SCREEN_POS_Y', 0))

# Kivy default is 60, we can save some CPU with 30
KIVY_MAX_FPS = int(os.environ.get('KIVY_MAX_FPS', 30))
