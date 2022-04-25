# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from itemloaders.processors import Compose, TakeFirst, MapCompose
from scrapy.loader import ItemLoader
from dataclasses import dataclass

# class like TakeFirst to pull second item in list without throwing IndexError
class TakeSecond():
    def __call__(self, values):
        count = 0
        for value in values:
            count += 1
            if count == 2 and value is not None and value != '':
                return value

# functions to be used during input processing for item fields
def remove_whitespace(value):
    return value.strip()

def split_hyphen(value):
    return value.split('--')

def split_space(value):
    return value.split(' ')

def split_comma(value):
    return value.split(',')

def str_to_float(value):
    return float(value)

def str_to_int(value):
    return int(value)

def regex_float(value):
    return re.findall(r'(\d*\.\d+)', value)

def regex_int(value):
    return re.findall(r'\d+', value)

def bool_roundtrip(value):
    return False if value.find('roundtrip') == -1 else True

def regex_sub_2019(value):
    return re.sub('(\u2018|\u2019)', "'", value)

# hike custom item, with fields having default values and input,output processor where applicable
class HikeItem(scrapy.Item):
    # A note on input and output processors: according to scrapy design they always work on iterables.
    # That is why everything goes through mapCompose, because almost all the data I'm pulling, except for
    # the hike features, are not originally iterables, but single value strings. MapCompose applies the functions
    # to each value in an iterable in succession. Most of the time that iterable, in this case, is a single item list.
    name = scrapy.Field(
        default='',
        output_processor=TakeFirst())

    region_1 = scrapy.Field(
        default='',
        input_processor=MapCompose(split_hyphen, remove_whitespace),
        output_processor=TakeFirst()
    )
    region_2 = scrapy.Field(
        default='',
        input_processor=MapCompose(split_hyphen, remove_whitespace),
        output_processor=TakeSecond()
    )
    length = scrapy.Field(
        default=0,
        input_processor=MapCompose(split_comma, regex_float, str_to_float),
        output_processor=TakeFirst()
    )
    roundtrip = scrapy.Field(
        default=None,
        input_processor=MapCompose(split_comma, bool_roundtrip),
        output_processor=TakeSecond()
    )
    gain = scrapy.Field(
        default=0,
        input_processor=MapCompose(regex_int, str_to_int),
        output_processor=TakeFirst()
    )
    highpoint = scrapy.Field(
        default=0,
        input_processor=MapCompose(regex_int, str_to_int),
        output_processor=TakeFirst()
    )
    features = scrapy.Field(
        default=None
    )
    rating = scrapy.Field(
        default=None,
        input_processor=MapCompose(regex_float, str_to_float),
        output_processor=TakeFirst()
    )
    votes = scrapy.Field(
        default=0,
        input_processor=MapCompose(regex_int, str_to_int),
        output_processor=TakeFirst()
    )
    desc = scrapy.Field(
        default='',
        input_processor=MapCompose(regex_sub_2019, remove_whitespace),
        output_processor=TakeFirst()
    )
    coords = scrapy.Field(
        output=None,
        input_processor=MapCompose(str_to_float)
    )

