"""
Module captures all custom workflows related to chatt_bot.
"""
# Native libraries.
import datetime
import os
import re
import subprocess
import typing
import warnings
import zipfile
# Custom modules
from chatt_bot import bot_utils
from chatt_bot import directory_utils
from chatt_bot import generic_utils
from chatt_bot import selenium_utils
# Non-native libraries
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup as bs


def execute_general_idle_command(
        *,
        command=''
):
    """
    Function that executes a generic command.

    :param str command:
            The command to be executed.
    """
    print(f'Starting generic command: start cmd /k {command}')
    os.system(f'start cmd /k "{command}"')
