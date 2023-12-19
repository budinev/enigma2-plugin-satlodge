import os
from . import _
from Screens.Screen import Screen
from Components.ConfigList import ConfigListScreen
from Components.config import config, configfile, ConfigSelection, ConfigText, getConfigListEntry
from Components.Harddisk import harddiskmanager
from Components.Sources.StaticText import StaticText

class EPGCacheSetupScreen(Screen, ConfigListScreen):
	instance = None

	skin = """
	<screen position="c-300,c-250" size="600,500" title="EPG Cache setup">
		<widget name="config" position="25,25" size="550,350" />
		<widget source="epgcachelocation" render="Label" position="25,405" size="550,30" zPosition="10" font="Regular;21" halign="left" valign="center" />
		<ePixmap pixmap="skin_default/buttons/red.png" position="20,e-45" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/green.png" position="160,e-45" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/yellow.png" position="300,e-45" size="140,40" alphatest="on" />
		<ePixmap pixmap="skin_default/buttons/blue.png" position="440,e-45" size="140,40" alphatest="on" />
		<widget source="key_red" render="Label" position="20,e-45" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
		<widget source="key_green" render="Label" position="160,e-45" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
		<widget source="key_yellow" render="Label" position="300,e-45" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />
		<widget source="key_blue" render="Label" position="440,e-45" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#18188b" transparent="1" />
	</screen>"""

	def __init__(self, session):
		assert not EPGCacheSetupScreen.instance, "only one EPGCacheSetupScreen instance is allowed!"
		EPGCacheSetupScreen.instance = self
		self.skin = EPGCacheSetupScreen.skin
		Screen.__init__(self, session)

		from Components.ActionMap import ActionMap
		self.lastepgcachepath = config.misc.epgcache_filename.value
		self.updateHDDChoices()

		self["key_red"] = StaticText(_("Cancel"))
		self["key_green"] = StaticText(_("OK"))
		self["key_yellow"] = StaticText()
		self["key_blue"] = StaticText()
		self["epgcachelocation"] = StaticText()

		self["actions"] = ActionMap(["SetupActions", "ColorActions", "MenuActions"],
		{
			"ok": self.keyGo,
			"save": self.keyGo,
			"cancel": self.keyCancel,
			"green": self.keyGo,
			"red": self.keyCancel,
			"menu": self.closeRecursive,
		}, -2)

		self.list = []
		ConfigListScreen.__init__(self, self.list, session = self.session)

		self.list.append(getConfigListEntry(_("EPG Cache Path"), config.misc.epgcachepath))
		self.list.append(getConfigListEntry(_("EPG Cache Filename"), config.misc.epgcachefilename))
		self["config"].list = self.list
		self["config"].l.setList(self.list)

		self.updateDestination()

	def keyLeft(self):
		ConfigListScreen.keyLeft(self)

	def keyRight(self):
		ConfigListScreen.keyRight(self)

	def keyGo(self):
		for x in self["config"].list:
			x[1].save()
		self.updateEpgCache()
		if self.lastepgcachepath != config.misc.epgcache_filename.value:
			if os.path.exists(self.lastepgcachepath):
				os.remove(self.lastepgcachepath)
		self.close()

	def keyCancel(self):
		for x in self["config"].list:
			x[1].cancel()
		self.close()

	def updateHDDChoices(self):
		hddchoises = [("/etc/enigma2/", "Internal Flash")]
		for p in harddiskmanager.getMountedPartitions():
			d = os.path.normpath(p.mountpoint)
			if os.path.exists(p.mountpoint):
				if p.mountpoint != "/":
					hddchoises.append((d + "/", p.mountpoint))

		config.misc.epgcachepath = ConfigSelection(default = "/etc/enigma2/", choices = hddchoises)
		config.misc.epgcachefilename = ConfigText(default="epg", fixed_size=False)

	def updateDestination(self):
		epgcachelocationlabel = _("EPG Cachefile on:") + " " + config.misc.epgcache_filename.value
		self["epgcachelocation"].setText(epgcachelocationlabel)

	def updateEpgCache(self):
		config.misc.epgcache_filename.setValue(os.path.join(config.misc.epgcachepath.value, config.misc.epgcachefilename.value.replace(".dat","") + ".dat"))
		config.misc.epgcache_filename.save()
		configfile.save()
		from enigma import eEPGCache
		eEPGCache.getInstance().setCacheFile(config.misc.epgcache_filename.value)
		eEPGCache.getInstance().save()

def main(session, **kwargs):
	session.open(EPGCacheSetupScreen)

def Plugins(**kwargs):
	from Plugins.Plugin import PluginDescriptor
	# return [PluginDescriptor(name = "EPG Cache setup", description = _("Adjust your EPG Cache settings"), where = PluginDescriptor.WHERE_PLUGINMENU, fnc = main)]
	return [PluginDescriptor(name = "EPG Cache setup", description = _("Adjust your EPG Cache settings"), where = PluginDescriptor.WHERE_MENU, fnc = mainmenu)]    
    
    
def mainmenu(menuid):
    # if menuid != "setup":
    if menuid != "system":
            return [ ]
    return [(_("EPG Cache setup"), startConfig, "Adjust your EPG Cache settings", None)]   

def startConfig(session, **kwargs):
        session.open(EPGCacheSetupScreen)    
