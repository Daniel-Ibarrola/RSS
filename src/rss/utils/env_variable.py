from typing import Type
import os


class MissingEnvVariableError(ValueError):
    pass


def get_env_variable(name: str, var_type: Type[str] | Type[int] = str) -> str | int:
    """ Check that an environment variable is set in production mode.
    """
    config = os.environ.get("CONFIG", "dev")
    if "prod" in config:
        value = os.environ.get(name, None)
        if value is None:
            raise MissingEnvVariableError(
                f"The env variable {name} is necessary to run the app"
            )
        if var_type is str:
            return value
        elif var_type is int:
            return int(var_type)
        raise ValueError(f"Invalid var type {var_type}")

    if var_type is str:
        return ""
    elif var_type is int:
        return 0
    raise ValueError(f"Invalid var type {var_type}")