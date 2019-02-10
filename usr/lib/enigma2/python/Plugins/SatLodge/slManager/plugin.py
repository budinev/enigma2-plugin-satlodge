#"****************************************"
#"*    by Lululla                        *"
#"*     all right reserved               *"
#"*          no copy                     *"
#"****************************************"
# from skin import loadSkin
from Components.ActionMap import ActionMap, NumberActionMap
from Components.Button import Button
from Components.FileList import FileList
from Components.Label import Label
from Components.Language import language
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.Pixmap import Pixmap
from Components.PluginComponent import plugins
from Components.ScrollLabel import ScrollLabel
from Components.Sources.List import List
from Components.Sources.StaticText import StaticText
from Plugins.Plugin import PluginDescriptor
from Screens.ChoiceBox import ChoiceBox
from Screens.Console import Console
from Screens.Console import Console
from Screens.MessageBox import MessageBox
from Screens.PluginBrowser import PluginBrowser
from Screens.Screen import Screen
from Screens.Standby import TryQuitMainloop
from ServiceReference import ServiceReference
from Tools import Notifications
from Tools.BoundFunction import boundFunction
from Tools.Directories import *
from Tools.Directories import SCOPE_SKIN_IMAGE, resolveFilename, SCOPE_PLUGINS, fileExists, copyfile, SCOPE_LANGUAGE
from Tools.GetEcmInfo import GetEcmInfo
from Tools.LoadPixmap import LoadPixmap
from enigma import *
from enigma import getDesktop, gFont, eListboxPythonMultiContent, eTimer, ePicLoad, loadPNG, RT_HALIGN_LEFT, RT_HALIGN_RIGHT, RT_HALIGN_CENTER, RT_VALIGN_CENTER
from os import path, listdir, remove, mkdir, chmod, walk
from twisted.web.client import getPage
from xml.dom import Node, minidom
import os
import os, gettext, sys, time
import time
import urllib
Version = '1.6'
plugin_path = '/usr/lib/enigma2/python/Plugins/SatLodge/slManager/'



dwidth = getDesktop(0).size().width()
DESKHEIGHT = getDesktop(0).size().height()
skin_path = plugin_path
HD = getDesktop(0).size()
if HD.width() > 1280:
   skin_path = plugin_path + 'res/skins/fhd/'
else:
   skin_path = plugin_path + 'res/skins/hd/'
   
   
########skin
# global HD_Res
# try:
    # sz_w = getDesktop(0).size().width()
# except:
    # sz_w = 1280
# if sz_w == 1920:
    # HD_Res = True
# else:
    # HD_Res = False
# if HD_Res:
    # loadSkin(plugin_path + 'img/skinFHD.xml')
# else:
    # loadSkin(plugin_path + 'img/skin.xml')
    







def show_list(h):
    # png1 = '/usr/lib/enigma2/python/Plugins/SatLodge/slManager/res/img/actcam.png'
    # png2 = '/usr/lib/enigma2/python/Plugins/SatLodge/slManager/res/img/defcam.png'
    png1 = plugin_path + 'res/img/actcam.png'
    png2 = plugin_path + 'res/img/defcam.png'    
    cond = readCurrent_1()
    if HD.width() > 1280:  

        res = [(h)]
        # cond = readCurrent_1()
        if cond == h:
            res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 6), size=(51, 40), png=loadPNG(png1)))
            res.append(MultiContentEntryText(pos=(60, 2), size=(698, 50), font=8, text=h+' (Active)', color = 0xadff00 , flags=RT_HALIGN_CENTER))

        else:
            res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 6), size=(51, 40), png=loadPNG(png2)))
            res.append(MultiContentEntryText(pos=(60, 2), size=(698, 50), font=8, text=h, flags=RT_HALIGN_CENTER))
        return res    
    else:
        res = [(h)]
        if cond == h:
            res.append(MultiContentEntryText(pos=(60, 2), size=(406, 40), font=5, text=h+' (Active)', color = 0xadff00, flags=RT_HALIGN_CENTER))
            res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 2), size=(51, 40), png=loadPNG(png1)))
        else:
            res.append(MultiContentEntryText(pos=(60, 2), size=(406, 40), font=5, text=h, flags=RT_HALIGN_CENTER))
            res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 2), size=(51, 40), png=loadPNG(png2)))
        return res
class webList(MenuList):
    def __init__(self, list):
        MenuList.__init__(self, list, True, eListboxPythonMultiContent)
        if DESKHEIGHT == 1920:
            self.l.setItemHeight(50)
            self.l.setFont(0, gFont('Regular', 36))
        else:
            self.l.setItemHeight(40)
            self.l.setFont(0, gFont('Regular', 23))
            
def showlist(data, list):
    icount = 0
    plist = []
    for line in data:
        name = data[icount]
        plist.append(show_list_1(name))
        icount = icount + 1
        list.setList(plist)
 
        
def show_list_1(h):

    if HD.width() > 1280: 

        res = [h]
        res.append(MultiContentEntryText(pos=(2, 2), size=(670, 40), font=8, text=h, flags=RT_HALIGN_LEFT))    
    else:       


        res = [h]
        res.append(MultiContentEntryText(pos=(2, 2), size=(660, 30), font=3, text=h, flags=RT_HALIGN_LEFT))    
    return res
        
# def show_list_1(h):

    # if HD.width() == 1280:
    # # if sz_w == 1280:
        # res = [h]
        # res.append(MultiContentEntryText(pos=(2, 2), size=(660, 40), font=0, text=h, flags=RT_HALIGN_LEFT))
        # return res
    # else:
        # res = [h]
        # res.append(MultiContentEntryText(pos=(2, 2), size=(670, 50), font=0, text=h, flags=RT_HALIGN_LEFT))
        # return res
        
class m2list(MenuList):
    def __init__(self, list):
        MenuList.__init__(self, list, False, eListboxPythonMultiContent)
        self.l.setFont(0, gFont('Regular', 16))
        self.l.setFont(1, gFont('Regular', 20))
        self.l.setFont(2, gFont('Regular', 22))
        self.l.setFont(3, gFont('Regular', 24))
        self.l.setFont(4, gFont('Regular', 26))
        self.l.setFont(5, gFont('Regular', 28))
        self.l.setFont(6, gFont('Regular', 30))
        self.l.setFont(7, gFont('Regular', 32))
        self.l.setFont(8, gFont('Regular', 34))
        if HD.width() > 1280: 
            self.l.setItemHeight(50)        
        else:        
            self.l.setItemHeight(45)  
        
   


ECM_INFO = '/tmp/ecm.info'
EMPTY_ECM_INFO = ('', '0', '0', '0')

old_ecm_time = time.time()
info = {}
ecm = ''
data = EMPTY_ECM_INFO

class slManager(Screen):

        instance = None
    
        # if DESKHEIGHT < 1280:		
        skin = skin_path + 'slManager.xml'
        # else:	
            # skin = skin_path + 'slManagerFHD.xml'
        f = open(skin, 'r')
        skin = f.read()
        f.close()    

  
        
        def __init__(self, session, args = 0):
    
                assert not slManager.instance, "only one slManager instance is allowed!"
                slManager.instance = self
                self.skin = slManager.skin

                Screen.__init__(self, session)

                self.setTitle(_('Sat-Lodge Manager by lululla V. %s' % Version))         
                self.session = session
        

                
                self.index = 0
                self.emulist = []
                self.namelist = []
                self.oldService = self.session.nav.getCurrentlyPlayingServiceReference()
                self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
                {
                        "ok": self.action,
                        "cancel": self.close,
                        "yellow": self.download,
                        "green": self.action,
                        "blue": self.slpanel,

                        "red": self.stop,
                }, -1)
                self["key_green"] = Button(_("Start"))
                # self["key_green2"] = Button(_("ReStart"))
                
                self["key_blue"] = Button(_("SatLodge Panel"))
                self['key_blue'].hide()
                if fileExists('/usr/lib/enigma2/python/Plugins/SatLodge/slPanel/plugin.pyo'):
                    self["key_blue"].show()

                self["key_yellow"] = Button(_("Download"))
                self["key_red"] = Button(_("Stop"))
                self['version'] = Label(_('V. %s' % Version))
                self['maintener'] = Label(_('by ))^^(('))
                self['team'] = Label(_('..:: Sat-Lodge Manager ::..'))                
                self['info'] = Label()
                self.currCam = self.readCurrent()
                self.softcamslist = []
                self['desc'] = Label()
                self['ecminfo'] = Label(_('Ecm Info')) 
                self["list"] = m2list([])
                self.timer = eTimer()
                self['desc'].setText(_('Scanning and retrieval list softcam ...'))
                try:
                    self.timer.callback.append(self.cgdesc)
                except:
                    self.timer_conn = self.timer.timeout.connect(self.cgdesc)
                self.timer.start(200, 1)
                self.readScripts()
                self.ecminfo = GetEcmInfo()
                (newEcmFound, ecmInfo) = self.ecminfo.getEcm()
                self["info"] = ScrollLabel("".join(ecmInfo))
                self.EcmInfoPollTimer = eTimer()
                try:
                    self.EcmInfoPollTimer.callback.append(self.setEcmInfo)
                except:
                    self.timer_conn = self.EcmInfoPollTimer.timeout.connect(self.setEcmInfo)
                self.EcmInfoPollTimer.start(100)
               

        def slpanel(self):
            if fileExists('/usr/lib/enigma2/python/Plugins/SatLodge/slPanel/plugin.pyo'):
                from Plugins.SatLodge.slPanel.plugin import logoStrt                
                self.session.openWithCallback(self.close, logoStrt)
            else: 
                self.session.open(MessageBox,("slPanel Not Installed!!"), type=MessageBox.TYPE_INFO, timeout=3)
               
               
        def setEcmInfo(self):
            (newEcmFound, ecmInfo) = self.ecminfo.getEcm()
            if newEcmFound:
                self["info"].setText("".join(ecmInfo))
            else:
                self.ecm()
       

        def ecm(self):
            ecmf = ""
            if os.path.isfile("/tmp/ecm.info")is True :
                myfile = file(r"/tmp/ecm.info")
                ecmf = ""
                for line in myfile.readlines():
                      print line
                      ecmf = ecmf + line

                self["info"].setText(ecmf)
            else:
                self["info"].setText(ecmf)
                #return


        def cgdesc(self):
                self['desc'].setText(_('Select a cam to run ...'))

        def openTest(self):
#                self["pixmap"].instance.setPixmapFromFile("/usr/lib/enigma2/python/Plugins/SatLodge/slManager/camd.png")
                return
                
        def download(self):
                self.session.open(GetipklistLs)
                self.onShown.append(self.readScripts)
                #self.close()
        
        def getLastIndex(self):
                a = 0
                if len(self.namelist) > 0:
                        for x in self.namelist:
                                if x == self.currCam:
                                        return a
                                else:
                                        a+=1
                else:
                        return -1
                return -1

        def action(self):
                self.session.nav.playService(None)
                last = self.getLastIndex()
                var = self["list"].getSelectionIndex()
                if last > -1:
                        if last == var:
                                self.cmd1 = "/usr/camscript/" + self.softcamslist[var][0]+'.sh' + " cam_res &"
                                os.system(self.cmd1)
                                os.system("sleep 1")
                        else:
                                self.cmd1 = "/usr/camscript/" + self.softcamslist[last][0]+'.sh' + " cam_down &"
                                os.system(self.cmd1)
                                os.system("sleep 1")
                                self.cmd1 = "/usr/camscript/" + self.softcamslist[var][0]+'.sh' + " cam_up &"
                                os.system(self.cmd1)
                else:
                        try:
                                self.cmd1 = "/usr/camscript/" + self.softcamslist[var][0]+'.sh' + " cam_up &"
                                os.system(self.cmd1)
                                os.system("sleep 1")
                        except:
                                self.close()

                if last != var:
                        try:
                                self.currCam = self.softcamslist[var][0]
                                self.writeFile()
                        except:
                                self.close()
                self.readScripts()
                self.session.nav.playService(self.oldService)
                ##self.close()



        def writeFile(self):
                if not self.currCam is None:
                        clist = open("/etc/clist.list", "w")
                        clist.write(self.currCam)
                        clist.close()
                        
                stcam = open("/etc/startcam.sh", "w")
                stcam.write("#!/bin/sh\n" + self.cmd1)
                stcam.close()
                self.cmd2 = "chmod 755 /etc/startcam.sh &"
                os.system(self.cmd2)




        def stop(self):
                self.session.nav.playService(None)
                last = self.getLastIndex()


                if last > -1:
                        self.cmd1 = "/usr/camscript/" + self.softcamslist[last][0]+'.sh' + " cam_down &"
                        os.system(self.cmd1)
                else:
                        return
                
                self.currCam = "no"
                self.writeFile()
                os.system("sleep 1")
                self.readScripts()
                self["info"].setText(" ")
                self.session.nav.playService(self.oldService)



        def readScripts(self):
                self.index = 0
                self.indexto = ''
                scriptlist = []
                pliste = []
                path = "/usr/camscript/"
                for root, dirs, files in os.walk(path):
                        for name in files:
                                scriptlist.append(name)
                self.emulist = scriptlist
                i = len(self.softcamslist)
                del self.softcamslist[0:i]
                for lines in scriptlist:
                        dat = path + lines 
                        sfile = open(dat, "r")
                        for line in sfile:
                            if line[0:3] == 'OSD':
                                nam = line[5:len(line) - 2]
                                print 'We are in slManager readScripts 2 nam = ', nam
                                if self.currCam is not None:
                                    if nam == self.currCam:
                                        self.softcamslist.append(show_list(nam))
                                    else:
                                        self.softcamslist.append(show_list(nam))
                                        self.index += 1
                                else:
                                    self.softcamslist.append(show_list(nam))



                                    self.index += 1
                                pliste.append(nam)
                        sfile.close()
                        # self['list'].setList(self.softcamslist)
                        self['list'].l.setList(self.softcamslist)
                        # if HD.width() == 1280:                        
                        # # if sz_w == 1280:
                            # self['list'].l.setItemHeight(40)
                        # else:
                            # self['list'].l.setItemHeight(50)
                        self.namelist = pliste
                return

        def readCurrent(self):
                currCam = ''
                FilCurr = ''
                if fileExists("/etc/CurrentBhCamName"):
                    FilCurr = "/etc/CurrentBhCamName"
                else:FilCurr = "/etc/clist.list"
                try:
                    clist = open(FilCurr, "r")
                except:
                    return None
                if not clist is None:
                    for line in clist:
                        currCam = line#.replace('"','').replace('\t','').replace('\n','').replace('\r','').replace(' ','')
                    clist.close()
                return currCam


        def autocam(self):
                current = None
                try:
                        clist = open("/etc/clist.list", "r")
                        print 'found list'
                except:
                        return None
                
                if not clist is None:
                        for line in clist:
                                current = line
                        clist.close()
                
                print "current =", current
                
                if os.path.isfile("/etc/autocam.txt")is False :
                        alist = open("/etc/autocam.txt", "w")
                        alist.close()
                self.autoclean()
                alist = open("/etc/autocam.txt", "a")
                alist.write(self.oldService.toString() + "\n")
                last = self.getLastIndex()
                alist.write(current + "\n")
                alist.close()
                self.session.openWithCallback(self.callback, MessageBox, _("Autocam assigned to the current channel"), type = 1, timeout = 10)

        def autoclean(self):
                delemu = "no"
                if os.path.isfile("/etc/autocam.txt")is False :
                       return
                myfile = open("/etc/autocam.txt", "r")
                myfile2 = open("/etc/autocam2.txt", "w")
                icount = 0
                for line in myfile.readlines():
                       print "We are in slManager line, self.oldService.toString() =", line, self.oldService.toString()
                       if line[:-1] == self.oldService.toString():
                               delemu = "yes"
                               icount = icount+1
                               continue
                       if delemu == "yes":
                               delemu = "no"
                               icount = icount+1
                               continue        
                               
                       myfile2.write(line)
                       icount = icount+1

                myfile.close() 
                myfile2.close() 
                os.system("rm /etc/autocam.txt")
                os.system("cp /etc/autocam2.txt /etc/autocam.txt")


###################################                
class GetipklistLs(Screen):

    instance = None
    
    # if DESKHEIGHT < 1280:		
    skin = skin_path + 'GetipklistLs.xml'
    # else:	
        # skin = skin_path + 'GetipklistLsFHD.xml'
    f = open(skin, 'r')
    skin = f.read()
    f.close()    

    
    def __init__(self, session):
    
        assert not GetipklistLs.instance, "only one GetipklistLs instance is allowed!"
        GetipklistLs.instance = self
        self.skin = GetipklistLs.skin

        Screen.__init__(self, session)

        self.setTitle(_('Sat-Lodge Manager by lululla V. %s' % Version))         
        self.session = session
        


    # def __init__(self, session):
        # Screen.__init__(self, session)
        # # self.list = []
        self.names = []
        self.names_1 = []
        self.list = []		
        self['text'] = m2list([])
        # self['text'] = webList([])
        self['maintener'] = Label(_(' by ))^^(('))         
        self['info'] = Label(_('Getting the list, please wait ...'))
        self['version'] = Label(_('V. %s' % Version)) 
        self['team'] = Label(_('..:: Sat-Lodge Manager ::..'))    
        self.addon = 'emu'
        self.icount = 0
        self.downloading = False
        self.timer = eTimer()
        try:
            self.timer.callback.append(self.downloadxmlpage)
        except:
            self.timer_conn = self.timer.timeout.connect(self.downloadxmlpage)
        self.timer.start(100, 1)
        self['actions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.okClicked,
        'cancel': self.close}, -1)
        # self.onShown.append(self.get_list)


    # def get_list(self):
        # self.timer = eTimer()
        # try:
            # self.timer.callback.append(self.downloadxmlpage)

        # except:
            # self.timer_conn = self.timer.timeout.connect(self.downloadxmlpage)
    def downloadxmlpage(self):
        url = 'http://sat-lodge.it/xml/PluginEmulators.xml'    

        getPage(url).addCallback(self._gotPageLoad).addErrback(self.errorLoad)

    def errorLoad(self, error):
        print str(error)

        self['info'].setText(_('Try again later ...'))

        self.downloading = False

    def _gotPageLoad(self, data):
        self.xml = data
        try:
            if self.xml:
                xmlstr = minidom.parseString(self.xml)
            else:
                self.downloading = False
                return
            self.data = []
            self.names = []
            icount = 0
            list = []
            xmlparse = xmlstr
            self.xmlparse = xmlstr
            for plugins in xmlstr.getElementsByTagName('plugins'):
                self.names.append(plugins.getAttribute('cont').encode('utf8'))
            self['info'].setText(_('PLEASE SELECT...'))
            # self.list = list
            # self['text'].l.setList(self.names)
            showlist(self.names, self['text'])
            self.downloading = True
        except:
            self.downloading = False

    def okClicked(self):
        inx = self['text'].getSelectionIndex()
        if self.downloading == True:
            try:
                # selection = str(self['text'].getCurrent())
                selection = self.names[inx]
                self.session.open(GetipkLs, self.xmlparse, selection)
            except:
                return

        else:
            return        




class GetipkLs(Screen):

    instance = None
    
    # if DESKHEIGHT < 1280:		
    skin = skin_path + 'GetipkLs.xml'
    # else:	
        # skin = skin_path + 'GetipkLsFHD.xml'
    f = open(skin, 'r')
    skin = f.read()
    f.close()    
    
    def __init__(self, session, xmlparse, selection):
    
        assert not GetipkLs.instance, "only one GetipkLs instance is allowed!"
        GetipkLs.instance = self
        self.skin = GetipkLs.skin

        Screen.__init__(self, session)
        self.setTitle(_('Sat-Lodge Manager by lululla V. %s' % Version))         
        self.session = session
                
    # def __init__(self, session, xmlparse, selection):
        # Screen.__init__(self, session)
        self.xmlparse = xmlparse
        self.selection = selection
        self['text'] = m2list([])        
        # self['text'] = webList([])
        self.list = []
        for plugins in self.xmlparse.getElementsByTagName('plugins'):
            if str(plugins.getAttribute('cont').encode('utf8')) == self.selection:
                for plugin in plugins.getElementsByTagName('plugin'):
                    self.list.append(plugin.getAttribute('name').encode('utf8'))

        showlist(self.list, self['text'])
        self['maintener'] = Label(_(' by ))^^(('))   
        self['version'] = Label(_('V. %s' % Version))  
        self['team'] = Label(_('..:: Sat-Lodge Manager ::..'))           
        self['info'] = Label(_('PLEASE SELECT...'))
        self['actions'] = ActionMap(['SetupActions'], {'ok': self.message,
         'cancel': self.close}, -1)


    def selclicked(self, result):
        inx = self['text'].getSelectionIndex()
        try:
            selection_country = self.list[inx]
        except:
            return

        if result:
            for plugins in self.xmlparse.getElementsByTagName('plugins'):
                if str(plugins.getAttribute('cont').encode('utf8')) == self.selection:
                    for plugin in plugins.getElementsByTagName('plugin'):
                        if plugin.getAttribute('name').encode('utf8') == selection_country:
                            urlserver = str(plugin.getElementsByTagName('url')[0].childNodes[0].data)
                            pluginname = plugin.getAttribute('name').encode('utf8')
                            self.prombt(urlserver, pluginname)

        else:
            return 

    def message(self):
        self.session.openWithCallback(self.selclicked,MessageBox,_("Do you want to install?"), MessageBox.TYPE_YESNO)  
        
    def prombt(self, com, dom):
        self.com = com
        self.dom = dom
        if self.selection == '':
            self.session.openWithCallback(self.callMyMsg, MessageBox, _('Installare...'), MessageBox.TYPE_YESNO)
        else:
            self.session.open(Console, _('Installing: %s') % dom, ['opkg install -force-overwrite %s' % com])

    def callMyMsg(self, result):
        if result:
            dom = self.dom
            com = self.com
            self.session.open(Console, _('Installing: %s') % dom, ['ipkg install -force-overwrite %s' % com])























def startConfig(session, **kwargs):
        session.open(slManager)


def mainmenu(menuid):
        if menuid != "setup":
                return [ ]
        return [(_("SatLodge Manager"), startConfig, "softcam", None)]
        
def autostart(reason, session=None, **kwargs):
    "called with reason=1 to during shutdown, with reason=0 at startup?"
    print "[Softcam] Started"
    if reason == 0:
        try:
	        os.system("mv /usr/bin/dccamd /usr/bin/dccamdOrig &")
	        os.system("ln -sf /usr/bin /var/bin")
	        os.system("ln -sf /usr/keys /var/keys")
	        os.system("ln -sf /usr/scce /var/scce")
	        os.system("ln -sf /usr/camscript /var/camscript")
	        os.system("sleep 1")
	        os.system("/etc/startcam.sh &")

        except:
	        pass	
    else:
        pass              







def main(session, **kwargs):
			session.open(slManager)

def StartSetup(menuid):
	if menuid == 'mainmenu':

		return [('SatLodge Manager',

		         main,

		         'Softcam Manager',
		         44)]
	else:
		return []
        

def Plugins(**kwargs):
	 return [
         PluginDescriptor(
            name=_("SatLodge Manager"), 
            where = PluginDescriptor.WHERE_MENU, fnc=mainmenu),
         PluginDescriptor(
            name=_("SatLodge Manager"),
            description = "Softcam",
            where = [
                PluginDescriptor.WHERE_AUTOSTART,
            ],
            fnc = autostart,
        ), 
	PluginDescriptor(
		name=_("SatLodge Manager"),
		description=_("Softcam"), 
		where = PluginDescriptor.WHERE_EXTENSIONSMENU,
		fnc=main),]
        
def readCurrent_1():
                currCam = ''
                FilCurr = ''
                if fileExists("/etc/CurrentBhCamName"):
                    FilCurr = "/etc/CurrentBhCamName"
                else:FilCurr = "/etc/clist.list"
                try:
                    clist = open(FilCurr, "r")
                except:
                    return None
                if not clist is None:
                    for line in clist:
                        currCam = line
                    clist.close()
                return currCam		
