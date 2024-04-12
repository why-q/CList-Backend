import sys
from pathlib import Path

from dynaconf import Dynaconf

_BASE_DIR = Path(__file__).parent.parent
_settings_files = [
    Path(__file__).parent / "settings.yml",
]
_external_files = [Path(sys.prefix, "etc", "app", "settings.yml")]


settings = Dynaconf(
    envvar_prefix="APP",
    settings_files=_settings_files,
    environments=False,
    load_dotenv=True,
    env_switcher="APP_ENV",
    lowercase_read=True,
    includes=_external_files,
    base_dir=_BASE_DIR,
)


print(_external_files)
