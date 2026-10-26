from ...extensions import EXTENSIONS
from ...formats.lirc.protocols import PROTOCOLS as LIRC_PROTOCOLS
from ...inputs import INPUTS
from ...outputs import OUTPUTS
from ..base import Command


class FormatsCommand(Command):
    name = "formats"
    help = "list inputs, outputs, protocols and extensions"

    def run(self, args, messages):
        print("Inputs:")
        for input_class in INPUTS:
            item = input_class()
            print("  %-16s %s" % (item.name, item.description))
            print("  %-16s protocols: %s" % ("", ", ".join(item.protocols())))
        print("Outputs:")
        for output_class in OUTPUTS:
            print("  %-16s %s" % (output_class.name, output_class.description))
        print("  %-16s IR protocols: %s" % ("", ", ".join(LIRC_PROTOCOLS)))
        print("Extensions:")
        for extension_class in EXTENSIONS:
            print("  %-16s %s" % (extension_class.name, extension_class.description))
        return 0
