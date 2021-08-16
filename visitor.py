import itertools
import panphon
from enum import Enum, auto

from arpeggio import PTNodeVisitor, visit_parse_tree

FT = panphon.FeatureTable()


class DocumentVisitor(PTNodeVisitor):
    def visit_document(self, node, children):
        # TODO: Decide on whether to replace entries as I'm doing now or to add entries by appending or concatenating
        entries = []
        for document in node:
            entries = visit_parse_tree(document, self)

        return entries

    def visit_multi_line_document(self, node, children):
        entries = []
        for line in node:
            if line.rule_name == "line":
                entries += visit_parse_tree(line, self)

        return entries

    def visit_single_line_document(self, node, children):
        return self.visit_multi_line_document(node, children)

    def visit_line(self, node, children):
        entries = []
        for entry in node:
            if entry.rule_name == "entry":
                entries += visit_parse_tree(entry, self)

        return entries

    def visit_entry(self, node, children):
        entries = []
        sources = node[0]
        _arrow = node[1]
        destination = node[2]
        context = None
        if len(node) >= 4:
            context = node[3]
            context = visit_parse_tree(context, self)

        sources = visit_parse_tree(sources, self)
        destination = visit_parse_tree(destination, self)

        for source in sources:
            entries.append(Entry(source, destination, context))

        return entries

    def visit_sound_list(self, node, children):
        raw_sounds = []
        for sound_item in node:
            if sound_item.rule_name == "sound_item":
                new_sounds = visit_parse_tree(sound_item, self)
                raw_sounds.append(new_sounds)

        sounds = itertools.product(*raw_sounds)
        return sounds

    def visit_r_sound_list(self, node, children):
        sounds = []
        for sound in node:
            if sound.rule_name == "sound":
                sounds.append(visit_parse_tree(sound, self))

        return sounds

    def visit_sound_item(self, node, children):
        # TODO: Maybe go back to using a list, if strings are too difficult to handle
        # With this I mean that the individual sounds in the source/destination
        # Will be elements of a list
        # As opposed to characters in a string
        for sound in node:
            if sound.rule_name == "sound":
                return [visit_parse_tree(sound, self)]
            elif sound.rule_name == "many_sounds":
                return visit_parse_tree(sound, self)

    def visit_many_sounds(self, node, children):
        sounds = []
        current_sound = []
        for sound in node:
            if sound.rule_name == "sound":
                current_sound.append(visit_parse_tree(sound, self))
            if sound.rule_name == "comma":
                sounds.append(''.join(current_sound))
                current_sound = []
        sounds.append(''.join(current_sound))  # TODO: If a current_sound is a string, I won't need the joins

        return sounds

    def visit_sound(self, node, children):
        return node.flat_str()

    def visit_context(self, node, children):
        # print(node.flat_str())
        # tn = None
        for x in node:
            if x.rule_name == "context_description":
                return visit_parse_tree(x, self)
        # return Context.from_string(node.flat_str())

    def visit_context_description(self, node, children):
        description = visit_parse_tree(node[0], self)
        return description
        # return Context.from_string("")

    def visit_left_desc(self, node, children):
        preceded_by = visit_parse_tree(node[0], self)

    def visit_description(self, node, children):
        specification = None
        for sound in node:
            description = visit_parse_tree(sound, self)

    def visit_description_sound(self, node, children):
        pass


class Entry:
    def __init__(self, source, destination, context):
        self.source = source
        self.destination = destination
        self.context = context

    def __str__(self):
        base_str = f"{''.join(self.source)} > {''.join(self.destination)}"
        if self.context:
            base_str += f" / {self.context.to_string()}"

        return base_str


class Context:  # TODO
    def __init__(self):
        pass

    @staticmethod
    def from_string(string):
        return Context()

    def to_string(self):
        pass


class Sound:
    def is_elongated(self):
        pass  # TODO


class Vowel(Sound):
    pass  # TODO


class Consonant(Sound):
    pass  # TODO


class Specifier(Enum):
    CONSONANT = auto()
    VOWEL = auto()


class Description:
    def __init__(self, specifier, attributes):
        pass
