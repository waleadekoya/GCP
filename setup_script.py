import os

# https://stackoverflow.com/questions/1534210/use-different-python-version-with-virtualenv

curr_dir = os.path.dirname(__file__)

os.chdir(curr_dir)

venv_tag = "gcp_venv"


class CreateVirtualEnv:

    install_virtualenv_pkg = "py -m pip install virtualenv"
    venv_directory = os.path.abspath(os.path.join(f"./{venv_tag}"))
    create_venv = f"python -m venv {venv_directory}"
    activate_venv = os.path.abspath(os.path.join(f"./{venv_tag}/Scripts/activate"))
    install_packages = "pip install -r requirements.txt"
    upgrade_pip = "python -m pip install --upgrade pip"

    def __init__(self):
        if not os.path.exists(os.path.abspath(os.path.join(f"./{venv_tag}/Scripts"))):
            # https://docs.python.org/3/library/venv.html#module-venv
            os.mkdir(self.venv_directory)
            os.system(f"{self.install_virtualenv_pkg} & {self.create_venv}")
            print(
                f"'{venv_tag}' virtual environment successfully created! in "
                f"'{os.path.abspath(os.path.join(self.venv_directory))}' "
            )
        self.initial_commands()

    def initial_commands(self):
        os.system(
            f"{self.activate_venv} & {self.install_packages} & {self.upgrade_pip}"
        )


CreateVirtualEnv()
