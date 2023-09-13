from typing import Type, Literal
import os


class MissingEnvVariableError(ValueError):
    pass


def get_env_variable(
        name: str,
        var_type: Type[str] | Type[int] = str,
        service: Literal["cap", "api"] = "cap"
) -> str | int:
    """ Check that an environment variable is set in production mode.

        This function should only be called by production config classes.
        In dev mode, this variables will be set to an empty string.

        :param name: Name of the env variable.
        :param var_type: The type of variable that will be returned.
        :param service: The service that is running. Can be 'api' or 'cap'. This is used
            so there are no problems with undefined variables that the current service
            does not require.

        :return: The value of the env variable.
    """
    if "dev" in os.environ.get("CONFIG", "dev"):
        return ""

    if service != os.environ.get("SERVICE", "cap"):
        return ""

    value = os.environ.get(name, None)
    if value is None:
        raise MissingEnvVariableError(
            f"The env variable {name} is necessary to run the app"
        )
    if var_type is str:
        return value
    elif var_type is int:
        return int(value)

    raise TypeError(f"Invalid var type {var_type}")
