"""
Module that contains methods of directory manipulation.
"""
# Native libraries
import getpass
import pathlib

def get_user_path():
    """Function that determines the user path."""
    # get the name of the local user running program.
    local_user = getpass.getuser()
    user_path = f'C:\\Users\\{local_user}'
    return user_path


def setup_documents_folder(
        folder_name
):
    """
    Function that creates a folder in the {user}\\Documents directory.

    :param str folder_name:
            Name of folder/folders to create under {user}\\Documents.
    :return: str:
            Returns the directory path created.
    """
    user_path = get_user_path()
    directory_path = f"{user_path}\\Documents\\{folder_name}"
    # create the folder
    pathlib.Path(directory_path).mkdir(parents=True, exist_ok=True)
    return directory_path
