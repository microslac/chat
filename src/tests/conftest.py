import pytest
from app.settings.test import TestSettings

test_settings = TestSettings()


@pytest.fixture()
def settings() -> TestSettings:
    return test_settings


instruction = "You are a helpful assistant."


@pytest.fixture()
def llm_instruction():
    return instruction
