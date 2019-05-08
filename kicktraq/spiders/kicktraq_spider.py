from scrapy import Spider, Request
from kicktraq.items import KicktraqItem
import re
from datetime import datetime, date
from dateutil.parser import parse
import pandas as pd
import time
import random


class kicktraqSpider(Spider):
    name = 'kicktraq_spider'
    allowed_urls = ['https://www.kicktraq.com/','https://www.kickstarter.com/']
    start_urls = ['https://www.kicktraq.com/archive/']

    def parse(self, response):
        # Find the total number of pages in the result
        number_pages = int(response.xpath('//div[@class="paging"]/a[contains(@title,"go to page") and not(@class="prn")][last()]/text()').extract_first())

        # List comprehension to construct all the urls
        result_urls = ['https://www.kicktraq.com/archive?page={}'.format(x) for x in range(1200,1204)] # Only top 2500 pages are allowed to scrape by kicktraq.com

        # Show pages to scrape and yield to next level
        for url in result_urls:
            yield Request(url=url, callback=self.parse_result_page)
            print('smthhhhhh')
            print('*' * 50)
            #time.sleep(random.randint(0,1))


    def parse_result_page(self, response):

        detail_urls = response.xpath('//div[@class="project-infobox"]/h2/a/@href').extract()

        print('burayi yaz bakalim')
        print(detail_urls)

        for url in detail_urls:
            yield Request(url='https://www.kicktraq.com' + url, callback=self.parse_detail_page)
            print('Checkpoint')
            print('*' * 50)
            #time.sleep(random.randint(1,2))


    def parse_detail_page(self, response):

        def strip_not_none(n):
            if pd.isnull(n) == False:
                n = n.strip()
                return n

        title = response.xpath('//div[@id="project-title"]/h2/text()').extract_first()
        title = strip_not_none(title)
        description = response.xpath('//div[@id="project-info-text"]/text()[1]').extract_first()
        description = strip_not_none(description)

        detail_info_str = response.xpath('//div[@id="project-title"]/span/text()').extract_first()

        if detail_info_str is not None:
            owner = detail_info_str.split(' by ')[1]
            owner = strip_not_none(owner)
            city = detail_info_str.split(' by ')[0].split(' in ')[1].strip().split(',')[0]
            city = strip_not_none(city)
            state = detail_info_str.split(' by ')[0].split(' in ')[1].strip().split(',')[1].strip()
            state = strip_not_none(state)

        status = response.xpath('//div[@id="project-infobox"]/div[@class="ribbon"]//h3/text()').extract_first()
        
        num_backers = response.xpath('//div[@id="project-info-text"]/text()[3]').extract_first()
        num_backers = strip_not_none(num_backers)
        if num_backers is not None:
            if re.search('\d*$', num_backers) is not None:
                num_backers = int(re.search('\d*$', num_backers).group())
        else:
            num_backers = 0

        if num_backers <= 1:
            funding = response.xpath('//div[@id="project-info-text"]/text()[5]').extract_first()
        else:
            funding = response.xpath('//div[@id="project-info-text"]/text()[6]').extract_first()

        funding = strip_not_none(funding)
        
        if funding is not None:
            funding_currency = funding.split(' of ')[1].replace(',','')
            funding_currency = re.search('\D*', funding_currency).group()
            funding_raised = funding.split(' of ')[0].split(funding_currency)[1].replace(',','')
            funding_raised = int(re.search('^\d*', funding_raised).group())
            funding_goal = funding.split(' of ')[1].split(funding_currency)[1].replace(',','')
            funding_goal = int(re.search('^\d*', funding_goal).group())
            funding_percentage = round(funding_raised/funding_goal*100, 2)
        
        category = response.xpath('//div[@id="project-info-text"]/div[@class="project-cat"]/a/text()').extract_first()

        # Calculate avg pledge amount per backer
        if num_backers != 0:
            avg_pledge_amount_per_backer = round(funding_raised / num_backers, 2)
        else:
            avg_pledge_amount_per_backer = 0

        campaign_start_date = response.xpath('//div[@id="project-info-text"]/a[@class="datelink"][1]/@title').extract_first()
        
        if campaign_start_date is not None:
            campaign_start_date = campaign_start_date.split('@')[0].strip()
            campaign_start_date = parse(campaign_start_date).date()

        campaign_end_date = response.xpath('//div[@id="project-info-text"]/a[@class="datelink"][2]/@title').extract_first()

        if campaign_end_date is not None:
            campaign_end_date = campaign_end_date.split('@')[0].strip()
            campaign_end_date = parse(campaign_end_date).date()


        # Checkpoint
        # print(title)
        # print(description)
        # print(owner)
        # print(city)
        # print(state)
        # print('#' * 50)


        url_to_kickstarter = response.xpath('//div[@id="project-info-image"]/a/@href').extract_first()
        yield Request(url=url_to_kickstarter, meta={'title': title, 'description': description, 'owner': owner, 'city': city, 'state': state,
            'status': status, 'num_backers': num_backers, 'avg_pledge_amount_per_backer': avg_pledge_amount_per_backer, 'funding_currency': funding_currency,
            'funding_raised': funding_raised, 'funding_goal': funding_goal, 'funding_percentage': funding_percentage, 'category': category,
            'campaign_start_date': campaign_start_date, 'campaign_end_date': campaign_end_date}, 
                        callback=self.kickstarter_page)


    def kickstarter_page(self, response):

        title = response.meta['title']
        description = response.meta['description']
        owner = response.meta['owner']
        city = response.meta['city']
        state = response.meta['state']
        status = response.meta['status']
        num_backers = response.meta['num_backers']
        avg_pledge_amount_per_backer = response.meta['avg_pledge_amount_per_backer']
        funding_currency = response.meta['funding_currency']
        funding_raised = response.meta['funding_raised']
        funding_goal = response.meta['funding_goal']
        funding_percentage = response.meta['funding_percentage']
        category = response.meta['category']
        campaign_start_date = response.meta['campaign_start_date']
        campaign_end_date = response.meta['campaign_end_date']

        description_length = len(description)

        #################################

        patterns = ['//div[@class="hide block-md mb2-md"]/a[@class="dark-grey-500 keyboard-focusable"]/text()',
                    '//div[@class="hide block-md mb2-md"]/a[@class=class="dark-grey-500"]/text()',
                    '//div[@class="grid-row pt9-lg mt3 mt0-lg mb6-lg order-2-md order-1-lg"]//div[@class="hide block-md mb2-md"]//span[@class="dark-grey-500"]/text()']

        for pattern in patterns:
            num_created_by_owner = response.xpath(pattern).extract_first()
            if pd.isnull(num_created_by_owner) == False:
                if re.search('[0-9]+', num_created_by_owner) is not None:
                    num_created_by_owner = int(re.search('[0-9]+', num_created_by_owner).group())
                    break
            if not num_created_by_owner:
                continue

        if num_created_by_owner is None:
            num_created_by_owner = 1

        #################################

        num_comments = response.xpath('//div[@class="project-nav__links"]/a[@class="js-load-project-comments js-load-project-content mx3 project-nav__link--comments tabbed-nav__link type-14"]/span[@class="count"]/data/text()').extract_first()        
        num_updates = response.xpath('//div[@class="project-nav__links"]/a[@class="js-load-project-content js-load-project-updates mx3 project-nav__link--updates tabbed-nav__link type-14"]/span[@class="count"]/text()').extract_first()
        num_faqs = response.xpath('//div[@class="project-nav__links"]/a[@class="js-load-project-content js-load-project-faqs mx3 project-nav__link--faqs tabbed-nav__link type-14"]/span[@class="count"]/text()').extract_first()


        def replace_comma(n):
            if pd.isnull(n) == False:
                n = int(n.replace(',',''))
            else:
                n = 0
            return n

        num_comments = replace_comma(num_comments)
        num_updates = replace_comma(num_updates)
        num_faqs = replace_comma(num_faqs)


        #############################

        list_of_pledge_tiers = response.xpath('//div[@class="pledge__info"]/h2[@class="pledge__amount"]/span[@class="money"]/text()').extract()
        list_of_pledge_backers = response.xpath('//div[@class="pledge__backer-stats"]/span[@class="pledge__backer-count" or @class="block pledge__backer-count"]/text()').extract()

        # Take only the numerical part
        pledge_tiers = list(map(lambda x: int(re.search('[0-9]+', x).group()), list_of_pledge_tiers))
        pledge_backers = list(map(lambda x: int(re.search('[0-9]+', x).group()), list_of_pledge_backers))
        num_pledge_backers = sum(pledge_backers)
        num_pledge_tiers = len(pledge_tiers)

        # Calculate avg number of backers per pledge tier
        if len(list_of_pledge_tiers) > 0:
            avg_backers_per_pledge_tier = round(num_pledge_backers / num_pledge_tiers, 2)
        else:
            avg_backers_per_pledge_tier = 0

        # Create list of tuples
        zipped_ = list(zip(pledge_tiers, pledge_backers))
        
        # Init dict
        dict_pledge_tier_backer = {}

        # Consolidate and sum backers of same pledge tiers
        for e in zipped_:
            key = e[0]
            value = e[1]
            
            if key not in dict_pledge_tier_backer.keys():
                dict_pledge_tier_backer[key] = value
            else:
                dict_pledge_tier_backer[key] += value

        #############################


        #############################

        patterns = ['//div[@class="mx-4 mx-12-md mx0-lg"]//div[@class="aspect-ratio aspect-ratio--16x9 w100p"]//img',
                    '//div[@class="full-description js-full-description responsive-media formatted-lists"]//figure//img']


        for pattern in patterns:
            project_img = response.xpath(pattern).extract_first()
            if project_img is not None:
                project_img = len(response.xpath(pattern).extract())
                break
            if not project_img:
                continue
        
        if project_img is None:
            project_img = 0

        feature_img = response.xpath('//div[@class="grid-container pb3 pb10-sm"]//img[@class="js-feature-image "]').extract_first()

        if feature_img is not None:
            feature_img = 1
        else:
            feature_img = 0

        project_img += feature_img

        #############################


        #############################

        patterns = ['//div[@class="video-player"]',
                    '//div[@class="mx-4 mx-12-md mx0-lg"]//div[@class="aspect-ratio aspect-ratio--16x9 w100p ksr-video-player bg-black"]']

        for pattern in patterns:
            project_video = response.xpath(pattern).extract_first()
            if project_video is not None:
                project_video = len(response.xpath(pattern).extract())
                break
            if not project_video:
                continue

        if project_video is None:
            project_video = 0

        #############################        


        full_desc_len = response.xpath('//div[@class="full-description js-full-description responsive-media formatted-lists"]//p/text()').extract()
        full_desc_len = sum(list(map(lambda e: len(e.strip()), full_desc_len)))


        #############################

        featured_project = response.xpath('//div[@class="NS_projects__category_location ratio-16-9 flex items-center"]/a[@class="grey-dark mr3 nowrap type-12 flex items-center"]/text()').extract_first()

        if featured_project is None:
            featured_project = 0
        else:
            featured_project = 1

        #############################


        # Yield all scraped items

        item = KicktraqItem()
        item['title'] = title
        item['description'] = description
        item['description_length'] = description_length
        item['owner'] = owner
        item['city'] = city
        item['state'] = state
        item['status'] = status
        item['num_backers'] = num_backers
        item['avg_pledge_amount_per_backer'] = avg_pledge_amount_per_backer
        item['funding_currency'] = funding_currency
        item['funding_raised'] = funding_raised
        item['funding_goal'] = funding_goal
        item['funding_percentage'] = funding_percentage
        item['category'] = category
        item['campaign_start_date'] = campaign_start_date
        item['campaign_end_date'] = campaign_end_date
        item['num_comments'] = num_comments
        item['num_updates'] = num_updates
        item['num_created_by_owner'] = num_created_by_owner
        item['avg_backers_per_pledge_tier'] = avg_backers_per_pledge_tier
        item['num_faqs'] = num_faqs
        item['dict_pledge_tier_backer'] = dict_pledge_tier_backer
        item['project_img'] = project_img
        item['project_video'] = project_video
        item['full_desc_len'] = full_desc_len
        item['featured_project'] = featured_project
        item['num_pledge_backers'] = num_pledge_backers
        item['num_pledge_tiers'] = num_pledge_tiers

        yield(item)


