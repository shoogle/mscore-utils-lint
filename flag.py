import yaml
import re

class FlagInvalid(Exception):
    pass

class Flag(object):
    name_regex = '^[0-9a-zA-Z_-]+$'
    severities = ["major", "normal", "minor", "wishlist"]
    certainties = ["certain", "probable", "possible", "guess"]

    def __init__(self, dictionary):
        self.name               = dictionary['flag']
        self.severity           = dictionary['severity']
        self.certainty          = dictionary['certainty']
        self.info               = dictionary['info']
        if 'affected-strings' in dictionary:
            self.affected_strings   = dictionary['affected-strings']
            self.list_attribute_is_alphabetical_and_unique("affected-strings", self.affected_strings)
        self.ref                = dictionary['ref']
        self.help               = dictionary['help']
        self.self_check()

    def promote(self, subclass):
        if self.name != subclass.name:
            print("Error!")
        self.__class__ = subclass

    def self_check(self):
        self.attribute_matches_pattern("name", self.name, self.name_regex)
        self.attribute_in_list("severity", self.severity, self.severities)
        self.attribute_in_list("certainty", self.certainty, self.certainties)

    def attribute_matches_pattern(self, attr_name, attr, pattern):
        if not re.match(pattern, attr):
            raise FlagInvalid("%s: %s '%s' invalid. Must match regex '%s'." % (self.name, attr_name, attr, pattern))

    def attribute_in_list(self, attr_name, attr, lst):
        if attr not in lst:
            raise FlagInvalid("%s: Unrecognised %s '%s'. Must be one of %s." % (self.name, attr_name, attr, lst))

    def list_attribute_is_alphabetical_and_unique(self, attr_name, lst_attr):
        capitals_before_lowercase = lambda item: (item.lower(), item) # CAR before Car before car
        prev_item = lst_attr[0]
        for item in lst_attr[1:]:
            if item == prev_item:
                raise FlagInvalid("%s: %s list contains duplicate item '%s'." % (self.name, attr_name, item))
            elif sorted((prev_item, item), key=capitals_before_lowercase)[0] != prev_item:
                raise FlagInvalid("%s: %s list item '%s' not in alphabetical order." % (self.name, attr_name, item))
            prev_item = item

class FlagList(list):

    def check(self):
        pass

    def self_check(self):
        pass

def load_flags(flag_file):
    flags = []
    prev_flag = None
    stream = open(flag_file, 'r')
    try:
        for f in list(yaml.load_all(stream)):
            flag = Flag(f)
            if prev_flag:
                flag.list_attribute_is_alphabetical_and_unique("flag", (prev_flag.name, flag.name))
            flags.append(flag)
            prev_flag = flag
    except yaml.YAMLError as e:
        raise FlagInvalid(e)
    return flags

print(load_flags("flags.yml")[0].name)
