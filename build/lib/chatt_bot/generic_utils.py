"""
Module that contains generic utility functions/classes.
"""
# Non-native libraries
import requests


class VerboseAttributes:
    """Class that contains boolean attribute verbose."""
    def __init__(
            self,
            verbose=False
    ):
        self.verbose = verbose

    @property
    def verbose(
            self
    ):
        """Property method for verbose attribute."""
        return self._verbose

    @verbose.setter
    def verbose(
            self,
            verbose
    ):
        """
        Setter method for verbose bool.
        """
        # Check that bool is bool.
        try:
            assert isinstance(verbose, bool)
        except AssertionError as bad_bool_value:
            raise ValueError(
                "Instancing keyword argument 'verbose' must be a boolean"
            ) from bad_bool_value
        self._verbose = verbose


def stream_data_to_file(
        url,
        local_file_name,
        chunk_size=1000
):
    """
    Function that saves streamed data to specific location.

    :param str url:
            The valid api/url accessing the data.
    :param str local_file_name:
            A valid file-name, where data will be streamed to.
    :param int chunk_size:
            The chunk-size to read into file.
    """
    # Create request session.
    request_session = requests.Session()
    with request_session.get(url, timeout=2000, stream=True) as response:
        response.raise_for_status()
        # Chunk stream data into file.
        with open(local_file_name, 'wb') as download_file:
            for chunk in response.iter_content(chunk_size=chunk_size):
                download_file.write(chunk)


def pretty_print_dict(
        input_dictionary,
        indent=1,
        depth=0
):
    """
    Function that returns a "pretty" string version of dict, intended to be
    read easily when read.

    :param dict input_dictionary:
            The dict to be stringified and prettied.
    :param int indent:
            How far formatted you want the string.
    :param int depth:
            Used internally, how far sub-dictionaries should be set back.
    :return: str:
            Printer-pretty string version of dict.
    """
    # Bool flag to add comma's after first item in dict.
    needs_comma = False
    # String for any dict will start with a '{'
    return_string = '\t' * depth + '{\n'
    # Iterate over keys and values, building the full string out.
    for key, value in input_dictionary.items():
        # Start with key. If key follows a previous item, add comma.
        if needs_comma:
            return_string = return_string + ',\n' + '\t' * (depth + 1) + str(key) + ': '
        else:
            return_string = return_string + '\t' * (depth + 1) + str(key) + ': '
        # If the value is a dict, recursively call function.
        if isinstance(value, dict):
            return_string = return_string + '\n' + pretty_print_dict(value, depth=depth+2)
        else:
            return_string = return_string + '\t' * indent + str(value)
        # After first line, flip bool to True to make sure commas make it.
        needs_comma = True
    # Complete the dict with a '}'
    return_string = return_string + '\n' + '\t' * depth + '}'
    # Return dict string.
    return return_string


def cast_integer(
        original_object,
        object_name: str,
        length_requirement: int = None
):
    """
    Function that attempts to cast an object to an integer, with additional
    ability to check length.

    :param original_object:
            Any object to be casted to an integer.
    :param str object_name:
            Name of variable being checked.
    :param int length_requirement:
            Length requirement for the casted integer.
    :return: int:
            Returns the successfully casted object as integer.
    """
    # Ensure length check is natural number.
    if length_requirement is not None and int(length_requirement) < 0:
        raise ValueError(
            "Parameter 'length_requirement' must be greater than or equal to zero."
        )
    try:
        original_object = int(original_object)
        if length_requirement is not None and len(str(original_object)) != length_requirement:
            raise ValueError(
                f"Length of  '{original_object}' does not match "
                f"length requirement (length_requirement={length_requirement})."
            )
    except ValueError as not_able_to_cast_to_integer:
        raise TypeError(
            f"The variable '{object_name}' could not be cast "
            "to an integer."
        ) from not_able_to_cast_to_integer
    return original_object
