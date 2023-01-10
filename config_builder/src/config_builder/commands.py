import argparse
import logging
from typing import Union
from pathlib import Path
from ipaddress import IPv4Interface, IPv4Network
from .loader import load_yaml, LoaderException, ConfigModel
from . import app_config
from jinja2 import (Environment, FileSystemLoader, select_autoescape, TemplateNotFound, StrictUndefined,
                    UndefinedError, TemplateSyntaxError)


logger = logging.getLogger('config_builder.commands')


#
# Custom Jinja2 filters
#
class FilterError(ValueError):
    """ Filter processing exception """
    pass


def read_file_filter(left_value: str) -> str:
    with open(left_value) as f:
        return f.read()


def ipv4_address_filter(left_value: Union[IPv4Interface, str], attribute: str = 'ip') -> str:
    try:
        interface = left_value if isinstance(left_value, IPv4Interface) else IPv4Interface(left_value)
        return str(getattr(interface, attribute))

    except (ValueError, AttributeError) as ex:
        raise FilterError(ex) from None


def ipv4_subnet_filter(left_value: Union[IPv4Network, str], prefix_len: int, subnet_index: int) -> IPv4Network:
    try:
        network = left_value if isinstance(left_value, IPv4Network) else IPv4Network(left_value)
        return list(network.subnets(new_prefix=prefix_len))[subnet_index]

    except IndexError:
        raise FilterError(
            f"subnet_index {subnet_index} is out of bounds for /{prefix_len} subnets in {left_value}") from None
    except ValueError as ex:
        raise FilterError(ex) from None


def ipv4_subnet_host_filter(left_value: Union[IPv4Network, str], host_index: int) -> IPv4Interface:
    try:
        subnet = left_value if isinstance(left_value, IPv4Network) else IPv4Network(left_value)
    except ValueError as ex:
        raise FilterError(ex) from None

    try:
        return IPv4Interface((list(subnet.hosts())[host_index], subnet.prefixlen))
    except IndexError:
        raise FilterError(
            f"host_index {host_index} is out of bounds for /{subnet.prefixlen}") from None


#
# Command implementation
#

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
    custom_filters = {
        'read_file': read_file_filter,
        'ipv4_address': ipv4_address_filter,
        'ipv4_subnet': ipv4_subnet_filter,
        'ipv4_subnet_host': ipv4_subnet_host_filter,
    }
    jinja_env.filters.update(custom_filters)
    jinja_env.globals = config_obj.dict(by_alias=True)

    for jinja_target in app_config.targets_config.jinja_renderer.targets:
        try:
            target_path = Path(jinja_target.filename)
            if not cli_args.update and target_path.exists():
                logger.info(f"Skipped '{jinja_target.filename}' target, file already exists")
                continue

            rendition = jinja_env.get_template(jinja_target.template).render()

            with open(target_path, 'w') as target_file:
                target_file.write(rendition)

            logger.info(f"Rendered {jinja_target.description}: '{jinja_target.template}' -> '{jinja_target.filename}'")

        except TemplateNotFound as ex:
            logger.critical(f"Template file not found: {ex}")
        except TemplateSyntaxError as ex:
            logger.critical(f"Template '{jinja_target.template}' syntax error: {ex}")
        except UndefinedError as ex:
            logger.critical(f"Template '{jinja_target.template}' error: {ex}")
        except FilterError as ex:
            logger.critical(f"Template '{jinja_target.template}' filter error: {ex}")


def export_cmd(cli_args: argparse.Namespace) -> None:
    """
    Export source configuration as JSON file
    :param cli_args: Parsed CLI args
    :return: None
    """
    try:
        config_obj = load_yaml(ConfigModel, 'config', app_config.loader_config.top_level_config)
        with open(cli_args.file, 'w') as export_file:
            export_file.write(config_obj.json(by_alias=True, indent=2))

        logger.info(f"Exported source configuration as '{cli_args.file}'")

    except LoaderException as ex:
        logger.critical(f"Failed loading config file: {ex}")


def schema_cmd(cli_args: argparse.Namespace) -> None:
    """
    Generate source configuration JSON schema
    :param cli_args: Parsed CLI args
    :return: None
    """
    with open(cli_args.file, 'w') as schema_file:
        schema_file.write(ConfigModel.schema_json(indent=2))

    logger.info(f"Saved configuration schema as '{cli_args.file}'")
