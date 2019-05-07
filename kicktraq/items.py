# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KicktraqItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
    description_length = scrapy.Field()
    owner = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    status = scrapy.Field()
    funding_raised = scrapy.Field()
    funding_goal = scrapy.Field()
    funding_percentage = scrapy.Field()
    category = scrapy.Field()
    num_backers = scrapy.Field()
    avg_pledge_amount_per_backer = scrapy.Field()
    funding_currency = scrapy.Field()
    campaign_start_date = scrapy.Field()
    campaign_end_date = scrapy.Field()
    num_comments = scrapy.Field()
    num_updates = scrapy.Field()
    num_created_by_owner = scrapy.Field()
    avg_backers_per_pledge_tier = scrapy.Field()
    num_faqs = scrapy.Field()
    dict_pledge_tier_backer = scrapy.Field()
    project_img = scrapy.Field()
    project_video = scrapy.Field()
    full_desc_len = scrapy.Field()
    featured_project = scrapy.Field()
    num_pledge_backers = scrapy.Field()
    num_pledge_tiers = scrapy.Field()