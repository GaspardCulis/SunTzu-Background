from random import choice

from numpy import average
#import deepl
import textwrap
import json
from main import setWallpaper
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont

QUOTE_FONT = 'Arialbd.ttf'
QUOTE_COLOR = (255, 255, 255)
AUTHOR_FONT = 'Arialbd.ttf'
AUTHOR_COLOR = (255, 255, 255)
BACKGROUND_IMAGE = 'sun_tzu_background.jpg'
AUTH_KEY = 'e6c656a4-8189-u-dont-get-to-see-that-3415ca6e8311:fx'


translator = "lol not working"#deepl.Translator(AUTH_KEY)


def translate(text: str, lang='FR') -> str:
    result = translator.translate_text(text, target_lang=lang)
    return str(result)


def generate_translated_quotes(quotes: list, path='sun_tzu/quotes_fr.json', lang='FR'):
    translated = list()
    i = 0
    for quote in quotes:
        trans_text = translate(quote, lang)
        translated.append(trans_text)
        i += 1
        print(f"Converted {i}/{len(quotes)} quotes")
    with open(path, "w", encoding='utf-8') as f:
        json.dump(translated, f, ensure_ascii=False)


def get_quotes(path="sun_tzu/quotes_fr.json") -> list:
    with open(path, "r", encoding='utf-8') as f:
        return json.load(f)


def get_quotes_new(path="sun_tzu/quotes_new_fr.txt") -> list:
    out = list
    with open(path, "r", encoding='utf-8') as f:
        out = f.read().split('\n\n')
    for i in range(len(out)):
        out[i] = out[i].replace('\n', ' ')
        out[i] = ('.'.join(out[i].split('.')[1:]))[1:]
    return out


# Returns the size of the font and the text with new lines for it to fit in a certain size
def get_font_and_text(quote: str, fnt_path: str, max_width: int, max_height: int, init_size=72) -> tuple:
    fnt = ImageFont.truetype(fnt_path, init_size)
    size = get_size(quote, fnt)
    average_char_width = size[0]/len(quote)
    max_chars_in_line = int(max_width // average_char_width - 2)

    wrapped = '\n'.join(textwrap.wrap(quote, max_chars_in_line))
    size = get_size(wrapped, fnt)
    if size[1] > max_height:
        print("Retrying with smaller font : " + str(init_size-1))
        return get_font_and_text(quote, fnt_path, max_width, max_height, init_size - 1)
    return fnt, wrapped


def get_size(text: str, font: ImageFont) -> tuple:
    im = Image.new('RGB', (1, 1))
    d = ImageDraw.Draw(im)
    size = d.textsize(text, font)
    return size


def generate_image(quote: str, path='wallpaper.png'):
    img = Image.open(BACKGROUND_IMAGE)
    d = ImageDraw.Draw(img)
    fnt, final_quote = get_font_and_text(
        quote, QUOTE_FONT, img.size[0]*0.5, img.size[1]*0.4)
    size = get_size(final_quote, fnt)
    text_pos = (img.size[0]/2.5, img.size[1]/2 - size[1]/2)
    d.text(text_pos, final_quote, font=fnt, fill=QUOTE_COLOR)

    author_fnt = ImageFont.truetype(AUTHOR_FONT, 42)
    d.text((text_pos[0] + 50, text_pos[1] + size[1] + 40), " - Sun Tzu, The Art of War",
           font=author_fnt, fill=AUTHOR_COLOR)
    img.save(path)


if __name__ == "__main__":
    quotes = get_quotes('quotes_new_fr.json')
    quote = '"'+choice(quotes)+'"'
    generate_image(quote)
    setWallpaper('wallpaper.png')
