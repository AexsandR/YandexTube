from PIL import Image


def setting_image(path):
    im = Image.new("RGB", (1280, 720), (200, 200, 200))
    img = Image.open(path)
    # изменяем размер
    w, h = img.size
    print(w,h)
    if w < h:
        new_image = img.resize((405, 720))
        im.paste(new_image, (437, 0))
        im.save(path)
    elif w == h:
        new_image = img.resize((720, 720))
        im.paste(new_image, (280, 0))
        im.save(path)
    else:
        new_image = img.resize((1280, 720))
        new_image.save(path)

