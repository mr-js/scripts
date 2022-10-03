import codecs
import pandas as pd
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

r = 100

def mark(x, y, text, img):
    scale_x = 0.0095; scale_y = 0.0085; scale_z = 1.0
    correct_x = 525; correct_y = 1000
    img_width, img_height = img.size
    img_x_center, img_y_center = img_width / 2.0, img_height / 2.0
    img_x = int((img_x_center + scale_x * x) * scale_z)
    img_x -= int(correct_x * ((img_width - img_x) / img_width))
    img_y = int((img_y_center - scale_y * y) * scale_z)
    img_y += int(correct_y * (img_y / img_height))
    img_text = f'{text}'
#     print(f'{img_text}:\n{x};{y} -> {img_x};{img_y}')
    draw = ImageDraw.Draw(img)
    # draw.line((0, img_y_center, img_width, img_y_center), fill=128, width=3)
    # draw.line((img_x_center, 0, img_x_center, img_height), fill=128, width=3)
    font = ImageFont.truetype(r'C:\Windows\Fonts\Arial.ttf', 32, encoding='UTF-8')
    draw.text((img_x, img_y), img_text, (255,255,255), font=font)
    draw.ellipse((img_x-r, img_y-r, img_x+r, img_y+r))

def main(targets):
    df = pd.DataFrame()
    store = pd.HDFStore('map.h5')
    df = store['df']
    img = Image.open('mwmap.jpg')
    for index, row in df.iterrows():
        if any(item.strip() in index for item in targets):
            mark(row['x'], row['y'], index, img)
    img.save('output.jpg')
    store.close()

print('Введите радиус (100 ... 1000) области отображения найденных локаций\n(чем меньше радиус, тем точнее результаты, но тем менее интересно исследовать область):')
try:
    r = int(input())
except:
    pass
if r < 100: r = 100
if r > 1000: r = 1000
print(f'Радиус области отображения локаций: {r}')
while True:
    print('Введите фрагменты названий локаций для поиска через запятую или Enter для выхода:')
    targets = input().split(',')
    if targets == ['']:
        break
    main(targets)
    print('Готово, см. результат: output.jpg\n')
