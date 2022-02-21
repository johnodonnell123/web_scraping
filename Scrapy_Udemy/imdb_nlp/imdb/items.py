# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbItem(scrapy.Item):
    # define the fields for your item here like:
    movie_url = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    maturity_rating = scrapy.Field()
    runtime = scrapy.Field()
    short_plot = scrapy.Field()
    genres = scrapy.Field()
    total_ratings = scrapy.Field()
    num_user_reviews = scrapy.Field()
    num_critic_reviews = scrapy.Field()
    metascore = scrapy.Field()
    top_cast = scrapy.Field()
    director = scrapy.Field()
    writers = scrapy.Field()
    storyline = scrapy.Field()
    plot_tags = scrapy.Field()
    release_date = scrapy.Field()
    country_of_origin = scrapy.Field()
    language = scrapy.Field()
    summaries = scrapy.Field()
    synopsis = scrapy.Field()

class UserItem(scrapy.Item):
    # define the fields for your item here like:
    user_name = scrapy.Field()
    movie = scrapy.Field()
    rating = scrapy.Field()
    rating_date = scrapy.Field()
