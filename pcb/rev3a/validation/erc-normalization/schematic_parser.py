"""Minimal read-only KiCad S-expression parser with exact source spans."""
import json
import re

TOKEN = re.compile(r'\s*(?:(\()|(\))|("(?:\\.|[^"\\])*"|[^\s()]+))')

class Node:
    def __init__(self, start, end, items):
        self.start, self.end, self.items = start, end, items

    def key(self):
        return self.items[0] if self.items else ''

    def all(self, key):
        return [x for x in self.items if isinstance(x, Node) and x.key() == key]

    def one(self, key):
        matches = self.all(key)
        return matches[0] if matches else None

    def v(self):
        return self.items[1:]


def parse(source):
    stack = []
    root = None
    for token in TOKEN.finditer(source):
        if token[1]:
            stack.append(Node(token.start(1), None, []))
        elif token[2]:
            node = stack.pop()
            node.end = token.end(2)
            if stack:
                stack[-1].items.append(node)
            else:
                assert root is None
                root = node
        else:
            atom = token[3]
            stack[-1].items.append(json.loads(atom) if atom.startswith('"') else atom)
    assert root is not None and not stack
    return root


def value(node):
    return [value(item) if isinstance(item, Node) else item for item in node.items]
