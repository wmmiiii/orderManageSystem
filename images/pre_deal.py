from PIL import Image

img = Image.open('loading.gif')
img = img.convert('RGBA')
x, y = img.size

for i in range(x):
    for j in range(y):
        color = img.getpixel((i, j))
        if color == (19, 109, 173, 255):
            color = (0, 0, 0, 0)
            img.putpixel((i, j), color)

# for i in range(x):
#     for j in range(y):
#         color = img.getpixel((i, j))
#         if color[:-1] == (255, 255, 255):
#             color = (0, 0, 0, 0)
#             img.putpixel((i, j), color)
img.save('loading.gif')