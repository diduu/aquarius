from picamera import PiCamera
from PIL import Image
from time import sleep

camera = PiCamera()


camera.start_preview(alpha=200)
camera.capture('/home/pi/aquarius/image.jpg')
sleep(1)
camera.stop_preview()



image = PIL.Image.open("/home/pi/aquarius/image.png")
image_rgb = image.convert("RGB")



rgb_pixel_value = image_rgb.getpixel((10,15))
print(rgb_pixel_value)