from pathlib import Path
import re,json,hashlib,subprocess,xml.etree.ElementTree as ET
ROOT=Path('/workspace/shared/ge-oct4-rev3a-erc-normalize')
SCH=ROOT/'pcb/rev3a/design/GEA-Adapter-Rev3A.kicad_sch'
TOKEN=re.compile(r'\s*(?:(\()|(\))|("(?:\\.|[^"\\])*"|[^\s()]+))')
class Node:
 def __init__(self,start,end,items): self.start,self.end,self.items=start,end,items
 def key(self): return self.items[0] if self.items else ''
 def all(self,k): return [x for x in self.items if isinstance(x,Node) and x.key()==k]
 def one(self,k):
  a=self.all(k); return a[0] if a else None
 def v(self): return self.items[1:]
def parse(s):
 toks=list(TOKEN.finditer(s)); stack=[]; root=None
 for t in toks:
  if t[1]: stack.append(Node(t.start(1),None,[]))
  elif t[2]:
   n=stack.pop();n.end=t.end(2)
   if stack: stack[-1].items.append(n)
   else:root=n
  else:
   a=t[3]; stack[-1].items.append(json.loads(a) if a.startswith('"') else a)
 return root
