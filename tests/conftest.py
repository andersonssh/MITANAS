from subprocess import CompletedProcess


def mock_get_contrab():
    return ("# whatever\n* * * * /other\n@reboot /full_path\n"
            "@reboot /full/path0 --example 0 \n@reboot /full_path1")


def mock_subprocess_run(*__, **___):
    return CompletedProcess(
        None,
        0
    )
