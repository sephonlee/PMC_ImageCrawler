"""Finds and reads text in an image.

Usage:
  main.py use_keyword KEYWORD PATH_TO_DRIVER [SAVE_PATH] [PAGE] 
  main.py use_url URL PATH_TO_DRIVER [SAVE_PATH] [PAGE]
  main.py (-h | --help)
  main.py --version
  main.py --debug

Options:
  --debug           Write debug output.
  -h --help         Show this screen.
  --version         Show version.
"""

# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
import urllib, os, csv
from docopt import docopt
import logging
# import BeautifulSoup


def saveCSV(path, filename, content = None, header = None, mode = 'wb', consoleOut = True):
    if consoleOut:
        print 'Saving image information...'
    filePath = os.path.join(path, filename) + '.csv'
    with open(filePath, mode) as outcsv:
        writer = csv.writer(outcsv, dialect='excel')
        if header is not None:
            writer.writerow(header)
        if content is not None:
            for c in content:
                writer.writerow(c)
    if consoleOut:  
        print filename, 'were saved in', filePath, '\n'
            
            

if __name__ == '__main__':
    arguments = docopt(__doc__, version='PMCImageCrawler 0.1') 

    path_chromedriver = "/Users/sephon/Desktop/Research/VizioMetrics/CrawlBot/chromedriver"
    csvFilename = 'metadata_'
    outpath = "./data/"
    page = 1
    url = None
    keyword = ""
    
    if arguments['--debug']:
        logging.basicConfig(level=logging.DEBUG)
        DEBUG = True
     
        
    if arguments['PAGE']:
        page = int(arguments['PAGE'])
          
    if arguments['PATH_TO_DRIVER']:
        path_chromedriver = arguments['PATH_TO_DRIVER']
        
    if arguments['SAVE_PATH']:
        outpath = arguments['SAVE_PATH']
        
    if arguments['PATH_TO_DRIVER']:
        path_chromedriver = arguments['PATH_TO_DRIVER']

    if arguments['KEYWORD']:
        keyword = arguments['KEYWORD']

    if arguments['URL']:
        url = arguments['URL']

    if arguments["use_keyword"]:
        url = 'https://www.ncbi.nlm.nih.gov/pmc/?term=%s&report=imagesdocsum' %keyword

    if arguments["use_url"]:
        url = url
    
    
    if not (os.path.isdir(outpath)):
        os.makedirs(outpath)
    print "outpath", outpath
    
    if url is not None:
       
        print "Open Chrome Driver..."
        
        driver = webdriver.Chrome(path_chromedriver)
        driver.get(url)
        
        jump = driver.find_element_by_xpath("//input[contains(@id, 'pageno')]")
        jump.clear()
        jump.send_keys(page)
        jump.send_keys(Keys.ENTER)         
        csvFilename = csvFilename + str(page)
        
        print "Metadata save in %s" %os.path.join(outpath, csvFilename + '.csv')
        print "Start crawling images from page %d" %page
        
        header = ["pmid", "pmc_img_url", "filename", "img_title", "caption"]
        saveCSV(outpath, csvFilename, header = header, mode = 'wb', consoleOut = False)
        while True:
            rslt = driver.find_elements_by_xpath("//div[contains(@class, 'rslt')]")
            for j, element in enumerate(rslt):
                try:
                    a = element.find_element_by_tag_name("a")
                    paper_url = a.get_attribute("href")
               
                    prefix = paper_url.split("/")[-2]
                    pmcid = paper_url.split("/")[-2][3:]
                   
                    img_url = a.find_element_by_tag_name("img").get_attribute("src")
                    img_url = img_url[0:-3] + "jpg"
                    filename = img_url.split("/")[-1]
                    filename = prefix + "_" + filename[0:-3] + "jpg"
               
                    img_title = element.find_element_by_xpath("div/p").text
                    img_title = img_title.encode('utf-8').decode('ascii', 'ignore')
               
                    caption = element.find_element_by_xpath("div/div[contains(@class, 'supp')]/div").text
                    caption = caption.encode('utf-8').decode('ascii', 'ignore')
               
                    urllib.urlretrieve(img_url, os.path.join(outpath, filename))
               
                    row = [pmcid, img_url, filename, img_title, caption]
                    print "page %d, image %d, pmcid: %s" %(page, j, pmcid)
                    outcsv = open(os.path.join(outpath, csvFilename + '.csv'), 'ab')
                    writer = csv.writer(outcsv, dialect = 'excel')
                    writer.writerow(row)
                    outcsv.flush()
                    outcsv.close()
                except:
                    pass
                   
            page += 1
            next_button = driver.find_element_by_class_name("next")
            class_next_button = next_button.get_attribute("class")
            if "inactive" in class_next_button.split(" "):
                break
            else:
                next_button.click()
    else:
        print "url not found"