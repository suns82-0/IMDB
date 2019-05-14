from scrapy import cmdline


name = 'IMDB'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())
