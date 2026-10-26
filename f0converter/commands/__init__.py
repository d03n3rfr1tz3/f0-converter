from .convert.lirc import LircCommand
from .convert.rf433 import Rf433Command
from .info.formats import FormatsCommand

# in the order of the help text
COMMANDS = (Rf433Command, LircCommand, FormatsCommand)
