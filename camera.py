from picamera import PiCamera
from PIL import Image
import PIL
from time import sleep

avgR, avgG, avgB = 0, 0, 0 
XL = 610
XR = 650
YB = 200
YT = 230
pixels = (XR - XL) * (YT - YB)

camera = PiCamera()
camera.start_preview(alpha=200)
camera.brightness = 60
camera.resolution = (1280, 720)

camera.capture('/home/pi/aquarius/images/image.jpg')
camera.stop_preview()

image = PIL.Image.open("/home/pi/aquarius/images/image.jpg")
image_rgb = image.convert("RGB")


for x in range(XL, XR):
     for y in range(YB, YT):
         rgb_pixel_value = image_rgb.getpixel((x, y))
         avgR += rgb_pixel_value[0]
         avgG += rgb_pixel_value[1]
         avgB += rgb_pixel_value[2]
R = avgR / pixels
G = avgG / pixels
B = avgB / pixels
print(round(R), round(G), round(B))

'''
measures = 5
for x in range(measures):
	camera.capture('/home/pi/aquarius/images/image' + str(x) + '.jpg')
	camera.stop_preview()

avgR, avgG, avgB = 0, 0, 0	

for x in range(measures):
	image = PIL.Image.open("/home/pi/aquarius/images/image" + str(x) + ".jpg")
	image_rgb = image.convert("RGB")
	rgb_pixel_value = image_rgb.getpixel((690, 360))
	avgR += rgb_pixel_value[0]
	avgG += rgb_pixel_value[1]
	avgB += rgb_pixel_value[2]



R = avgR / measures
G = avgG / measures
B = avgB / measures

print(round(R), round(G), round(G))
'''
