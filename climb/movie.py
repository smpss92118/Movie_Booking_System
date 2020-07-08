import scrapy
import time


class movieSpider(scrapy.Spider):
    name = 'movie'
    start_urls = ['https://www.ambassador.com.tw/home/MovieList?Type=1']

    def parse(self, response):
        target = response.xpath('//*[@id="tab1"]/div/div')
        for tag in target:
            ticks = time.time()
            title = tag.xpath('.//div[@class = "poster-info"]/div/h6/a/text()').extract_first()
            href = tag.xpath('.//a[contains(@class, "poster")]/@href').extract_first()
            #yield response.follow(url=href, meta={'Title': title[11:-1], 'sequence': ticks}, callback=self.parse_content)
            #print(f"title = {title}")
            #print(f"href = {href}")
            yield response.follow(url=href, meta={'Title': title, 'sequence': ticks}, callback=self.parse_day)
        #a_next = response.xpath('//a[contains(@rel, "next")]/@href').extract_first()
        #if a_next:
            #a_next = 'https://icook.tw' + a_next
            #yield response.follow(a_next, callback=self.parse)



    def parse_day(self, response):
        title = response.meta['Title']
        x = response.meta['sequence']
        day = response.xpath('.//*[@id="search-bar-page"]/div/div/div[1]/ul/li/ul/li')
        for d in day:
            movie_day = d.xpath('.//a/text()').extract_first()
            href = d.xpath('.//a/@href').extract_first()
            print(f"day = {movie_day} href = {href}")
            print(type(href))
            yield response.follow(url=href, meta={'Title': title, 'sequence': x, 'movie_day': movie_day}, callback=self.parse_info)


    def parse_info(self,response):
        title = response.meta['Title']
        x = response.meta['sequence']
        movie_day = response.meta['movie_day']
        ingredients = response.xpath('//div[@class = "theater-box"]')
        ticks = time.time()
        for ingredient in ingredients:
            theater = ingredient.xpath('.//h3/a/text()').extract_first()
            location = ingredient.xpath('.//h3/span[1]/text()').extract_first()
            times = ingredient.xpath('.//ul/li')
            for t in times:
                movie_time = t.xpath('.//h6/text()').extract_first()

                if response.url and title and theater and location:
                    yield{
                        'movie_name': title,
                        'movie_day': movie_day,
                        'theater': theater,
                        't_location':location,
                        'movie_time':movie_time,
                    }

