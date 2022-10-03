import os
import shutil
from pdf2image import convert_from_path
import img2pdf
import codecs
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter
# Poppler Libraries in \Python\Scripts


def pdf2images(input_filename):
    images = convert_from_path(input_filename)
    input_file_base = os.path.basename(input_filename).rstrip('.pdf')
    output_dir = input_file_base
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    for i in range(len(images)):
        output_file = f'{i}.jpg'
        output_filename = os.path.join(output_dir, output_file)
        images[i].save(output_filename, 'JPEG')
    return output_dir


def images2pdf(input_dir, output_filename):
    input_files = list(map(lambda x: str(x) + '.jpg', sorted(
        [int(f.strip('.jpg')) for f in os.listdir(input_dir) if f.endswith('.jpg')])))
    output_images = []
    for input_file in input_files:
        input_filename = os.path.join(input_dir, input_file)
        output_images.append(input_filename)
    with codecs.open(output_filename, 'wb') as f:
        f.write(img2pdf.convert(output_images))


def create_watermark(text, size):
    text_font = ImageFont.truetype(r'..\shared\fonts\PT Mono Bold.ttf', size)
    text_size = ImageDraw.Draw(
        Image.new('RGB', (1000, 1000))).multiline_textsize(text, text_font)
    image_size = (16000, 16000)
    image = Image.new('RGBA', image_size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    max_x = image_size[0]//text_size[0]*2
    max_y = image_size[1]//text_size[1]*2
    offset_x = text_size[0]
    offset_y = text_size[1]
    start_x = 0
    start_y = 0
    for a in range(0, max_x):
        for b in range(0, max_y):
            x = start_x + a*offset_x
            y = start_y + b*offset_y
            draw.multiline_text((x, y), text, (0, 0, 0, 64), font=text_font)
    image = image.rotate(-45, expand=True, fillcolor=(0, 0, 0, 0))
    return image, image_size


def images2protect(input_dir, text, size, noise):
    watermark_font_size = size
    watemark_image, watemark_image_size = create_watermark(
        text, watermark_font_size)
    input_files = list(map(lambda x: str(x) + '.jpg', sorted(
        [int(f.strip('.jpg')) for f in os.listdir(input_dir) if f.endswith('.jpg')])))
    for input_file in input_files:
        input_filename = os.path.join(input_dir, input_file)
        file_name, file_ext = os.path.splitext(input_filename)
        original_image = Image.open(input_filename).convert("RGBA")
        original_image_size = original_image.size
        temp_image = Image.new('RGBA', original_image_size, (255, 255, 255, 0))
        temp_image.paste(
            watemark_image, (-watemark_image_size[0]//2, -watemark_image_size[1]//2))
        combined_image = Image.alpha_composite(original_image, temp_image)
        combined_image.convert('RGB').save(input_filename)
        if noise != 0:
            for _ in range(noise):
                combined_image = combined_image.filter(
                    ImageFilter.EDGE_ENHANCE_MORE)
                combined_image = combined_image.filter(ImageFilter.DETAIL)
        combined_image.convert('RGB').save(input_filename, quality=30)


def work_protect(input_dir,  scan_only='', text='', size=32, noise=0):
    print('scan for pdf files...')
    input_files = [f for f in os.listdir(input_dir) if f.endswith(
        '.pdf') and not f.endswith('_locked.pdf')]
    if input_files:
        for input_file in input_files:
            print(f'{input_file}', end='')
            input_filename = os.path.join(input_dir, input_file)
            images_dir = pdf2images(input_filename)
            if not scan_only:
                images2protect(images_dir, text, size, noise)
            output_file = f'{os.path.basename(input_file).rstrip(".pdf")}_locked.pdf'
            output_filename = os.path.join(input_dir, output_file)
            images2pdf(images_dir, output_filename)
            shutil.rmtree(images_dir)
            print(f' -> {output_file}')
    print('scan for images files...')
    input_files = [f for f in os.listdir(input_dir) if f.endswith(
        '.jpg') and not f.endswith('_locked.jpg')]
    if input_files:
        for input_file in input_files:
            print(f'{input_file}', end='')
            input_filename = os.path.join(input_dir, input_file)
            images_dir = input_filename + '_temp'
            if os.path.isdir(images_dir):
                shutil.rmtree(images_dir)
            os.mkdir(images_dir)
            shutil.copy(input_filename, os.path.join(images_dir, '0.jpg'))
            if not scan_only:
                images2protect(images_dir, text, size, noise)
            output_file = f'{os.path.basename(input_file).rstrip(".jpg")}_locked.pdf'
            output_filename = os.path.join(input_dir, output_file)
            images2pdf(images_dir, output_filename)
            shutil.rmtree(images_dir)
            print(f' -> {output_file}')


if __name__ == "__main__":
    while (True):
        input_dir = input(
            'input directory (press Enter to set default directory "C:\\Test\\files"):\n') or r'C:\Test\files'
        scan_only = input(
            'add protect layer (press Enter to set default or any value for pass protect):\n')
        if not scan_only:
            destination = input(
                'destination (press Enter to set default destination):\n') or 'ООО «Терабайт»'
            date = input('date (press Enter to set current date):\n') or str(
                datetime.today().strftime('%d.%m.%Y'))
            title = input(
                'title (press Enter to set default title):\n') or 'КОПИЯ ДЛЯ ОЗНАКОМЛЕНИЯ'
            subject = input(
                'subject (press Enter to set default subject):\n') or f'Договор {datetime.today().strftime("%Y-%m%d")}'
            noise = input(
                'images noise level (Enter to pass image noise):\n') or 0
            size = input(
                'text size (press Enter to set default text size):\n') or 32
            text_auto_offset = max(len(title), len(
                'Тема:'+subject), len('Кому:'+destination), len('Дата:'+date))-5
            text = f"""
            {title}
            {'Тема:':<0}{subject:>{text_auto_offset}}
            {'Кому:':<0}{destination:>{text_auto_offset}}
            {'Дата:':<0}{date:>{text_auto_offset}}
            """
            print(text)
            no_correct = input(
                '\nAll OK? (press Enter to start protect or any key for edit values):\n')
            if no_correct:
                continue
            work_protect(input_dir, bool(scan_only),
                         text, int(size), int(noise))
        else:
            work_protect(input_dir, bool(scan_only))
