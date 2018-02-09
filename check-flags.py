#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK - see https://argcomplete.readthedocs.io/

# Argcomplete generates Bash completions dynamically by running the file up to
# the point where arguments are parsed. Want minimal code before this point.

import argparse

try:
    import argcomplete
except ImportError:
    pass # no bash completion :(

parser = argparse.ArgumentParser()

parser.add_argument("scores", nargs='+', help="path to input files with flags")

breaks = parser.add_mutually_exclusive_group()
breaks.add_argument("-f", "--flag", action="store_true", help="print flag")
breaks.add_argument("-p", "--print", action="store_true", help="print flags")

try:
    argcomplete.autocomplete(parser)
except NameError:
    pass # no bash completion :(

args = parser.parse_args()

# argcomplete has exited by this point, so here comes the actual program code.

import flags
import score
import re
import sys
import os
import xml.etree.ElementTree as ET   # XML parser: <tag attrib="val">text</tag>

class FlagArcoOrPizzTextLacksChannelChange(flags.Flag):
    name = "arco-or-pizz-text-lacks-channel-change"
    foo = "bar"

    def check(self, score):
        print("Checking! name=%s severity=%s foo=%s" % (self.name, self.severity, self.foo))

scriptname = os.path.basename(sys.argv[0])

flag_file="flags.yml"
flgs = flags.load_flags(flag_file)

def eprint(*args, **kwargs):
    # This is for error and status messages concerning this script.
    # Print on STDERR in case user has redirected STDOUT to a file.
    print(*args, file=sys.stderr, **kwargs) # print to STDERR

def error_msg(msg):
    eprint("%s: Error: %s" % (scriptname, msg))

def flag_error(flag, msg):
    # This is actual program output regarding the validity of the flag.
    # Print on STDOUT so user can redirect this information to a file.
    print("%s: %s" % (flag.name, msg))

if args.print:
    print(flgs)
else:
    # flags_list = []
    # flags_list.append(FlagArcoOrPizzTextLacksChannelChange(flags[0]))
    # flags_list[0].check()
    flgs[0].promote(FlagArcoOrPizzTextLacksChannelChange)
    flgs[0].check(None)
    # print("File '%s' contains %s flags" % (flag_file, len(flags)))
    # num_errors = 0
    # prev_flag = flags[0]
    # for flag in flags:
    #     prev_flag = flag
    # print("%s errors detected" % num_errors)
