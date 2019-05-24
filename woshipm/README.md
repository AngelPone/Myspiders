# README

描述：人人都是产品经理网页分类浏览文章抓取，主要包括title、author、link、time、content
网址主页：http://www.woshipm.com/

## Usage

```bash
python3 pmSpider.py -n [category_ranges] -c [category]
```
category可以从分类的主页上获得 `http://www.woshipm.com/category/{category_code}`
category_ranges 为爬取该分类的页数 `http://www.woshipm.com/category/{category_code}/page/{category_ranges}`


## Config

`pmSpider.py`中有两个配置项

`METADATADIR='./pmdocs/'` 保存文章信息（title、author、link、time）的CSV文件目录，每个category会在该目录下创建一个CSV文件用于保存
`OUTPUTDIR='./pmdocs/'` 文章正文文件保存目录，对于每个分类，会在当前目录下创建对应的文件夹


## requirment

```
requests-html
pandas
requests
```
