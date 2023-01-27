"""
Module that contains a Class that determines available actions of chatt_bot.
"""
# Native libraries
import datetime
# Custom modules
from chatt_bot import bot_utils
from chatt_bot import bot_workflows
from chatt_bot import generic_utils


def get_allowable_actions():
    """
    Function that stores the allowable action types for chatt_bot.
    :return: dict:
    Return the dict of built action_types and aliases.
    """
    return {
        'workflow': ['w', 'workflow'],
        'command': ['c', 'command']
    }


def get_action_description():
    """
    Function that stores the descriptions for action_types.

    :return: dict:
            The dict containing action_types as keys,
            and descriptions as values.
    """
    return {
        'workflow':
            'Relates to a pre-built workflow script '
            'located in bot_workflows modules.',
        'command':
            'A straight command line call.'
    }


def get_allowable_requests():
    """
    Function that stores the built-out requests for each action_type.

    :return: dict:
            Dictionary that maps all requests belonging to an
            action_type.
    """
    allowable_requests = {
            'workflow': [
                ],
            'command': [
               'gen_comm'
            ]
        }
    for action_type in allowable_requests.keys():
        allowable_requests[action_type] = sorted(allowable_requests[action_type] )
    return allowable_requests


def get_request_description():
    """
    Function that stores the description of each request.

    :return: dict:
            Dictionary that stores request names as keys,
            and descriptions as values.
    """
    return {
        'gen_comm':
            'Executes any command line argument.'
    }


def get_request_additional_arguments():
    """
    Function that stores the additional arguments available
    for an action_type+request

    :return: dict:
            Additional arguments related to an action_type+request.
    """
    return {
        'gen_comm': {
            'command': 'str, required'
        }
    }


def check_additional_arguments(
        request,
        **kwargs
):
    """
    Function that checks that additional arguments passed in for an action_type+request
    are legitimate.

    :param str request:
            The request to check.
    :param dict kwargs:
            The arguments passed for the request, to be checked.
    """
    defined_arguments = get_request_additional_arguments()[request]
    # If there are additional arguments needed, check them.
    if defined_arguments != {}:
        for additional_argument, req_text in defined_arguments.items():
            is_optional ='optional' in req_text
            if additional_argument not in kwargs.keys() and not is_optional:
                raise ValueError(
                    f"Request '{request}' requires the non-optional argument -->"
                    f"'{additional_argument}': {req_text}."
                )
            if (additional_argument in kwargs.keys()) and \
                    (kwargs[additional_argument] in [None, '']):
                raise ValueError(
                    f"Keyword argument {additional_argument} for request {request}"
                    f" cannot be in [None, '']."
                )
        # Check if passe in args keys match defined.
        try:
            assert set(kwargs.keys()) <= set(defined_arguments.keys())
        except AssertionError as bad_additional_argument:
            raise ValueError(
                f"The passed in key(s) [{kwargs.keys()}] are not "
                f"a subset of defined key(s) [{defined_arguments.keys()}]"
            ) from bad_additional_argument


class Allowable:
    """
    Class that contains the allowable actions related to chatt_bot.
    """
    def __init__(
            self
    ):
        self.allowable_actions = get_allowable_actions()
        self.action_description = get_action_description()
        self.allowable_requests = get_allowable_requests()
        self.request_description = get_request_description()

    @property
    def action_description(
            self
    ):
        """Property method for action_description."""
        return self._action_description

    @action_description.setter
    def action_description(
            self,
            action_description
    ):
        """Setter method for action_description"""
        try:
            assert isinstance(
                action_description,
                dict
            )
        except AssertionError as not_a_dict:
            raise TypeError(
                "The action description must be a dictionary, where "
                "the keys of the dictionary match the keys in the "
                "allowable_actions attribute, and the values are a "
                "description of that action."
            ) from not_a_dict
        for action_key in action_description.keys():
            if action_key not in self.allowable_actions.keys():
                raise ValueError(
                    "A key in the action_description attribute must "
                    "exist as a key in the allowable_actions dictionary."
                )
        self._action_description = action_description

    @property
    def request_description(
            self
    ):
        """Property method for request_description"""
        return self._request_description

    @request_description.setter
    def request_description(
            self,
            request_description
    ):
        """Setter method for request_description"""
        try:
            assert isinstance(
                request_description,
                dict
            )
        except AssertionError as not_a_dict:
            raise TypeError(
                "The request description must be a dictionary, where "
                "the keys of the dictionary match a value in the "
                "allowable_requests attribute; and the values are a "
                "description of that value."
            ) from not_a_dict
        for request_key in request_description.keys():
            all_requests = [
                item for sublist in self.allowable_requests.values()
                for item in sublist
            ]
            if request_key not in all_requests:
                raise ValueError(
                    "A key in the action_description attribute must "
                    "exist as a value in the allowable_requests dictionary."
                )
        self._request_description = request_description

    def actions_help_text(
            self
    ):
        """Function that generates help text (not used live)"""
        help_text = '\n' \
                    'ALLOWABLE ACTIONS:\n' \
                    '________________________________\n' \
                    'Below is a list of the allowable actions ' \
                    'that chatt_bot can perform:\n'
        # Iterate over allowable actions, creating help text.
        for single_action, aliases in self.allowable_actions.items():
            help_text = \
                help_text + \
                f'\t  Allowable Action: {single_action}\n' \
                f'\tAcceptable Aliases: {aliases}\n' \
                f'\tAction Description: {self.action_description[single_action]}'
        help_text = help_text + '\n________________________________'
        return help_text

    def request_help_text(
            self
    ):
        """Function that generates help text for request (not used lived)"""
        help_text = '\n' \
                    'ALLOWABLE REQUESTS:\n' \
                    '________________________________\n' \
                    'Below is a list of the allowable requests ' \
                    'that chatt_bot can execute:\n'
        all_requests = [
            item for sublist in self.allowable_requests.values()
            for item in sublist
        ]
        # Iterate over allowable actions, creating help text.
        for single_request in all_requests:
            help_text = \
                help_text + \
                f'\t  Allowable Request: {single_request}\n' \
                f'\tRequest Description: {self.request_description[single_request]}'
        help_text = help_text + '\n________________________________'
        return help_text

    def full_help_text(
            self
    ):
        """Function that generates full help text (not used live)"""
        return self.actions_help_text() + self.request_help_text()


class BotAction(generic_utils.VerboseAttributes):
    """Class that houses all of the actions of chatt_bot."""
    def __init__(
            self,
            action_type = 'w',
            request=None,
            verbose=False
    ):
        """
        Initialization function, that needs the action type and request.

        :param str action_type:
                Action that chatt_bot is expected to perform.
                Currently supports one action-type, "workflow",
                which kicks of a pre-built workflow.
        :param str request:
                The specific request related to the action-type.
                For example, the specific workflow desired to kick-off.
        :param bool verbose:
                Specifies whether user wants all print out statements.
        """
        # Inherit and set verbose attribute
        super().__init__()
        # Specifies built-in actions and requests.
        temp_allowable = Allowable()
        self.allowable_actions = temp_allowable.allowable_actions
        self.allowable_requests = temp_allowable.allowable_requests
        self.action_type = action_type
        self.request = request

    @property
    def action_type(
            self
    ):
        """Property method that sets action type."""
        return self._action_type

    @action_type.setter
    def action_type(
            self,
            action_type
    ):
        """Setter method for action_type."""
        self._action_type = None
        action_type = str(action_type).strip().lower()
        # Ensure action type in allowable actions.
        for action_key, allowed_syntax_list in self.allowable_actions.items():
            if action_type in allowed_syntax_list:
                self._action_type = action_key
                break
        # Raise error if action type not assigned.
        if self._action_type is None:
            raise ValueError(
                f"Value '{action_type}' passed for parameter 'action_type' "
                "not in allowable actions. "
                f"Allowable actions are as follows: {self.allowable_actions}"
            )

    @property
    def request(
            self
    ):
        """Property method for request."""
        return self._request

    @request.setter
    def request(
            self,
            request
    ):
        """Setter method for request."""
        self._request = None
        request = str(request).strip().lower()
        # Ensure action type in allowable actions.
        for allowed_requests in self.allowable_requests[self.action_type]:
            if request in allowed_requests:
                self._request = request
                break
        # Raise error if action type not assigned.
        if self._request is None:
            raise ValueError(
                f"Value '{request}' passed for parameter 'request' "
                "not in allowable request. "
                f"Allowable requests are as follows: {self.allowable_requests}"
            )

    def execute_action(
            self,
            *args,
            **kwargs
    ):
        """
        Function that will execute the instantiated action requested of chatt_bot.

        :param tuple args:
                All passed in positional arguments.
        :param dict kwargs:
                All passed in keyword arguments.
        """
        run_log_name = \
            f"{self.request}_{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')}.txt"
        run_log_location = f"{bot_utils.setup_bot_folders()}\\{run_log_name}"
        start_time = datetime.datetime.now()
        run_log_dict = {
            'action_type': self.action_type,
            'request': self.request,
            'start_time': start_time,
            'end_time': None,
            'run_time': None
        }
        print(
            f"chatt_bot Action started\n"
            f"Action Type: {self.action_type},\n"
            f"    Request: {self.request},\n"
            f" Start Time: {start_time.strftime('%c')}\n"
        )
        print('-'*100)
        # Check the workflow arguments
        check_additional_arguments(
            self.request,
            **kwargs
        )
        # ALL WORKFLOWS BELOW
        # ALL COMMANDS BELOW
        if self.action_type == 'command':
            # Check the workflow arguments
            check_additional_arguments(
                self.request,
                **kwargs
            )
            # GENERIC COMMAND CALL
            if self.request == 'gen_comm':
                try:
                    bot_workflows.execute_general_idle_command(
                        *args,
                        **kwargs
                    )
                except TypeError as bad_arguments:
                    raise TypeError(
                        "Encountered error when trying to run gen_comm. "
                        "You may be missing additional arguments, or have too many.\n"
                        f"The additional_arguments passed in for action_type='{self.action_type}'"
                        f" and request='{self.request}' were {kwargs}.\n\n The built additional"
                        f" arguments for this are "
                    ) from bad_arguments
        # On completion of action, save end time and print log
        end_time = datetime.datetime.now()
        run_time = end_time - start_time
        run_log_dict['end_time'] = end_time.strftime('%c')
        run_log_dict['run_time'] = f"{run_time.total_seconds()}"
        with open(run_log_location, 'w', encoding="utf-8") as run_log_file:
            run_log_file.write(
                str(run_log_dict)
            )
        print('-'*100)
        print(f'Job completed in {run_log_dict["run_time"]} seconds.')
