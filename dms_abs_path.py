import os


def path_resources_folder() -> str:  # Return abs path resources folder
    abs_path = os.path.abspath("resources/config")
    return abs_path