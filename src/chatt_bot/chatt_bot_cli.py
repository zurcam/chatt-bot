"""
Module that kicks off chatt_bot workflow.
"""
import ast
# Custom modules
from chatt_bot import generic_utils
from chatt_bot import robot_actions
# Non-native libraries
import typer

app = typer.Typer(help="chatt_bot cli")

@app.command(
    help='Welcome to chatt_bot, which is a a simple CLI tool '
         'that easily allows for the exploration of Chattanooga. \n\n'
         'chatt_bot takes in two required arguments: '
         '1) action_type and 2) request.'
         ' The available action_types (and aliases) are:\n ' +
         str(robot_actions.get_allowable_actions()) +
         '. \nAs for a request, request is the specific action_type you want'
         ' to kick off. '
         'The available requests are:\n' + str(robot_actions.get_allowable_requests())
)

def kickoff(
        action_type: str = typer.Argument(
            ..., help="The action you want to perform."
        ),
        request: str = typer.Argument(
            ..., help="The specific request related to action_type."
        ),
        add_args: str = typer.Option(
            '{}', help='Dictionary of other arguments in string form.'
        ),
        describe: bool = typer.Option(
            False,
            help='Describes a specific action_type/request. '
                 'If added, then describes (but does not run), action_type/request.'
        )
):
    """
    Kicks off a chatt_bot job.
    """
    allowable_action_types = robot_actions.get_allowable_actions()
    action_type = str(action_type).strip().lower().replace("'", "").replace('"', "")
    # Format string args
    original_arg_string = add_args
    # try to convert additional args to dictionary
    try:
        add_args = ast.literal_eval(original_arg_string)
    except (ValueError, SyntaxError):
        add_args = str(original_arg_string).replace("}","").replace("{","")
        add_args = add_args.replace("'", "").replace('"','')
        add_args = {
            i.split(':')[0]: i.split(':')[1] for i in add_args.split(',')
        }
    # Ensure action_type is listed in built-out options.
    for built_action_type in allowable_action_types.keys():
        if action_type in allowable_action_types[built_action_type]:
            action_type = built_action_type
    try:
        assert action_type in allowable_action_types.keys()
    except AssertionError as bad_action_type:
        raise ValueError(
            f"action_type='{action_type}' not recognized. "
            f"Allowable action_type list: {allowable_action_types.keys()}"
        ) from bad_action_type
    # Ensure action_type/request are valid.
    request = str(request).strip().lower().replace("'", "").replace('"', "")
    try:
        assert request in robot_actions.get_allowable_requests()[action_type]
    except AssertionError as request_not_found:
        allowable_list = robot_actions.get_allowable_requests()[action_type]
        allowable_list.sort()
        raise ValueError(
            f"Request {request} not found for action_type='{action_type}'.\n"
            f"Available requests for action_type='{action_type}' are:\n"
            f"{allowable_list}"
        ) from request_not_found
    # Check if user wants to describe action_type/request:
    if describe:
        try:
            description= {
                'action_type': action_type,
                'request': request,
                'description': robot_actions.get_request_description()[
                    request
                ]
            }
            # Get the all possible additional args.
            try:
                more_args = robot_actions.get_request_additional_arguments()[request]
                more_args = None if more_args == {} else more_args
            except KeyError:
                more_args = None
            finally:
                description['Additional Arguments'] = more_args
            description = generic_utils.pretty_print_dict(
                description
            )
        except KeyError:
            description = "Description not built for " \
                        f"action_type='{action_type}', request='{request}'"
        print(description)
        return
    # Check additional arguments
    robot_actions.check_additional_arguments(
        request,
        **add_args
    )
    # Call the bot action.
    robot_actions.BotAction(
        action_type=action_type,
        request=request
    ).execute_action(**add_args)


if __name__ == "__main__":
    app()
