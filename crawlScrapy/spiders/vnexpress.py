import scrapy
class VnExpress(scrapy.Spider):
    name = "vnexpress"
    folder_path = "vnexpress"
    post_limit = 500
    start_urls = [
    ]
    numOfpost = 0
    '''
    category = [
        the-thao,
        khoa-hoc,
        giao-duc,
        du-lich,
        kinh-doanh,
        phap-luat,
        suc-khoe,
        .....
    ]
    '''
    def __init__(self,category):
        URL = 'https://vnexpress.net/'+ category
        self.start_urls = [URL]
        
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_list_posts)

    def parse_list_posts(self, response):
        if self.numOfpost > self.post_limit:
            return
        next_page_url = self.get_next_page_url(response)
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse_list_posts)
        else:
            return
        section = response.css("section div")
        for list_posts in section.css("article"):
            relative_url = list_posts.css("a::attr(href)").extract_first()
            url = response.urljoin(relative_url)
            yield scrapy.Request(url, callback=self.parse_posts)

                
    def get_next_page_url(self, response):
        next_page_url = response.css("div.pagination a.btn-page.next-page::attr(href)").extract_first()
        return next_page_url

    def parse_posts(self, response):
        self.numOfpost += 1
        if self.numOfpost>self.post_limit:
            return
        jsonData = self.extract_posts(response)
        yield jsonData
        

    def extract_posts(self, response):
        date = self.extract_date(response)
        title = self.extract_title(response)
        content = self.extract_content(response)
        author = self.extract_author(response)
        description = self.extract_description(response)

        jsonData = {
            'date': date,
            'author': author,
            'title': title,
            'description': description,
            'link': response.url,
            'content': content,
            'label': 'Suc Khoe'
        }

        return jsonData

    def extract_title(self, response):
        news = response.css("section h1")
        title = news.css("h1::text").extract_first()
        return title

    def extract_description(self, response):
        description = response.css("section p::text").extract_first()
        return description

    def extract_content(self, response):
        content = response.css("section article p::text").getall()
        if not content:
            content = response.css("section p::text").getall()
        if not content or len(content)<5:
            content = response.css("section img::attr(src)").getall()
        return content

    def extract_date(self, response):
        out = response.css("section span.date::text").extract_first()
        if not out:
            out = response.css("section span.time.right::text").extract_first()
        if not out:
            out = response.css("span.date::text").extract_first()
        return out
    
    def extract_author(self, response):
        out = response.css("section article p.Normal strong::text").extract_first()
        if not out:
            out = response.css("section article p.Normal em::text").extract_first()
        if not out:
            out = response.css("section article p.author_mail strong::text").extract_first()
        if not out:
            out = response.css("section article p strong::text").extract_first()
        if not out:
            out = response.css("section p strong::text").extract_first()
        if not out:
            out = response.css("section b::text").getall()[-1]
        return out
