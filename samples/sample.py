__author__ = 'BluABK <abk@blucoders.net'

# This is a module specification, which contains everything you need to get started on writing a module.

# Imports
import ConfigParser
import os

import colours as clr


# Variables
my_name = os.path.basename(__file__).split('.', 1)[0]
my_colour = ""
commandsavail = "wishfulthinking, pipedreams, 42, imagination"


# Classes


class Config:  # Mandatory Config class
    config = ConfigParser.RawConfigParser()

    def __init__(self):
        print "%s[%s]%s:\t Initiating config..." % (my_colour, my_name, clr.off)
        self.config.read('config.ini')

    def sample(self):
        return str(self.config.get('sample', 'sampleitem'))


cfg = Config()


# Functions


def helpcmd(cmdsym):
    cmdlist = list()
    cmdlist.append("Syntax: %scommand help arg1..argN" % cmdsym)
    cmdlist.append("Available commands: %s (* command contains sub-commands)" % commandsavail)
    return cmdlist
