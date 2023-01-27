"""Module containing custom selenium-related utilites."""
# Native libraries
import os
import random as rand
import textwrap
import time
# Custom modules
from chatt_bot import directory_utils
# Non-native libraries
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- SELENIUM STUFF
class ReadyMadeSeleniumDriver:
    """
    Class that creates a selenium chrome driver,
    alongside saving the location of the driver path.
    """
    def __init__(
            self,
            **kwargs
    ):
        #self.driver_path = get_driver_path()
        self.driver = create_chrome_driver(
            is_headless=True,
            **kwargs
        )

def create_chrome_driver(
        driver_path=None,
        is_headless=False
):
    """
    Function that create a Selenium.webdriver.Chrome driver.


    Parameters
    __________
    :param str driver_path:
            Path that holds the chrome driver executable. If not given,
            the driver path must be in Windows PATH.
    :param bool is_headless:
            Boolean flag, decides if the driver will be run as headless.
    :return: Selenium.webdriver.Chrome:
            The chrome web driver.
    """
    # Options for chrom driver.
    chrome_options = webdriver.chrome.options.Options()
    # Always have browser maximised with fullscreen.
    chrome_options.add_argument(
        '--start-maximized'
    )
    chrome_options.add_argument(
        '--start-fullscreen'
    )
    # If headless, add headless option to driver settings.
    if is_headless:
        chrome_options.add_argument(
            "--disable-gpu"
        )
        chrome_options.add_argument(
            "--headless"
        )
    # If the driver_path is specified, use it.
    if driver_path is None:
        driver = webdriver.Chrome(
            options=chrome_options
        )
    else:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
    # Return chrome driver.
    return driver



def get_driver_path():
    """
    Returns the location of a driver path,
    dependent on user set-up.

    :return: str:
            The path to the chrome driver file.
    """
    partial_path = directory_utils.get_user_path()
    # Driver folder path variable using local user information.
    driver_path = f'{partial_path}\\Desktop\\Utilities\\Drivers\\' \
                         f'chromedriver_win32\\chromedriver.exe'
    if not os.path.exists(driver_path):
        raise FileNotFoundError(
            textwrap.fill(
                f"The file '{driver_path}' was not found.",
                200
            )
        )
    return driver_path

def save_driver_screenshot(
        driver,
        save_path_location,
        screenshot_name
):
    """
    Function that takes in an active Selenium driver, a file location;
    and saves a screenshot of the driver.
    :param Selenium.webdriver driver:
    A Selenium webdriver. Driver must have active GET call.
    :param str save_path_location:
    Folder path location to store saved screenshot.
    :param str screenshot_name:
    Name given to saved screenshot.
    """
    # Ensures that get call fully loaded javascript objects,
    # buy waiting a couple of seconds. Second benefit is that
    # it makes it seem that website calls are more randomized,
    # mimicking a natural user's behavior.
    time.sleep(
        rand.randint(
            3,
            6
        )
    )
    # Save the screenshot.
    driver.save_screenshot(
        f"{save_path_location}\\{screenshot_name}.png"
    )

def driver_get_call(
        driver,
        url,
        expected_condition=None,
        wait_time=None,
        implicitly_wait=False
):
    """
    Function that executes an HTTP GET call through a Selenium Driver.

    Parameters
    __________
    :param Selenium.webdriver driver:
            A selenium webdriver (should be able to use any type).
    :param str url:
            The url to be used in GET.
    :param expected_conditions expected_condition:
            The customized expected condition. Only used if implicitly_wait == False.
    :param int wait_time:
            The wait_time, in seconds, to wait for the expected condition to arise.
            If None, then will wait between a random interval of 10 to 15 seconds.
    :param bool implicitly_wait:
            Boolean flag, stating whether the driver employs an implicit wait.
            If False, url requires a passed in expected_condition.
    """
    # If the driver does not implement an implicit wait,
    # then generate a wait time between 10 and 15 seconds.
    if implicitly_wait:
        if wait_time is None:
            wait_time = rand.randint(
                10,
                15
            )
        else:
            wait_time = int(wait_time)
        driver.implicitly_wait(wait_time)
        driver.get(url)
    # If the driver does not implement an implicit wait -- it waits on an expected condition.
    if not implicitly_wait:
        if wait_time is None:
            wait_time = rand.randint(
                10,
                15
            )
        else:
            wait_time = int(wait_time)
        driver.get(url)
        # Try to wait for the expected condition.
        WebDriverWait(
            driver,
            wait_time
        ).until(expected_condition)
