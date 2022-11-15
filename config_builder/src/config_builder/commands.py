import argparse
import logging
import json
from .loader import load_yaml, LoaderException, ConfigModel
from . import app_config
from jinja2 import (Environment, FileSystemLoader, select_autoescape, TemplateNotFound, StrictUndefined,
                    UndefinedError, Undefined, TemplateSyntaxError)


logger = logging.getLogger('config_builder.commands')


def render_cmd(cli_args: argparse.Namespace) -> None:
    """
    Render configuration files
    :param cli_args: Parsed CLI args
    :return: None
    """
    try:
        config_obj = load_yaml(ConfigModel, 'config', app_config.loader_config.top_level_config)
    except LoaderException as ex:
        logger.critical(f"Failed loading config file: {ex}")
        return

    jinja_env = Environment(
        autoescape=select_autoescape(
            disabled_extensions=('txt', 'j2',),
            default_for_string=True,
            default=True
        ),
        loader=FileSystemLoader(app_config.targets_config.jinja_renderer.templates_dir),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )

    jinja_env.globals = config_obj.dict(by_alias=True)

    for jinja_target in app_config.targets_config.jinja_renderer.targets:
        try:
            rendition = jinja_env.get_template(jinja_target.template).render()

            with open(jinja_target.filename, 'w') as target_file:
                target_file.write(rendition)

        except TemplateNotFound as ex:
            logger.critical(f"Template file not found: {ex}")
        except TemplateSyntaxError as ex:
            logger.critical(f"Template '{jinja_target.template}' error: {ex}")
        except UndefinedError as ex:
            logger.critical(f"Template '{jinja_target.template}' error: {ex}")


def export_cmd(cli_args: argparse.Namespace) -> None:
    """
    Export source configuration as JSON file
    :param cli_args: Parsed CLI args
    :return: None
    """
    try:
        config_obj = load_yaml(ConfigModel, 'config', app_config.loader_config.top_level_config)
        with open(cli_args.file, 'w') as export_file:
            json.dump(config_obj.dict(), export_file, indent=2)

    except LoaderException as ex:
        logger.critical(f"Failed loading config file: {ex}")

    logger.info(f"Exported source configuration as '{cli_args.file}'")


def schema_cmd(cli_args: argparse.Namespace) -> None:
    """
    Generate source configuration JSON schema
    :param cli_args: Parsed CLI args
    :return: None
    """
    with open(cli_args.file, 'w') as schema_file:
        json.dump(ConfigModel.schema(), schema_file, indent=2)

    logger.info(f"Saved configuration schema as '{cli_args.file}'")
