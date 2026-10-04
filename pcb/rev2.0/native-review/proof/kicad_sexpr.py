import re
class Atom(str):pass
def parse(text):
 tokens=re.findall(r'\(|\)|"(?:\\.|[^"\\])*"|[^\s()]+',text)
 stack=[]; root=None
 for token in tokens:
  if token=='(':
   node=[]
   if stack:stack[-1].append(node)
   else:root=node
   stack.append(node)
  elif token==')':stack.pop()
  elif token.startswith('"'):
   stack[-1].append(token[1:-1].replace('\\"','"').replace('\\\\','\\'))
  else:stack[-1].append(Atom(token))
 assert not stack
 return root
def children(node,key):return [x for x in node if isinstance(x,list) and x and x[0]==key]
def child(node,key,default=None):return next(iter(children(node,key)),default)
def val(node,key,default=None):
 n=child(node,key);return n[1] if n and len(n)>1 else default
