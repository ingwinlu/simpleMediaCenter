#-*- encoding: utf-8 -*-
try:
    from urllib.request import urlopen, Request
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus
    from urllib2 import Request, urlopen

import logging
import sys
import xml.etree.ElementTree as et

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'

class XMLScraper():
    
    def downloadWebData(self, url):
        data = ""
        try:
            req = Request(url)
            req.add_header('User-Agent', USER_AGENT)
            response = urlopen(req)
            
            if sys.version_info < (3, 0):
                data = response.read()
            else:
                data = response.readall().decode('utf-8')
            response.close()
        except:
            raise Exception()
        return data
    
    def downloadXML(self, url):
        try:
            xmlString = self.downloadWebData(url)
            tree = et.fromstring(xmlString)
            logging.debug(et.dump(tree))
            return tree
        except:
            raise Exception()
    
    
class Youtube():
    NAMESPACES = {
        'Atom': 'http://www.w3.org/2005/Atom',
        'openSearch': 'http://a9.com/-/spec/opensearchrss/1.0/'}
    URLS = {
        'uploads':'https://gdata.youtube.com/feeds/api/users/{0[0]}/uploads?start-index={0[1]}&max-results={0[2]}'}
    
    __scraper = None
    
    
    def __init__(self):
        self.__scraper=XMLScraper()
        
    def __prepareURL(self, url_key, replacement_list):
        return self.URLS[url_key].format(replacement_list)
        
    def listChannelVideos(self, channelName, startindex=1, maxresults=25):
        url = self.__prepareURL('uploads', (channelName, startindex, maxresults))
        return self.__scraper.downloadXML(url)
        
