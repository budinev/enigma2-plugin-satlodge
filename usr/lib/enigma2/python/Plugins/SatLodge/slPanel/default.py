import sys
import urllib, urllib2, re, os
from urllib import urlencode
from HTMLParser import HTMLParser
from urllib import quote
from urllib2 import Request, urlopen, URLError, HTTPError
from twisted.web.client import downloadPage, getPage
from xml.etree.cElementTree import fromstring
from xml.dom import minidom, Node

module_path = '/usr/lib/enigma2/python/Plugins/SatLodge/slPanel/'
temppath = '/tmp/'

list2=[]

def readnet(url):
    try:
     req = urllib2.Request(url)
     response = urllib2.urlopen(req)
     data = response.read()
     response.close()
     return data
    except:
     return None

    return None

def main_cats():
    cats=[]
    cats.append(("SatLodge Images",''))
    for cat in cats:
        print "cat",cat
        cats.sort()
        addDir(cat[0], cat[0], 100, cat[1], '', 1)             
             

def getteams(name,url,page):
    if name == 'SatLodge Images':
        mode=159
        teams = [('AirDigital Images','http://webplus.sat-lodge.it/index.php?dir=Zgemma/','')]
			 
    for team in teams:
        print 'page',page
        teams.sort()
        addDir(team[0], team[1], mode, team[2], '', 1)

def lodgemodels(name,url,page):
        models = ['All_Models',
         'zgemmah2',
         'zgemmah3',
         'zgemmah5',
         'zgemmah7',
         'zgemmah9',]
        for model in models:
            print "model",model
            href = url + model  
            addDir(model, href,160, '','', 1)             

             
def extract_lodgeimages(model,url,page):
    if 'sat-lodge' in url: 
        if model == 'All_Models':
            model = ''
        else:
            model = model        

        print 'model',model 	
        url='http://webplus.sat-lodge.it/index.php?dir=Zgemma/' + model + '/'
	   
    print "image_url",url   
    data=readnet(url)    
    if data is None:
       print "download error"
       return (False, 'Download error')
    url=url.lower()
    listdata=[]
	
    regx='''<a class="autoindex_a" href="(.*?)">'''
    images=re.findall(regx,data, re.M|re.I)
    for href in images:
           if not '.zip' in href:
              continue		   
           try:href=href.split("file=")[1]
           except:continue
           name=href   
           href='http://webplus.sat-lodge.it/Zgemma/' + model + '/' + href
           listdata.append((name,href))
	
    print "listdata",listdata
    for item in listdata:
        addDir(item[0],item[1],10,'','',1,True)
    return True,listdata 

			
def addDir(name, url, mode, iconimage, desc = '', page = '',link=False):
    global list2
    if not page == '':
        u = module_path + '?url=' + urllib.quote_plus(url) + '&mode=' + str(mode) + '&name=' + urllib.quote_plus(name) + '&desc=' + urllib.quote_plus(desc) + '&page=' + str(page)
    else:
        u = module_path + '?url=' + urllib.quote_plus(url) + '&mode=' + str(mode) + '&name=' + urllib.quote_plus(name) + '&desc=' + urllib.quote_plus(desc) + '&page='
    if link:
        u=url
        list2.append((name,
         u,
         iconimage,
         page))
    else:
        list2.append((name,
         u,
         iconimage,
         page))
         
         
def get_params(action_param):
    param = []
    paramstring = action_param
    if paramstring is None or paramstring == '':
        paramstring = ''
    else:
        paramstring = '?' + action_param.split('?')[1]
    if len(paramstring) >= 2:
        params = paramstring
        cleanedparams = params.replace('?', '')
        if params[len(params) - 1] == '/':
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if len(splitparams) == 2:
                param[splitparams[0]] = splitparams[1]

    print 'input,output', paramstring, param
    return param
def process_mode(action_param=None):
    global list2
    try:        
        if os.path.exists(temppath+'ImageDowanloder.log'):
            os.remove(temppath+'ImageDowanloder.log')
        list2 = []
        print "action_param",action_param
        try:params = get_params(action_param)
        except:params={}
        url = None
        name = None
        mode=None
        page = ''
        try:
            url = urllib.unquote_plus(params['url'])
        except:
            pass
        try:
            name = urllib.unquote_plus(params['name'])
        except:
            pass
        try:
            mode=int(params['mode'])
        except:
            pass
        try:
            page = str(params['pageToken'])
        except:
            page = 1
            pass
            
        print 'Mode: ' + str(mode)
        print 'URL: ' + str(url)
        print 'Name: ' + str(name)
        print 'page: ' + str(page)
        if type(url) == type(str()):
            url = urllib.unquote_plus(url)
        if mode == None:
            main_cats()
        elif mode == 100:
            print '' + url
            getteams(name, url, page)

        elif mode==159:
            print '' + url
            lodgemodels(name, url, page)
        elif mode==160:
            extract_lodgeimages(name,url,1)
			
    except:
        addDir('', '', '', '', desc='', page='')
    print "list2",list2
    return list2