# Naver 뉴스기사 크롤러

## Menual
> * mongodb  
>     MONGO_DATABASE = 'articles'   
>     collection = 'major'
> * today news paper scrap  
>     scrapy crawl article  
> * specific date news paper scrap  
>     scrapy crawl article -a from_date=20181119 to_date=20181215
