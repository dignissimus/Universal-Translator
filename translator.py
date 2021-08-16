from arpeggio import ParserPython, visit_parse_tree

from parser import document
from visitor import DocumentVisitor


def debug():
    parser = ParserPython(document)
    while True:
        tree = parser.parse(input(">> "))
        print(tree)
        for node in tree:
            print(node)


def main():
    parser = ParserPython(document, skipws=False)

    with open("Sound Changes/English/PIE to Common Germanic") as file:
        content = file.read()
        tree = parser.parse(content)
        entries = visit_parse_tree(tree, DocumentVisitor())
        for entry in entries:
            print(entry)


if __name__ == '__main__':
    main()
