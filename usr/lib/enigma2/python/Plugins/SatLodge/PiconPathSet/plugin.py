from __init__ import _
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.Sources.StaticText import StaticText
from Components.config import config, ConfigSelection, getConfigListEntry, NoSave, ConfigText, ConfigDirectory
from Components.ConfigList import ConfigListScreen
from os import path as os_path
from Components.FileList import FileList
from Components.Label import Label
from Screens.MessageBox import MessageBox
from Screens.Standby import TryQuitMainloop
import os
config.misc.picon_path = ConfigText(default='/media/usb')
if os.path.exists('%s' % config.misc.picon_path.value) is False:
    config.misc.picon_path.value = '/media/usb'
#modded lululla    

class SetPiconPath(Screen, ConfigListScreen):
    skin = '\n\t\t<screen position="center,center" size="560,320" title="PiconPathSet" >\n\t\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="0,0" zPosition="0" size="140,40" transparent="1" alphatest="on" />\n\t\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="140,0" zPosition="0" size="140,40" transparent="1" alphatest="on" />\n\t\t\t<ePixmap pixmap="skin_default/buttons/yellow.png" position="280,0" zPosition="0" size="140,40" transparent="1" alphatest="on" />\n\t\t\t<ePixmap pixmap="skin_default/buttons/blue.png" position="420,0" zPosition="0" size="140,40" transparent="1" alphatest="on" />\n\t\t\t<widget render="Label" source="key_red" position="0,0" size="140,40" zPosition="5" valign="center" halign="center" backgroundColor="red" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />\n\t\t\t<widget render="Label" source="key_green" position="140,0" size="140,40" zPosition="5" valign="center" halign="center" backgroundColor="red" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />\n\t\t\t<widget name="config" position="20,50" size="520,250" scrollbarMode="showOnDemand" />\n\t\t</screen>'

    def __init__(self, session):
        self.session = session
        Screen.__init__(self, session)
        self['key_red'] = StaticText(_('Cancel'))
        self['key_green'] = StaticText(_('Save'))
        path = config.misc.picon_path.value
        self.picon_path = NoSave(ConfigDirectory(default=path))
        list = []
        list.append(getConfigListEntry(_('Picon path'), self.picon_path))
        ConfigListScreen.__init__(self, list)
        self['setupActions'] = ActionMap(['SetupActions', 'ColorActions'], {'ok': self.keySelect,
         'green': self.save,
         'red': self.exit,
         'cancel': self.exit}, -1)

    def save(self):
        config.misc.picon_path.value = self.picon_path.value
        config.misc.picon_path.save()
        config.misc.picon_path.changed()
        restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, _('GUI needs a restart to apply the new piconpath\nDo you want to Restart the GUI now?'), MessageBox.TYPE_YESNO)
        restartbox.setTitle(_('Restart GUI now?'))

    def restartGUI(self, answer):
        if answer is True:
            self.session.open(TryQuitMainloop, 3)

    def exit(self):
        self.close()

    def keySelect(self):
        self.session.openWithCallback(self.pathSelected, piconPath, self.picon_path.value)

    def pathSelected(self, res):
        if res is not None:
            self.picon_path.value = res
        return


class piconPath(Screen):
    skin = '<screen name = "piconPath" position="center,center" size="560,320" title="Select path for Picons">\n\t\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="0,0" zPosition="0" size="140,40" transparent="1" alphatest="on" />\n\t\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="140,0" zPosition="0" size="140,40" transparent="1" alphatest="on" />\n\t\t\t<ePixmap pixmap="skin_default/buttons/yellow.png" position="280,0" zPosition="0" size="140,40" transparent="1" alphatest="on" />\n\t\t\t<ePixmap pixmap="skin_default/buttons/blue.png" position="420,0" zPosition="0" size="140,40" transparent="1" alphatest="on" />\n\t\t\t<widget name="target" position="0,60" size="540,22" valign="center" font="Regular;22" />\n\t\t\t<widget name="filelist" position="0,100" zPosition="1" size="560,220" scrollbarMode="showOnDemand"/>\n\t\t\t<widget render="Label" source="key_red" position="0,0" size="140,40" zPosition="5" valign="center" halign="center" backgroundColor="red" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />\n\t\t\t<widget render="Label" source="key_green" position="140,0" size="140,40" zPosition="5" valign="center" halign="center" backgroundColor="red" font="Regular;21" transparent="1" foregroundColor="white" shadowColor="black" shadowOffset="-1,-1" />\n\t\t</screen>'

    def __init__(self, session, initDir):
        Screen.__init__(self, session)
        inhibitDirs = ['/bin',
         '/boot',
         '/dev',
         '/etc',
         '/home',
         '/lib',
         '/proc',
         '/sbin',
         '/sys',
         '/var']
        inhibitMounts = []
        self['filelist'] = FileList(initDir, showDirectories=True, showFiles=False, inhibitMounts=inhibitMounts, inhibitDirs=inhibitDirs)
        self['target'] = Label()
        self['actions'] = ActionMap(['WizardActions',
         'DirectionActions',
         'ColorActions',
         'PiconSelectActions'], {'back': self.cancel,
         'left': self.left,
         'right': self.right,
         'up': self.up,
         'down': self.down,
         'ok': self.ok,
         'green': self.green,
         'red': self.cancel}, -1)
        self['key_red'] = StaticText(_('Cancel'))
        self['key_green'] = StaticText(_('OK'))

    def cancel(self):
        self.close(None)
        return

    def green(self):
        self.close(self['filelist'].getSelection()[0])

    def up(self):
        self['filelist'].up()
        self.updateTarget()

    def down(self):
        self['filelist'].down()
        self.updateTarget()

    def left(self):
        self['filelist'].pageUp()
        self.updateTarget()

    def right(self):
        self['filelist'].pageDown()
        self.updateTarget()

    def ok(self):
        if self['filelist'].canDescent():
            self['filelist'].descent()
            self.updateTarget()

    def updateTarget(self):
        currFolder = self['filelist'].getSelection()[0]
        if currFolder is not None:
            self['target'].setText(currFolder)
        else:
            self['target'].setText(_('Invalid Location'))
        return


def openPiconPath(session, **kwargs):
    session.open(SetPiconPath)


def startPiconPath(menuid, **kwargs):
    if menuid == 'system':
        return [(_('Picon Path'),
          openPiconPath,
          'PiconPath',
          None)]
    else:
        return []
        return None


def Plugins(**kwargs):
    return [PluginDescriptor(name='Picon Path', where=PluginDescriptor.WHERE_MENU, fnc=startPiconPath)]