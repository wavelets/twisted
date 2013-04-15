
from twisted.tubes.tube import Tube
from twisted.tubes.framing import bytesToLines, linesToBytes
from twisted.tubes.protocol import factoryFromFlow
from twisted.internet.defer import Deferred
from twisted.internet.endpoints import TCP4ServerEndpoint

from intparse import LinesToIntegersOrCommands
from worker import CommandsAndIntegersToResultIntegers
from output import IntegersToLines

def mathFlow(fount, drain):
    (fount.flowTo(Tube(bytesToLines()))
          .flowTo(Tube(LinesToIntegersOrCommands()))
          .flowTo(Tube(CommandsAndIntegersToResultIntegers()))
          .flowTo(Tube(IntegersToLines()))
          .flowTo(Tube(linesToBytes()))
        .flowTo(drain))

def main(reactor, port="4321"):
    endpoint = TCP4ServerEndpoint(reactor, int(port))
    endpoint.listen(factoryFromFlow(mathFlow))
    return Deferred()

from twisted.internet.task import react
from sys import argv
react(main, argv[1:])