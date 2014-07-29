__author__ = 'bluabk'

# Import necessary modules
import socket           # A rather useful network tool
import time             # For time-based greeting functionality

# Project-specific modules
import ConfigParser, io
import samba    # for server-specific samba functionality

# Some basic and/or static configuration
run = True

# Read the rest from file


class binfo: # Shizu's config class
    config = ConfigParser.RawConfigParser()

    def __init__ (self):
        self.config.read("config.ini")

    def server(self):
        return self.config.get('irc', 'server')

    def spass(self):
        return self.config.get('irc', 'password')

    def port(self):
        return self.config.get('irc', 'port')

    def chan(self):
        return self.config.get('irc', 'channel')

    def nick(self):
        return self.config.get('irc', 'nickname')

    def cmdsym(self):
        return self.config.get('irc', 'cmdsymbol')

    def quitmsg(self):
        return self.config.get('irc', 'quit-message')

    def quitpro(self):
        return self.config.get('irc', 'quit-protection')

    def nspass(self):
        return self.config.get('nickserv', 'password')

bI = binfo()


def commands(nick, chan, msg):
    # syntax: elif msg.find(nick + ": <trigger>") != 1:
    if msg.find(bI.cmdsym() + "awesome") != -1:
        sendmsg("Everything is awesome!")
    elif msg.find(bI.cmdsym() + "smblogins") != -1:
        for item in xrange(len(samba.getLogins())):
            sendmsg("%s@%s        [ID: %s]" % (samba.getLogins()[item].name, samba.getLogins()[item].host, samba.getLogins()[item].id))
    elif msg.find(bI.cmdsym() + "nyaa") != -1:
        nyaa()
    elif msg.find(bI.cmdsym() + "quit%s" % bI.quitpro()) != -1:
        quit()
    elif ircmsg.find(bI.cmdsym() + "help") != -1:
        ircsock.send("PRIVMSG %s :Syntax incorrect, please rephrase.\r\n" % chan)


def triggers(usernick, chan, msg, raw):  # TODO : Doesn't work apparently =/
    global nick
    if raw.find(":Hello " + nick) != -1:  # If someone greets me, I will greet back.
        greeter = ircmsg.strip(":").split("!")[0]
        sendmsg((getGreeting(greeter)))
    elif msg.find((":hi " or ":Hi " or ":ohi ") + nick) != -1:  # If someone greets me, I will greet back.
        sendmsg("H-h...Hi there")


def ping():
    ircsock.send("PONG :Pong\n")


def sendmsg(msg): # TODO : implement across code
    global chan
    ircsock.send("PRIVMSG %s :%s\r\n" % (chan, msg))


def debug(msg):
    global chan
    ircsock.send("PRIVMSG %s :DEBUG: %s\r\n" % (chan, msg))


def join(chan):
    ircsock.send("JOIN " + chan + "\n")


def getGreeting(greeter):
    t = int(time.strftime("%H"))
    debug(str(t))
    if t >= 17 or t < 4:
        greeting = "Konbanwa"
    elif t >= 12:
        greeting = "Konnichiwa"
    elif t >= 4:
        greeting = "Ohayou gozaimasu"
    else:
        greeting = "ohi dur"

    return "%s %s~" % (greeting,  greeter)


def nyaa():
    sendmsg("Nyaa~")


def quit():
    global run
    run = False

if __name__ == "__main__":
    # Connect to the the server
    ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ircsock.connect((bI.server(), bI.port()))
    #if server_pass != "" {
    #    ircsock.send("PASS " + server_pass + "\n")
    #}

    # Register with the server
    ircsock.send("USER " + bI.nick() + " " + bI.nick() + " " + bI.nick() + " :Nibiiro Shizuka\n")
    ircsock.send("NICK " + bI.nick() + "\n")

    while run:
        ircmsg = ircsock.recv(2048)             # Receive data from the server
        ircraw = ircmsg                         # Keep a raw handle
        ircmsg = ircmsg.strip("\n\r")           # Remove protocol junk (linebreaks and return carriage)
        print(ircmsg)                           # print received data

        if ircmsg.find("PING :") != -1:  # Gotta pong that ping...pong..<vicious cycle>
            ping()

        if ircmsg.find("NOTICE %s :This nickname is registered" % bI.nick()) != -1:
            ircsock.send("PRIVMSG NickServ :identify %s\r\n" % bI.nspass())

        if ircmsg.find("NOTICE Auth :Welcome") != -1:
            join(chan)

        if ircmsg.find(' PRIVMSG ') != -1:
            usernick = ircmsg.split('!')[0][1:]
            chan = ircmsg.split(' PRIVMSG ')[-1].split(' :')[0]
            commands(usernick, chan, ircmsg)
            triggers(usernick, chan, ircmsg, ircraw)

# See ya!
ircsock.send("QUIT %s\r\n" % bI.quitmsg())
ircsock.close()