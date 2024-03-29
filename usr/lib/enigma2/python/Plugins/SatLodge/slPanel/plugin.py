#"****************************************"
#"*    by Lululla 16.08.2019             *"
#"*     all right reserved               *"
#"*          no copy                     *"
#"*     all right reserved               *"
#       mod daimon 11-03-2021            *"
#"****************************************"
from Components.ActionMap import ActionMap, NumberActionMap
from Components.Button import Button
from Components.ConfigList import ConfigListScreen
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
from Components.config import config, getConfigListEntry, ConfigText, ConfigInteger, ConfigSelection, ConfigSubsection, ConfigYesNo
from Plugins.Plugin import PluginDescriptor
from Screens.Console import Console
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.Standby import *
from Screens.Standby import TryQuitMainloop
from Tools.Directories import *
from Tools.Directories import SCOPE_SKIN_IMAGE, resolveFilename, SCOPE_PLUGINS, fileExists, copyfile, SCOPE_LANGUAGE, pathExists
from Tools.LoadPixmap import LoadPixmap
from enigma import *
from enigma import RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_HALIGN_CENTER, getDesktop, loadPNG, loadPic
from enigma import eListbox, eTimer, eListboxPythonMultiContent, eConsoleAppContainer, addFont, gFont 
from os import environ as os_environ
from os import path, listdir, remove, mkdir, chmod
from twisted.web.client import downloadPage, getPage
from xml.dom import Node, minidom
import base64
import gettext
import os, re, sys
import shutil
import urllib
import urllib2
import ssl
#############################################
from Components.ProgressBar import ProgressBar
from Components.Sources.Progress import Progress
from Tools.Downloader import downloadWithProgress
#############################################   

# def mountipkpth():
	# ipkpth = []
	# if os.path.isfile('/proc/mounts'):
		# for line in open('/proc/mounts'):
			# if '/dev/sd' in line or '/dev/disk/by-uuid/' in line or '/dev/mmc' in line or '/dev/mtdblock' in line:
				# ipkpth.append(line.split()[1].replace('\\040', ' ') + '/')
	# ipkpth.append('/tmp')
	# return ipkpth

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
        
def freespace():
    try:
        diskSpace = os.statvfs('/')
        capacity = float(diskSpace.f_bsize * diskSpace.f_blocks)
        available = float(diskSpace.f_bsize * diskSpace.f_bavail)
        fspace = round(float(available / 1048576.0), 2)
        tspace = round(float(capacity / 1048576.0), 1)
        spacestr = 'Free space(' + str(fspace) + 'MB) Total space(' + str(tspace) + 'MB)'
        return spacestr
    except:
        return ''    
        

def ReloadBouquet():
    eDVBDB.getInstance().reloadServicelist()
    eDVBDB.getInstance().reloadBouquets() 
    
def deletetmp():
    os.system('rm -rf /tmp/unzipped;rm -f /tmp/*.ipk;rm -f /tmp/*.tar;rm -f /tmp/*.zip;rm -f /tmp/*.tar.gz;rm -f /tmp/*.tar.bz2;rm -f /tmp/*.tar.tbz2;rm -f /tmp/*.tar.tbz')    
   
def mountipkpth():
    ipkpth = []
    if os.path.isfile('/proc/mounts'):
        for line in open('/proc/mounts'):
            if '/dev/sd' in line or '/dev/disk/by-uuid/' in line or '/dev/mmc' in line or '/dev/mtdblock' in line:
                drive = line.split()[1].replace('\\040', ' ') + '/'

                if not drive in ipkpth:
                      ipkpth.append(drive)
    ipkpth.append('/tmp')
    return ipkpth    
    
    
config.plugins.slPanel = ConfigSubsection()
config.plugins.slPanel.strtext = ConfigYesNo(default=True)
# config.plugins.slPanel.strtmain = ConfigYesNo(default=True)
config.plugins.slPanel.strtst = ConfigYesNo(default=False)
config.plugins.slPanel.ipkpth = ConfigSelection(default = "/tmp",choices = mountipkpth())
# config.plugins.slPanel.autoupd = ConfigYesNo(default=False)


DESKHEIGHT = getDesktop(0).size().height()

currversion = '2.6'
plugin_path = '/usr/lib/enigma2/python/Plugins/SatLodge/slPanel'
ico_path = plugin_path +  '/res/pics/addons3.png'
##########################################
data_upd = 'aHR0cHM6Ly93ZWJwbHVzZmVlZHMuc2F0LWxvZGdlLml0Lw=='
upd_path = base64.b64decode(data_upd)
data_xml = 'aHR0cHM6Ly93ZWJwbHVzZmVlZHMuc2F0LWxvZGdlLml0L3htbC8='
xml_path = base64.b64decode(data_xml)
#########################################
pics_path = plugin_path +  '/res/pics/icon.png'
ico1_path = plugin_path +  '/res/pics/plugins.png'
ico2_path = plugin_path +  '/res/pics/plugin.png'
ico3_path = plugin_path +  '/res/pics/instuninstl.png'

skin_path = plugin_path
HD = getDesktop(0).size()
if HD.width() >= 1280:
   skin_path = plugin_path + '/res/skins/fhd/'
else:
   skin_path = plugin_path + '/res/skins/hd/'
#########################################################
PluginLanguageDomain = 'slpanel'
PluginLanguagePath = '/usr/lib/enigma2/python/Plugins/SatLodge/slPanel/res/locale'
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
#########################################################
class logoStrt(Screen):
    skin = """
    <screen name="logoStrt" position="center,center" size="462,454" flags="wfNoBorder">
    <ePixmap position="0,0" size="462,454" pixmap="/usr/lib/enigma2/python/Plugins/SatLodge/slPanel/res/pics/sl_hd.png" />
    </screen> """    

    def __init__(self, session):
        self.session = session  
        Screen.__init__(self, session)
        self['actions'] = ActionMap(['SetupActions'], {'ok': self.disappear,
        'cancel': self.disappear}, -1)
        self.timer = eTimer() 
        self.timer.start(100, 1)        
        try: 
            self.timer_conn = self.timer.timeout.connect(self.disappear)
        except:
            self.timer.callback.append(self.disappear)    

    def disappear(self):
        self.session.openWithCallback(self.close, Homesl)

Panel_list = [
 _('SATLODGE IMAGE'),
 _('SETTINGS DAILY'), 
 _('PLUGIN EMULATORS CAMS'),
 _('PLUGIN MULTIMEDIA')]						 
         
class SLList(MenuList):

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
        if HD.width() >= 1280:
            self.l.setItemHeight(50)
        else:		
            self.l.setItemHeight(50)
            
def SLListEntry(name, idx):
    res = [name]
    if idx == 0:
        png = ico1_path
    elif idx == 1:
        png = ico1_path
    if idx == 2:
        png = ico1_path
    elif idx == 3:
        png = ico1_path
    if idx == 4:
        png = ico1_path
    elif idx == 5:
        png = ico1_path
    if idx == 6:
        png = ico1_path
    elif idx == 7:
        png = ico1_path
    if idx == 8:
        png = ico1_path
    elif idx == 9:
        png = ico1_path
    if idx == 10:
        png = ico1_path 
    elif idx == 11:
        png = ico1_path   
    if idx == 12:
        png = ico1_path      
    elif idx == 13:
        png = ico1_path
    if idx == 14:
        png = ico1_path 
    elif idx == 15:
        png = ico1_path 
    if idx == 16:
        png = ico1_path
    elif idx == 17:
        png = ico1_path 
        
    if HD.width() >= 1280:
    	if fileExists(png):
    		res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 4), size=(34, 25), png=loadPNG(png)))
    		res.append(MultiContentEntryText(pos=(60, 0), size=(1200, 50), font=6, text=name, color = 0xa6d1fe, flags=RT_HALIGN_LEFT )) #| RT_VALIGN_CENTER
    else:
    	if fileExists(png):
    		res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 0), size=(34, 25), png=loadPNG(png)))
    		res.append(MultiContentEntryText(pos=(60, 0), size=(1200, 50), font=1, text=name, color = 0xa6d1fe, flags=RT_HALIGN_LEFT )) #| RT_VALIGN_CENTER
    return res        
        
Panel_list2 = [
 ('UPDATE SATELLITES.XML'), 
 ('UPDATE TERRESTRIAL.XML'),
 ('SETTINGS CIEFP'), 
 ('SETTINGS MALIMALI'),  
 ('SETTINGS MANUTEK'),  
 ('SETTINGS MILENKA61'), 
 ('SETTINGS MORPHEUS'),
 ('SETTINGS PREDRAG'), 
 ('SETTINGS VHANNIBAL')] 
 
def DailyListEntry(name, idx):
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
        
    if HD.width() >= 1280:    
    	if fileExists(png):
    		res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 2), size=(34, 25), png=loadPNG(png)))
    		res.append(MultiContentEntryText(pos=(60, 0), size=(1200, 50), font=6, text=name, color = 0xa6d1fe, flags=RT_HALIGN_LEFT )) #| RT_VALIGN_CENTER
    else:
    	if fileExists(png):
    		res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 0), size=(34, 25), png=loadPNG(png)))
    		res.append(MultiContentEntryText(pos=(60, 0), size=(1200, 50), font=1, text=name, color = 0xa6d1fe, flags=RT_HALIGN_LEFT )) #| RT_VALIGN_CENTER
    return res
    
######################

class oneListsl(MenuList):
    def __init__(self, list):
            MenuList.__init__(self, list, True, eListboxPythonMultiContent)
            if HD.width() >= 1280:
                    self.l.setItemHeight(50)
                    textfont = int(32)
                    self.l.setFont(0, gFont('Regular', textfont))            
            else:            
                    self.l.setItemHeight(45)
                    textfont = int(22)
                    self.l.setFont(0, gFont('Regular', textfont))
               
def oneListEntry(name):
    png2 = ico3_path     
    res = [name]
    #
    if HD.width() >= 1280:   
        res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 8), size=(30, 30), png=loadPNG(png2)))
        res.append(MultiContentEntryText(pos=(60, 4), size=(1200, 50), font=0, text=name, color = 0xa6d1fe, flags=RT_HALIGN_LEFT ))#| RT_VALIGN_CENTER
    else:    
        res.append(MultiContentEntryPixmapAlphaTest(pos=(10, 0), size=(30, 30), png=loadPNG(png2)))
        res.append(MultiContentEntryText(pos=(60, 0), size=(1200, 50), font=0, text=name, color = 0xa6d1fe, flags=RT_HALIGN_LEFT )) #| RT_VALIGN_CENTER
    return res

def showlist(data, list):                   
    icount = 0
    plist = []
    for line in data:
        name = data[icount]                               
        plist.append(oneListEntry(name))                               
        icount = icount+1
        list.setList(plist)			
   
class Homesl(Screen):

    def __init__(self, session):
        self.session = session
        skin = skin_path + 'Homesl.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('Hometv')
        Screen.__init__(self, session)
        self.setTitle(_('Sat-Lodge Panel V. %s' % currversion))         
        self.session = session
        self['text'] = SLList([])
        self.working = False
        self.selection = 'all'
        self['title'] = Label(_('..:: Sat-Lodge Panel ::..'))
        self['version'] = Label(_('V. %s' %  currversion))
        self['maintener'] = Label(_(' by ))^^((')) 
        self['key_red'] = Button(_('Exit')) 
        self["key_yellow"] = Button(_("Uninstall"))
        self['key_green'] = Button(_('Extensions')) 
        self["key_blue"] = Button(_("SatLodge Manager"))
        self['key_blue'].hide()
        if fileExists('/usr/lib/enigma2/python/Plugins/SatLodge/slManager/plugin.pyo'):
            self["key_blue"].show()          
        self['actions'] = NumberActionMap(['SetupActions', 'ColorActions', "MenuActions"], {'ok': self.okRun,
         'green': self.IPKinst,
         'menu': self.goConfig,
         'blue': self.slManager,
         # 'yellow': self.slUpdate,
         'yellow': self.ipkDs,
         'red': self.closerm,
         'back': self.closerm,
         'cancel': self.closerm}, -1)
        self.onLayoutFinish.append(self.updateMenuList)

    def slImageDownloader(self):
        from .main import STBmodel
        session.open(STBmodel)
    
    def slManager(self):
        if fileExists('/usr/lib/enigma2/python/Plugins/SatLodge/slManager/plugin.pyo'):
            from Plugins.SatLodge.slManager.plugin import slManager
            self.session.openWithCallback(self.close, slManager)
        else: 
            self.session.open(slMessageBox,("slManager Not Installed!!"), type=slMessageBox.TYPE_INFO, timeout=3)

    def closerm(self):
        #os.system('rm -f /tmp/*.ipk;rm -f /tmp/*.tar;rm -f /tmp/*.zip;rm -f /tmp/*.tar.gz;rm -f /tmp/*.tar.bz2;rm -f /tmp/*.tar.tbz2;rm -f /tmp/*.tar.tbz')
        self.close()
        
    def goConfig(self):
        self.session.open(slPanelConfig)
                
    def updateMenuList(self):
        self.menu_list = []
        for x in self.menu_list:
            del self.menu_list[0]

        list = []
        idx = 0
        for x in Panel_list:
            list.append(SLListEntry(x, idx))
            self.menu_list.append(x)
            idx += 1
        self['text'].setList(list)

    def okRun(self):
        self.keyNumberGlobal(self['text'].getSelectedIndex())

    def ipkDs(self):
        self.session.open(pluginSl)  
        
    # def slUpdate(self):
        # self.session.open(slUpdate)    
            
    def IPKinst(self):
        self.session.open(IPKinst)          
        
    def keyNumberGlobal(self, idx):
        sel = self.menu_list[idx]
		
        if sel == _('PLUGIN EMULATORS CAMS'):
            self.session.open(PluginEmulators)   			
        elif sel == _('PLUGIN MULTIMEDIA'):
            self.session.open(PluginMultim)
        elif sel == _('SETTINGS DAILY'):
            self.session.open(DailySetting)
        elif sel == _('SATLODGE IMAGE'):
            from .main import STBmodel
            self.session.open(STBmodel)  
            
class PluginEmulators(Screen):

    def __init__(self, session):        
        self.session = session
        skin = skin_path + 'all.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('Picons')
        Screen.__init__(self, session)
        self.setTitle(_('Sat-Lodge Panel V. %s' % currversion)) 
        self.list = []
        self['text'] = oneListsl([])
        self.addon = 'emu'
        self.icount = 0
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))   
        self['info'] = Label(_('Getting the list, please wait ...'))			
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))  
        self.downloading = False
        self.timer = eTimer() 
        self.timer.start(100, 1)        
        try: 
            self.timer_conn = self.timer.timeout.connect(self.downloadxmlpage)
        except:
            self.timer.callback.append(self.downloadxmlpage) 
        self['title'] = Label(_('..:: PLUGIN EMULATORS CAMS ::..'))
        self['version'] = Label(_('V. %s' %  currversion))
        self['maintener'] = Label(_(' by ))^^((')) 
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close, 
         'cancel': self.close}, -2)


    def downloadxmlpage(self):
        url = xml_path + 'PluginEmulators.xml'
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)
	
    def errorLoad(self, error):
        print str(error)	
        self['info'].setText(_('Try again later ...'))
        self.downloading = False

    def _gotPageLoad(self, data):
        print "In PluginEmulators data =", data
        self.xml = data
        try:
            print "In PluginEmulators self.xml =", self.xml
            regex = '<plugins cont="(.*?)"'
            match = re.compile(regex,re.DOTALL).findall(self.xml)
            print "In PluginEmulators match =", match
            for name in match:
                   self.list.append(name)
                   self['info'].setText(_('Please select ...'))					   
            showlist(self.list, self['text'])							
            self.downloading = True
        except:
            self.downloading = False

    def okRun(self):
        if self.downloading == True:
            try:
                selection = str(self['text'].getCurrent())
                idx = self["text"].getSelectionIndex()
                name = self.list[idx]
                self.session.open(InstallGo, self.xml, name)
            except:
                return
        else:
            self.close
                        
class PluginMultim(Screen):

    def __init__(self, session):        
        self.session = session
        skin = skin_path + 'all.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('PluginMultim')
        Screen.__init__(self, session)
        self.setTitle(_('Sat-Lodge Panel V. %s' % currversion)) 
        self.list = []
        self['text'] = oneListsl([]) 
        self.addon = 'emu'
        self.icount = 0
        self['info'] = Label(_('Getting the list, please wait ...'))		
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back')) 
        self.downloading = False
        self.timer = eTimer() 
        self.timer.start(100, 1)        
        try: 
            self.timer_conn = self.timer.timeout.connect(self.downloadxmlpage)
        except:
            self.timer.callback.append(self.downloadxmlpage) 
        self['title'] = Label(_('..:: PLUGIN MULTIMEDIA ::..'))
        self['version'] = Label(_('V. %s' %  currversion))
        self['maintener'] = Label(_(' by ))^^(('))        
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,   
         'cancel': self.close}, -2)

    def downloadxmlpage(self):
        url = xml_path + 'PluginIptv.xml'
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)

    def errorLoad(self, error):
        print str(error)	
        self['info'].setText(_('Try again later ...'))
        self.downloading = False

    def _gotPageLoad(self, data):
        print "In PluginIptv data =", data
        self.xml = data
        try:
            print "In PluginIptv self.xml =", self.xml
            regex = '<plugins cont="(.*?)"'
            match = re.compile(regex,re.DOTALL).findall(self.xml)
            print "In PluginIptv match =", match
            for name in match:
                   self.list.append(name)
                   self['info'].setText(_('Please select ...'))					   
            showlist(self.list, self['text'])							
            self.downloading = True
        except:
            self.downloading = False

    def okRun(self):
        if self.downloading == True:
            try:
                selection = str(self['text'].getCurrent())
                idx = self["text"].getSelectionIndex()
                name = self.list[idx]
                self.session.open(InstallGo, self.xml, name)
            except:
                return
        else:
            self.close



##############################
class DailySetting(Screen):

    def __init__(self, session):        
        self.session = session
        # skin = skin_path + 'DailySetting.xml'
        skin = skin_path + 'all.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('DailySetting')
        Screen.__init__(self, session)
        self.setTitle(_('Sat-Lodge Panel V. %s' % currversion)) 
        self['text'] = SLList([])
        self.working = False
        self.selection = 'all'
        self['info'] = Label('') 
        self['info'].setText(_('Please select ...'))
        self['title'] = Label(_('..:: DAILY SETTINGS ::..'))
        self['version'] = Label(_('V. %s' %  currversion))
        self['maintener'] = Label(_(' by ))^^((')) 
        self['key_green'] = Button(_('Select'))         
        self['key_red'] = Button(_('Back')) 
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
        for x in Panel_list2:
            list.append(DailyListEntry(x, idx))
            self.menu_list.append(x)
            idx += 1
        self['text'].setList(list)

    def okRun(self):
        self.keyNumberGlobalCB(self['text'].getSelectedIndex())
  
    def keyNumberGlobalCB(self, idx):
        sel = self.menu_list[idx]
        if sel == _('UPDATE SATELLITES.XML'):
            self.UpdSatellites()             
        elif sel == _('UPDATE TERRESTRIAL.XML'):
            self.UpdTerrestrial()           
        elif sel == _('SETTINGS CIEFP'):
            self.session.open(slSettingCiefp)             
        elif sel == _('SETTINGS MALIMALI'):
            self.session.open(slSettingMalimali)            
        elif sel == _('SETTINGS MANUTEK'):
            self.session.open(PluginslSettingManutek)             
        elif sel == _('SETTINGS MILENKA61'):
            self.session.open(PluginslMilenka61)             
        elif sel == _('SETTINGS MORPHEUS'):
            self.session.open(PluginslSettingMorpheus) 
        elif sel == _('SETTINGS PREDRAG'):
            self.session.open(slSettingPredrag)             
        elif sel == _('SETTINGS VHANNIBAL'):
            self.session.open(PluginslSettingVhan)             
            

# url_sat_oealliance  = 'http://raw.githubusercontent.com/oe-alliance/oe-alliance-tuxbox-common/master/src/satellites.xml'
# url_sat_openpli   = 'http://raw.githubusercontent.com/OpenPLi/tuxbox-xml/master/xml/satellites.xml' 
 
    def UpdSatellites(self):
        self.session.openWithCallback(self.okSatellites,slMessageBox,(_("Do you want to install?")), slMessageBox.TYPE_YESNO)             
            
    def okSatellites(self, result):
        if result:
            if checkInternet():
                try:            
                    url_sat_openpli  = 'http://raw.githubusercontent.com/OpenPLi/tuxbox-xml/master/xml/satellites.xml' 
                    dirCopy = '/etc/tuxbox/satellites.xml' #'/etc/enigma2/satellites.xml'
                    urllib.urlretrieve(url_sat_openpli, dirCopy, context=ssl._create_unverified_context())
                    self.mbox = self.session.open(slMessageBox, _('Satellites.xml Updated!'), slMessageBox.TYPE_INFO, timeout=5)
                    self['info'].setText(_('Installation performed successfully!'))   
        
                except:
                    return
            else:
                session.open(slMessageBox, "No Internet", slMessageBox.TYPE_INFO)             
            
            
    def UpdTerrestrial(self):
        self.session.openWithCallback(self.okTerrInstall,slMessageBox,(_("Do you want to install?")), slMessageBox.TYPE_YESNO)             
            
    def okTerrInstall(self, result):
        if result:
            if checkInternet():
                try:            
                    url_sat_openpli  = 'http://raw.githubusercontent.com/OpenPLi/tuxbox-xml/master/xml/terrestrial.xml'
                    dirCopy       = '/etc/tuxbox/terrestrial.xml' #'/etc/enigma2/terrestrial.xml'
                    urllib.urlretrieve(url_sat_openpli, dirCopy, context=ssl._create_unverified_context())
                    self.mbox = self.session.open(slMessageBox, _('Terrestrial.xml Updated!'), slMessageBox.TYPE_INFO, timeout=5)
                    self['info'].setText(_('Installation performed successfully!'))   
        
                except:
                    return
            else:
                session.open(slMessageBox, "No Internet", slMessageBox.TYPE_INFO, timeout=5)         
                
                
class PluginslSettingVhan(Screen):

    def __init__(self, session):  
        self.session = session
        skin = skin_path + 'all.xml'        
        # skin = skin_path + 'Setting.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('PluginslSettingVhan')
        Screen.__init__(self, session)
        self.setTitle(_('Sat-Lodge Panel V. %s' % currversion))  
        self.list = []		
        self['text'] = oneListsl([]) 		
        self.addon = 'emu'
        self.icount = 0
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))   
        self.downloading = False
        self.timer = eTimer() 
        self.timer.start(100, 1)        
        try: 
            self.timer_conn = self.timer.timeout.connect(self.downloadxmlpage)
        except:
            self.timer.callback.append(self.downloadxmlpage) 		
        self['title'] = Label(_('..:: SETTING Vhannibal ::..'))
        self['version'] = Label(_('V. %s' %  currversion))
        self['maintener'] = Label(_(' by ))^^(('))           
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,
         'cancel': self.close}, -2)


    def downloadxmlpage(self):
        url = base64.b64decode("aHR0cDovL3NhdC5hbGZhLXRlY2gubmV0L3VwbG9hZC9zZXR0aW5ncy92aGFubmliYWwv")
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)			
        
    def errorLoad(self, error):
        print str(error)	
        self['info'].setText(_('Try again later ...'))
        self.downloading = False

    def _gotPageLoad(self, data):
#        print "In Setting data =", data
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
                    # name = name.replace("Vhannibal", "")  
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
        self.session.openWithCallback(self.okInstall,slMessageBox,(_("Do you want to install?")), slMessageBox.TYPE_YESNO)             
            
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
            title = _("Install the Settings")          
            self.session.open(slConsole,_(title),cmd)              
            #self.onShown.append(self.reloadSettings)

    def reloadSettings(self):
        ReloadBouquet()
        self.mbox = self.session.open(slMessageBox, _('Setting Installed!'), slMessageBox.TYPE_INFO, timeout=5)
        self['info'].setText(_('Installation performed successfully!')) 

        
class PluginslMilenka61(Screen):

    def __init__(self, session):        
        self.session = session
        skin = skin_path + 'all.xml'        
        # skin = skin_path + 'Setting.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('PluginslMilenka61')
        Screen.__init__(self, session)
        self.setTitle(_('Sat-Lodge Panel V. %s' % currversion)) 
        self.list = []		
        self['text'] = oneListsl([]) 		
        self.addon = 'emu'
        self.icount = 0
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back')) 
        self.downloading = False
        self.timer = eTimer() 
        self.timer.start(100, 1)        
        try: 
            self.timer_conn = self.timer.timeout.connect(self.downloadxmlpage)
        except:
            self.timer.callback.append(self.downloadxmlpage) 	
        self['title'] = Label(_('..:: SETTING Milenka61 ::..'))
        self['version'] = Label(_('V. %s' %  currversion))
        self['maintener'] = Label(_(' by ))^^(('))           
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,  
         'cancel': self.close}, -2)

    def downloadxmlpage(self):
        url = base64.b64decode("aHR0cDovL3ZlbnVzY3MubmV0L3NhdHZlbnVzRTIv")
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)			
        
    def errorLoad(self, error):
        print str(error)	
        self['info'].setText(_('Try again later ...'))
        self.downloading = False

    def _gotPageLoad(self, data):
#        print "In Setting data =", data
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
                    # name = name.replace("Vhannibal", "")  
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
        self.session.openWithCallback(self.okInstall,slMessageBox,(_("Do you want to install?")), slMessageBox.TYPE_YESNO)             
            
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
            title = _("Install the Settings")          
            self.session.open(slConsole,_(title),cmd) 

    def reloadSettings(self):
        ReloadBouquet()
        self.mbox = self.session.open(slMessageBox, _('Setting Installed!'), slMessageBox.TYPE_INFO, timeout=5)
        self['info'].setText(_('Installation performed successfully!')) 
        
class PluginslSettingManutek(Screen):

    def __init__(self, session):        
        self.session = session
        skin = skin_path + 'all.xml'        
        # skin = skin_path + 'Setting.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('PluginslSettingManutek')
        Screen.__init__(self, session)
        self.setTitle(_('Sat-Lodge Panel V. %s' % currversion)) 
        self.list = []		
        self['text'] = oneListsl([]) 		
        self.addon = 'emu'
        self.icount = 0
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))    
        self.downloading = False
        self.timer = eTimer() 
        self.timer.start(100, 1)        
        try: 
            self.timer_conn = self.timer.timeout.connect(self.downloadxmlpage)
        except:
            self.timer.callback.append(self.downloadxmlpage) 	
        self['title'] = Label(_('..:: SETTING Manutek ::..'))
        self['version'] = Label(_('V. %s' %  currversion))
        self['maintener'] = Label(_(' by ))^^(('))           
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,  
         'cancel': self.close}, -2)

    def downloadxmlpage(self):
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
        self.session.openWithCallback(self.okInstall,slMessageBox,(_("Do you want to install?")), slMessageBox.TYPE_YESNO)             
            
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
                self.session.open(slConsole,_(title),cmd) 
        
    def reloadSettings(self):
        ReloadBouquet()
        self.mbox = self.session.open(slMessageBox, _('Setting Installed!'), slMessageBox.TYPE_INFO, timeout=5)
        self['info'].setText(_('Installation performed successfully!'))                 
        
class PluginslSettingMorpheus(Screen):

    def __init__(self, session):        
        self.session = session
        skin = skin_path + 'all.xml'        
        # skin = skin_path + 'Setting.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('PluginslSettingMorpheus')
        Screen.__init__(self, session)
        self.setTitle(_('Sat-Lodge Panel V. %s' % currversion)) 
        self.list = []		
        self['text'] = oneListsl([]) 		
        self.addon = 'emu'
        self.icount = 0
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))
        self.downloading = False
        self.timer = eTimer() 
        self.timer.start(100, 1)        
        try: 
            self.timer_conn = self.timer.timeout.connect(self.downloadxmlpage)
        except:
            self.timer.callback.append(self.downloadxmlpage) 	
        self['title'] = Label(_('..:: SETTING Morpheus883 ::..'))
        self['version'] = Label(_('V. %s' %  currversion))
        self['maintener'] = Label(_(' by ))^^(('))           
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,   
         'cancel': self.close}, -2)
         
    def downloadxmlpage(self):
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
        self.session.openWithCallback(self.okInstall,slMessageBox,(_("Do you want to install?")), slMessageBox.TYPE_YESNO)             
            
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
                self.session.open(slConsole,_(title),cmd) 
            deletetmp()
            self.reloadSettings()              
        
    def reloadSettings(self):
        ReloadBouquet()
        self.mbox = self.session.open(slMessageBox, _('Setting Installed!'), slMessageBox.TYPE_INFO, timeout=5)
        self['info'].setText(_('Installation performed successfully!'))     

class slSettingCiefp(Screen):
    def __init__(self, session):        
        self.session = session
        skin = skin_path + 'all.xml'        
        # skin = skin_path + 'Setting.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('slSettingCiefp')
        Screen.__init__(self, session)
        self.setTitle(_('Sat-Lodge Panel V. %s' % currversion)) 
        self.list = []		
        self['text'] = oneListsl([]) 		
        self.addon = 'emu'
        self.icount = 0
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))         
        self.downloading = False
        self.timer = eTimer() 
        self.timer.start(100, 1)        
        try: 
            self.timer_conn = self.timer.timeout.connect(self.downloadxmlpage)
        except:
            self.timer.callback.append(self.downloadxmlpage) 	
        self['title'] = Label(_('..:: SETTING Ciefp ::..'))
        self['version'] = Label(_('V. %s' %  currversion))
        self['maintener'] = Label(_(' by ))^^(('))           
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,        
         'cancel': self.close}, -2)
         
    def downloadxmlpage(self):
        url = base64.b64decode("aHR0cDovLzE3OC42My4xNTYuNzUvcGFuZWxhZGRvbnMvQ2llZnAv")
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)			

        
    def errorLoad(self, error):
        print str(error)	
        self['info'].setText(_('Try again later ...'))
        self.downloading = False

    def _gotPageLoad(self, data):
#        print "In Setting data =", data
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
                    # name = name.replace(".zip", "")
                    name = name.replace(".tar.gz", "")                    
                    name = name.replace("%20", " ")
                    #Settings_Morph883_0.8W-4.8E-13E.tar.gz
                    # name = name.replace("_Morph883_", "Morpheus883 ")                     
                    # name = name.replace("Settings", "")                     
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
        self.session.openWithCallback(self.okInstall,slMessageBox,(_("Do you want to install?")), slMessageBox.TYPE_YESNO)             
            
    def okInstall(self, result):
        if result:
            if self.downloading == True:
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
            title = _("Install the Settings")          
            self.session.open(slConsole,_(title),cmd)              
        
    def reloadSettings(self):
        ReloadBouquet()
        self.mbox = self.session.open(slMessageBox, _('Setting Installed!'), slMessageBox.TYPE_INFO, timeout=5)
        self['info'].setText(_('Installation performed successfully!')) 
        
class slSettingMalimali(Screen):
    
    def __init__(self, session):        
        self.session = session
        skin = skin_path + 'all.xml'        
        # skin = skin_path + 'Setting.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('slSettingMalimali')
        Screen.__init__(self, session)
        self.setTitle(_('Sat-Lodge Panel V. %s' % currversion)) 
        self.list = []		
        self['text'] = oneListsl([]) 		
        self.addon = 'emu'
        self.icount = 0
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back')) 
        self.downloading = False
        self.timer = eTimer() 
        self.timer.start(100, 1)        
        try: 
            self.timer_conn = self.timer.timeout.connect(self.downloadxmlpage)
        except:
            self.timer.callback.append(self.downloadxmlpage) 	
        self['title'] = Label(_('..:: SETTING Malimali ::..'))
        self['version'] = Label(_('V. %s' %  currversion))
        self['maintener'] = Label(_(' by ))^^(('))           
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,  
         'cancel': self.close}, -2)
         
    def downloadxmlpage(self):
        url = base64.b64decode("aHR0cDovLzE3OC42My4xNTYuNzUvcGFuZWxhZGRvbnMvTWFsaW1hbGkv")
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)			

        
    def errorLoad(self, error):
        print str(error)	
        self['info'].setText(_('Try again later ...'))
        self.downloading = False

    def _gotPageLoad(self, data):
#        print "In Setting data =", data
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
        self.session.openWithCallback(self.okInstall,slMessageBox,(_("Do you want to install?")), slMessageBox.TYPE_YESNO)             
            
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
            title = _("Install the Settings")          
            self.session.open(slConsole,_(title),cmd)              
        
    def reloadSettings(self):
        ReloadBouquet()
        self.mbox = self.session.open(slMessageBox, _('Setting Installed!'), slMessageBox.TYPE_INFO, timeout=5)
        self['info'].setText(_('Installation performed successfully!'))         

class slSettingPredrag(Screen):

    def __init__(self, session):        
        self.session = session
        skin = skin_path + 'all.xml'        
        # skin = skin_path + 'Setting.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('slSettingPredrag')
        Screen.__init__(self, session)
        self.setTitle(_('Sat-Lodge Panel V. %s' % currversion)) 
        self.list = []		
        self['text'] = oneListsl([]) 		
        self.addon = 'emu'
        self.icount = 0
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))   
        self.downloading = False
        self.timer = eTimer() 
        self.timer.start(100, 1)        
        try: 
            self.timer_conn = self.timer.timeout.connect(self.downloadxmlpage)
        except:
            self.timer.callback.append(self.downloadxmlpage) 	
        self['title'] = Label(_('..:: SETTING Predrag ::..'))
        self['version'] = Label(_('V. %s' %  currversion))
        self['maintener'] = Label(_(' by ))^^(('))           
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okRun,
         'green': self.okRun,
         'red': self.close,    
         'cancel': self.close}, -2)
         
    def downloadxmlpage(self):
        url = base64.b64decode("aHR0cDovLzE3OC42My4xNTYuNzUvcGFuZWxhZGRvbnMvUHJlZHJAZy8=")
        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)			

        
    def errorLoad(self, error):
        print str(error)	
        self['info'].setText(_('Try again later ...'))
        self.downloading = False

    def _gotPageLoad(self, data):
#        print "In Setting data =", data
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
        self.session.openWithCallback(self.okInstall,slMessageBox,(_("Do you want to install?")), slMessageBox.TYPE_YESNO)             
            
    def okInstall(self, result):
        if result:
            if self.downloading == True:
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
            title = _("Install the Settings")          
            self.session.open(slConsole,_(title),cmd)              
        
    def reloadSettings(self):
        ReloadBouquet()
        self.mbox = self.session.open(slMessageBox, _('Setting Installed!'), slMessageBox.TYPE_INFO, timeout=5)
        self['info'].setText(_('Installation performed successfully!'))         


        
class InstallGo(Screen):

    def __init__(self, session, data, name, selection = None):     
        self.session = session
        
        skin = skin_path + 'InstallGo.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('InstallGo')
        
        Screen.__init__(self, session)
        self.setTitle(_('Sat-Lodge Panel V. %s' % currversion)) 
        print "In slInstallGo data =", data
        print "In slInstallGo name =", name
        self.selection = selection
        self['info'] = Label()   
        self['progress'] = Progress()
        self['progresstext'] = StaticText()
        list = []
        list.sort()				
        n1 = data.find(name, 0)
        n2 = data.find("</plugins>", n1)
        data1 = data[n1:n2]
        print "In slInstallGo data1 =", data1
        self.names = []
        self.urls = []
        regex = '<plugin name="(.*?)".*?url>"(.*?)"'
        match = re.compile(regex,re.DOTALL).findall(data1)
        print "In slInstallGo match =", match
        for name, url in match:
                self.names.append(name)
                self.urls.append(url)				
        print "In slInstallGo self.names =", self.names
        self['text'] = oneListsl([])
        self['info'].setText(_('Please install ...'))	
        self['key_green'] = Button(_('Install'))
        self['key_red'] = Button(_('Back'))  
        self['title'] = Label(_('..:: Please Select to Install::..'))
        self['version'] = Label(_('V. %s' %  currversion))
        self['maintener'] = Label(_(' by ))^^((')) 
        self['actions'] = ActionMap(['SetupActions'], {'ok': self.message,
         'green': self.message,
         'red': self.close,
         'cancel': self.close}, -2)
        self.onLayoutFinish.append(self.start)
        
    def start(self):	
        showlist(self.names, self['text'])

    def message(self):
        self.session.openWithCallback(self.selclicked,slMessageBox,(_("Do you want to install?")), slMessageBox.TYPE_YESNO, timeout = 15, default = False) 

    def selclicked(self, result):
        idx = self["text"].getSelectionIndex()
        if idx is None :
            self.close()
                
        if result:
            idx = self["text"].getSelectionIndex()
            dom = self.names[idx]
            com = self.urls[idx]
            self.prombt(com, dom)      

#11.05.19            
    def downloadProgress(self, recvbytes, totalbytes):
        self['progress'].value = int(100 * recvbytes / float(totalbytes))
        self['progresstext'].text = '%d of %d kBytes (%.2f%%)' % (recvbytes / 1024, totalbytes / 1024, 100 * recvbytes / float(totalbytes)) 
                
    def install(self, fplug):
        checkfile = '/tmp/ipkdownloaded.ipk'

        if os.path.exists(checkfile):
            # self.session.open(slConsole, _('Installing: %s') % self.dom, ['opkg install -force-overwrite -force-depends %s' % self.com])
            self.session.open(slConsole, _('Installing: %s') % self.dom, ['opkg install %s' % self.com])			
            # self.timer = eTimer()
            # self.timer.start(100, True)			
            # if fileExists(BRAND)or fileExists(BRANDP):
                # self.timer.callback.append(deletetmp) #pli
            # else:
                # self.timer_conn = self.timer.timeout.connect(deletetmp) #cvs    
            self.timer = eTimer() 
            self.timer.start(100, 1)        
            try: 
                self.timer_conn = self.timer.timeout.connect(deletetmp)
            except:
                self.timer.callback.append(deletetmp) 	
				
            self['info'].setText(_('Installation performed successfully!'))      
        self['info'].setText(_('Please select ...')) 
        self['progresstext'].text = ''  
        self.progclear = 0
        self['progress'].setValue(self.progclear)
        return
            
    def showError(self, error):
        print "download error =", error
        self.close()
##########            
            
    def prombt(self, com, dom):
        self.com = com
        self.dom = dom
        #self.command = ''
        print 'self.com', self.com
        self['info'].setText(_('Installing ') + self.dom + _('... please wait'))
        # if self.com.endswith('.ipk'):
            # self['info'].setText(_('Installing ') + self.dom + _('... please wait'))
            # self.session.open(slConsole, _('Installing: %s') % self.dom, ['opkg install -force-overwrite -force-depends %s' % self.com])
            
        if self.com.endswith('.ipk'):
            self['info'].setText(_('Installing ') + self.dom + _('... please wait'))
            url = self.com
            dest = '/tmp/ipkdownloaded.ipk'
            self.download = downloadWithProgress(url, dest)
            self.download.addProgress(self.downloadProgress)
            self.download.start().addCallback(self.install).addErrback(self.showError)  
			
        elif self.com.endswith('.tar.gz'):
            self['info'].setText(_('Installing ') + self.dom + _('... please wait'))
            self.timer = eTimer() 
            self.timer.start(100, 1)        
            try: 
                self.timer_conn = self.timer.timeout.connect(deletetmp)
            except:
                self.timer.callback.append(deletetmp) 				
            os.system('wget %s -O /tmp/download.tar.gz > /dev/null' % self.com )
            self.session.open(slConsole, _('Installing: %s') % self.dom, ['tar -xzvf ' + '/tmp/download.tar.gz' + ' -C /'])
            self.mbox = self.session.open(slMessageBox, _('Installation successful!'), slMessageBox.TYPE_INFO, timeout=5)
            self['info'].setText(_('Installation successful!'))
        elif self.com.endswith('.tar.bz2'):
            self['info'].setText(_('Installing ') + self.dom + _('... please wait'))
            self.timer = eTimer() 
            self.timer.start(100, 1)        
            try: 
                self.timer_conn = self.timer.timeout.connect(deletetmp)
            except:
                self.timer.callback.append(deletetmp) 				
            os.system('wget %s -O /tmp/download.tar.bz2 > /dev/null' % self.com )
            self.session.open(slConsole, _('Installing: %s') % self.dom, ['tar -xyvf ' + '/tmp/download.tar.bz2' + ' -C /'])
            self.mbox = self.session.open(slMessageBox, _('Installation successful!'), slMessageBox.TYPE_INFO, timeout=5)
            self['info'].setText(_('Installation successful!'))
        elif self.com.endswith('.tbz2'):
            self['info'].setText(_('Installing ') + self.dom + _('... please wait'))
            self.timer = eTimer() 
            self.timer.start(100, 1)        
            try: 
                self.timer_conn = self.timer.timeout.connect(deletetmp)
            except:
                self.timer.callback.append(deletetmp) 				
				
            os.system('wget %s -O /tmp/download.tbz2 > /dev/null' % self.com )
            self.session.open(slConsole, _('Installing: %s') % self.dom, ['tar -xyvf ' + '/tmp/download.tbz2' + ' -C /'])
            self.mbox = self.session.open(slMessageBox, _('Installation successful!'), slMessageBox.TYPE_INFO, timeout=5)
            self['info'].setText(_('Installation successful!'))
        elif self.com.endswith('.tbz'):
            self['info'].setText(_('Installing ') + self.dom + _('... please wait'))
            self.timer = eTimer() 
            self.timer.start(100, 1)        
            try: 
                self.timer_conn = self.timer.timeout.connect(deletetmp)
            except:
                self.timer.callback.append(deletetmp) 				
            os.system('wget %s -O /tmp/download.tbz > /dev/null' % self.com )
            self.session.open(slConsole, _('Installing: %s') % self.dom, ['tar -xyvf ' + '/tmp/download.tbz' + ' -C /'])
            self.mbox = self.session.open(slMessageBox, _('Installation successful!'), slMessageBox.TYPE_INFO, timeout=5)
            self['info'].setText(_('Installation successful!'))
        elif self.com.endswith('.deb'):
            if fileExists(BRAND)or fileExists(BRANDP):
                self.mbox = self.session.open(slMessageBox, _('Unknow Image!'), slMessageBox.TYPE_INFO, timeout=5)
                self['info'].setText(_('Installation aborted!'))
            else:
                self['info'].setText(_('Installing ') + self.dom + _('... please wait'))
                self.timer = eTimer() 
                self.timer.start(100, 1)        
                try: 
                    self.timer_conn = self.timer.timeout.connect(deletetmp)
                except:
                    self.timer.callback.append(deletetmp) 
				
                os.system('wget %s -O /tmp/download.deb > /dev/null' % self.com )
                self.session.open(slConsole, _('Installing: %s') % self.dom, ['dpkg -i ' + '/tmp/download.deb'])
                self.mbox = self.session.open(slMessageBox, _('Installation successful!'), slMessageBox.TYPE_INFO, timeout=5)
                self['info'].setText(_('Installation successful!'))
        elif self.com.endswith('.zip'):
            if 'setting' in self.dom.lower():
                self['info'].setText(_('Installing ') + self.dom + _('... please wait'))
                self.timer = eTimer() 
                self.timer.start(100, 1)        
                try: 
                    self.timer_conn = self.timer.timeout.connect(deletetmp)
                except:
                    self.timer.callback.append(deletetmp) 				
                os.system('wget %s -O /tmp/download.zip > /dev/null' % self.com )
                #controllo esistenza file 
                checkfile = '/tmp/download.zip'
                if os.path.exists(checkfile):
                    os.system('unzip -o /tmp/download.zip -d /tmp/')
                    os.system('rm -rf /etc/enigma2/lamedb')
                    os.system('rm -rf /etc/enigma2/*.radio')
                    os.system('rm -rf /etc/enigma2/*.tv')
                    linkzipname = 'aHR0cDovL215dXBkYXRlci5keW5kbnMtaXAuY29tLw=='
                    data_zip = base64.b64decode(linkzipname)
                    self.zipname1 = str(self.com.replace(data_zip,'').replace('.zip', ''))
                    os.system('cp -rf /tmp/%s/*.tv  /etc/enigma2/' % self.zipname1 )
                    os.system('cp -rf /tmp/%s/*.radio  /etc/enigma2/' % self.zipname1)
                    os.system('cp -rf /tmp/%s/lamedb  /etc/enigma2/' % self.zipname1)
                    os.system('cp -rf /tmp/%s/blacklist /etc/enigma2/' % self.zipname1)
                    os.system('cp -rf /tmp/%s/whitelist /etc/enigma2/' % self.zipname1)
                    os.system('cp -rf /tmp/%s/satellites.xml /etc/tuxbox/' % self.zipname1 )
                    os.system('cp -rf /tmp/%s/terrestrial.xml /etc/tuxbox/' % self.zipname1 )
                    os.system('rm -rf /tmp/download.zip')
                    os.system('rm -rf /tmp/%s' % self.zipname1)
                    self.reloadSettings2()
                else:
                    self.mbox = self.session.open(slMessageBox, _('Download Failed!'), slMessageBox.TYPE_INFO, timeout=5)
            
            if 'plugin.' or 'repository.' or 'script.' in self.dom.lower():
                checkfile = '/usr/lib/enigma2/python/Plugins/Extensions/KodiLite'
                # if os.path.exists(checkfile):
                if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/KodiLite/plugin.pyo"):
                    self['info'].setText(_('Installing ') + self.dom + _('... please wait'))
                    self.timer = eTimer() 
                    self.timer.start(100, 1)        
                    try: 
                        self.timer_conn = self.timer.timeout.connect(deletetmp)
                    except:
                        self.timer.callback.append(deletetmp) 
					
                    downplug = self.dom.replace(' ', '') + '.zip' 
                    os.system('wget %s -O /tmp/%s > /dev/null' % (self.com,downplug) ) 
                    checkfiledwn = '/tmp/%s' % downplug
                    checkfile = '/usr/lib/enigma2/python/Plugins/Extensions/KodiLite'         
                    if os.path.exists(checkfiledwn): 
                        if downplug.startswith('plugin.') :
                            foldername = 'plugins'
                        if downplug.startswith('repository'):
                            foldername = 'repos'
                        if downplug.startswith('script'):
                            foldername = 'scripts'
                        os.system('unzip -o %s -d %s/%s/' %(checkfiledwn, checkfile, foldername))  
                        #os.system('unzip -o /tmp/%s -d %s/%s/' %(downplug, checkfile, foldername))                          
                        self.mbox = self.session.open(slMessageBox, _('Addon KodiLite installed!'), slMessageBox.TYPE_INFO, timeout=5)
                        self['info'].setText(_('Addon KodiLite installed!'))
                else:
                        self.mbox = self.session.open(slMessageBox, _('KodiLite not installed!'), slMessageBox.TYPE_INFO, timeout=5)
                        #pass
            else:
                self['info'].setText(_('Downloading file select in /tmp') + self.dom + _('... please wait'))
                downplug = self.dom.replace(' ', '') + '.zip' 
                os.system('wget %s -O /tmp/%s > /dev/null' % (self.com,downplug) )                
                self.mbox = self.session.open(slMessageBox, _('Download file in /tmp successful!'), slMessageBox.TYPE_INFO, timeout=5)
                self['info'].setText(_('Download file in /tmp successful!!'))
        else:
            self['info'].setText(_('Download failed!') + self.dom + _('... Not supported'))
            return

    def deletetmp(self):
        os.system('rm -f /tmp/*.ipk;rm -f /tmp/*.tar;rm -f /tmp/*.zip;rm -f /tmp/*.tar.gz;rm -f /tmp/*.tar.bz2;rm -f /tmp/*.tar.tbz2;rm -f /tmp/*.tar.tbz')

    def reloadSettings2(self):
            ReloadBouquet()
            self.mbox = self.session.open(slMessageBox, _('Setting Installed!'), slMessageBox.TYPE_INFO, timeout=5)
            self['info'].setText(_('Installation successful!'))  
            
class slConsole(Screen):
        
    def __init__(self, session, title = None, cmdlist = None, finishedCallback = None, closeOnSuccess = False):
        self.session = session
        skin = skin_path + 'slConsole.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('slConsole')
        Screen.__init__(self, session)
        self.setTitle(_('Sat-Lodge Panel V. %s' % currversion)) 
        self['version'] = Label(_('V. %s' %  currversion))
        self['maintener'] = Label(_(' by ))^^(('))         
        self.finishedCallback = finishedCallback
        self.closeOnSuccess = closeOnSuccess
        self['text'] = ScrollLabel('')
        self['actions'] = ActionMap(['WizardActions', 'DirectionActions'], {'ok': self.cancel,
         'back': self.cancel,
         'up': self['text'].pageUp,
         'down': self['text'].pageDown}, -1)
        self.cmdlist = cmdlist
        self.container = eConsoleAppContainer()
        self.run = 0
        self.container.appClosed.append(self.runFinished)
        self.container.dataAvail.append(self.dataAvail)
        self.onLayoutFinish.append(self.startRun)

    def updateTitle(self):
        self.setTitle(self.newtitle)

    def startRun(self):
        self['text'].setText(_('Execution Progress:') + '\n\n')
        print 'Console: executing in run', self.run, ' the command:', self.cmdlist[self.run]
        if self.container.execute(self.cmdlist[self.run]):
            self.runFinished(-1)

    def runFinished(self, retval):
        self.run += 1
        if self.run != len(self.cmdlist):
            if self.container.execute(self.cmdlist[self.run]):
                self.runFinished(-1)
        else:
            str = self['text'].getText()
            str += _('Execution finished!!')
            self['text'].setText(str)
            self['text'].lastPage()
            if self.finishedCallback is not None:
                self.finishedCallback()
            if not retval and self.closeOnSuccess:
                self.cancel()
        return

    def cancel(self):
        if self.run == len(self.cmdlist):
            self.close()
            self.container.appClosed.remove(self.runFinished)
            self.container.dataAvail.remove(self.dataAvail)

    def dataAvail(self, str):
        self['text'].setText(self['text'].getText() + str)

class IPKinst(Screen):

    def __init__(self, session):
    
        self.session = session
        skin = skin_path + 'IPKinst.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('IPKinst')
        Screen.__init__(self, session)
        self.setTitle(_('Sat-Lodge Panel V. %s' % currversion))     

        self.flist = []
        idx = 0
        ipkpth = config.plugins.slPanel.ipkpth.value
        ##ipkpth = ("/tmp")
        pkgs = listdir(ipkpth)
        for fil in pkgs:
            if fil.find('.ipk') != -1 or fil.find('.tar.gz') != -1 or fil.find('.deb') != -1: 
        #    if fil.find('.ipk') != -1:
                res = (fil, idx)
                self.flist.append(res)
                idx = idx + 1
        self['ipkglisttmp'] = List(self.flist)
        self['title'] = Label(_('..:: INSTALL EXTENSIONS ::..'))
        self['version'] = Label(_('V. %s' %  currversion))
        # self['info1'] = Label(_('Put addon .ipk .tar.gz .deb and install\nSet path from config')) 
        self['info1'] = Label(_('Put addon .ipk .tar.gz .deb and install from config path') + ' ' + str(ipkpth) ) 

        self['info'] = Label('')
        self['maintener'] = Label(_(' by ))^^(('))   
        self['key_green'] = Button(_('Install'))
        self['key_yellow'] = Button(_('Restart'))
        self['key_blue'] = Button(_('Remove'))
        self['key_red'] = Button(_('Back'))  
        self['actions'] = ActionMap(['OkCancelActions', 'WizardActions', 'ColorActions', "MenuActions"], {'ok': self.ipkinst,
         'green': self.ipkinst,
         'yellow': self.msgipkinst,
         'blue': self.msgipkrmv,
         'red': self.close,
         'menu': self.goConfig,
         'cancel': self.close}, -1)
        self.getfreespace()

    def getfreespace(self):
        fspace = freespace()
        self.freespace = fspace
        self['info'].setText(self.freespace)

    def freespace():
        try:
            diskSpace = os.statvfs('/')
            capacity = float(diskSpace.f_bsize * diskSpace.f_blocks)
            available = float(diskSpace.f_bsize * diskSpace.f_bavail)
            fspace = round(float(available / 1048576.0), 2)
            tspace = round(float(capacity / 1048576.0), 1)
            spacestr = 'Free space(' + str(fspace) + ' MB) Total space(' + str(tspace) + ' MB)'
            return spacestr
        except:
            return ''

    def goConfig(self):
        self.session.open(slPanelConfig)
        
    def ipkinst(self):
        self.sel = self['ipkglisttmp'].getCurrent()
        if self.sel:
            self.sel = self.sel[0]
            self.session.openWithCallback(self.ipkinst2, slMessageBox, (_('Do you really want to install the selected Addon?')+ '\n' + self.sel), slMessageBox.TYPE_YESNO, timeout = 15, default = False)

    def ipkinst2(self, answer):
        if answer is True:
            ipkpth = config.plugins.slPanel.ipkpth.value
            dest = ipkpth + '/' + self.sel
            if self.sel.find('.ipk') != -1:
                self.sel = self.sel[0]
                cmd0 = 'opkg install --force-overwrite ' + dest
                self.session.open(slConsole, title='IPK Local Installation', cmdlist=[cmd0, 'sleep 5'], finishedCallback=self.msgipkinst)              

            if self.sel.find('.tar.gz') != -1:
                self.sel = self.sel[0]
                cmd0 = 'tar -xzvf ' + dest + ' -C /'
                self.session.open(slConsole, title='TAR GZ Local Installation', cmdlist=[cmd0, 'sleep 5'], finishedCallback=self.msgipkinst)   
                
            if self.sel.find('.deb') != -1:
                if fileExists(BRAND)or fileExists(BRANDP):
                     self.mbox = self.session.open(slMessageBox, _('Unknow Image!'), slMessageBox.TYPE_INFO, timeout=5)
                else:
                    self.sel = self.sel[0]
                    cmd0 = 'dpkg -i ' + dest
                    self.session.open(slConsole, title='DEB Local Installation', cmdlist=[cmd0, 'sleep 5'], finishedCallback=self.msgipkinst)                  
            
    def msgipkrmv(self):
        self.sel = self['ipkglisttmp'].getCurrent()
        if self.sel:
            self.sel = self.sel[0]
            self.session.openWithCallback(self.msgipkrmv2, slMessageBox, (_('Do you really want to remove selected?')+ '\n' + self.sel), slMessageBox.TYPE_YESNO, timeout = 15, default = False)

    def msgipkrmv2(self, answer):
        if answer is True:
            ipkpth = config.plugins.slPanel.ipkpth.value
            #ipkpth = ("/tmp")
            dest = ipkpth + '/' + self.sel
            cmd0 = 'rm -rf ' + dest
            #self.session.open(slConsole, title='IPK Local Installation', cmdlist=[cmd0, cmd1, 'sleep 5'], finishedCallback=self.close)
            self.session.open(slConsole, title='Local Remove', cmdlist=[cmd0, 'sleep 3'], finishedCallback=self.close)             

    def msgipkinst(self):
        self.session.openWithCallback(self.ipkrestart, slMessageBox, (_('Do you want restart enigma2 to reload installed addons ?')), slMessageBox.TYPE_YESNO, timeout = 15, default = False)

    def ipkrestart(self, result):
        if result:
            # ipkpth = config.plugins.slPanel.ipkpth.value
            # cmd2 = 'rm -f ' + ipkpth + '/*.ipk'
            # os.system(cmd2)
            self.session.open(TryQuitMainloop, 3)
        else:
            self.close() 

            
class pluginSl(Screen):

    def __init__(self, session):
        self.session = session
        skin = skin_path + 'pluginSl.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('pluginSl')
        Screen.__init__(self, session)
        self.setTitle(_('Sat-Lodge Panel V. %s' % currversion)) 
        self.list = []
        self['list'] = oneListsl([])  
        self['title'] = Label(_('..:: SAT-LODGE UNINSTALLER ::..'))
        self['version'] = Label(_('V. %s' %  currversion))
        self['maintener'] = Label(_(' by ))^^(('))        
        self['key_green'] = Button(_('Uninstall'))
        self['key_yellow'] = Button(_('Restart'))
        self['key_red'] = Button(_('Back'))    
        self['info'] = Label()
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'green': self.message1,
         'ok': self.message1,
         'yellow': self.msgipkrst,
         'red': self.close,
         'cancel': self.close}, -1)
        self.getfreespace()
        ###########
        self.onLayoutFinish.append(self.openList)

    def openList(self):
        self.names = []
        path = ('/var/lib/opkg/info')
        for root, dirs, files in os.walk(path):
            if files is not None:
                files.sort()  
                for name in files:
                
                    if name.endswith('control'):
                        name= name.replace('.control', '')
                        self.names.append(name)

        showlist(self.names, self['list'])
        
    def callMyMsg1(self, result):
        if result:
            idx = self['list'].getSelectionIndex()
            if idx == -1 or None:
                return
            dom = self.names[idx]    
            com = dom
            self.session.open(slConsole, _('Removing: %s') % dom, ['opkg remove --force-removal-of-dependent-packages %s' % com], self.getfreespace, False)          
            self.onShown.append(self.openList)
            
    def getfreespace(self):
        fspace = freespace()
        self.freespace = fspace
        self['info'].setText(self.freespace)
        self.openList()

    def freespace():
        try:
            diskSpace = os.statvfs('/')
            capacity = float(diskSpace.f_bsize * diskSpace.f_blocks)
            available = float(diskSpace.f_bsize * diskSpace.f_bavail)
            fspace = round(float(available / 1048576.0), 2)
            tspace = round(float(capacity / 1048576.0), 1)
            spacestr = 'Free space(' + str(fspace) + 'MB) Total space(' + str(tspace) + 'MB)'
            return spacestr
        except:
            return ''

    def message1(self):
        self.session.openWithCallback(self.callMyMsg1,slMessageBox,_("Do you want to remove?"), slMessageBox.TYPE_YESNO, timeout = 15, default = False)       
        
#############################        
    def msgipkrst(self):
        self.session.openWithCallback(self.ipkrestrt, slMessageBox, _('Do you want restart enigma2 ?'), slMessageBox.TYPE_YESNO, timeout = 15, default = False)

            
    def ipkrestrt(self, result):
        if result:
            epgpath = '/media/hdd/epg.dat'
            epgbakpath = '/media/hdd/epg.dat.bak'
            if os.path.exists(epgbakpath):
                os.remove(epgbakpath)
            if os.path.exists(epgpath):
                copyfile(epgpath, epgbakpath)
            self.session.open(TryQuitMainloop, 3)
        else:
            self.close()              

class slMessageBox(Screen):

    TYPE_YESNO = 0
    TYPE_INFO = 1
    TYPE_WARNING = 2
    TYPE_ERROR = 3
    TYPE_MESSAGE = 4
   
    def __init__(self, session, text, type = TYPE_YESNO, timeout = -1, close_on_any_key = False, default = True, enable_input = True, msgBoxID = None, picon = None, simple = False, list = [], timeout_default = None):
        self.session = session
        skin = skin_path + 'slMessageBox.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('slMessageBox')
        Screen.__init__(self, session)
        self.setTitle(_('Sat-Lodge Panel V. %s' % currversion)) 
        self.type = type
        self.msgBoxID = msgBoxID
        self['text'] = Label(text)
        self['Text'] = StaticText(text)
        self['selectedChoice'] = StaticText()
        self.text = text
        self.close_on_any_key = close_on_any_key
        self.timeout_default = timeout_default
        self['ErrorPixmap'] = Pixmap()
        self['QuestionPixmap'] = Pixmap()
        self['InfoPixmap'] = Pixmap()
        self['WarningPixmap'] = Pixmap()
        self['title'] = Label(_('..:: Sat_Lodge Message::..'))
        self['version'] = Label(_('V. %s' %  currversion))
        self['maintener'] = Label(_(' by ))^^((')) 
        self.timerRunning = False
        self.initTimeout(timeout)
        picon = picon or type
        if picon != self.TYPE_ERROR:
            self['ErrorPixmap'].hide()
        if picon != self.TYPE_YESNO:
            self['QuestionPixmap'].hide()
        if picon != self.TYPE_INFO:
            self['InfoPixmap'].hide()
        if picon != self.TYPE_WARNING:
            self['WarningPixmap'].hide()
        self.title = self.type < self.TYPE_MESSAGE and [_('Question'),
         _('Information'),
         _('Warning'),
         _('Error')][self.type] or _('Message')
        if type == self.TYPE_YESNO:
            if list:
                self.list = list
            elif default == True:
                self.list = [(_('Yes'), True), (_('No'), False)]
            else:
                self.list = [(_('No'), False), (_('Yes'), True)]
        else:
            self.list = []
        self['list'] = MenuList(self.list)
        if self.list:
            self['selectedChoice'].setText(self.list[0][0])
        else:
            self['list'].hide()
        if enable_input:
            self['actions'] = ActionMap(['MsgBoxActions', 'DirectionActions'], {'cancel': self.cancel,
             'ok': self.ok,
             'alwaysOK': self.alwaysOK,
             'up': self.up,
             'down': self.down,
             'left': self.left,
             'right': self.right,
             'upRepeated': self.up,
             'downRepeated': self.down,
             'leftRepeated': self.left,
             'rightRepeated': self.right}, -1)
        self.onLayoutFinish.append(self.layoutFinished)

    def layoutFinished(self):
        self.setTitle(self.title)

    def initTimeout(self, timeout):
        self.timeout = timeout
        if timeout > 0:
            self.timer = eTimer() 
            # self.timer.start(100, 1)        
            try: 
                self.timer_conn = self.timer.timeout.connect(self.timerTick)
            except:
                self.timer.callback.append(self.timerTick) 				
            self.onExecBegin.append(self.startTimer)
            self.origTitle = None
            if self.execing:
                self.timerTick()
            else:
                self.onShown.append(self.__onShown)
            self.timerRunning = True
        else:
            self.timerRunning = False
        return

    def __onShown(self):
        self.onShown.remove(self.__onShown)
        self.timerTick()

    def startTimer(self):
        self.timer.start(500)

    def stopTimer(self):
        if self.timerRunning:
            del self.timer
            self.onExecBegin.remove(self.startTimer)
            self.setTitle(self.origTitle)
            self.timerRunning = False

    def timerTick(self):
        if self.execing:
            self.timeout -= 1
            if self.origTitle is None:
                self.origTitle = self.instance.getTitle()
            self.setTitle(self.origTitle + ' (' + str(self.timeout) + ')')
            if self.timeout == 0:
                self.timer.stop()
                self.timerRunning = False
                self.timeoutCallback()
        return

    def timeoutCallback(self):
        print 'Timeout!'
        if self.timeout_default is not None:
            self.close(self.timeout_default)
        else:
            self.ok()
        return

    def cancel(self):
        self.close(False)

    def ok(self):
        if self.list:
            self.close(self['list'].getCurrent()[1])
        else:
            self.close(True)

    def alwaysOK(self):
        self.close(True)

    def up(self):
        self.move(self['list'].instance.moveUp)

    def down(self):
        self.move(self['list'].instance.moveDown)

    def left(self):
        self.move(self['list'].instance.pageUp)

    def right(self):
        self.move(self['list'].instance.pageDown)

    def move(self, direction):
        if self.close_on_any_key:
            self.close(True)
        self['list'].instance.moveSelection(direction)
        if self.list:
            self['selectedChoice'].setText(self['list'].getCurrent()[0])
        self.stopTimer()

    def __repr__(self):
        return str(type(self)) + '(' + self.text + ')'  


class slPanelConfig(Screen, ConfigListScreen):

    def __init__(self, session):
        self.session = session
        skin = skin_path + 'slPanelConfig.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        self.setup_title = ('slPanelConfig')
        Screen.__init__(self, session)
        self.setTitle(_('Sat-Lodge Panel V. %s' % currversion)) 
        self['title'] = Label(_('..:: Sat-Lodge Config ::..'))
        self['version'] = Label(_('V. %s' %  currversion))
        self['maintener'] = Label(_(' by ))^^((')) 
        self['info'] = Label(_('Config Panel Addon'))       
        self['key_red'] = Button(_('Back'))
        self['key_green'] = Button(_('Save'))
        # self['key_yellow'] = Button(_('Update'))
        configlist = []
        ConfigListScreen.__init__(self, configlist, session=session)
        # configlist.append(getConfigListEntry(_('Auto Update Plugin'), config.plugins.slPanel.autoupd))
        configlist.append(getConfigListEntry(_('Path Manual IPK'), config.plugins.slPanel.ipkpth))
        configlist.append(getConfigListEntry(_('Link in Extensions Menu'), config.plugins.slPanel.strtext))
        # configlist.append(getConfigListEntry(_('Link in Main Menu'), config.plugins.slPanel.strtmain))
        configlist.append(getConfigListEntry(_('Link in Setup Menu'), config.plugins.slPanel.strtst))
        self['config'].setList(configlist)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'cancel': self.extnok,
         'red': self.extnok,
         'back': self.close,
         'ok': self.msgok,
         # 'yellow': self.slUpdate,
         'green': self.msgok}, -1)
        
     # def slUpdate(self):
        # self.session.open(slUpdate) 
        
    def extnok(self, answer = None):
        if answer is None:
            if self['config'].isChanged():
                self.session.openWithCallback(self.ShowMain2, slMessageBox, _('Quit without saving') + ' ?')
            else:
                self.close()
        return

    def ShowMain2(self, result):
        if result:
            self.close()

    def msgok(self):
        if os.path.exists(config.plugins.slPanel.ipkpth.value) is False:
            self.mbox = self.session.open(slMessageBox, _('Device not detected!'), slMessageBox.TYPE_INFO, timeout=4)
        else:

            for x in self["config"].list:
              x[1].save()
        
        plugins.clearPluginList()
        plugins.readPluginList(resolveFilename(SCOPE_PLUGINS))
        self.mbox = self.session.open(slMessageBox, _('Successfully saved configuration'), slMessageBox.TYPE_INFO, timeout=4)
        self.close(True)            
           
###################################################			
def main(session, **kwargs):

    if checkInternet():
        session.open(logoStrt)
    else:
        session.open(MessageBox, "No Internet", MessageBox.TYPE_INFO)      
        
        
    # session.open(logoStrt)                     
            
def menu(menuid, **kwargs):
    if menuid == 'mainmenu':
        return [(_('SatLodge Panel'),
          main,
          'SatLodge Panel',
          44)]
    return []

def cfgmain(menuid):
    if menuid == 'mainmenu':
        return [('SatLodge Panel',
          main,
          'SatLodge Panel',
          44)]
    else:
        return []    

def mainmenu(session, **kwargs):
    main(session, **kwargs)

def StartSetup(menuid):
    if menuid == 'setup':
        return [('SatLodge Panel',
          main,
          'SatLodge Panel',
          44)]
    else:
        return []

extDescriptor = PluginDescriptor(name='SatLodge Panel', description=_('SatLodge Panel'), where=PluginDescriptor.WHERE_EXTENSIONSMENU, icon=ico_path, fnc=main)
# mainDescriptor = PluginDescriptor(name='SatLodge Panel', description=_('SatLodge Panel'), where=PluginDescriptor.WHERE_MENU, icon=ico_path, fnc=cfgmain)
strtstDescriptor = PluginDescriptor(name=_('SatLodge Panel'), description=_('SatLodge Panel'), where=PluginDescriptor.WHERE_MENU, icon=ico_path, fnc=StartSetup)

def Plugins(**kwargs):
    result = [PluginDescriptor(name='SatLodge Panel', description=_('SatLodge Panel V. %s' % currversion), where=[PluginDescriptor.WHERE_PLUGINMENU], icon=ico_path, fnc=main)]
    if config.plugins.slPanel.strtext.value:
        result.append(extDescriptor)
    # if config.plugins.slPanel.strtmain.value:
        # result.append(mainDescriptor)
    if config.plugins.slPanel.strtst.value:
        result.append(strtstDescriptor)
    return result   
