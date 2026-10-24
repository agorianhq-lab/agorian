import json,base64,sys,re
f,out=sys.argv[1],sys.argv[2]
t=json.load(open(f))[0]['text']
m=re.search(r'"([A-Za-z0-9+/=]+)"',t)
raw=base64.b64decode(m.group(1))
open(out,'wb').write(raw)
from PIL import Image; im=Image.open(out); print(out, im.size, len(raw)//1024,'KB')
