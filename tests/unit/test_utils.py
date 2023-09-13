import os
import pytest
from rss.utils.env_variable import get_env_variable, MissingEnvVariableError


class TestGetEnvVariable:

    @pytest.fixture
    def prod_config(self):
        os.environ["CONFIG"] = "prod"

    def test_gets_str_variable(self, prod_config):
        os.environ["TEST_VAR"] = "hello world"
        value = get_env_variable("TEST_VAR", str)
        assert value == "hello world"

    def test_gets_int_variable(self, prod_config):
        os.environ["TEST_VAR"] = "20"
        value = get_env_variable("TEST_VAR", int)
        assert value == 20

    def test_raises_error_if_variable_is_not_set(self, prod_config):
        name = "MISSING_VAR"
        match = f"The env variable {name} is necessary to run the app"
        with pytest.raises(MissingEnvVariableError, match=match):
            get_env_variable(name)

    def test_raises_error_if_invalid_type_is_used(self, prod_config):
        os.environ["TEST_VAR"] = "hello world"
        with pytest.raises(TypeError):
            get_env_variable("TEST_VAR", list)

    def test_return_empty_string_on_dev_mode(self):
        os.environ["CONFIG"] = "dev"
        os.environ["TEST_VAR"] = "hello world"
        assert get_env_variable("TEST_VAR") == ""

    def test_does_not_raise_error_for_missing_var_if_service_is_different(self, prod_config):
        os.environ["SERVICE"] = "api"
        name = "MISSING_VAR"
        value = get_env_variable(name, service="cap")
        assert value == ""
