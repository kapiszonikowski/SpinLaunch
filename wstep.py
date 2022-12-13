import ctypes
import PIL
from PIL import Image
import codecs


plik1 = open('1.wstep.txt', 'r')
wstep = plik1.read()
wstep1 = wstep.encode('1252')
wstep2 = wstep1.decode('utf-8')

plik2 = open('2.teoria.txt', 'r')
teoria = plik2.read()
#teoria1 = teoria.encode('1252')
#teoria2 = teoria1.decode('utf-8')
#teoria1 = teoria.encode('1252').decode('utf-8')



plik3 = open('3.komunikat o starcie.txt', 'r')
komunikat = plik3.read()
#komunikat1 = str(komunikat).encode('1252').decode('utf-8')


img = Image.open('SpinLaunch.logo.jpg')
img.show()
response = ctypes.windll.user32.MessageBoxW(0, wstep2, "Spinlaunch", 4)

IDYES = 6
IDNO = 7
if response==6:
    ctypes.windll.user32.MessageBoxW(0, teoria, "Spinlaunch", 1)
    im = Image.open('schemat.jpg')
    im.show()
    ctypes.windll.user32.MessageBoxW(0, komunikat, "Spinlaunch", 1)
elif response==7:
    ctypes.windll.user32.MessageBoxW(0, komunikat1, "Spinlaunch", 1)







