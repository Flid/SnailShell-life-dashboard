#!/usr/bin/env python3
from logging.config import dictConfig

from life_dashboard.app import LifeDashboardApp
from life_dashboard.settings import LOGGING

dictConfig(LOGGING)

app = LifeDashboardApp()
app.run()
