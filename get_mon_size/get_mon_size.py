import math
import pandas as pd
import codecs
import webbrowser
import base64

##    options_horizontal = {
##    0 : 'Горизонтальный поворот головы - нет. Горизонтальное вращение глаз - нет.',
##    1 : 'Горизонтальный поворот головы - нет. Горизонтальное вращение глаз - да.',
##    2 : 'Горизонтальный поворот головы - да. Горизонтальное вращение глаз - да.'}
##    options_vertical = {
##    0 : 'Положение сидя. Вертикальный поворот головы - нет. Вертикальное вращение глаз - нет.',
##    1 : 'Положение стоя. Вертикальный поворот головы - нет. Вертикальное вращение глаз - нет.',
##    2 : 'Положение сидя. Вертикальный поворот головы - нет. Вертикальное вращение глаз - да.'}

def get_mon_size(eye_mon_distance=54, eye_x_option = 0, eye_y_option = 0):
    eye_x_degrees = {0: 15, 1 : 30, 2 : 60}
    eye_y_degrees = {0: 15, 1 : 10, 2 : 30}
    eye_x_degree = eye_x_degrees.get(eye_x_option, 15)
    eye_y_degree = eye_y_degrees.get(eye_y_option, 15)
    mon_size_x = 2 * eye_mon_distance * math.tan(math.radians(eye_x_degree))
    mon_size_y = 2 * eye_mon_distance * math.tan(math.radians(eye_y_degree))
    mon_size_h = math.hypot(mon_size_x, mon_size_y) / 2.54
    mon_size_total = f'{round(mon_size_h, 1)}\" ({round(mon_size_x)} x {round(mon_size_y)} cm)'
    return mon_size_total

def df2html(title, df):
    header = r'<!DOCTYPE html>'+ '\n' + '<html>' + '\n' + '<head>' + '\n' + \
    '<meta http-equiv="content-type" content="text/html; charset=utf-8" />' + \
    '\n' + '<title>' + title + '</title>' + '\n' + '</head>' + '\n' + \
    '<style>a {text-decoration: нетne;} </style>' + '\n'
    content = f'{header}<body style="font-family:Arial">\n<b>{title}</b><br><br> \
        {df.to_html(index=False, render_links=True, escape=False)}<br><br>'
    with codecs.open(f'{title}.html', 'w', 'utf-8') as f:
        f.write(content)
    webbrowser.open(f'{title}.html')

def main():
    columns=['Дистанция от глаз до монитора', 'Рекомендуемая диагональ экрана (если работать сидя)', 'Рекомендуемая диагональ экрана (если работать стоя)']
    df = pd.DataFrame(columns=columns)

    img_eyes_view_vertical = f'<img src="data:image/png;charset=utf-8;base64,{base64.b64encode(open("eyes_view_vertical.png", "rb").read()).decode("utf-8")}" alt="eyes_view_vertical" />'
    img_eyes_view_horizontal = f'<img src="data:image/png;charset=utf-8;base64,{base64.b64encode(open("eyes_view_horizontal.png", "rb").read()).decode("utf-8")}" alt="eyes_view_horizontal" />'
    df = df.append(pd.DataFrame([['Оптимальные соотношения расстояния и размера монитора для минимальной нагрузки на глаза (при которых экран находится целиком в поле прямого зрения: без необходимости постоянных поворотов головы и вращений глаз в процессе работы)', img_eyes_view_vertical, img_eyes_view_horizontal]], columns=columns))
    for eye_mon_distance in range(10, 501, 1):
        distance = f'{eye_mon_distance} cm'
        df = df.append(pd.DataFrame([[distance, get_mon_size(eye_mon_distance, 0, 0), get_mon_size(eye_mon_distance, 0, 1)]], columns=columns))
    df2html('Выбор рекомендуемого расстояния и размера монитора (панели) для наименьшей усталости глаз при продолжительной работе', df)

main()
