from Components.AVSwitch import AVSwitch
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.Pixmap import Pixmap
from Components.ProgressBar import ProgressBar
from Components.ScrollLabel import ScrollLabel
from Components.ServiceEventTracker import ServiceEventTracker
from Components.Sources.List import List
from Components.Task import Task, Job, job_manager, Condition
from Components.config import config, ConfigSelection, ConfigSubsection, ConfigText, ConfigYesNo, getConfigListEntry, ConfigPassword
from Tools import Notifications, ASCIItranslit
from Plugins.Plugin import PluginDescriptor
from Screens.ChoiceBox import ChoiceBox
from Screens.InfoBarGenerics import InfoBarNotifications, InfoBarSeek
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Tools.BoundFunction import boundFunction
from Tools.Directories import resolveFilename, SCOPE_HDD, SCOPE_CURRENT_PLUGIN
from Tools.Downloader import downloadWithProgress
from enigma import eConsoleAppContainer, getDesktop
from enigma import eTimer, ePoint, RT_HALIGN_LEFT, RT_VALIGN_CENTER, gFont, ePicLoad, eServiceReference, iPlayableService
from os import path as os_path, remove as os_remove, system as os_system
import os
from twisted.web import client
from Screens.Screen import Screen
from Screens.LocationBox import MovieLocationBox
from Components.config import config, ConfigText, getConfigListEntry
from Components.config import KEY_DELETE, KEY_BACKSPACE, KEY_ASCII, KEY_TIMEOUT
from Components.ConfigList import ConfigListScreen
from Components.ActionMap import ActionMap
from Components.Button import Button
from Components.Label import Label
from Components.Sources.List import List
from Components.MultiContent import MultiContentEntryText
from Components.Task import job_manager
from Components.Sources.StaticText import StaticText
from Tools.Directories import resolveFilename, SCOPE_HDD
from threading import Thread
from xml.etree.cElementTree import fromstring as cet_fromstring
from StringIO import StringIO
from urllib import FancyURLopener
total = 0
dlocation = config.plugins.ImageDown.Downloadlocation.value
if not dlocation.endswith("/"):
   dlocation=dlocation+"/"

DESKHEIGHT = getDesktop(0).size().height()
dwidth = getDesktop(0).size().width()


from plugin import currversion

plugin_path = '/usr/lib/enigma2/python/Plugins/SatLodge/slPanel'
skin_path = plugin_path
HD = getDesktop(0).size()
if HD.width() > 1280:
   skin_path = plugin_path + '/res/skins/fhd/'

else:
   skin_path = plugin_path + '/res/skins/hd/'
   
class skins(Screen):
    instance = None
    skin = skin_path + 'all.xml'  
    f = open(skin, 'r')
    skin = f.read()
    f.close() 
    
###################   
def freespace():
         downloadlocation=dlocation
         try:  
            diskSpace = os.statvfs(downloadlocation)
            capacity = float(diskSpace.f_bsize * diskSpace.f_blocks)
            available = float(diskSpace.f_bsize * diskSpace.f_bavail)           
            fspace=round(float((available) / (1024.0*1024.0)),2)        
	    tspace=round(float((capacity) / (1024.0 * 1024.0)),1)
            spacestr='Free space(' +str(fspace)+'MB) Total space(' + str(tspace)+'MB)'
            return spacestr
         except:
            return ' '   

def stopdownload():
    cmd1 = 'killall -9 rtmpdump'
    cmd2 = 'killall -9 wget'
    os.system(cmd1)
    os.system(cmd2)
    self.close()

def getsize(site):
        import urllib,os
        try:
           if os.path.exists("/tmp/filesize"):
            os.remove("/tmp/filesize")
           site = urllib.urlopen(site)
           meta = site.info()
           size= meta.getheaders("Content-Length")[0]                           
           afile=open("/tmp/filesize","w")
           afile.write(str(size))
           afile.close()
           return size
        except:
           pass
							
def getdownloadrtmp(url, filename):
    try:
        parts = []
        url = url.strip()
        parts = url.split(' ')
        if len(parts) < 1:
            link = "'" + url + "'"
            commandstr = 'rtmpdump -r ' + link + ' -o ' + filename
            return commandstr
        link = "'" + parts[0] + "'"
        print link
        playpath = ''
        swfUrl = ''
        pageUrl = ''
        live = ''
        for item in parts:
            if 'playpath' in item:
                parts2 = item.split('=')
                playpath = " --playpath='" + parts2[1] + "'"
            if 'swfUrl' in item:
                parts2 = item.split('=')
                swfUrl = " --swfUrl='" + parts2[1] + "'"
            if 'live' in item:
                parts2 = item.split('=')
                live = " --live='" + parts2[1] + "'"
            if 'pageUrl' in item:
                parts2 = item.split('=')
                pageUrl = " --pageUrl='" + parts2[1] + "'"
            commandstr = 'rtmpdump -r ' + link + playpath + swfUrl + pageUrl + ' -o ' + filename

        return commandstr
    except:
        link = "'" + url + "'"
        print 'error'
        commandstr = 'rtmpdump -r ' + link + ' -o ' + filename
        return commandstr

class downloadJobrtmp(Job):

    def __init__(self, cmdline, filename, filetitle):
        Job.__init__(self, 'Download: %s' % filetitle)
        self.filename = filename
        self.retrycount = 0
        print '63', filename
        downloadTaskrtmp(self, cmdline, filename)

    def retry(self):
        self.retrycount += 1
        self.restart()

    def cancel(self):
        stopdownload()
        self.abort()

class downloadTaskrtmp(Task):
    ERROR_CORRUPT_FILE, ERROR_RTMP_ReadPacket, ERROR_SEGFAULT, ERROR_SERVER, ERROR_UNKNOWN = range(5)

    def __init__(self, job, cmdline, filename):
        Task.__init__(self, job, _('Downloading ...'))
        self.postconditions.append(downloadTaskPostcondition())
        self.setCmdline(cmdline)
        self.filename = filename
        self.error = None
        self.lasterrormsg = None
        self.end = 300
        return

    def processOutput(self, data):
        if os.path.exists(self.filename):
            filesize = os.path.getsize(self.filename)
            currd = round(float(filesize / 1048576.0), 2)
            totald = 600
            recvbytes = filesize
            totalbytes = 629145600
            self.progress = int(currd)
        try:
            if data.endswith('%)'):
                startpos = data.rfind('sec (') + 5
                if startpos and startpos != -1:
                    self.progress = int(float(data[startpos:-4]))
            elif data.find('%') != -1:
                tmpvalue = data[:data.find('%')]
                tmpvalue = tmpvalue[tmpvalue.rfind(' '):].strip()
                tmpvalue = tmpvalue[tmpvalue.rfind('(') + 1:].strip()
                print '105', tmpvalue
            else:
                Task.processOutput(self, data)
        except Exception as errormsg:
            print 'Error processOutput: ' + str(errormsg)
            Task.processOutput(self, data)

    def processOutputLine(self, line):
        line = line[:-1]
        self.lasterrormsg = line
        if line.startswith('ERROR:'):
            if line.find('RTMP_ReadPacket') != -1:
                self.error = self.ERROR_RTMP_ReadPacket
                print '126', self.error
            elif line.find('corrupt file!') != -1:
                self.error = self.ERROR_CORRUPT_FILE
                os_system('rm -f %s' % self.filename)
            else:
                self.error = self.ERROR_UNKNOWN
        elif line.startswith('wget:'):
            if line.find('server returned error') != -1:
                self.error = self.ERROR_SERVER
        elif line.find('Segmentation fault') != -1:
            self.error = self.ERROR_SEGFAULT

    def afterRun(self):
       
        if self.getProgress() == 0 or self.getProgress() == 100:
            pass

class downloadTaskPostcondition(Condition):
    RECOVERABLE = True

    def check(self, task):
        return True
        if task.returncode == 0 or task.error is None:
            return True
        else:
            return False
            return

    def getErrorMessage(self, task):
        return {task.ERROR_CORRUPT_FILE: _('Video Download Failed!\n\nCorrupted Download File:\n%s' % task.lasterrormsg),
         task.ERROR_RTMP_ReadPacket: _('Video Download Failed!\n\nCould not read RTMP-Packet:\n%s' % task.lasterrormsg),
         task.ERROR_SEGFAULT: _('Video Download Failed!\n\nSegmentation fault:\n%s' % task.lasterrormsg),
         task.ERROR_SERVER: _('Video Download Failed!\n\nServer returned error:\n%s' % task.lasterrormsg),
         task.ERROR_UNKNOWN: _('Video Download Failed!\n\nUnknown Error:\n%s' % task.lasterrormsg)}[task.error]

class downloadJob(Job):

    def __init__(self, url, file, title):
        Job.__init__(self, title)
        downloadTask(self, url, file)

class downloadTask(Task):
    global total
    total = 0

    def __init__(self, job, url, file):
        Task.__init__(self, job, 'download task')
        self.end = 100
        self.url = url
        self.local = file

    def prepare(self):
        self.error = None
        return

    def run(self, callback):
        self.callback = callback
        getsize(self.url)
        self.download = downloadWithProgress(self.url, self.local)
        self.download.addProgress(self.http_progress)
        print "self.url, self.local",self.url, self.local
        self.download.start().addCallback(self.http_finished).addErrback(self.http_failed)

    def http_progress(self, recvbytes, totalbytes):
        currd = round(float(recvbytes / 1048576.0), 2)
        totald = round(float(totalbytes / 1048576.0), 1)
        info = _('%d of %d MB' % (currd, totald))
        total = totald
        self.progress = int(self.end * recvbytes / float(totalbytes))

    def http_finished(self, string = ''):
        print '[http_finished]' + str(string), self.local
        Task.processFinished(self, 0)        
        try:
            filetitle = os_path.basename(self.local)
        except:
            filetile = ''
        if not '_update.zip'  in self.local:           

            return 
        if '_plugin.' in self.local or '_update.zip' in self.local:

            return       
        if self.local.endswith(".zip") and not "-et" in self.local and "-vu" not in self.local:

            return 
    def http_failed(self, failure_instance = None, error_message = ''):
        if error_message == '' and failure_instance is not None:
            error_message = failure_instance.getErrorMessage()
            print '[http_failed] ' + error_message
            Task.processFinished(self, 1)
            try:
                filetitle = os_path.basename(self.local)
            except:
                filetile = ''
        if  '_update.zip'  in self.local:
          return 

    def afterRun(self):        
        return
        if self.getProgress() == 0 or self.getProgress() == 100:
            return 

class downloadTask(Screen):

    instance = None
    skin = skin_path + 'downloadTask.xml'  
    f = open(skin, 'r')
    skin = f.read()
    f.close()     
    
    def __init__(self, session, plugin_path, tasklist, filename = None):   
        assert not downloadTask.instance, "only one downloadTask instance is allowed!"
        downloadTask.instance = self
        self.skin = downloadTask.skin
        Screen.__init__(self, session)
        self.setTitle(_('Sat-Lodge Panel by lululla V. %s' % currversion))         
        self.session = session

				
    # def __init__(self, session, plugin_path, tasklist, filename = None):
        # self.session = session

        # skin = skin_path + 'downloadTask.xml'
        # f = open(skin, 'r')
        # self.skin = f.read()
        # f.close()
        # Screen.__init__(self, session)
        self.tasklist = tasklist
        self.filename = filename
        self['tasklist'] = List(self.tasklist)
        self['shortcuts'] = ActionMap(['ColorActions',
         'ShortcutActions',
         'WizardActions',
         'MediaPlayerActions'], {#'red': self.abort,     
         'back': self.keyCancel}, -1)
        self['title'] = Label()
        self.onLayoutFinish.append(self.layoutFinished)
        self.onClose.append(self.__onClose)      
        self.Timer = eTimer()       
        self.Timer.callback.append(self.TimerFire)
		
    def __onClose(self):
        del self.Timer

    def layoutFinished(self):
        try:size=freespace()
        except:size=''
        sizestr=dlocation+" "+size
        print "sizestr",sizestr
        self['title'].setText(_(sizestr))
        self.Timer.startLongTimer(2)

    def TimerFire(self):
        self.Timer.stop()
        self.rebuildTaskList()

    def rebuildTaskList(self):
        size=''           
        try:
            txt=open("/tmp/filesize").read()
            size=str(int(txt)/(1024*1024))+"MB"           
        except:
            size=" "        
        self.tasklist = []        
        for job in job_manager.getPendingJobs():            
            status=job.getStatustext()
            try:fsize=freespace()
            except:fsize=''
            sizestr=dlocation+" "+fsize
            self['title'].setText(_(sizestr))            
            if 'progress' in status.lower():                
                try:
                    filesize=os.path.getsize(dlocation+job.name)
                    filesize=str(int(filesize)/(1024*1024))+"MB"
                except:
                    filesize=''
                size=filesize+"/"+size    
                self.tasklist.append((job,
                 job.name,
                 status,
                 int(100 * job.progress / float(job.end)),
                 str(100 * job.progress / float(job.end)) + '%'+" "+size))
            else :
                self.tasklist.append((job,
                 job.name,
                 status,
                 int(100 * job.progress / float(job.end)),
                 str(100 * job.progress / float(job.end)) + '%'))
        self['tasklist'].setList(self.tasklist)
        self['tasklist'].updateList(self.tasklist)
        self.Timer.startLongTimer(2)

    def JobViewCB(self, why):
        print 'WHY---', why

    def keyCancel(self):
        self.close()

    def keySave(self):
        self.close()

def startdownload(session, answer = 'download', myurl = None, filename = None, title = None, plugin_path = None, show = True):
    url = myurl
    print '365', url, filename
    if answer == 'download':
        fname = filename
        svfile = filename
        svf = svfile
        try:
            if title is None:
                title = os.path.split(svfile)[1]
        except:
            pass
        if 'rtmp' not in url:
            urtmp = "wget -O '" + svfile + "' -c '" + url + "'"
            job_manager.AddJob(downloadJob(url, svfile, title))
        else:
            params = url
            print 'params A=', params
            svfile = svfile.replace(' ', '').strip()
            params = params.replace(' swfVfy=', ' --swfVfy ')
            params = params.replace(' playpath=', ' --playpath ')
            params = params.replace(' app=', ' --app ')
            params = params.replace(' pageUrl=', ' --pageUrl ')
            params = params.replace(' tcUrl=', ' --tcUrl ')
            params = params.replace(' swfUrl=', ' --swfUrl ')
            print 'params B=', params
            cmd = 'rtmpdump -r ' + params + " -o '" + svfile + "'"
            print '384cmd', cmd
            job_manager.AddJob(downloadJobrtmp(cmd, svfile, title))
        if show == True:
                tasklist = []
                size=''
                try:
                    txt=open("/tmp/filesize").read()
                    size=str(int(txt)/(1024*1024))+"MB"                   
                except:
                    size=" "                    
                for job in job_manager.getPendingJobs():                    
                    status=job.getStatustext()
                    if 'progress' in status.lower():
                         try:
                            filesize=os.path.getsize(dlocation+job.name)
                            filesize=str(int(filesize)/(1024*1024))+"MB"
                         except:
                            filesize=''
                         size=filesize+"/"+size                          
                         tasklist.append((job,
                         job.name,
                         status,
                         int(100 * job.progress / float(job.end)),
                         str(100 * job.progress / float(job.end)) + '%'+" "+size))
                    else :
                         tasklist.append((job,
                         job.name,
                         status,
                         int(100 * job.progress / float(job.end)),
                         str(100 * job.progress / float(job.end)) + '%'))
                session.open(downloadTask, plugin_path, tasklist)
    elif answer == 'view':
                tasklist = []
                size=''
                try:
                    txt=open("/tmp/filesize").read()
                    size=str(int(txt)/(1024*1024))+"MB"                   
                except:
                    size=" "                    
                for job in job_manager.getPendingJobs():                     
                    status=job.getStatustext()
                    if 'progress' in status.lower():
                         try:
                            filesize=os.path.getsize(dlocation+job.name)
                            filesize=str(int(filesize)/(1024*1024))+"MB"
                         except:
                            filesize=''
                         size=filesize+"/"+size                         
                         tasklist.append((job,
                         job.name,
                         status,
                         int(100 * job.progress / float(job.end)),
                         str(100 * job.progress / float(job.end)) + '%'+" "+size))
                    else :
                         tasklist.append((job,
                         job.name,
                         status,
                         int(100 * job.progress / float(job.end)),
                         str(100 * job.progress / float(job.end)) + '%'))
                session.open(downloadTask, plugin_path, tasklist)
                return True