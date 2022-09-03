import tempfile
from unittest.mock import Mock, patch

import pytest

from sucks.cli import *


def test_config_file_name():
    if platform.system() == "Windows":
        print(config_file())
        assert re.match(
            r"[A-Z]:\\.+\\\w+\\AppData(\\Roaming)?\\sucks.conf", config_file()
        )
    else:
        assert re.match(r"/.+/\w+/.config/sucks.conf", config_file())


def test_write_and_read_config():
    with patch(
        "sucks.cli.config_file",
        Mock(
            return_value=os.path.join(
                tempfile.mkdtemp(), "some_other_dir", "sucks.conf"
            )
        ),
    ):
        write_config({"a": "ayyy", "b": 2})
        config2 = read_config()
        assert config2["a"] == "ayyy"
        assert config2["b"] == "2"


def test_frequency_param_type():
    t = FREQUENCY
    assert t.convert("0", None, None) == 0
    assert t.convert("1", None, None) == 1.0
    assert t.convert("1/2", None, None) == 0.5
    assert t.convert("1/7", None, None) == 1.0 / 7.0
    assert t.convert("1/14", None, None) == 1.0 / 14.0
    assert t.convert("1/1000", None, None) == 1.0 / 1000.0
    assert t.convert("1.5/2", None, None) == 1.5 / 2.0
    assert t.convert("0/2", None, None) == 0
    with pytest.raises(click.exceptions.BadParameter):
        t.convert("bob", None, None)
    with pytest.raises(click.exceptions.BadParameter):
        t.convert("2", None, None)
    with pytest.raises(click.exceptions.BadParameter):
        t.convert("7/5", None, None)
    with pytest.raises(click.exceptions.BadParameter):
        t.convert("1/0", None, None)


def test_should_run():
    count = 0
    for _ in range(10000):
        if should_run(0.1):
            count += 1
    assert count == pytest.approx(1000, 200)

    count = 0
    for _ in range(10000):
        if should_run(0.9):
            count += 1
    assert count == pytest.approx(9000, 200)


def test_continent_for_country():
    assert continent_for_country("us") == "na"
    assert continent_for_country("fr") == "eu"
