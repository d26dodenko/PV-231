import os
import sys
from pathlib import Path

import django
import pytest
from django.conf import settings

def pytest_addoption(parser):
    parser.addoption(
        "--casino-project",
        type=Path,
        help="Папка исходного проекта Casino, в которой лежит manage.py",
    )


def pytest_configure(config):
    project_path = config.getoption("--casino-project")
    if project_path is None:
        raise pytest.UsageError("Укажите каталог курсового: --casino-project=ПУТЬ")
    project = project_path.resolve()
    if not (project / "apps" / "games" / "views.py").is_file():
        raise pytest.UsageError(f"Не найден исходный код Casino в каталоге {project}")

    sys.path.insert(0, str(project))
    os.environ["DJANGO_SETTINGS_MODULE"] = "casino.settings"
    settings.DATABASES = {"default": {"ENGINE": "django.db.backends.dummy"}}
    django.setup()
