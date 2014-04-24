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
    __logger=logging.getLogger(__name__)
    
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
            self.__logger.debug(et.dump(tree))
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
        
    '''
        list all Channel videos
        @param channelName name of the channel
        @param offset where to start(smallest is 1)
        @param limit max amount of videos to pull, max limit is 25
    '''
    def listChannelVideos(self, channelName, offset=1, limit=25):
        url = self.__prepareURL('uploads', (channelName, offset, limit))
        return self.__scraper.downloadXML(url)
        
