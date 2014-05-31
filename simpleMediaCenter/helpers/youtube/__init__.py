#-*- encoding: utf-8 -*-
#Note: The YouTube Data API (v2) has been officially deprecated as of March 4, 2014. Please refer to our deprecation policy for more information.
#https://developers.google.com/youtube/2.0/developers_guide_protocol_api_query_parameters

try:
    from urllib.request import urlopen, Request
    from urllib.parse import quote_plus, quote
except ImportError:
    from urllib import quote_plus, quote
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
    __scraper = None
    __logger=logging.getLogger(__name__)
    NAMESPACES = {
        'Atom': 'http://www.w3.org/2005/Atom',
        'openSearch': 'http://a9.com/-/spec/opensearchrss/1.0/',
        'yt': 'http://gdata.youtube.com/schemas/2007'}
    URLS = {
        'uploads'      : 'https://gdata.youtube.com/feeds/api/users/{0[0]}/uploads?start-index={0[1]}&max-results={0[2]}',
        'channelSearch': 'https://gdata.youtube.com/feeds/api/channels?q="{0[0]}"&start-index={0[1]}&max-results={0[2]}&v=2',
        'videoSearch': 'https://gdata.youtube.com/feeds/api/videos?q="{0[0]}"&start-index={0[1]}&max-results={0[2]}&v=2'}
    
    def __init__(self):
        self.__scraper=XMLScraper()
        
    def __prepareURL(self, url_key, replacement_list):
        url = self.URLS[url_key].format(replacement_list)
        url = quote(url, safe="%/:=&?~#+!$,;'@()*[]")
        self.__logger.debug('prepareURL: ' + url)
        return url
        
    '''
        list all Channel videos
        @param channelName name of the channel
        @param offset where to start(smallest is 1)
        @param limit max amount of videos to pull, max limit is 25
    '''
    def listChannelVideos(self, channelName, offset=1, limit=25):
        url = self.__prepareURL('uploads', (channelName, offset, limit))
        return self.__scraper.downloadXML(url)
        
    '''
        search for Channel
        @param channelName name of the channel
        @param offset where to start(smallest is 1)
        @param limit max amount of videos to pull, max limit is 25
    '''
    def searchChannel(self, channelName, offset=1, limit=25):
        url = self.__prepareURL('channelSearch', (channelName, offset, limit))
        return self.__scraper.downloadXML(url)
        
    '''
        search for Channel
        @param videoName name of the video
        @param offset where to start(smallest is 1)
        @param limit max amount of videos to pull, max limit is 25
    '''
    def searchVideo(self, videoName, offset=1, limit=25):
        url = self.__prepareURL('videoSearch', (videoName, offset, limit))
        return self.__scraper.downloadXML(url)
        
