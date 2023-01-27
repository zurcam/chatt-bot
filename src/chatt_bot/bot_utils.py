"""
This module houses all bot-specific utilities that chatt_bot relies upon.
"""
# Native libraries
import warnings
import textwrap
# Custom modules
from chatt_bot import directory_utils
from chatt_bot import generic_utils
# Non-native libraries
import requests


class CodePolice(generic_utils.VerboseAttributes):
    """
    Code that serves as "one-stop-shop" for checking all things bot-related.
    """
    def __init__(
            self,
            verbose=False
    ):
        self.verbose = verbose
        # Inherit attribute from verbose class.
        super().__init__()

    def static_url_validation(
            self,
            url_requested,
            desired_status_codes=200,
            on_bad_status_code='w',
            **kwargs
    ):
        """
        Validates if a url returns a desired status code.

        :param  str url_requested:
                Url requested to be checked via GET.
        :param int,list desired_status_codes:
                Status code or list of status codes to be
                compared to returned code from GET.
        :param str on_bad_status_code:
                Specifies whether to warn or error on non-expected
                code. Must be 'e' or 'w'.
        :param dict kwargs:
        """
        # Format desired_status_codes to list if not.
        if not isinstance(desired_status_codes, list):
            desired_status_codes = [desired_status_codes]
        # Check that all codes in list are ints.
        for i, single_status_code in enumerate(desired_status_codes):
            try:
                assert isinstance(single_status_code, int)
            except AssertionError as bad_status_code:
                raise TypeError(
                    textwrap.wrap(
                        f"Status code at index {i} in Keyword argument "
                        f"{desired_status_codes} must be of type integer.",
                        100
                    )
                ) from bad_status_code
        # Format on_bad_status_code and check if equal to 'e' or 'w'.
        on_bad_status_code = str(on_bad_status_code).lower().strip()
        try:
            assert on_bad_status_code in ['e', 'w']
        except AssertionError as bad_keyword_argument:
            raise ValueError(
                f"Keyword argument {on_bad_status_code} must be equal to either "
                f"'e'(asking to throw error) or 'w' (asking to throw warning)."
            ) from bad_keyword_argument
        # Open session to check url.
        with requests.Session() as request_session:
            url_response = request_session.get(
                url_requested,
                timeout=60,
                **kwargs
            )
            # Either warn or error if status code not in desired list.
            if url_response.status_code not in desired_status_codes:
                status_code_message = f"Url '{url_requested}' failed to return " \
                                      f"a desired status code in:" \
                                      f" {desired_status_codes}, " \
                                      f"and instead returned {url_response.status_code}"
                status_code_message = textwrap.fill(status_code_message, 100)
                if on_bad_status_code == 'w':
                    warnings.warn(
                        status_code_message,
                        UserWarning
                    )
                else:
                    raise ValueError(
                        status_code_message
                    )
            elif self.verbose:
                print(
                    f"Url {url_requested} returned "
                    f"desired status code: {url_response.status_code}"
                )

    @staticmethod
    def string_standard_format(string):
        """Returns a standard format for strings across modules."""
        return str(string).strip().lower()

class UrlHouser(generic_utils.VerboseAttributes):
    """Class that houses all Url related to chatt_bot."""
    def __init__(
            self,
            verbose=False
    ):
        # Inherit verbose attribute.
        super().__init__()


def setup_bot_folders():
    """
    Function that creates a series of folders where chatt_bot
    will store its information.
    """
    # Create folder in local documents for bot, and sub-folder for bot runs.
    return directory_utils.setup_documents_folder(
        "chatt_bot\\chatt_bot_runs"
    )
