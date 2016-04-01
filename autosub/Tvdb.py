#
# Autosub Tvdb.py -  https://github.com/Donny87/autosub-bootstrapbill
#
# The Tvdb API module
#

import logging

import urllib,requests
from difflib import SequenceMatcher as SM
try:
    import xml.etree.cElementTree as ET
except:
    import xml.etree.ElementTree as ET
from xml.dom import minidom
import autosub
import autosub.Helpers

# Settings
log = logging.getLogger('thelogger')



def FindName(Url,Root,Tag):
    Session = requests.Session()
    try:
        Result = Session.get(Url)
    except:
        return None
    root = ET.fromstring(Result.content)
    try:
        for node in root.findall(Root):
            try:
                Found = node.find(Tag).text
            except:
                log.error("FindName: Could not find %s in %s on Tvdb URL: " % (Root,Tag,Url))
                log.error("FindName: message is: " % error)
                return None
            if Found:
                return Found
            else:
                log.error("Tvdb: Could not find %s in %s on Tvdb URL: " % (Root,Tag,Url))
                return None
    except Exception as error:
        log.error("FindName: Could not find %s in %s on Tvdb URL: " % (Root,Tag,Url))
        log.error("FindName: message is: " % error)
        return None

def getShowidApi(showName):
    """
    Search for the IMDB ID by using the TvDB API and the name of the show.
    Keyword arguments:
    showName -- Name of the show to search the showid for
    """
    Url = "%sGetSeries.php?seriesname=%s" % (autosub.IMDBAPI, urllib.quote(showName.encode('utf8')))
    Session = requests.Session()
    try:
        Result = Session.get(Url)
    except:
        return None
    root = ET.fromstring(Result.content)
    ImdbId = None
    HighName = None
    HighScore = 0
    try:
        for node in root.findall('Series'):
            try:
                FoundName = node.find('SeriesName').text
                Score = SM(None, FoundName, showName).ratio()
                if Score > HighScore:
                    ImdbId = None
                    try:
                        ImdbId = node.find('IMDB_ID').text[2:]
                    except:
                        ImdbId = None
                    if ImdbId:
                        HighScore = Score
                        HighName = FoundName
            except:
                pass
    except Exception as error:
            log.error("getShowidApi: Could not find %s in %s on Tvdb URL: " % (Root,Tag,Url))
            log.error("getShowidApi: message is: " % error)
    return ImdbId,HighName


def getShowName(ImdbId):
    """
    Search for the official TV show name using the IMDB ID
    """
    
    Url = autosub.IMDBAPI + 'GetSeriesByRemoteID.php?imdbid=' + ImdbId
    return FindName(Url, 'Series', 'SeriesName')

    
    
def GetEpisodeName(ImdbId,SeasonNum, EpisodeNum):
    Session = requests.Session()
    Url = autosub.IMDBAPI + 'GetSeriesByRemoteID.php?imdbid=' + ImdbId
    SerieId = FindName(Url, 'Series', 'seriesid')

    Url = "%sDECE3B6B5464C552/series/%s/default/%s/%s" % (autosub.IMDBAPI,SerieId,SeasonNum.lstrip('0'),EpisodeNum.lstrip('0'))
    return FindName(Url,'Episode','EpisodeName')
