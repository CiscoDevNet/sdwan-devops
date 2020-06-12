from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.module_utils.six import PY3, string_types
from ansible.errors import AnsibleError, AnsibleFilterError

try:
    from genie.conf.base import Device, Testbed
    from genie.libs.parser.utils import get_parser
    from genie.utils.diff import Diff
    HAS_GENIE = True
except ImportError:
    HAS_GENIE = False

try:
    from pyats.datastructures import AttrDict
    HAS_PYATS = True
except ImportError:
    HAS_PYATS = False

class FilterModule(object):

    def pyats_parser(self, cli_output, command, os):
        if not PY3:
            raise AnsibleFilterError("Genie requires Python 3")

        if not HAS_GENIE:
            raise AnsibleFilterError("Genie not found. Run 'pip install genie'")

        if not HAS_PYATS:
            raise AnsibleFilterError("pyATS not found. Run 'pip install pyats'")

        device = Device("uut", os=os)

        device.custom.setdefault("abstraction", {})["order"] = ["os"]
        device.cli = AttrDict({"execute": None})

        # import sys;
        # sys.stdin = open('/dev/tty')
        # import pdb;
        # pdb.set_trace()

        try:
            get_parser(command, device)
        except Exception as e:
            raise AnsibleFilterError("Unable to find parser for command '{0}' ({1})".format(command, e))

        try:
            parsed_output = device.parse(command, output=cli_output)
        except Exception as e:
            raise AnsibleFilterError("Unable to parse output for command '{0}' ({1})".format(command, e))

        if parsed_output:
            return parsed_output
        else:
            return None

    def pyats_diff(self, output1, output2):
        if not PY3:
            raise AnsibleFilterError("Genie requires Python 3")

        if not HAS_GENIE:
            raise AnsibleFilterError("Genie not found. Run 'pip install genie'")

        if not HAS_PYATS:
            raise AnsibleFilterError("pyATS not found. Run 'pip install pyats'")

        diff = Diff(output1, output2)

        diff.findDiff()

        return diff


    def filters(self):
        return {
            'pyats_parser': self.pyats_parser,
            'pyats_diff': self.pyats_diff
        }