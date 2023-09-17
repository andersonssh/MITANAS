from mitanas import StartupHandler
from tests.conftest import mock_subprocess_run, mock_get_contrab
from unittest.mock import patch, call
from shlex import quote


def test_startup_handler_attrs():
    startup_handler = StartupHandler("/full/path")
    assert startup_handler.main_command == "@reboot /full/path"
    assert startup_handler.full_command == "@reboot /full/path"

    startup_handler = StartupHandler("/full/path2", ["--example 1", "--ex 2"])
    assert startup_handler.main_command == "@reboot /full/path2"
    assert startup_handler.full_command == "@reboot /full/path2 --example 1 --ex 2"


@patch("mitanas.mitanas.CrontabManager.get_crontab", mock_get_contrab)
def test_already_exists_at_startup():
    startup_handler = StartupHandler("/full/path0", ["--example 0"])
    assert startup_handler.already_exists_at_startup() == "@reboot /full/path0 --example 0"
    startup_handler = StartupHandler("/full_path")
    assert startup_handler.already_exists_at_startup() == "@reboot /full_path"
    startup_handler = StartupHandler("/full_path1")
    assert startup_handler.already_exists_at_startup() == "@reboot /full_path1"


@patch("mitanas.mitanas.CrontabManager.get_crontab", mock_get_contrab)
@patch("subprocess.run", return_value=mock_subprocess_run())
def test_add_at_startup(mock_subprocess):
    startup_handler = StartupHandler("/full/path", ["--ex 2"])
    startup_handler.add_at_startup()
    new_contrab = mock_get_contrab().strip() + "\n" + startup_handler.full_command
    assert mock_subprocess.call_args == call(
        f"echo {quote(new_contrab)} | crontab -", shell=True, stdout=-1, stderr=-1
    )
