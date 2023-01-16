"""
SDWAN Config Builder Tool

"""
import argparse
import logging
from datetime import date
from .__version__ import __version__ as version
from .commands import render_cmd, export_cmd, schema_cmd


logger = logging.getLogger('sdwan_config_builder.main')


def main():
    cli_parser = argparse.ArgumentParser(description=__doc__)
    cli_parser.add_argument("--version", action="version", version=f"SDWAN Config Builder Tool Version {version}")
    commands = cli_parser.add_subparsers(title="commands")
    commands.required = True

    render_parser = commands.add_parser("render", help="render configuration files")
    render_parser.set_defaults(cmd_handler=render_cmd)
    render_parser.add_argument("-u", "--update", action="store_true",
                               help="override target files that already exist, by default they are skipped")

    export_parser = commands.add_parser("export", help="export source configuration as JSON file")
    export_parser.set_defaults(cmd_handler=export_cmd)
    export_parser.add_argument("-f", "--file", metavar="<filename>", default=f"config_{date.today():%Y%m%d}.json",
                               help="export filename (default: %(default)s)")

    schema_parser = commands.add_parser("schema", help="generate source configuration JSON schema")
    schema_parser.set_defaults(cmd_handler=schema_cmd)
    schema_parser.add_argument("-f", "--file", metavar="<filename>", default=f"config_schema.json",
                               help="export filename (default: %(default)s)")

    cli_args = cli_parser.parse_args()
    try:
        cli_args.cmd_handler(cli_args)
    except KeyboardInterrupt:
        logger.critical("Interrupted by user")


if __name__ == '__main__':
    main()
