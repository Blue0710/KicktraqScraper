# -*- coding: utf-8 -*-

# Scrapy settings for kicktraq project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'kicktraq'

SPIDER_MODULES = ['kicktraq.spiders']
NEWSPIDER_MODULE = 'kicktraq.spiders'

# Stop when number of items scraped reach a certain number
#CLOSESPIDER_ITEMCOUNT = 5

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko'
#'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36 OPR/15.0.1147.153'
#'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko'
#'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False


DOWNLOADER_MIDDLEWARES = {
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500
}


USER_AGENTS = [
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/57.0.2987.110 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/61.0.3163.79 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) '
     'Gecko/20100101 '
     'Firefox/55.0'),  # firefox
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/61.0.3163.91 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/62.0.3202.89 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/63.0.3239.108 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko ',
     'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko ',
     'Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0) ',
     'Mozilla/1.22 (compatible; MSIE 10.0; Windows 3.1)'), # IE
    ('Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16 ',
     'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14 ',
     'Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02 ',
     'Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00') # Opera
]


ROTATING_PROXY_PAGE_RETRY_TIMES = 20

ROTATING_PROXY_LIST = [
'167.99.72.197:8080',
'209.222.17.226:8181',
'202.154.180.53:35421',
'68.183.233.146:3128',
'206.189.44.220:8080',
'185.124.86.11:3128',
'96.9.74.160:39305',
'181.113.131.98:47961',
'142.93.158.26:3128',
'88.12.48.61:42365',
'1.20.97.204:50496',
'104.236.48.178:8080',
'117.206.83.46:30733',
'80.179.157.80:80',
'203.205.34.52:25',
'198.27.67.35:3128',
'52.68.127.244:80',
'52.124.6.146:40834',
'142.93.36.10:3128',
'103.205.26.78:52193',
'68.183.217.42:3128',
'35.247.152.119:3128',
'35.238.72.25:3128',
'23.97.142.47:3128',
'35.247.218.193:80',
'165.22.254.197:8080',
'165.22.254.195:8080',
'3.17.193.18:3128',
'81.223.122.78:30052',
'200.37.83.2:53399',
'118.174.232.128:45019',
'1.179.188.205:58505',
'124.41.243.22:57391',
'79.61.94.186:30108',
'125.27.179.88:36127',
'118.70.116.227:61651',
'118.174.232.4:50660',
'138.122.51.87:3128',
'1.20.103.135:31128',
'194.87.101.45:3128',
'142.93.36.10:3128',
'117.54.200.242:53281',
'191.7.209.74:52000',
'181.113.225.198:53281',
'138.204.117.191:61987',
'217.78.5.57:3128',
'86.110.189.118:56710',
'105.27.143.190:53962',
'94.232.57.231:51064',
'123.49.49.98:23500',
'213.16.55.138:36690',
'176.36.118.116:44873',
'187.6.67.43:80',
'95.65.1.200:58768',
'83.240.29.109:55754',
'210.5.208.34:53664',
'185.99.64.75:56217',
'187.190.9.80:57963',
'1.20.101.201:45863',
'177.92.160.254:54868',
'177.104.252.246:33757',
'109.75.140.158:59916',
'103.231.163.58:45893',
'1.20.100.8:47974',
'222.252.15.114:45575',
'93.183.220.101:53281',
'1.10.186.167:51907',
'197.242.206.64:34680',
'1.20.102.19:55118',
'195.34.90.121:41258',
'151.106.10.51:8080',
'62.249.140.198:41555',
'46.183.56.107:46342',
'1.20.101.118:54880',
'124.41.240.205:36752',
'138.97.12.150:36570',
'212.230.130.221:49698',
'86.57.219.181:23500',
'51.38.162.2:32231',
'180.248.14.70:8080',
'190.5.225.178:53383',
'35.236.116.197:3128',
'103.58.145.18:55951',
'31.210.66.217:3128',
'103.241.227.105:50313',
'62.152.75.110:50287',
'103.250.157.38:45879',
'197.231.202.252:55436',
'94.180.249.187:38051',
'95.140.19.9:8080',
'201.158.63.174:55287',
'1.10.185.133:53044',
'187.188.189.19:34337',
'177.124.184.72:55072',
'46.241.120.230:33516',
'181.143.106.162:52162',
'176.192.58.78:60412',
'138.204.23.158:53281',
'118.174.220.148:54853',
'109.87.33.2:53381',
'5.59.141.68:54684',
'34.254.192.173:80',
'27.74.247.140:42977',
'213.6.45.18:52041',
'117.74.113.45:50091',
'202.52.9.130:42655',
'165.22.147.72:3128',
'45.112.56.2:46224',
'190.11.15.2:43827',
'185.132.133.214:8080',
'109.86.225.33:55850',
'104.236.55.48:8080',
'163.172.220.221:8888',
'169.57.1.84:8080',
'170.79.16.19:8080',
'169.57.1.84:25',
'169.57.1.84:80',
'79.120.177.106:8080',
'91.194.42.51:80',
'191.36.192.196:3128',
'202.138.127.66:80',
'58.27.217.75:3128',
'91.102.218.9:3128',
'199.195.251.143:3128',
'86.34.133.118:8080',
'84.22.61.46:53281',
'91.102.219.73:3128',
'50.206.204.14:3128',
'193.93.216.95:8080',
'189.125.170.36:80',
'187.58.58.163:3128',
'113.200.56.13:8010',
'173.192.21.89:80',
'159.8.114.37:8123',
'173.192.21.89:8123',
'113.161.173.10:3128',
'159.8.114.37:25',
'145.239.93.131:80',
'94.242.58.108:10010',
'61.160.210.223:808',
'169.57.1.84:8123',
'94.242.58.142:10010',
'103.20.204.104:80',
'187.115.10.50:20183',
'187.95.34.10:8080',
'62.221.41.130:8080',
'195.208.172.70:8080',
'212.95.180.50:53281',
'103.14.232.22:8080',
'188.165.240.92:3128',
'109.167.207.72:8080',
'177.185.114.89:53281',
'82.193.123.230:53281',
'46.253.12.46:53281',
'165.16.3.54:53281',
'109.197.188.8:8080',
'46.229.187.169:53281',
'193.188.254.67:53281',
'177.101.122.178:20183',
'195.138.83.218:53281',
'78.140.6.68:53281',
'177.71.77.202:20183',
'177.135.248.75:20183',
'189.45.199.37:20183',
'91.185.21.124:8123',
'86.100.77.210:53281',
'185.128.104.125:8080',
'85.21.240.153:8080',
'188.169.87.246:8080',
'200.254.125.10:80',
'187.108.36.250:20183',
'82.147.116.201:41234',
'37.220.195.14:53281',
'200.105.209.118:8080',
'185.158.127.9:53281',
'94.154.31.136:53281',
'186.42.185.94:31588',
'109.197.184.81:8080',
'200.206.70.162:20183',
'83.246.139.24:8080',
'109.197.184.50:8080',
'77.94.144.164:3128',
'190.186.59.22:52335',
'62.148.67.110:81',
'88.204.154.155:3128',
'46.150.174.90:53281',
'77.94.144.162:3128',
'87.228.103.111:8080',
'85.15.179.5:8080',
'187.32.123.177:3128',
'118.174.64.219:8080',
'80.32.235.77:3128',
'177.46.148.142:3128',
'91.214.179.12:8080',
'173.192.21.89:25',
'123.31.47.8:3128',
'193.95.228.13:53281',
'64.23.56.171:3128',
'178.132.220.241:8080',
'177.200.83.238:8080',
'123.231.203.254:8080',
'94.242.58.142:1448',
'85.238.105.190:8181',
'181.129.183.19:53281',
'181.176.209.86:8080',
'94.242.59.135:10010',
'194.126.183.141:53281',
'81.30.216.147:41258',
'66.70.188.148:3128',
'116.12.89.81:8080',
'79.115.245.227:8080',
'200.233.136.177:20183',
'176.118.49.54:53281',
'5.148.128.44:8080',
'77.75.6.34:8080',
'81.17.131.59:8080',
'178.44.113.205:53281',
'103.199.159.153:40049',
'134.175.55.112:1080',
'92.244.36.69:47150',
'5.58.56.109:34242',
'188.166.145.121:3128',
'94.158.22.187:8085',
'93.110.94.114:8080',
'96.23.13.71:8082',
'41.66.82.21:8888',
'5.62.159.92:8085',
'121.232.148.176:9000',
'146.185.203.219:8085',
'138.204.233.198:59813',
'95.85.80.191:8085',
'175.20.114.152:8080',
'196.25.12.2:52895',
'85.202.195.14:8085',
'85.144.19.205:80',
'91.106.82.195:80',
'197.210.143.182:36496',
'77.36.226.25:80',
'31.40.208.238:8085',
'95.170.113.165:43364',
'46.161.60.11:8085',
'84.54.58.207:8085',
'43.240.5.41:31777',
'185.251.14.188:8085',
'202.158.17.150:30204',
'131.196.141.117:33729',
'193.32.94.201:8085',
'182.34.34.187:9999',
'5.160.144.19:80',
'5.202.47.186:80',
'185.89.100.227:8085',
'80.78.70.24:39516',
'103.225.228.17:58732',
'138.197.102.119:80',
'80.234.5.69:8080',
'188.170.234.58:33877',
'31.40.208.121:8085',
'185.120.139.96:53281',
'93.88.74.58:92',
'5.202.121.50:80'
]


# Pass all responses, regardless of its status code. (Added to handle 400 errors)
HTTPERROR_ALLOW_ALL = True

# Write stdout to file for debugging purposes
LOG_STDOUT = True
LOG_FILE = "C:\\Users\\hilmiuysal\\Desktop\\NYC Data Science Academy\\Projects\\WebScraping\\kicktraq\\kicktraq\\kicktraq.log" #+ log_filename

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'kicktraq.middlewares.KicktraqSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'kicktraq.middlewares.KicktraqDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'kicktraq.pipelines.WriteItemPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
