#"****************************************"
#"*         by ))^^((                    *"
#"*     05/06/2019                       *"
#"****************************************"
from Components.ActionMap import ActionMap, NumberActionMap
from Components.Button import Button
# from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.Language import language
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.Pixmap import Pixmap
from Components.PluginComponent import plugins
from Components.PluginList import *
from Components.ScrollLabel import ScrollLabel
from Components.Sources.List import List
from Components.Sources.StaticText import StaticText 
# from Components.config import config, getConfigListEntry, ConfigText, ConfigInteger, ConfigSelection, ConfigSubsection, ConfigYesNo
from Plugins.Plugin import PluginDescriptor
from Screens.Console import Console
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
# from Screens.Standby import *
# from Screens.Standby import TryQuitMainloop
from Tools.Directories import *
from Tools.Directories import SCOPE_SKIN_IMAGE, resolveFilename, SCOPE_PLUGINS, fileExists, copyfile, SCOPE_LANGUAGE, pathExists
from Tools.LoadPixmap import LoadPixmap
from enigma import *
from enigma import RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_HALIGN_CENTER, getDesktop, loadPNG, loadPic
from enigma import eTimer, eListboxPythonMultiContent #, addFont, eListbox, eConsoleAppContainer,  gFont 
from os import environ as os_environ
from os import path, listdir, remove, mkdir, chmod
from twisted.web.client import downloadPage
from twisted.web.client import getPage
from xml.dom import Node, minidom
import base64
import gettext
import os, re, sys
# import shutil
import urllib
import urllib2
import ssl
  
BRAND = '/usr/lib/enigma2/python/boxbranding.so'
BRANDP = '/usr/lib/enigma2/python/Plugins/PLi/__init__.pyo'
BRANDPLI ='/usr/lib/enigma2/python/Tools/StbHardware.pyo'
############################################# 
try:
    import zipfile
except:
    pass
    
def checkInternet():
    try:
        response = urllib2.urlopen("http://google.com", None, 5)
        response.close()
    except urllib2.HTTPError:
        return False
    except urllib2.URLError:
        return False
    except socket.timeout:
        return False
    else:
        return True

        
def ReloadBouquet():
    eDVBDB.getInstance().reloadServicelist()
    eDVBDB.getInstance().reloadBouquets() 
    
def deletetmp():
    os.system('rm -rf /tmp/unzipped;rm -f /tmp/*.ipk;rm -f /tmp/*.tar;rm -f /tmp/*.zip;rm -f /tmp/*.tar.gz;rm -f /tmp/*.tar.bz2;rm -f /tmp/*.tar.tbz2;rm -f /tmp/*.tar.tbz')    
    

DESKHEIGHT = getDesktop(0).size().height()

currversion = '1.1'
plugin_path = '/usr/lib/enigma2/python/Plugins/SatLodge/slSettings'
# ico_path = plugin_path + '/logo.png'    
ico1_path = plugin_path + '/res/pics/plugins.png' 
ico2_path = plugin_path + '/res/pics/plugin.png' 
skin_path = plugin_path
HD = getDesktop(0).size()
 
if HD.width() > 1280:
   skin_path = plugin_path + '/res/skins/fhd/' 
else:
   skin_path = plugin_path + '/res/skins/hd/'  
################################
PluginLanguageDomain = 'slSettings'
PluginLanguagePath = plugin_path + '/res/locale'
def localeInit():
    lang = language.getLanguage()[:2]
    os.environ['LANGUAGE'] = lang
    gettext.bindtextdomain(PluginLanguageDomain, PluginLanguagePath)
    gettext.bindtextdomain('enigma2', resolveFilename(SCOPE_LANGUAGE, ''))

def _(txt):
    t = gettext.dgettext(PluginLanguageDomain, txt)
    if t == txt:
        t = gettext.dgettext('enigma2', txt)
    return t
localeInit()
language.addCallback(localeInit)
    
    
         
class SetList(MenuList):

    def __init__(self, list):
        MenuList.__init__(self, list, False, eListboxPythonMultiContent)
        self.l.setFont(0, gFont('Regular', 20))
        self.l.setFont(1, gFont('Regular', 22))
        self.l.setFont(2, gFont('Regular', 24))
        self.l.setFont(3, gFont('Regular', 26))
        self.l.setFont(4, gFont('Regular', 28))
        self.l.setFont(5, gFont('Regular', 30))
        self.l.setFont(6, gFont('Regular', 32))
        self.l.setFont(7, gFont('Regular', 34))
        self.l.setFont(8, gFont('Regular', 36))
        self.l.setFont(9, gFont('Regular', 40))        
        if HD.width() > 1280:
            self.l.setItemHeight(50)
        else:		
            self.l.setItemHeight(50)


#############daily list
Panel_Dlist = [
 ('UPDATE SATELLITES.XML'), 
 ('UPDATE TERRESTRIAL.XML'), 
 ('SETTINGS CIEFP'), 
 ('SETTINGS MALIMALI'),  
 ('SETTINGS MANUTEK'),  
 ('SETTINGS MILENKA61'),  
 ('SETTINGS MORPHEUS'),
 ('SETTINGS PREDRAG'), 
 ('SETTINGS VHANNIBAL')
 ]
 
def DListEntry(name, idx):
    res = [name]
    if idx == 0:
        png = ico1_path
    elif idx == 1:
        png = ico1_path
    elif idx == 2:
        png = ico1_path  
    elif idx == 3:
        png = ico1_path         
    elif idx == 4:
        png = ico1_path   
    elif idx == 5:
        png = ico1_path 
    elif idx == 6:
        png = ico1_path  
    elif idx == 7:
        png = ico1_path 
    elif idx == 8:
        png = ico1_path 
        

    if HD.width() > 1280:    
    	if fileExists(png):
    		res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 12), size=(34, 25), png=loadPNG(png)))
    		res.append(MultiContentEntryText(pos=(60, 0), size=(1200, 50), font=7, text=name, color = 0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))# 
    else:
    	if fileExists(png):
    		res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 10), size=(34, 25), png=loadPNG(png)))
    		res.append(MultiContentEntryText(pos=(60, 7), size=(1200, 50), font=1, text=name, color = 0xa6d1fe, flags=RT_HALIGN_LEFT))# | RT_VALIGN_CENTER
    return res

#############OneSetList
class OneSetList(MenuList):
    def __init__(self, list):
            MenuList.__init__(self, list, True, eListboxPythonMultiContent)
            if HD.width() > 1280:
                    self.l.setItemHeight(50)
                    textfont = int(34)
                    self.l.setFont(0, gFont('Regular', textfont))            
            
            else:            
                    self.l.setItemHeight(50)
                    textfont = int(22)
                    self.l.setFont(0, gFont('Regular', textfont))

def OneSetListEntry(name):
    png2 = ico2_path 
    res = [name]
    if HD.width() > 1280:   
        res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 12), size=(34, 25), png=loadPNG(png2)))
        res.append(MultiContentEntryText(pos=(60, 0), size=(1200, 50), font=0, text=name, color = 0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))#
    else:    
        res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 10), size=(34, 25), png=loadPNG(png2)))
        res.append(MultiContentEntryText(pos=(60, 7), size=(1200, 50), font=0, text=name, color = 0xa6d1fe, flags=RT_HALIGN_LEFT))# | RT_VALIGN_CENTER
    return res

def showlist(data, list):                   
    icount = 0
    plist = []
    for line in data:
        name = data[icount]                               
        plist.append(OneSetListEntry(name))                               
        icount = icount+1
        list.setList(plist)			


#############MainSetting

class MainSetting(Screen):
    
    def __init__(self, session):        
        self.session = session
        # skin = skin_path + 'SettingsDaily.xml'
        skin = skin_path + 'settings.xml'        
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('MainSetting')
        Screen.__init__(self, session)
        self.setTitle(_('..:: slSettings V. %s  ~ Thanks all SettingMan ::..' % currversion)) 
        self['text'] = SetList([])
        self.working = False
        self.selection = 'all'
        self['title'] = Label(_('..:: slSettings V. %s  ~ Thanks all SettingMan ::..' % currversion)) 
        self['info'] = Label('') 
        self['info'].setText(_('Please select ...'))
        self['key_green'] = Button(_('Select'))      
        self['key_red'] = Button(_('Exit'))            
        self['actions'] = NumberActionMap(['SetupActions', 'ColorActions', ], {'ok': self.okRun,
         'green': self.okRun,
         'back': self.closerm,
         'red': self.closerm,
         'cancel': self.closerm}, -1)
        self.onLayoutFinish.append(self.updateMenuList)

    def closerm(self):
        self.close()
        
                
    def updateMenuList(self):
        self.menu_list = []
        for x in self.menu_list:
            del self.menu_list[0]
        list = []
        idx = 0
        for x in Panel_Dlist:
            list.append(DListEntry(x, idx))
            self.menu_list.append(x)
            idx += 1
        self['text'].setList(list)

    def okRun(self):
        self.keyNumberGlobalCB(self['text'].getSelectedIndex())

  
    def keyNumberGlobalCB(self, idx):
        sel = self.menu_list[idx]
        
        if sel == _('UPDATE SATELLITES.XML'):
            self.okSATELLITE()             
        elif sel == _('UPDATE TERRESTRIAL.XML'):
            self.okTERRESTRIAL()
        elif sel == ('SETTINGS CIEFP'):
            self.session.open(SettingCiefp)             
        elif sel == ('SETTINGS MALIMALI'):
            self.session.open(SettingMalimali)              
        elif sel == ('SETTINGS MANUTEK'):
            self.session.open(SettingManutek)    
        elif sel == ('SETTINGS MILENKA61'):
            self.session.open(SettingMilenka61)               
        elif sel == ('SETTINGS MORPHEUS'):
            self.session.open(SettingMorpheus) 
        elif sel == ('SETTINGS PREDRAG'):
            self.session.open(SettingPredrag)             
        elif sel == ('SETTINGS VHANNIBAL'):
            self.session.open(SettingVhan) 
     

# url_sat_oealliance  = 'http://raw.githubusercontent.com/oe-alliance/oe-alliance-tuxbox-common/master/src/satellites.xml'
# url_sat_openpli   = 'http://raw.githubusercontent.com/OpenPLi/tuxbox-xml/master/xml/satellites.xml' 
 
    def okSATELLITE(self):
        self.session.openWithCallback(self.okSatInstall,MessageBox,(_("Do you want to install?")), MessageBox.TYPE_YESNO)             
            
    def okSatInstall(self, result):
        if result:
            if checkInternet():
                try:            
                    url_sat_oealliance  = 'http://raw.githubusercontent.com/oe-alliance/oe-alliance-tuxbox-common/master/src/satellites.xml'
                    dirCopy = '/etc/tuxbox/satellites.xml' #'/etc/enigma2/satellites.xml'
                    urllib.urlretrieve(url_sat_oealliance, dirCopy, context=ssl._create_unverified_context())
                    self.mbox = self.session.open(MessageBox, _('Satellites.xml Updated!'), MessageBox.TYPE_INFO, timeout=5)
                    self['info'].setText(_('Installation performed successfully!'))   
        
                except:
                    return
            else:
                session.open(MessageBox, "No Internet", MessageBox.TYPE_INFO)             
            
            
    def okTERRESTRIAL(self):
        self.session.openWithCallback(self.okTerrInstall,MessageBox,(_("Do you want to install?")), MessageBox.TYPE_YESNO)             
            
    def okTerrInstall(self, result):
        if result:
            if checkInternet():
                try:            
                    url_sat_oealliance  = 'https://github.com/oe-alliance/oe-alliance-tuxbox-common/blob/master/src/terrestrial.xml'
                    dirCopy       = '/etc/tuxbox/terrestrial.xml' #'/etc/enigma2/terrestrial.xml'
                    urllib.urlretrieve(url_sat_oealliance, dirCopy, context=ssl._create_unverified_context())
                    self.mbox = self.session.open(MessageBox, _('Terrestrial.xml Updated!'), MessageBox.TYPE_INFO, timeout=5)
                    self['info'].setText(_('Installation performed successfully!'))   
        
                except:
                    return
            else:
                session.open(MessageBox, "No Internet", MessageBox.TYPE_INFO)                        
                    
          
class SettingVhan(Screen):
   
    def __init__(self, session):        

        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('SettingVhan')
        Screen.__init__(self, session)
        self.setTitle(_('..:: slSettings V. %s  ~ Thanks all SettingMan ::..' % currversion)) 
        self.list = []		
        self['text'] = OneSetList([]) 		
        self.addon = 'emu'
        self.icount = 0     
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))            
        self.downloading = False
        self.timer = eTimer()
        
        # if fileExists(BRAND)or fileExists(BRANDP):
            # self.timer.callback.append(self.downxmlpage) #pli
        # else:
            # self.timer_conn = self.timer.timeout.connect(self.downxmlpage) #cvs            
        # self.timer.start(1500, True)
        self.timer = eTimer() 
        self.timer.start(100, 1)        
        try: 
            self.timer_conn = self.timer.timeout.connect(self.downxmlpage)
        except:
            self.timer.callback.append(self.downxmlpage)		
		
		
		
        self['title'] = Label(_('..:: slSettings V. %s  ~ Thanks all SettingMan ::..' % currversion))      
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)


    def downxmlpage(self):
        url = base64.b64decode("aHR0cDovL3NhdC5hbGZhLXRlY2gubmV0L3VwbG9hZC9zZXR0aW5ncy92aGFubmliYWwv")
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)			
        
    def errorLoad(self, error):
        print str(error)	
        self['info'].setText(_('Try again later ...'))
        self.downloading = False

    def _gotPageLoad(self, data):
        self.xml = data
        self.names = []
        self.urls = []
        try:
            print "In Setting self.xml =", self.xml
            regex = '<a href="Vhannibal(.*?)"'
            match = re.compile(regex,re.DOTALL).findall(self.xml)
            print "In Setting match =", match
            for url in match:
                    name = "Vhannibal" + url
                    name = name.replace(".zip", "")
                    name = name.replace("%20", " ")
                    url64b = base64.b64decode("aHR0cDovL3NhdC5hbGZhLXRlY2gubmV0L3VwbG9hZC9zZXR0aW5ncy92aGFubmliYWwvVmhhbm5pYmFs")
                    url = url64b + url
                    self.urls.append(url)
                    self.names.append(name)
                    self['info'].setText(_('Please select ...'))					   
            showlist(self.names, self['text'])							
            self.downloading = True
        except:
            self.downloading = False
            
    def okRun(self):
        self.session.openWithCallback(self.okInstall,MessageBox,(_("Do you want to install?")), MessageBox.TYPE_YESNO)             
            
    def okInstall(self, result):
        if result:
            if self.downloading == True:
                selection = str(self['text'].getCurrent())
                idx = self["text"].getSelectionIndex()
                self.name = self.names[idx]
                url = self.urls[idx]
                dest = "/tmp/settings.zip"
                print "url =", url
                downloadPage(url, dest).addCallback(self.install).addErrback(self.showError)

            else:
                self.close  

                
    def showError(self, error):
                print "download error =", error
                self.close()

    def install(self, fplug):
        checkfile = '/tmp/settings.zip'
        if os.path.exists(checkfile):
            # os.system('unzip -o /tmp/download.zip -d /tmp/')
            os.system('rm -rf /etc/enigma2/lamedb')
            os.system('rm -rf /etc/enigma2/*.radio')
            os.system('rm -rf /etc/enigma2/*.tv')

            fdest1 = "/tmp" 
            fdest2 = "/etc/enigma2"
            cmd1 = "unzip -o -q '/tmp/settings.zip' -d " + fdest1
#        self.name2 = self.name.replace("%20", " ")
            cmd2 = "cp -rf  '/tmp/" + self.name + "'/* " + fdest2
            print "cmd2 =", cmd2
            cmd3 = "wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"
            cmd4 = "rm -rf /tmp/settings.zip"
            cmd5 = "rm -rf /tmp/Vhannibal*" #+ name + '*' # + selection
            cmd = []
            cmd.append(cmd1)
            cmd.append(cmd2)
            cmd.append(cmd3)
            cmd.append(cmd4)
            cmd.append(cmd5)
            title = _("Installation Settings")          
            self.session.open(Console,_(title),cmd)              

class SettingMilenka61(Screen):
   
    def __init__(self, session):        
 
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('SettingMilenka61')
        Screen.__init__(self, session)
        self.setTitle(_('..:: slSettings V. %s  ~ Thanks all SettingMan ::..' % currversion))  
        self.list = []		
        self['text'] = OneSetList([]) 		
        self.addon = 'emu'
        self.icount = 0       
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))    
        self.downloading = False
        self.timer = eTimer() 
        self.timer.start(100, 1)        
        try: 
            self.timer_conn = self.timer.timeout.connect(self.downxmlpage)
        except:
            self.timer.callback.append(self.downxmlpage)	
        self['title'] = Label(_('..:: slSettings V. %s  ~ Thanks all SettingMan ::..' % currversion))      
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,        
         'cancel': self.close}, -2)


    def downxmlpage(self):
        url = base64.b64decode("aHR0cDovL3ZlbnVzY3MubmV0L3NhdHZlbnVzRTIv")
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)			
        
    def errorLoad(self, error):
        print str(error)	
        self['info'].setText(_('Try again later ...'))
        self.downloading = False

    def _gotPageLoad(self, data):

        self.xml = data
        self.names = []
        self.urls = []
        try:
            print "In Setting self.xml =", self.xml
            regex = '<a href="Satvenus(.*?)"'
            match = re.compile(regex,re.DOTALL).findall(self.xml)
            print "In Setting match =", match
            for url in match:
                    name = "Satvenus" + url
                    name = name.replace(".zip", "")
                    name = name.replace("Satvenus%20EX-YU%20Lista%20za%20milenka61%20", "")                     
                    name = name.replace("%20", " ")
                    url64b = base64.b64decode("aHR0cDovL3ZlbnVzY3MubmV0L3NhdHZlbnVzRTIvU2F0dmVudXM=")
                    url = url64b + url
                    self.urls.append(url)
                    self.names.append(name)
                    self['info'].setText(_('Please select ...'))					   
            showlist(self.names, self['text'])							
            self.downloading = True
        except:
            self.downloading = False
            
    def okRun(self):
        self.session.openWithCallback(self.okInstall,MessageBox,(_("Do you want to install?")), MessageBox.TYPE_YESNO)             
            
    def okInstall(self, result):
        if result:
            if self.downloading == True:
#            try:
                selection = str(self['text'].getCurrent())
                idx = self["text"].getSelectionIndex()
                self.name = self.names[idx]
                url = self.urls[idx]
                dest = "/tmp/settings.zip"
                print "url =", url
                downloadPage(url, dest).addCallback(self.install).addErrback(self.showError)
            else:
                self.close  

                
    def showError(self, error):
                print "download error =", error
                self.close()

    def install(self, fplug):
        checkfile = '/tmp/settings.zip'
        if os.path.exists(checkfile):
            # os.system('unzip -o /tmp/download.zip -d /tmp/')
            os.system('rm -rf /etc/enigma2/lamedb')
            os.system('rm -rf /etc/enigma2/*.radio')
            os.system('rm -rf /etc/enigma2/*.tv')
            
            os.system('mkdir /tmp/milenka61')
            fdest1 = "/tmp/milenka61" 
            fdest2 = "/etc/enigma2"
            cmd1 = "unzip -o -q '/tmp/settings.zip' -d " + fdest1
#        self.name2 = self.name.replace("%20", " ")
            cmd2 = "cp -rf /tmp/milenka61/* " + fdest2
            print "cmd2 =", cmd2
            cmd3 = "wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"
            cmd4 = "rm -rf /tmp/settings.zip"
            cmd5 = "rm -rf /tmp/milenka61*" #+ name + '*' # + selection
            cmd = []
            cmd.append(cmd1)
            cmd.append(cmd2)
            cmd.append(cmd3)
            cmd.append(cmd4)
            cmd.append(cmd5)
            title = _("Installation Settings")          
            self.session.open(Console,_(title),cmd)              

class SettingManutek(Screen):
   
    def __init__(self, session):        
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('SettingManutek')
        Screen.__init__(self, session)
        self.setTitle(_('..:: slSettings V. %s  ~ Thanks all SettingMan ::..' % currversion))    
        self.list = []		
        self['text'] = OneSetList([]) 		
        self.addon = 'emu'
        self.icount = 0      
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))    
        self.downloading = False
        self.timer = eTimer() 
        self.timer.start(100, 1)        
        try: 
            self.timer_conn = self.timer.timeout.connect(self.downxmlpage)
        except:
            self.timer.callback.append(self.downxmlpage)	
        self['title'] = Label(_('..:: slSettings V. %s  ~ Thanks all SettingMan ::..' % currversion)) 
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,            
         'cancel': self.close}, -2)


    def downxmlpage(self):
        url = base64.b64decode("aHR0cDovL3d3dy5tYW51dGVrLml0L2lzZXR0aW5nLw==")
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)			

        
    def errorLoad(self, error):
        print str(error)	
        self['info'].setText(_('Try again later ...'))
        self.downloading = False

    def _gotPageLoad(self, data):

        self.xml = data
        self.names = []
        self.urls = []
        try:
            print "In Setting self.xml =", self.xml
            match = re.compile('href=".*?file=(.+?)">', re.DOTALL).findall(self.xml)            
            print "In Setting match =", match
            for url in match:
                    # name = "NemoxyzRLS" + url
                    name = url
                    name = name.replace(".zip", "")
                    name = name.replace("%20", " ")
                    name = name.replace("NemoxyzRLS_", "")                     
                    name = name.replace("_", " ")
                    url64b = base64.b64decode("aHR0cDovL3d3dy5tYW51dGVrLml0L2lzZXR0aW5nL2VuaWdtYTIv")
                    url = url64b + url
                    self.urls.append(url)
                    self.names.append(name)
                    self['info'].setText(_('Please select ...'))					   
            showlist(self.names, self['text'])							
            self.downloading = True
        except:
            self.downloading = False
            
    def okRun(self):
        self.session.openWithCallback(self.okInstall,MessageBox,(_("Do you want to install?")), MessageBox.TYPE_YESNO)             
            
    def okInstall(self, result):
        if result:
            if self.downloading == True:
                selection = str(self['text'].getCurrent())
                idx = self["text"].getSelectionIndex()
                self.name = self.names[idx]
                url = self.urls[idx]
                dest = "/tmp/settings.zip"
                print "url =", url
                downloadPage(url, dest).addCallback(self.install).addErrback(self.showError)

            else:
                self.close  

                
    def showError(self, error):
                print "download error =", error
                self.close()

    def install(self, fplug):
        checkfile = '/tmp/settings.zip'
        if os.path.exists(checkfile):
            fdest1 = "/tmp/unzipped" 
            fdest2 = "/etc/enigma2"
            if os.path.exists("/tmp/unzipped"):
                cmd = "rm -rf '/tmp/unzipped'"
                os.system(cmd)
            cmd1 = "mkdir -p '/tmp/unzipped'"
            os.system(cmd1)
            cmd2 = "unzip -o -q '/tmp/settings.zip' -d " + fdest1
            os.system(cmd2)

            for root, dirs, files in os.walk(fdest1):
                for name in dirs:
                    os.system('rm -rf /etc/enigma2/lamedb')
                    os.system('rm -rf /etc/enigma2/*.radio')
                    os.system('rm -rf /etc/enigma2/*.tv')
                    cmd3 = "cp -rf  '/tmp/unzipped/" + name + "'/* " + fdest2
                    cmd4 = "wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"
                    cmd5 = "rm -rf /tmp/settings.zip"
                    cmd6 = "rm -rf /tmp/unzipped" 
                    cmd = []
                    cmd.append(cmd3)
                    cmd.append(cmd4)
                    cmd.append(cmd5)
                    cmd.append(cmd6)
                title = _("Installation Settings")          
                self.session.open(Console,_(title),cmd)              

class SettingMorpheus(Screen):
   
    def __init__(self, session):        
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('SettingMorpheus')
        Screen.__init__(self, session)
        self.setTitle(_('..:: slSettings V. %s  ~ Thanks all SettingMan ::..' % currversion))         
        self.list = []		
        self['text'] = OneSetList([]) 		
        self.addon = 'emu'
        self.icount = 0      
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))    
        self.downloading = False
        self.timer = eTimer() 
        self.timer.start(100, 1)        
        try: 
            self.timer_conn = self.timer.timeout.connect(self.downxmlpage)
        except:
            self.timer.callback.append(self.downxmlpage)	
        self['title'] = Label(_('..:: slSettings V. %s  ~ Thanks all SettingMan ::..' % currversion))
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,           
         'cancel': self.close}, -2)
         
    def downxmlpage(self):
        url = base64.b64decode("aHR0cDovL21vcnBoZXVzODgzLmFsdGVydmlzdGEub3JnL2Rvd25sb2FkL2luZGV4LnBocD9kaXI9")
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)			

    def errorLoad(self, error):
        print str(error)	
        self['info'].setText(_('Try again later ...'))
        self.downloading = False

    def _gotPageLoad(self, data):
        self.xml = data
        self.names = []
        self.urls = []
        try:
            print "In Setting self.xml =", self.xml
            match = re.compile('href=".*?file=(.+?)">', re.DOTALL).findall(self.xml)            
            print "In Setting match =", match
            for url in match:
                if 'zip' in url.lower():
                    if 'settings' in url.lower():
                        continue    
                    name = url
                    name = name.replace(".zip", "")
                    name = name.replace("%20", " ")
                    name = name.replace("_", " ")
                    name = name.replace("Morph883", "Morpheus883")    
                    url64b = base64.b64decode("aHR0cDovL21vcnBoZXVzODgzLmFsdGVydmlzdGEub3JnL3NldHRpbmdzLw==")
                    url = url64b + url
                    print 'url 64b-url-', url
                    self.urls.append(url)
                    self.names.append(name)
                    self['info'].setText(_('Please select ...'))					   
            showlist(self.names, self['text'])							
            self.downloading = True
        except:
            self.downloading = False
            
    def okRun(self):
        self.session.openWithCallback(self.okInstall,MessageBox,(_("Do you want to install?")), MessageBox.TYPE_YESNO)             
            
    def okInstall(self, result):
        if result:
            if self.downloading == True:
                idx = self["text"].getSelectionIndex()
                self.name = self.names[idx]
                url = self.urls[idx]
                dest = "/tmp/settings.zip"
                print "url =", url
                url= str(url)
                downloadPage(url, dest).addCallback(self.install).addErrback(self.showError)
            else:
                self.close  
                
    def showError(self, error):
                print "download error =", error
                self.close()

    def install(self, fplug):
            checkfile = '/tmp/settings.zip'
            if os.path.exists(checkfile):
                if os.path.exists("/tmp/unzipped"):
                    os.system('rm -rf /tmp/unzipped')
                os.system('mkdir -p /tmp/unzipped')
                os.system('unzip -o -q /tmp/settings.zip -d /tmp/unzipped')
                path = '/tmp/unzipped'
                for root, dirs, files in os.walk(path):
                    for pth in dirs:
                        cmd = []
                        os.system('rm -rf /etc/enigma2/lamedb')
                        os.system('rm -rf /etc/enigma2/*.radio')
                        os.system('rm -rf /etc/enigma2/*.tv')
                        cmd1 = "cp -rf /tmp/unzipped/" + pth + "/* '/etc/enigma2'"   
                        cmd.append(cmd1)                      
                title = _("Installation Settings")          
                self.session.open(Console,_(title),cmd) 
                
            deletetmp()
            self.reloadSettings()            

    def reloadSettings(self):
        ReloadBouquet()
        self.mbox = self.session.open(MessageBox, _('Setting Installed!'), MessageBox.TYPE_INFO, timeout=5)
        self['info'].setText(_('Installation performed successfully!'))     
    
        
class SettingCiefp(Screen):
   
    def __init__(self, session):        
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('SettingCiefp')
        Screen.__init__(self, session)
        self.setTitle(_('..:: slSettings V. %s  ~ Thanks all SettingMan ::..' % currversion))         
        self.list = []		
        self['text'] = OneSetList([]) 		
        self.addon = 'emu'
        self.icount = 0       
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))    
        self.downloading = False
        self.timer = eTimer() 
        self.timer.start(100, 1)        
        try: 
            self.timer_conn = self.timer.timeout.connect(self.downxmlpage)
        except:
            self.timer.callback.append(self.downxmlpage)	
        self['title'] = Label(_('..:: slSettings V. %s  ~ Thanks all SettingMan ::..' % currversion))
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,         
         'cancel': self.close}, -2)
         
    def downxmlpage(self):
        url = base64.b64decode("aHR0cDovLzE3OC42My4xNTYuNzUvcGFuZWxhZGRvbnMvQ2llZnAv")
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)			

        
    def errorLoad(self, error):
        print str(error)	
        self['info'].setText(_('Try again later ...'))
        self.downloading = False

    def _gotPageLoad(self, data):
        self.xml = data
        self.names = []
        self.urls = []
        try:
            print "In Setting self.xml =", self.xml
            regex = '<a href="ciefp(.*?)"'
            match = re.compile(regex,re.DOTALL).findall(self.xml)
            print "In Setting match =", match
            for url in match:
                if url.find('.tar.gz') != -1 : 
                    name = "ciefp" + url
                    name = name.replace(".tar.gz", "")                    
                    name = name.replace("%20", " ")
                    url64b = base64.b64decode("aHR0cDovLzE3OC42My4xNTYuNzUvcGFuZWxhZGRvbnMvQ2llZnAvY2llZnA=")                    
                    url = url64b + url
                    self.urls.append(url)
                    self.names.append(name)
                    self['info'].setText(_('Please select ...'))					   
            showlist(self.names, self['text'])							
            self.downloading = True
        except:
            self.downloading = False
            
    def okRun(self):
        self.session.openWithCallback(self.okInstall,MessageBox,(_("Do you want to install?")), MessageBox.TYPE_YESNO)             
            
    def okInstall(self, result):
        if result:
            if self.downloading == True:
#            try:
                selection = str(self['text'].getCurrent())
                idx = self["text"].getSelectionIndex()
                self.name = self.names[idx]
                url = self.urls[idx]
                dest = "/tmp/settings.tar.gz"
                print "url =", url
                downloadPage(url, dest).addCallback(self.install).addErrback(self.showError)

            else:
                self.close  
                
    def showError(self, error):
                print "download error =", error
                self.close()

    def install(self, fplug):
        
        checkfile = '/tmp/settings.tar.gz'
        if os.path.exists(checkfile):
            # os.system('unzip -o /tmp/download.zip -d /tmp/')
            os.system('rm -rf /etc/enigma2/lamedb')
            os.system('rm -rf /etc/enigma2/*.radio')
            os.system('rm -rf /etc/enigma2/*.tv')
            cmd1 = "tar -xvf /tmp/*.tar.gz -C /" 
            print "cmd1 =", cmd1
            cmd3 = "wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"
            cmd4 = "rm -rf /tmp/*.tar.gz"
            cmd = []
            cmd.append(cmd1)
            cmd.append(cmd3)
            cmd.append(cmd4)
            title = _("Installation Settings")          
            self.session.open(Console,_(title),cmd)              
        
  
        
class SettingMalimali(Screen):

    def __init__(self, session):        
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('SettingMalimali')
        Screen.__init__(self, session)
        self.setTitle(_('..:: slSettings V. %s  ~ Thanks all SettingMan ::..' % currversion)) 
        self.list = []		
        self['text'] = OneSetList([]) 		
        self.addon = 'emu'
        self.icount = 0
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))    
        self.downloading = False
        self.timer = eTimer() 
        self.timer.start(100, 1)        
        try: 
            self.timer_conn = self.timer.timeout.connect(self.downxmlpage)
        except:
            self.timer.callback.append(self.downxmlpage)	
        self['title'] = Label(_('..:: slSettings V. %s  ~ Thanks all SettingMan ::..' % currversion))
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,          
         'cancel': self.close}, -2)
         
    def downxmlpage(self):
        url = base64.b64decode("aHR0cDovLzE3OC42My4xNTYuNzUvcGFuZWxhZGRvbnMvTWFsaW1hbGkv")
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)			

        
    def errorLoad(self, error):
        print str(error)	
        self['info'].setText(_('Try again later ...'))
        self.downloading = False

    def _gotPageLoad(self, data):

        self.xml = data
        self.names = []
        self.urls = []
        try:
            print "In Setting self.xml =", self.xml
            regex = '<a href="malimali(.*?)"'
            match = re.compile(regex,re.DOTALL).findall(self.xml)
            print "In Setting match =", match
            for url in match:
                if url.find('.tar.gz') != -1 : 
                    name = "malimali" + url
                    name = name.replace(".tar.gz", "")                    
                    name = name.replace("%20", " ")
                    url64b = base64.b64decode("aHR0cDovLzE3OC42My4xNTYuNzUvcGFuZWxhZGRvbnMvTWFsaW1hbGkvbWFsaW1hbGk=")                    
                    url = url64b + url
                    self.urls.append(url)
                    self.names.append(name)
                    self['info'].setText(_('Please select ...'))					   
            showlist(self.names, self['text'])							
            self.downloading = True
        except:
            self.downloading = False
            
    def okRun(self):
        self.session.openWithCallback(self.okInstall,MessageBox,(_("Do you want to install?")), MessageBox.TYPE_YESNO)             
            
    def okInstall(self, result):
        if result:
            if self.downloading == True:
#            try:
                selection = str(self['text'].getCurrent())
                idx = self["text"].getSelectionIndex()
                self.name = self.names[idx]
                url = self.urls[idx]
                dest = "/tmp/settings.tar.gz"
                print "url =", url
                downloadPage(url, dest).addCallback(self.install).addErrback(self.showError)
            else:
                self.close  

                
    def showError(self, error):
                print "download error =", error
                self.close()

    def install(self, fplug):
        
        checkfile = '/tmp/settings.tar.gz'
        if os.path.exists(checkfile):
            # os.system('unzip -o /tmp/download.zip -d /tmp/')
            os.system('rm -rf /etc/enigma2/lamedb')
            os.system('rm -rf /etc/enigma2/*.radio')
            os.system('rm -rf /etc/enigma2/*.tv')
            cmd1 = "tar -xvf /tmp/*.tar.gz -C /" 
            print "cmd1 =", cmd1
            cmd3 = "wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"
            cmd4 = "rm -rf /tmp/*.tar.gz"
            cmd = []
            cmd.append(cmd1)
            cmd.append(cmd3)
            cmd.append(cmd4)
            title = _("Installation Settings")          
            self.session.open(Console,_(title),cmd)              
        
class SettingPredrag(Screen):
   
    def __init__(self, session):        
        self.session = session
        skin = skin_path + 'settings.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('SettingPredrag')
        Screen.__init__(self, session)
        self.setTitle(_('..:: slSettings V. %s  ~ Thanks all SettingMan ::..' % currversion)) 
        self.list = []		
        self['text'] = OneSetList([]) 		
        self.addon = 'emu'
        self.icount = 0
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))           
        self.downloading = False
        self.timer = eTimer() 
        self.timer.start(100, 1)        
        try: 
            self.timer_conn = self.timer.timeout.connect(self.downxmlpage)
        except:
            self.timer.callback.append(self.downxmlpage)	
        self['title'] = Label(_('..:: slSettings V. %s  ~ Thanks all SettingMan ::..' % currversion))
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,         
         'cancel': self.close}, -2)
         
    def downxmlpage(self):
        url = base64.b64decode("aHR0cDovLzE3OC42My4xNTYuNzUvcGFuZWxhZGRvbnMvUHJlZHJAZy8=")
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)			

        
    def errorLoad(self, error):
        print str(error)	
        self['info'].setText(_('Try again later ...'))
        self.downloading = False

    def _gotPageLoad(self, data):

        self.xml = data
        self.names = []
        self.urls = []
        try:
            print "In Setting self.xml =", self.xml
            regex = '<a href="predrag(.*?)"'
            match = re.compile(regex,re.DOTALL).findall(self.xml)
            print "In Setting match =", match
            for url in match:
                if url.find('.tar.gz') != -1 : 
                    name = "predrag" + url
                    name = name.replace(".tar.gz", "")                    
                    name = name.replace("%20", " ")
                    url64b = base64.b64decode("aHR0cDovLzE3OC42My4xNTYuNzUvcGFuZWxhZGRvbnMvUHJlZHJAZy9wcmVkcmFn")                    
                    url = url64b + url
                    self.urls.append(url)
                    self.names.append(name)
                    self['info'].setText(_('Please select ...'))					   
            showlist(self.names, self['text'])							
            self.downloading = True
        except:
            self.downloading = False
            
    def okRun(self):
        self.session.openWithCallback(self.okInstall,MessageBox,(_("Do you want to install?")), MessageBox.TYPE_YESNO)             
            
    def okInstall(self, result):
        if result:
            if self.downloading == True:
#            try:
                selection = str(self['text'].getCurrent())
                idx = self["text"].getSelectionIndex()
                self.name = self.names[idx]
                url = self.urls[idx]
                dest = "/tmp/settings.tar.gz"
                print "url =", url
                downloadPage(url, dest).addCallback(self.install).addErrback(self.showError)
            else:
                self.close  

                
    def showError(self, error):
                print "download error =", error
                self.close()

    def install(self, fplug):
        
        checkfile = '/tmp/settings.tar.gz'
        if os.path.exists(checkfile):
            # os.system('unzip -o /tmp/download.zip -d /tmp/')
            os.system('rm -rf /etc/enigma2/lamedb')
            os.system('rm -rf /etc/enigma2/*.radio')
            os.system('rm -rf /etc/enigma2/*.tv')
            cmd1 = "tar -xvf /tmp/*.tar.gz -C /" 
            print "cmd1 =", cmd1
            cmd3 = "wget -qO - http://127.0.0.1/web/servicelistreload?mode=0 > /tmp/inst.txt 2>&1 &"
            cmd4 = "rm -rf /tmp/*.tar.gz"
            cmd = []
            cmd.append(cmd1)
            cmd.append(cmd3)
            cmd.append(cmd4)
            title = _("Installation Settings")          
            self.session.open(Console,_(title),cmd)              
        
        

def main(session, **kwargs):
    if checkInternet():
        session.open(MainSetting)
    else:
        session.open(MessageBox, "No Internet", MessageBox.TYPE_INFO)   
		
def StartSetup(menuid):
    if menuid == 'scan':
        return [('SatLodge Settings',
          main,
          'SatLodge Settings',
          None)]
    else:
        return []

		
def Plugins(**kwargs):
    return [PluginDescriptor(name=_('SatLodge Settings'), description=_('SatLodge Settings'), where=PluginDescriptor.WHERE_MENU, fnc=StartSetup),
	 PluginDescriptor(name='SatLodge Settings', description=_('SatLodge Settings'), where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=main)]   
    
    # return [PluginDescriptor(name='slSettings', description=_('slSettings V.' + currversion), where=[PluginDescriptor.WHERE_PLUGINMENU], icon=ico_path, fnc=main), 
	 # PluginDescriptor(name=_('slSettings'), description=_('slSettings'), where=PluginDescriptor.WHERE_MENU, fnc=StartSetup),
	 # PluginDescriptor(name='slSettings', description=_('slSettings'), where=PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=main)]  
	 
