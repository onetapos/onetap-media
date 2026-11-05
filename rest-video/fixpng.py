import sys, glob
from PIL import Image
for f in sorted(glob.glob(sys.argv[1]+'/*.png')):
    im=Image.open(f)
    if im.mode!='RGBA': im.convert('RGBA').save(f)
print('fixed')
