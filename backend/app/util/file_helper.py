import os
from pathlib import Path


def get_file(path_to_file: str):
    root_directory = os.path.dirname(os.path.abspath(__file__))
    custom_model_directory = root_directory + '/custom_model/'
    file = Path(os.path.join(custom_model_directory, path_to_file))
    return file