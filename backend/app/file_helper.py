import os
from pathlib import Path


def get_file(path_to_file: str) -> Path:
    """ Use this method to access files in the custom_model directory this ensures the functionality on every
    computer and also in docker.
    Example: file lies in /custom_model/my_labels.json --> json.load(open(get_file("labels_map.txt"), "r"))

    :param path_to_file: relative to the custom_model directory
    :return: path to the file
    """

    root_directory = os.path.dirname(os.path.abspath(__file__))
    custom_model_directory = root_directory + '/custom_model/'
    file = Path(os.path.join(custom_model_directory, path_to_file))
    return file
