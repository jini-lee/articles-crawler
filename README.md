# Naver 뉴스기사 크롤러
## 일간지 종류
> 경향신문 국민일보 동아일보 문화일보 서울신문  
> 세계일보 조선일보 중앙일보 한겨레 한국일보
## Install
> [install mongodb](https://docs.mongodb.com/manual/installation/)  
> [install scrapy](http://doc.scrapy.org/en/latest/intro/install.html)  
## Menual
> * mongodb
>     MONGO_DATABASE = 'articles' 
>     collection = major
> * today news paper scrap  
>     scrapy crawl article  
> * specific date news paper scrap  
>     scrapy crawl article -a from_date=20181119 to_date=20181215
