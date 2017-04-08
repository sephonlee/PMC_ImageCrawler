# PMC_ImageCrawler: Crawl figure images on PubMed Central server

The repositoy contains a set of scripts to crawl figure images on PubMed Central by giving keywords or urls. This is a simple crawler using webdriver to go throught returned pages of PMC image search and extract metadata and corresponding figure images. 

## Requirements

Install python support. 
Download chrome driver from here https://sites.google.com/a/chromium.org/chromedriver/downloads

## Usage

```sh
Usage:
  main.py use_keyword KEYWORD PATH_TO_DRIVER [SAVE_PATH] [PAGE] 
  main.py use_url URL PATH_TO_DRIVER [SAVE_PATH] [PAGE]
  main.py (-h | --help)
  main.py --version
  main.py --debug
```

### Search images by keywords and download all return images
#### $ python PMCImageCrawler.py use_keyword metabolic+pathway path_to_chromedriver
Images and metadata will be saved in current_directory/data/

#### $ python PMCImageCrawler.py use_keyword metabolic+pathway path_to_chromedriver directory_of_output 5
Start crawling from page 5 and the images and metadata will be saved in given directory

### Search images by keywords and download all return images
#### $ python PMCImageCrawler.py use_url "https://www.ncbi.nlm.nih.gov/pmc/?term=metabolic+pathway&report=imagesdocsum" path_to_chromedriver directory_of_output 1
Start crawling from given url(must be the result page of PMC image searching)
