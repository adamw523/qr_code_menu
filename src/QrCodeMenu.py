import objc
import Cocoa

from Foundation import *
from AppKit import *

from PyObjCTools import AppHelper

class QrCodeMenu (NSObject):

    @objc.IBAction
    def about_(self, sender):
        print "About stuff", sender

    def openLeftWindow_(self,sender):
        print "openLeftWindow_"

    def openWin_(self, sender):
        print "openWindow_"

    def applicationDidFinishLaunching_(self, notification):
    	self.icon = NSImage.alloc().initByReferencingFile_('images/status_bar_icon.png')
        self.chart = NSImage.alloc().initByReferencingFile_('images/chart_150.png')
    	#self.icon.lockFocus()

        statusbar = NSStatusBar.systemStatusBar()
        # Create the statusbar item
    	self.statusItem = statusbar.statusItemWithLength_(NSVariableStatusItemLength)
    	self.statusItem.setImage_(self.icon)
    	# self.statusItem.setTitle_('QR Code')
    	self.statusItem.setToolTip_('QR Code')
    	self.statusItem.setHighlightMode_(True)

    	# self.statusItem.setTarget_(some_target) # for opening a window / view
    	self.menu = NSMenu.alloc().init()

        # About
        aboutItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('About QR Code Menu', 'about:', '')
        self.menu.addItem_(aboutItem)

        self.menu.addItem_(NSMenuItem.separatorItem())

        # QR Code Image
        qrCodeItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('', '', '')
        qrCodeItem.setImage_(self.chart)
        self.menu.addItem_(qrCodeItem)

        # Customize
        customizeItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Change...', 'about:', '')
        self.menu.addItem_(customizeItem)

        # Save Image
        saveItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Save Image...', 'about:', '')
        self.menu.addItem_(saveItem)

        self.menu.addItem_(NSMenuItem.separatorItem())

        # Quit
    	quitItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit QR Code Menu', 'terminate:', '')
    	self.menu.addItem_(quitItem)

        # self.popUpStatusItemMenu_(self.menu)
    	self.statusItem.setMenu_(self.menu)
        # self.statusItem.setAction_(self.menu)

    def applicationWillTerminate_(self, aNotification):
        pass

if __name__ == "__main__":
    app = NSApplication.sharedApplication()
    delegate = QrCodeMenu.alloc().init()
    app.setDelegate_(delegate)
    AppHelper.runEventLoop()
