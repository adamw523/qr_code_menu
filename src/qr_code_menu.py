import random

from AppKit import *
from Foundation import *

#import QrCodeMaker
#import QrCodeMenuApp
from qr_code_menu import *
class QrCodeMenu(NSMenu):
    def draw(self, delegate):
        # About
        aboutItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('About QR Code Menu', 'about:', '')
        aboutItem.setTarget_(delegate)
        self.addItem_(aboutItem)

        self.addItem_(NSMenuItem.separatorItem())  

        # QR Code Image
        self.qrCodeItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('', '', '')
        self.qrCodeItem.setTarget_(delegate)
        self.setLoading()
        self.addItem_(self.qrCodeItem)
        self.addItem_(NSMenuItem.separatorItem())  

        # Customize
        customizeItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Contents...', 'changeValue:', '')
        customizeItem.setTarget_(delegate)
        self.addItem_(customizeItem)

        # Save Image
        saveItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Save Image...', 'saveImage:', '')
        saveItem.setTarget_(delegate)
        self.addItem_(saveItem)

        self.addItem_(NSMenuItem.separatorItem())

        # Quit
        quitItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit QR Code Menu', 'terminate:', '')
        self.addItem_(quitItem)

        # track menu activation
        nc = NSNotificationCenter.defaultCenter()
        nc.addObserver_selector_name_object_(delegate, 'menuActivated:', NSMenuDidBeginTrackingNotification, self)

    def setQrImage(self, image):
        self.qrCodeItem.setImage_(image)
        self.qrCodeItem.setTitle_("")

    def setLoading(self):
        self.qrCodeItem.setTitle_("Loading...")

