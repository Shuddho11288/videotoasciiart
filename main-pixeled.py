import cv2
import os
import time
from PIL import Image
from tkinter.filedialog import askopenfile
import rich

# get image path
class ImageToAscii:
    def __init__(self,path:str, n_w:int):
        image_path = path
        print(image_path)
        self.img = Image.open(image_path)
        self.n_w = n_w
        self._convertToRGBA()
        self._resize()
        self._main()
        # resizing the image

    def _convertToRGBA(self):
        bands = self.img.getbands()
        if len(bands) == 1 or len(bands) == 3:
            self.img = self.img.convert("RGBA")

    def _resize(self):
        self.width, self.height = self.img.size
        aspect_ratio = self.height / self.width
        self.new_width = self.n_w
        self.new_height = aspect_ratio * self.new_width / 2
        self.img = self.img.resize((self.new_width, int(self.new_height)))

    def _main(self):
        lista = []
        pixels = self.img.getdata()
        for pixel in pixels:
            lista.append(pixel)

        img = self.img.convert("L")

        pixels = img.getdata()



        def getChar(inputInt, col):

            r, g, b, a = col

            return "[rgb({},{},{})]{}[/]".format(
                r, g, b, "█"
            )

        new_pixels = [getChar(pixel, col) for pixel, col in zip(pixels, lista)]

        new_pixels_count = len(new_pixels) + len(str(lista))
        self.ascii_image = [
            new_pixels[index : index + self.new_width]
            for index in range(0, new_pixels_count, self.new_width)
        ]
        final_res = []
        for x in self.ascii_image:
            final_res.append("".join(x))
        while True:
            try:
                final_res.remove("")
            except Exception:
                break
        final_res = "\n".join(final_res)
        self.ascii_image = final_res

    def show(self):
        rich.print(self.ascii_image)

    def getText(self):
        return self.ascii_image
    def saveText(self):
        with open("output.html", "w") as fp:
            fp.write(self.ascii_image)



vidcap = cv2.VideoCapture(askopenfile().name)
success,image = vidcap.read()
count = 0
#framelist = []
while success:
  #os.system("cls")
  cv2.imwrite("frame.jpg", image)     # save frame as JPEG file      
  success,image = vidcap.read()
  im = ImageToAscii("./frame.jpg", 200)
  #framelist.append(im.getText())
  im.show()
  
  
"""  count += 1
for x in framelist:
    rich.print(x)
    time.sleep(0.1)
    os.system("cls")"""
  
  
