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

parser.add_argument("files", nargs='+', help="path to input files with flags")

breaks = parser.add_mutually_exclusive_group()
breaks.add_argument("-f", "--flag", action="store_true", help="print flag")
breaks.add_argument("-p", "--print", action="store_true", help="print flags")

try:
    argcomplete.autocomplete(parser)
except NameError:
    pass # no bash completion :(

args = parser.parse_args()

# argcomplete has exited by this point, so here comes the actual program code.

import yaml
import re
import sys
import os

scriptname = os.path.basename(sys.argv[0])

# Flag template class
class ft():
    flag = "flag"
    severity = "severity"
    certainty = "certainty"
    info = "info"
    ref = "ref"
    help = "help"

flag_file="flags.yml"

flag_id_regex = '^[0-9a-zA-Z_-]+$'
flag_severities = ["major", "normal", "minor", "wishlist"]
flag_certainties = ["certain", "probable", "possible", "guess"]

def eprint(*args, **kwargs):
    # This is for error and status messages concerning this script.
    # Print on STDERR in case user has redirected STDOUT to a file.
    print(*args, file=sys.stderr, **kwargs) # print to STDERR

def error_msg(msg):
    eprint("%s: Error: %s" % (scriptname, msg))

def flag_error(flag, msg):
    # This is actual program output regarding the validity of the flag.
    # Print on STDOUT so user can redirect this information to a file.
    print("%s: %s" % (flag[ft.flag], msg))

def check_flags_in_alphabetical_order(flag1, flag2):
    capitals_before_lowercase = lambda F: (F[ft.flag].lower(), F[ft.flag])
    if sorted([flag1, flag2], key=capitals_before_lowercase)[0] == flag1:
        return True
    flag_error(flag2, "flags not in alphabetical order")
    return False

def check_flags_unique(flag1, flag2):
    if flag1[ft.flag].lower() != flag2[ft.flag].lower():
        return True
    flag_error(flag2, "duplicate flag")

def check_flag_name_valid(flag):
    if re.match(flag_id_regex, flag[ft.flag]):
        return True
    flag_error(flag, "invalid flag name. Must match regex %s" % flag_id_regex)
    return False

def check_flag_attribute_in_list(flag, attr, lst):
    if flag[attr] in lst:
        return True
    flag_error(flag, "invalid %s '%s'. Must be one of %s" % (attr, flag[attr], lst))
    return False

with open(flag_file, 'r') as stream:
    try:
        flags = list(yaml.load_all(stream))
        if args.print:
            print(flags)
        else:
            print("File '%s' contains %s flags" % (flag_file, len(flags)))
            num_errors = 0
            prev_flag = {ft.flag: "0000000"}
            for flag in flags:
                if not check_flags_in_alphabetical_order(prev_flag, flag): num_errors += 1
                if not check_flags_unique(prev_flag, flag): num_errors += 1
                if not check_flag_name_valid(flag): num_errors += 1
                if not check_flag_attribute_in_list(flag, ft.severity, flag_severities): num_errors += 1
                if not check_flag_attribute_in_list(flag, ft.certainty, flag_certainties): num_errors += 1
                prev_flag = flag
            print("%s errors detected" % num_errors)
    except yaml.YAMLError as e:
        error_msg(e)
