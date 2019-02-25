#thanks mfaraj57-gogj from plugin Universal ImageDownloader
from Plugins.Plugin import PluginDescriptor
from Screens.ChoiceBox import ChoiceBox
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.HelpMenu import HelpableScreen
from Components.ActionMap import ActionMap, NumberActionMap, HelpableActionMap
from Components.Input import Input
from Components.Sources.StaticText import StaticText
from Components.ScrollLabel import ScrollLabel
from Components.Pixmap import Pixmap
from Components.Button import Button
from Components.Label import Label
from Components.ProgressBar import ProgressBar
from Components.FileList import FileList
from Components.MenuList import MenuList
from Components.Sources.List import List
from Components.Slider import Slider
from Components.Harddisk import harddiskmanager
from Components.config import getConfigListEntry, ConfigSubsection, ConfigText, ConfigLocations, ConfigSelection, ConfigBoolean, ConfigYesNo
from Components.config import config
from Components.ConfigList import ConfigListScreen
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.SelectionList import SelectionList
from Components.PluginComponent import plugins
from Components.AVSwitch import AVSwitch
from Tools.Directories import pathExists, fileExists, resolveFilename, SCOPE_PLUGINS, SCOPE_CURRENT_PLUGIN, SCOPE_CURRENT_SKIN, SCOPE_METADIR, SCOPE_MEDIA, SCOPE_LANGUAGE
from Tools.LoadPixmap import LoadPixmap
from enigma import  eConsoleAppContainer, ePicLoad, loadPNG, eTimer, quitMainloop, RT_HALIGN_LEFT, RT_VALIGN_CENTER, eListboxPythonMultiContent, eListbox, gFont, getDesktop
from cPickle import dump, load
from os import path as os_path, system as os_system, unlink, stat, mkdir, popen, makedirs, listdir, access, rename, remove, W_OK, R_OK, F_OK
from time import time, gmtime, strftime, localtime
from datetime import date
from Screens.Console import Console
import socket
import sys
import urllib, urllib2, re, os
from urllib import urlencode
from HTMLParser import HTMLParser
from urllib import quote
from urllib2 import Request, urlopen, URLError, HTTPError
from twisted.web.client import downloadPage, getPage
from xml.etree.cElementTree import fromstring
from xml.dom import minidom, Node
from default import process_mode
from plugin import currversion

mountedDevs = []
for p in harddiskmanager.getMountedPartitions(True):
    mountedDevs.append((p.mountpoint, _(p.description) if p.description else ''))
mounted_string = 'Nothing mounted at '
config.plugins.ImageDown = ConfigSubsection()
config.plugins.ImageDown.Downloadlocation = ConfigText(default='/media/hdd/', visible_width=50, fixed_size=False)

DESKHEIGHT = getDesktop(0).size().height()
dwidth = getDesktop(0).size().width()


plugin_path = '/usr/lib/enigma2/python/Plugins/SatLodge/slPanel'
skin_path = plugin_path
HD = getDesktop(0).size()
if HD.width() > 1280:
   skin_path = plugin_path + '/res/skins/fhd/'
else:
   skin_path = plugin_path + '/res/skins/hd/'
   
pics = plugin_path +  '/res/pics/icon.png'


   
def getDownloadPath():
    Downloadpath = config.plugins.ImageDown.Downloadlocation.value
    if Downloadpath.endswith('/'):
        return Downloadpath
    else:
        return Downloadpath + '/'

def freespace():
    downloadlocation = getDownloadPath()
    try:
        diskSpace = os.statvfs(downloadlocation)
        capacity = float(diskSpace.f_bsize * diskSpace.f_blocks)
        available = float(diskSpace.f_bsize * diskSpace.f_bavail)
        fspace = round(float(available / 1048576.0), 2)
        tspace = round(float(capacity / 1048576.0), 1)
        spacestr = 'Free space(' + str(fspace) + 'MB) Total space(' + str(tspace) + 'MB)'
        return fspace
    except:
        return 0

class STBmodel(Screen):

    def __init__(self, session):
        self.session = session
        skin = skin_path + 'STBmodel.xml'        
        with open(skin, 'r') as f:
            self.skin = f.read()
        Screen.__init__(self, session)
        self.setTitle(_('Sat-Lodge Panel by lululla V. %s' % currversion))         
        mktmp = 'mkdir -p /tmp/ImageDownloader'
        self.container = eConsoleAppContainer()
        self.container.execute(mktmp)
        self['title'] = Label('Teams')
        self['key_green'] = Label(_('Select'))
        self['key_red'] = Label(_('Exit'))
        self.list = []
        self['list'] = MenuList([], True, eListboxPythonMultiContent)
        self.addon = 'emu'
        self.icount = 0
        self.downloading = False
        self['actions'] = ActionMap(["DirectionActions",'SetupActions', 'ColorActions'], {'ok': self.okClicked,
         'green': self.okClicked,
         'up': self.up,
         'down': self.down,
         'left': self.left,
         'right': self.right,
         'cancel': self.exit}, -2)
        self.ListToMulticontent()

    def up(self):
        self['list'].up()
		
    def down(self):
        self['list'].down()
		
    def left(self):
        self['list'].pageUp()

    def right(self):
        self['list'].pageDown()
		
    def exit(self):
        cmd = 'rm -rf /tmp/ImageDownloader'
        container = eConsoleAppContainer()
        container.execute(cmd)
        self.close()

	
    def ListToMulticontent(self, result = None):
        res = []
        theevents = []
        self.data=process_mode(None)
        
        png = plugin_path + '/res/pics/yellow.png'
        
        if HD.width() > 1280:	

         self['list'].l.setItemHeight(50)
         self['list'].l.setFont(0, gFont('Regular', 32))                          
         for i in range(0, len(self.data)):		 
         
            res.append(MultiContentEntryText(pos=(0, 5), size=(2, 44), font=0, text='', color = 0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
            res.append(MultiContentEntryText(pos=(60, 0), size=(720, 44), font=0, text=str(self.data[i][0]), color = 0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
            theevents.append(res)
            res = []
        else:        
         self['list'].l.setItemHeight(45)
         self['list'].l.setFont(0, gFont('Regular', 22))
         for i in range(0, len(self.data)):
         
            res.append(MultiContentEntryText(pos=(0, 5), size=(2, 35), font=0, text='', color = 0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
            res.append(MultiContentEntryText(pos=(60, 0), size=(720, 35), text=str(self.data[i][0]), color = 0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))	
            theevents.append(res)
            res = []
			
        self['list'].l.setList(theevents)
        self['list'].show()
			
    def okClicked(self):
        cindex = self['list'].getSelectionIndex()
        param=self.data[cindex][1]
        self.session.open(FEEDmodel, param)

		
class FEEDmodel(Screen):
  
    def __init__(self, session,param=None):
        self.session = session
        skin = skin_path + 'FEEDmodel.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        Screen.__init__(self, session)  
        
        self.setTitle(_('Sat-Lodge Panel by lululla V. %s' % currversion))         
        
        self['title'] = Label("Brands")
        self['key_green'] = Label(_('Select'))
        self['key_red'] = Label(_('Back'))
        self.list = []
        self['list'] = MenuList([], True, eListboxPythonMultiContent)
        self.addon = 'emu'
        self.icount = 0
        self.downloading = False
        self.param=param
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okClicked,
         'green': self.okClicked,
         'red': self.close,		 
         'cancel': self.close}, -2)
        self.ListToMulticontent()
		
    def ListToMulticontent(self):
        res = []
        theevents = []
        self.data=process_mode(self.param)	
        if HD.width() > 1280:	  
         self['list'].l.setItemHeight(50)
         self['list'].l.setFont(0, gFont('Regular', 32))
         for i in range(0, len(self.data)):
            res.append(MultiContentEntryText(pos=(0, 5), size=(2, 44), font=0, text='', color = 0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
            res.append(MultiContentEntryText(pos=(60, 0), size=(720, 44), font=0, text=str(self.data[i][0]), color = 0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
            theevents.append(res)
            res = []		
        else:            
         self['list'].l.setItemHeight(45)
         self['list'].l.setFont(0, gFont('Regular', 22))
         for i in range(0, len(self.data)):
            res.append(MultiContentEntryText(pos=(0, 5), size=(2, 35), font=0, text='', color = 0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
            res.append(MultiContentEntryText(pos=(60, 0), size=(720, 35), font=0, text=str(self.data[i][0]), color = 0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
            theevents.append(res)
            res = []
        self['list'].l.setList(theevents)
        self['list'].show()
        

    def okClicked(self):
        cindex = self['list'].getSelectionIndex()	   
        param=self.data[cindex][1]
        print "param1",param
        self.session.open(SERVERmodel, param)

class SERVERmodel(Screen):
        
    def __init__(self, session,param=None):
        self.session = session
        skin = skin_path + 'SERVERmodel.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()        
        Screen.__init__(self, session)        
        self.setTitle(_('Sat-Lodge Panel by lululla V. %s' % currversion))         
        
        self['title'] = Label("Models")
        self['key_green'] = Label(_('Select'))
        self['key_red'] = Label(_('Back'))		
        self.list = []
        self.param=param
        self['list'] = MenuList([], True, eListboxPythonMultiContent)              
        self.downloading = False        
        self.downloading = True
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okClicked,
         'green': self.okClicked,
         'red': self.close,		 
         'cancel': self.close}, -2)
        self.ListToMulticontent()
        return

    def ListToMulticontent(self):
        res = []
        theevents = []
        self.data=process_mode(self.param)
        if HD.width() > 1280: 
         self['list'].l.setItemHeight(50)
         self['list'].l.setFont(0, gFont('Regular', 32))        
         for i in range(0, len(self.data)):
            model=str(self.data[i][0])
            res.append(MultiContentEntryText(pos=(0, 5), size=(2, 44), font=0, text='', color = 0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
            res.append(MultiContentEntryText(pos=(60, 0), size=(540, 44), font=0, text=model, color = 0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
            theevents.append(res)
            res = []
        else:        
         self['list'].l.setItemHeight(45)
         self['list'].l.setFont(0, gFont('Regular', 22))        
         for i in range(0, len(self.data)):
            model=str(self.data[i][0])
            res.append(MultiContentEntryText(pos=(0, 5), size=(2, 30), font=0, text='', color = 0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
            res.append(MultiContentEntryText(pos=(60, 0), size=(540, 30), font=0, text=model, color = 0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
            theevents.append(res)
            res = []
            

        

        self['list'].l.setList(theevents)
        self['list'].show()
        

    def okClicked(self):           
        cindex = self['list'].getSelectionIndex()
        param=self.data[cindex][1]        
        print "paramxx",param
        self.session.open(DownloaderImage, param)
        return

class DownloaderImage(Screen):

    def __init__(self, session,param=None):
        self.session = session
        skin = skin_path + 'DownloaderImage.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()        
        Screen.__init__(self, session)
        self.setTitle(_('Sat-Lodge Panel by lululla V. %s' % currversion))         
        
        self.param = param
        self['key_green'] = Label(_(' '))
        self['key_red'] = Label(_('Back'))
        self['info'] = Label(_(' '))
        self['menu'] = MenuList([], True, eListboxPythonMultiContent)
        list = []
        self.list = list
        self.status = []
        self.slist = []        
        self['actions'] = ActionMap(['SetupActions', 'MenuActions', 'ColorActions'], {'ok': self.selclicked,
         'cancel': self.close,
         'red': self.close,
         'green': self.selclicked}, -2)
        self.itempreview = False       
        self.ListToMulticontent()

    def ListToMulticontent(self, result = None):
        downloadpath = getDownloadPath()
        res = []
        theevents = []
        print "self.param1",self.param		
        if HD.width() > 1280: 
         self['menu'].l.setItemHeight(50)
         self['menu'].l.setFont(0, gFont('Regular', 32))        
         self.data=process_mode(self.param)
         if len(self.data)==0:
            self['info'].setText("Failed To Get Or No Image !")
            self['key_green'] = Label(_(' '))
            return
         self['key_green'] = Label(_('Select'))
         for i in range(0, len(self.data)):
            name=str(self.data[i][0])
            url = str(self.data[i][1])
            localname=os.path.split(url)[1]           
            nfiname=localname.replace(".zip","nfi")
            if os.path.exists(downloadpath + localname) or os.path.exists(downloadpath + nfiname):
                png = plugin_path + '/res/pics/green.png'
            else:
                png = plugin_path + '/res/pics/yellow.png'
            res.append(MultiContentEntryText(pos=(0, 1), size=(5, 30), font=0, text='', color = 0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
            res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 20), size=(30, 30), png=loadPNG(png)))
            res.append(MultiContentEntryText(pos=(40, 0), size=(1200, 44), font=0, text=name, color = 0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
            theevents.append(res)
            res = []	        
        else:        
         self['menu'].l.setItemHeight(45)
         self['menu'].l.setFont(0, gFont('Regular', 22))        
         self.data=process_mode(self.param)
         if len(self.data)==0:
            self['info'].setText("Failed To Get Or No Image !")
            self['key_green'] = Label(_(' '))
            return
         self['key_green'] = Label(_('Select'))
         for i in range(0, len(self.data)):
            name=str(self.data[i][0])
            url = str(self.data[i][1])
            localname=os.path.split(url)[1]			
            nfiname=localname.replace(".zip","nfi",)
            if os.path.exists(downloadpath + localname) or os.path.exists(downloadpath + nfiname):
                png = plugin_path + '/res/pics/green.png'
            else:
                png = plugin_path + '/res/pics/yellow.png'
            res.append(MultiContentEntryText(pos=(0, 1), size=(5, 30), font=0, text='', color = 0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
            res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 10), size=(30, 30), png=loadPNG(png)))
            res.append(MultiContentEntryText(pos=(40, 0), size=(730, 35), font=0, text=name, color = 0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
            theevents.append(res)
            res = []

        self.theevents = []
        self.theevents = theevents
        self['menu'].l.setList(theevents)
        self['menu'].show()

    def selclicked(self):
        cindex = self['menu'].getSelectionIndex()
        try:
            param = self.data[cindex][1]
        except:
            return
        self.session.openWithCallback(self.ListToMulticontent, ImageDownLoader, param)

class ImageDownLoader(Screen):   
   
    def __init__(self, session,param):
        self.session = session
        skin = skin_path + 'ImageDownloader.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()        
        Screen.__init__(self, session)
        self.setTitle(_('Sat-Lodge Panel by lululla V. %s' % currversion))         
        
        self.param=param
        self.imageurl=param
        self.menu = 0
        self.list = []
        self.oktext = _('\nSelect To Continue !')
        self.text = ''
        if True:
            self.list.append(('Download',
             _('Start Download'),
             _('\nStarts To Download Image !') + self.oktext,
             None))
            # self.list.append(('Background',
             # _('Download in Background'),
             # _('\nDownload in Background and Explore other Images !') + self.oktext,
             # None))
            self.list.append(('Downloadlocation',
             _('Set Download Location'),
             _('\nSelect Your Download Location : HDD or USB !') + self.oktext,
             None))
            self.list.append(('Files',
             _('Explore Local Images'),
             _('\nView Downloaded Images !') + self.oktext,
             None))            
        self['menu'] = List(self.list)
        
        # self['key_red'] = Label(_('Back'))
        # self['key_green'] = Label(_('Select'))	        
        
        self['key_red'] = StaticText(_('Back'))
        self['key_green'] = StaticText(_('Select'))		
        self['status'] = StaticText('')
        self['targettext'] = StaticText(_('Selected Download Location:'))
        fname = os.path.basename(self.param)
        if 'DreamEliteImages' in fname:
            a = []
            a = fname.split('=')
            fname = a[2]
        self['downloadtext'] = StaticText(_('Selected Image To Download:\n ' + fname))
        fspace = str(freespace()) + 'MB'
        self['target'] = Label(config.plugins.ImageDown.Downloadlocation.value + '\n' + 'Free Space: ' + fspace)
        self['shortcuts'] = ActionMap(['ShortcutActions', 'ColorActions', 'WizardActions', 'InfobarEPGActions'], {'ok': self.go,
         'green': self.go,		 
         'back': self.cancel,
         'red': self.cancel}, -1)
        self.onLayoutFinish.append(self.layoutFinished)
        self.onShown.append(self.setWindowTitle)
        return

    def layoutFinished(self):
        idx = 0
        self['menu'].index = idx

    def setWindowTitle(self):
        self.setTitle(_('Thanks Image Downloader 2.0 Tools'))

    def fnameexists(self):
        path = getDownloadPath()
        filename = path + os.path.basename(self.imageurl)
        if fileExists(filename):
            return True
        else:
            return False

    def callMyMsg(self, result):
        path = getDownloadPath()
        if self.checkmountDownloadPath(path) == False:
            return
        if result:
            if fileExists('/etc/init.d/flashexpander.sh'):
                self.session.open(MessageBox, _('FlashExpander is used,no Image DownLoad possible.'), MessageBox.TYPE_INFO)
                self.cancel()
            else:
                runDownload = True
                self.localfile = path + os.path.basename(self.imageurl)
                #########lower file for flashimage
                self.localfile =self.localfile.lower()  
                
                self.session.openWithCallback(self.cancel, Downloader, self.imageurl, self.localfile, path)
							
    def checkmountDownloadPath(self, path):
        if path is None:
            self.session.open(MessageBox, _('Nothing Entered'), MessageBox.TYPE_ERROR)
            return False
        elif freespace() < 60:
            self.session.open(MessageBox, _('Free space is less than 60MB,please choose another download location,or delete files from storage device'), MessageBox.TYPE_ERROR)
            return False
        else:
            sp = []
            sp = path.split('/')
            print sp
            if len(sp) > 1:
                if sp[1] != 'media':
                    self.session.open(MessageBox, mounted_string % path, MessageBox.TYPE_ERROR)
                    return False
            mounted = False
            self.swappable = False
            sp2 = []
            f = open('/proc/mounts', 'r')
            m = f.readline()
            while m and not mounted:
                if m.find('/%s/%s' % (sp[1], sp[2])) is not -1:
                    mounted = True
                    print m
                    sp2 = m.split(' ')
                    print sp2
                    if sp2[2].startswith('ext') or sp2[2].endswith('fat'):
                        print '[stFlash] swappable'
                        self.swappable = True
                m = f.readline()

            f.close()
            if not mounted:
                self.session.open(MessageBox, mounted_string + str(path), MessageBox.TYPE_ERROR)
                return False
            if os.path.exists(config.plugins.ImageDown.Downloadlocation.value):
                try:
                    os.chmod(config.plugins.ImageDown.Downloadlocation.value, 511)
                except:
                    pass

            return True
            return
                                     
    def go(self):
        current = self['menu'].getCurrent()
        if current:
            currentEntry = current[0]
        if self.menu == 0:
            if currentEntry == 'Download':
                if not self.fnameexists() == True:
                    runDownload = True
                    path = getDownloadPath()
                    self.localfile = path + os.path.basename(self.imageurl)
                    
                    #########lower file for flashimage
                    self.localfile =self.localfile.lower()  
                
                    self.session.openWithCallback(self.cancel, Downloader, self.imageurl, self.localfile, path)
                else:
                    self.session.openWithCallback(self.callMyMsg, MessageBox, _('The File Aleady Exists, ' + 'Overwrite ?'), MessageBox.TYPE_YESNO)
            if currentEntry == 'Files':
                self.session.open(ImageDownLoaderFiles)
            elif currentEntry == 'Downloadlocation':
                self.session.openWithCallback(self.Downloadlocation_choosen, ImageDownloadLocation)
            # elif currentEntry == 'Background':
                # if not self.fnameexists() == True:
                   # path = getDownloadPath()				
                   # self.localfile = path + os.path.basename(self.imageurl)
                   # title=os.path.basename(self.imageurl)
                   # from download import startdownload
                   # startdownload(self.session, 'download', self.imageurl, self.localfile, title, None, True)
                # else:
                   # path = getDownloadPath()				
                   # self.localfile = path + os.path.basename(self.imageurl)
                   # title=os.path.basename(self.imageurl)
                   # from download import startdownload
                   # startdownload(self.session, 'download', self.imageurl, self.localfile, title, None, True)

				
    def Downloadlocation_choosen(self, option):
        self.updateTarget()
        if option is not None:
            config.plugins.ImageDown.Downloadlocation.value = str(option[1])
        config.plugins.ImageDown.Downloadlocation.save()
        config.plugins.ImageDown.save()
        config.save()
        self.createDownloadfolders()
        return

    def createDownloadfolders(self):
        self.Downloadpath = getDownloadPath()
        try:
            if os_path.exists(self.Downloadpath) == False:
                makedirs(self.Downloadpath)
        except OSError:
            self.session.openWithCallback(self.goagaintoDownloadlocation, MessageBox, _('Sorry, your Download destination is not writeable.\n\nPlease choose another one.'), MessageBox.TYPE_ERROR)

    def goagaintoDownloadlocation(self, retval):
        self.session.openWithCallback(self.Downloadlocation_choosen, ImageDownloadLocation)

    def updateTarget(self):
        fspace = str(freespace()) + ' MB'
        self['target'].setText(''.join(config.plugins.ImageDown.Downloadlocation.value + ' Freespace:' + fspace))

    def cancel(self, result = None):
        self.close(None)
        return

class ImageDownLoaderFiles(Screen):

    def __init__(self, session):
        self.session = session
        skin = skin_path + 'ImageDownLoaderFiles.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()        
        Screen.__init__(self, session)
        self.setTitle(_('Sat-Lodge Panel by lululla V. %s' % currversion))         
        
        list = []
        self['menu'] = MenuList([], True, eListboxPythonMultiContent)
        self['key_red'] = Label(_('Back '))
        self['key_green'] = Label(_(' '))
        folder = str(config.plugins.ImageDown.Downloadlocation.value)
        fspace = str(freespace()) + 'MB'
        self['menu'].onSelectionChanged.append(self.selectionChanged)
        self['info'] = Label(folder + '\n' + ' Free space: ' + fspace)
        if folder.endswith('/'):
            self.folder = folder
        else:
            self.folder = folder + '/'
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'green': self.delimage,
         'cancel': self.close}, -2)
        self.fillplgfolders()
		
    def selectionChanged(self):
        try:
            fname = self['menu'].getCurrent()
            cindex = self['menu'].getSelectionIndex()
            filename = self.nfifiles[cindex][0]
            if filename.endswith(".zip") :
               self['key_green'].setText('Delete')
            else:
                self['key_green'].setText(' ')  
        except:
            pass

    def delimage(self):
         fname = self['menu'].getCurrent()
         cindex = self['menu'].getSelectionIndex()
         filename = self.folder + self.nfifiles[cindex][0]
         if filename.endswith(".zip") :
            self['key_green'].setText('Delete')
            self.session.openWithCallback(self.removefile, MessageBox, _(filename + '\nWill Be Removed,\nAre You Sure ?'), MessageBox.TYPE_YESNO)

         else:
            self['key_green'].setText(' ') 
            
    def removefile(self, result):
        if result:
            try:
                fname = self['menu'].getCurrent()
                cindex = self['menu'].getSelectionIndex()
                filename = self.folder + self.nfifiles[cindex][0]
                remove(filename)
                self.fillplgfolders()
            except:
                self.session.open(MessageBox, _('Unable To Delete File !'), type=MessageBox.TYPE_ERROR, timeout=5, close_on_any_key=True)
						
    def fillplgfolders(self):
        try:
            self.nfifiles = []
            for x in listdir(self.folder):
                if os.path.isfile(self.folder + x):
                    if x.endswith('.zip'):
                        msize = os.path.getsize(self.folder + x)
                        localimagesize = str(round(float(msize / 1048576.0), 2))
                        self.nfifiles.append([x, localimagesize])

            self.ListToMulticontent()
        except:	
         self.session.open(MessageBox, _('Unable To Show Files, Check \n' + self.folder + '\nIf Available And Mounted !'), type=MessageBox.TYPE_ERROR, timeout=5, close_on_any_key=True)

    def ListToMulticontent(self):
        res = []
        theevents = []
        self.events = []
        self.events = self.nfifiles
        if HD.width() > 1280: 
         self['menu'].l.setItemHeight(50)
         self['menu'].l.setFont(0, gFont('Regular', 32))
         for i in range(0, len(self.events)):
            mfile = self.events[i][0]
            msize = self.events[i][1] + ' MB'
            res.append(MultiContentEntryText(pos=(0, 11), size=(2, 35), font=0, text='', color = 0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
            res.append(MultiContentEntryText(pos=(40, 11), size=(1100, 44), font=0, text=mfile, color = 0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
            res.append(MultiContentEntryText(pos=(1000, 11), size=(170, 35), font=0, text=msize, color = 0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
            theevents.append(res)
            res = []        
        else:        
         self['menu'].l.setItemHeight(45)
         self['menu'].l.setFont(0, gFont('Regular', 22))
         for i in range(0, len(self.events)):
            mfile = self.events[i][0]
            msize = self.events[i][1] + ' MB'
            res.append(MultiContentEntryText(pos=(0, 5), size=(2, 35), font=0, text='', color = 0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
            res.append(MultiContentEntryText(pos=(10, 5), size=(650, 35), font=0, text=mfile, color = 0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
            res.append(MultiContentEntryText(pos=(660, 5), size=(150, 35), font=0, text=msize, color = 0xa6d1fe, flags=RT_HALIGN_LEFT | RT_VALIGN_CENTER))
            theevents.append(res)
            res = []

        self['menu'].l.setList(theevents)
        self['menu'].show()
        self.selectionChanged()
		
class ImageDownloadLocation(Screen, HelpableScreen):

    def __init__(self, session, text = '', filename = '', currDir = None, location = None, userMode = False, windowTitle = _('Choose Download location'), minFree = None, autoAdd = False, editDir = False, inhibitDirs = [], inhibitMounts = []):
        
        self.session = session          
        skin = skin_path + 'ImageDownloadLocation.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()
        Screen.__init__(self, session)
        self.setTitle(_('Sat-Lodge Panel by lululla V. %s' % currversion))         
        HelpableScreen.__init__(self)
        self['text'] = StaticText(_('Selected Download Place:'))
        self.text = text
        self.filename = filename
        self.minFree = minFree
        self.reallocation = location
        self.location = location and location.value[:] or []
        self.userMode = userMode
        self.autoAdd = autoAdd
        self.editDir = editDir
        self.inhibitDirs = inhibitDirs
        self.inhibitMounts = inhibitMounts
        inhibitDirs = ['/bin',
         '/boot',
         '/dev',
         '/lib',
         '/proc',
         '/sbin',
         '/sys',
         '/mnt',
         '/var',
         '/home',
         '/tmp',
         '/srv',
         '/etc',
         '/share',
         '/usr',
         '/ba',
         '/MB_Images']
        inhibitMounts = ['/mnt', '/ba', '/MB_Images']
        self['filelist'] = FileList(currDir, showDirectories=True, showFiles=False, inhibitMounts=inhibitMounts, inhibitDirs=inhibitDirs)
        self['key_green'] = Label(_('Save'))
        self['key_red'] = Label(_('Back'))
        self['target'] = Label()
        if self.userMode:
            self.usermodeOn()

        class DownloadLocationActionMap(HelpableActionMap):

            def __init__(self, parent, context, actions = {}, prio = 0):
                HelpableActionMap.__init__(self, parent, context, actions, prio)

        self['WizardActions'] = DownloadLocationActionMap(self, 'WizardActions', {'left': self.left,
         'right': self.right,
         'up': self.up,
         'down': self.down,
         'ok': (self.ok, _('Select')),
         'back': (self.cancel, _('Cancel'))}, -2)
        self['ColorActions'] = DownloadLocationActionMap(self, 'ColorActions', {'red': self.cancel,
         'green': self.select}, -2)
        self.setWindowTitle()
        self.onLayoutFinish.append(self.switchToFileListOnStart)

    def setWindowTitle(self):
        self.setTitle(_('Choose Download location'))

    def switchToFileListOnStart(self):
        if self.reallocation and self.reallocation.value:
            self.currList = 'filelist'
            currDir = self['filelist'].current_directory
            if currDir in self.location:
                self['filelist'].moveToIndex(self.location.index(currDir))
        else:
            self.switchToFileList()

    def switchToFileList(self):
        if not self.userMode:
            self.currList = 'filelist'
            self['filelist'].selectionEnabled(1)
            self.updateTarget()

    def up(self):
        self[self.currList].up()
        self.updateTarget()

    def down(self):
        self[self.currList].down()
        self.updateTarget()

    def left(self):
        self[self.currList].pageUp()
        self.updateTarget()

    def right(self):
        self[self.currList].pageDown()
        self.updateTarget()

    def ok(self):
        if self.currList == 'filelist':
            if self['filelist'].canDescent():
                self['filelist'].descent()
                self.updateTarget()

    def updateTarget(self):
        currFolder = self.getPreferredFolder()
        if currFolder is not None:
            self['target'].setText(''.join((currFolder, self.filename)))
        else:
            self['target'].setText(_('Invalid Location'))
        return

    def cancel(self):
        self.close(None)
        return

    def getPreferredFolder(self):
        if self.currList == 'filelist':
            return self['filelist'].getSelection()[0]

    def saveSelection(self, ret):
        if ret:
            ret = ''.join((self.getPreferredFolder(), self.filename))
        config.plugins.ImageDown.Downloadlocation.value = ret
        config.plugins.ImageDown.Downloadlocation.save()
        config.plugins.ImageDown.save()
        config.save()
        self.close(None)
        return

    def checkmountDownloadPath(self, path):
        if path is None:
            self.session.open(MessageBox, _('Nothing Entered !'), MessageBox.TYPE_ERROR)
            return False
        else:
            sp = []
            sp = path.split('/')
            print sp
            if len(sp) > 1:
                if sp[1] != 'media':
                    self.session.open(MessageBox, mounted_string + path, MessageBox.TYPE_ERROR)
                    return False
            mounted = False
            self.swappable = False
            sp2 = []
            f = open('/proc/mounts', 'r')
            m = f.readline()
            while m and not mounted:
                if m.find('/%s/%s' % (sp[1], sp[2])) is not -1:
                    mounted = True
                    print m
                    sp2 = m.split(' ')
                    print sp2
                    if sp2[2].startswith('ext') or sp2[2].endswith('fat'):
                        print '[stFlash] swappable'
                        self.swappable = True
                m = f.readline()

            f.close()
            if not mounted:
                self.session.open(MessageBox, mounted_string + str(path), MessageBox.TYPE_ERROR)
                return False
            if os.path.exists(config.plugins.ImageDown.Downloadlocation.value):
                try:
                    os.chmod(config.plugins.ImageDown.Downloadlocation.value, 511)
                except:
                    pass

            return True
            return

    def select(self):
        currentFolder = self.getPreferredFolder()
        foldermounted = self.checkmountDownloadPath(currentFolder)
        if foldermounted == True:
            pass
        else:
            return
        if currentFolder is not None:
            if self.minFree is not None:
                try:
                    s = os.statvfs(currentFolder)
                    if s.f_bavail * s.f_bsize / 314572800 > self.minFree:
                        return self.saveSelection(True)
                except OSError:
                    pass

                self.session.openWithCallback(self.saveSelection, MessageBox, _('There Might Not Be Enough Space On The Selected Partition.\nDo You Really Want To Continue ?'), type=MessageBox.TYPE_YESNO)
            else:
                self.saveSelection(True)
        return

        

from Components.Sources.Progress import Progress
        
class Downloader(Screen):

    def __init__(self, session, url = None, target = None, path = None):
        self.session = session
            
        skin = skin_path + 'Downloader.xml'
        with open(skin, 'r') as f:
            self.skin = f.read()  
        Screen.__init__(self, session)
        self.setTitle(_('Sat-Lodge Panel by lululla V. %s' % currversion))         
        
        print url
        self.url = url
        self.target = target
        self.path = path
        self.nfifile = target
        self['info'] = Label('')
        self['info2'] = Label('')
        self['progress'] = ProgressBar()
        self.aborted = False
        self['progress'].setRange((0, 100))
        self['progress'].setValue(0)
        self.onLayoutFinish.append(self.startDownload)
        self['actions'] = ActionMap(['OkCancelActions'], {'cancel': self.cancel}, -1)
        self.connection = None
        return

    def startDownload(self):
        from Tools.Downloader import downloadWithProgress
        info = ' Downloading :\n %s ' % self.url
        self['info2'].setText(info)
        self.downloader = downloadWithProgress(self.url, self.target)
        self.downloader.addProgress(self.progress)
        self.downloader.start().addCallback(self.responseCompleted).addErrback(self.responseFailed)

    def progress(self, current, total):
        p = int(100 * (float(current) / float(total)))
        self['progress'].setValue(p)
        info = _('Downloading') + ' ' + '%d of %d kBytes' % (current / 1024, total / 1024)
        info = 'Downloading ... ' + str(p) + '%'
        self['info'].setText(info)
        self.setTitle(info)
        self.last_recvbytes = current

    def responseCompleted(self, string = ''):
        if self.aborted:
            self.finish(aborted=True)
        else:
            info = 'The Image Downloaded Successfully !'
            self['info2'].setText(info)
            if self.target.endswith('.zip'):
                info = 'The Image Downloaded Successfully !'
                self.session.openWithCallback(self.close, MessageBox, _(info), type=MessageBox.TYPE_INFO, timeout=3)
            else:
                self.close()
                return
       
    def responseFailed(self, failure_instance = None, error_message = ''):
        self.error_message = error_message
        if error_message == '' and failure_instance is not None:
            self.error_message = failure_instance.getErrorMessage()
        info = 'Download Failed ' + self.error_message
        self['info2'].setText(info)
        self.session.openWithCallback(self.close, MessageBox, _(info), timeout=3, close_on_any_key=True)
        return

    def cancel(self):
        if self.downloader is not None:
            info = 'You Are Going To Abort Download, Are You Sure ?'
            self.session.openWithCallback(self.abort, MessageBox, _(info), type=MessageBox.TYPE_YESNO)
        else:
            self.aborted = True
            self.close()
        return

    def abort(self, result = None):
        if result:
            self.downloader.stop
            self.aborted = True
            self.close()

    def exit(self, result = None):
        self.close()