"""Minimal KiCad s-expression parser (netlist files)."""
import re

_tok = re.compile(r'\(|\)|"((?:\\.|[^"\\])*)"|([^\s()"]+)')


def parse(text):
    stack, cur = [], []
    for m in _tok.finditer(text):
        t = m.group(0)
        if t == '(':
            stack.append(cur); cur = []
        elif t == ')':
            done, cur = cur, stack.pop(); cur.append(done)
        elif m.group(1) is not None:
            cur.append(m.group(1).replace('\\"', '"').replace('\\\\', '\\'))
        else:
            cur.append(t)
    return cur[0] if len(cur) == 1 else cur


def find_all(node, name):
    """All descendants (any depth) that are lists starting with `name`."""
    out = []
    if isinstance(node, list):
        if node and node[0] == name: out.append(node)
        for c in node: out += find_all(c, name) if isinstance(c, list) else []
    return out


def child(node, name):
    for c in node:
        if isinstance(c, list) and c and c[0] == name: return c
    return None


def get(node, name):
    c = child(node, name)
    return c[1] if c and len(c) > 1 and isinstance(c[1], str) else None
