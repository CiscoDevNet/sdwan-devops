import logging
import logging.config
import logging.handlers
from pathlib import Path
from typing import Any
from .loader import load_metadata


METADATA_FILENAME = "metadata.yaml"


def setup_logging(logging_config: dict[str, Any]) -> None:
    file_handler = logging_config.get("handlers", {}).get("file")
    if file_handler is not None:
        Path(file_handler["filename"]).parent.mkdir(parents=True, exist_ok=True)

    logging.config.dictConfig(logging_config)


app_config = load_metadata(METADATA_FILENAME)
setup_logging(app_config.logging_config)
