__author__ = 'BluABK <abk@blucoders.net'

# TODO: Load smbstatus on demand
# TODO: Load smbstatus' BATCHes into separate command
# TODO: Implement user exemption
# TODO: Implement path exemption
# TODO: Add try and SomeReasonableExceptionHandler across code
# TODO: Implement support for checking that samba installation is sane and contains all required binaries and libraries
# TODO: Implement nowplaying() that fetches BATCH media files from smbstatus for SambaUsers, ex: !np Heretic121
import ConfigParser
import os
import re
from sys import exc_info
from subprocess import check_output

# Define variables

regex = re.compile(" +")


class Config:  # Shizu's config class
    config = ConfigParser.RawConfigParser()

    def __init__(self):
        self.config.read(os.getcwd() + '/' + "config.ini")

    def loadconfig(self):
        configloc = os.getcwd() + '/' + "config.ini"
        print(configloc)
        self.config.read(configloc)
        return True

    def rawlogins(self):
        return str(self.config.get('samba', 'smbstatus-command'))

    def excludelogins(self):
        return str(self.config.get('samba', 'exclude-names'))

    def excludepaths(self):
        return str(self.config.get('samba', 'exclude-paths'))

cfg = Config()


class SambaUser:
    name = ''
    uid = 0
    host = ''
    playing = ''

    def __init__(self, uid, name, host):
        self.name = name
        self.uid = uid
        self.host = host

        def setplaying(media):
            self.playing = media

        def nowplaying():
            return self.playing


def getplaying():
    return True


def getlogins(msg):
    global cfg
    cfg.loadconfig
    loginhandlesraw = check_output(cfg.rawlogins(), shell=True)
    loginhandles = loginhandlesraw.splitlines()
    sambausers = list()
    indent = 4

    for index, line in enumerate(loginhandles):
        # throw out empty lines
        if not len(line):
            continue

        tmpline = regex.split(line)
        splitline = list()

        for test in tmpline:
            if not ' ' in test:
                splitline.append(test)

        if len(splitline) < 4:
            # TODO investigate
            print "samba/getlogins: splitline has not enough items, are you root?"
        else:
            sambausers.insert(index, SambaUser(splitline[0], splitline[1], splitline[3]))

    loginlist = list()

    longestname = 0
    maxspacing = ''
    spacing = ''
    try:
        for item in xrange(len(sambausers)):
            if not len(msg) or sambausers[item].name in msg:
                if len(sambausers[item].name) > longestname: longestname = len(sambausers[item].name)
        for i in range(0, longestname+indent):
            maxspacing += " "
        loginlist.append("user@host%sID" % maxspacing)
        for item in xrange(len(sambausers)):
            if not len(msg) or sambausers[item].name in msg:
                #if excluded user
                for i in range(0, maxspacing - len(sambausers[item].name)):
                    spacing += " "
                loginlist.append("%s@%s%s[ID: %s]" % (sambausers[item].name, sambausers[item].host, spacing, sambausers[item].uid))
    except:
        loginlist.append("Ouch, some sort of unexpected exception occurred, have fun devs!")
#        loginlist.append("Exception:")
#        for err in xrange(len(exc_info())):
#            loginlist.append(exc_info()[err])
        raise
    return loginlist


def helpcmd():
    cmdlist = list()
    cmdlist.append("Syntax: samba command arg1..argN")
    cmdlist.append("Available commands: logins* (* command contains sub-commands)")
    return cmdlist
