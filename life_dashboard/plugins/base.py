import importlib
import logging
import os

from kivy.lang import Builder

from life_dashboard import settings
from life_dashboard.settings import DEFAULT_PLUGINS, PLUGIN_ENV_VAR_PREFIX

logger = logging.getLogger(__name__)


class PluginInitError(Exception):
    pass


class PluginBase:
    """
    A base class for plugins. It's not necessary to use it as a base cluss,
    just use the same structure. Duck typing!

    Initialization order:
    * Importing a module, getting a `Plugin` class, instantiating.
    * Injecting name, config variables, settings etc.
    * Calling `on_import`
    * Loading `kv_files`
    * Calling `on_load`
    * Calling `load_screens`
    """
    # A list of filesystem paths to load.
    # Paths should be relative to the plugin root
    kv_files = []

    screens = []
    root_screen_name = None

    # The following attributes will be injected by the dashboard before `on_import`
    config = {}
    name = None
    root_directory = None
    settings = None

    def before_load(self):
        """
        Called right after the class is imported.
        """

    def after_load(self):
        """
        Called when all plugins are imported already,
        it's just another round of initialization.
        """

    def load_screens(self):
        """
        This method should add all the screens available to self.screens.
        It also should set self.root_screen_name to the name of the main screen.
        """


def _load_plugin(name, path, config_env_prefix):
    logger.info('Loading plugin %s...', name)

    try:
        module = importlib.import_module(path)
    except ImportError:
        logger.error(
            'Failed to import module %s for plugin %s',
            name,
            path,
        )
        raise PluginInitError()

    config = {
        key[len(config_env_prefix):]: value
        for key, value in os.environ.items()
        if key.startswith(config_env_prefix)
    }

    try:
        plugin_cls = module.Plugin
        plugin_instance = plugin_cls()
        plugin_instance.name = name
        plugin_instance.config = config
        plugin_instance.settings = settings
        plugin_instance.root_directory = os.path.dirname(module.__file__)

        if hasattr(plugin_instance, 'before_load'):
            plugin_instance.before_load()
    except Exception:
        logger.exception(
            'Failed to initialize plugin %s %s',
            name,
            path,
        )
        raise PluginInitError()

    return plugin_instance


def load_plugins():
    """
    Load plugins, based on a list of modules from settings.
    """

    for name, module_path in DEFAULT_PLUGINS.items():
        os.environ[f'{PLUGIN_ENV_VAR_PREFIX}{name}'] = module_path

    plugins = {}

    for key, path in os.environ.items():
        if not key.startswith(PLUGIN_ENV_VAR_PREFIX):
            continue

        key = key[len(PLUGIN_ENV_VAR_PREFIX):]
        name = key.lower()

        plugins[name] = _load_plugin(name, path, config_env_prefix=f'{key}_')

    return plugins


def after_load_plugins(plugins):
    for name, plugin in plugins.items():
        try:
            if hasattr(plugin, 'after_load'):
                plugin.after_load()
        except Exception:
            logger.exception('Failed to load plugin %s', name)
            raise PluginInitError()


def load_plugin_kv_files(plugins):
    for name, plugin in plugins.items():
        for filename in getattr(plugin, 'kv_files', []):
            path = os.path.join(plugin.root_directory, filename)

            try:
                Builder.load_file(path)
            except Exception:
                logger.exception(
                    'Failed to import KV file %s for plugin %s',
                    path,
                    name,
                )
                raise PluginInitError()


def load_plugin_screens(plugins):
    for name, plugin in plugins.items():
        try:
            if hasattr(plugin, 'load_screens'):
                plugin.load_screens()
        except Exception:
            logger.exception('Failed to load screens for plugin %s', name)
            raise PluginInitError()
