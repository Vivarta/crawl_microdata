# crawl_microdata
Will output to .csv the schema.org values found on a website of URL.

how to use:

 scrapy crawl microdata -a url=URL -o export.csv -t csv

 Will output to .csv the schema.org values found on a website of URL.

 Code is in spiders/microdata.py.

 The scrapy spider loads our MicrodataSpider class and will send in the html as the
 response variable. This is parsed looking for schema.org itemprop definitions on the page
 held within the microdata.
 
 Original code by https://github.com/stefangeorg
