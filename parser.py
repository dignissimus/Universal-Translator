from arpeggio import Optional, ZeroOrMore, OneOrMore, EOF
from arpeggio import RegExMatch as _


def document():
    return [multi_line_document, single_line_document]


def multi_line_document():
    return line, OneOrMore(newline, line), EOF


def single_line_document():
    return line, ZeroOrMore(newline), EOF


def line():
    return [(entry, optional_whitespace, Optional(comment)), comment, ""]


def comment():
    return ["//", "#"], ZeroOrMore(_(r"[^\n]"))


def entry():
    return sound_change


def sound_change():
    return sound_list, arrow, r_sound_list, Optional(context)


def context():
    return optional_whitespace, "/", optional_whitespace, context_description


def context_description():
    return [both_desc, left_desc, right_desc]


def both_desc():
    return description, delim, description


def left_desc():
    return description, delim


def right_desc():
    return delim, description


def delim():
    return ["__", "_"]


def description():
    return OneOrMore(description_sound)


def description_sound():
    return sound, Optional(modifier)


def modifier():
    return "[+short]"


def text():
    return _("[A-z]+")


def arrow():
    return optional_whitespace, ">", optional_whitespace


def r_sound_list():
    return sound, ZeroOrMore((optional_whitespace, sound))


def sound_list():
    return sound_item, ZeroOrMore((optional_whitespace, sound_item))


def sound_item():
    return [many_sounds, sound]


def many_sounds():
    return "{", OneOrMore(sound), ZeroOrMore(comma, OneOrMore(sound)), "}"


def comma():
    return optional_whitespace, ",", optional_whitespace


def sound():
    return [aspirated_sound, long_sound, base_sound]


def aspirated_sound():
    return [long_sound, base_sound], "ʱ"


def long_sound():
    return base_sound, ["ː", ":"]


def base_sound():
    return _(r"[^\s/\n>\^\$#_:ː\[\]{},]")


def optional_whitespace():
    return ZeroOrMore(whitespace)


def whitespace():
    return _(r"[ \t]")


def newline():
    return _(r"\n")
