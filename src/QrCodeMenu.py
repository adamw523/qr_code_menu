import objc
import Cocoa
import qrcode
import qrcode.image.pure
import StringIO

from Foundation import *
from AppKit import *

from PyObjCTools import AppHelper

class QrCodeMenu(NSMenu):
    def draw(self, delegate):
        # About
        aboutItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('About QR Code Menu', 'about:', '')
        self.addItem_(aboutItem)

        self.addItem_(NSMenuItem.separatorItem())  

        # QR Code Image
        self.qrCodeItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('', '', '')
        self.addItem_(self.qrCodeItem)

        # Customize
        customizeItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Change...', 'change:', '')
        self.addItem_(customizeItem)

        # Save Image
        saveItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Save Image...', 'saveImage:', '')
        self.addItem_(saveItem)

        self.addItem_(NSMenuItem.separatorItem())

        # Quit
        quitItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit QR Code Menu', 'terminate:', '')
        self.addItem_(quitItem)

        nc = NSNotificationCenter.defaultCenter()
        nc.addObserver_selector_name_object_(delegate, 'menuActivated:', NSMenuDidBeginTrackingNotification, self)

    def setImage(self, image):
        self.qrCodeItem.setImage_(image)

class QrCodeMaker():
    def getForText(self, text):

        # create the image
        qr = qrcode.QRCode(image_factory=qrcode.image.pure.PymagingImage, 
            version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, 
            box_size=3, 
            border=0)
        qr.add_data('NSBitmapImageRep 0x7faaeba5d180 Size={276, 276} ColorSpace=(not yet loaded) BPS=8 BPP=(not yet loaded) Pixels=276x276 Alpha=YES Planar=NO Format=(not yet loaded) CurrentBacking=nil (faulting) CGImageSource=0x7faaeb')
        qr.make(fit=True)
        img = qr.make_image()

        # output Stream
        output = StringIO.StringIO()
        img.save_stream(output)
        image = NSImage.alloc().initWithData_(NSData.dataWithData_(buffer(output.getvalue())))
        output.close()

        return image

class QrCodeMenuApp(NSObject):
    @objc.IBAction
    def about_(self, sender):
        print "About stuff", sender

    @objc.IBAction
    def menuActivated_(self, notification):
        maker = QrCodeMaker()
        i = maker.getForText("testing this thing")

        self.menu.setImage(i)

    def applicationDidFinishLaunching_(self, notification):
    	self.icon = NSImage.alloc().initByReferencingFile_('images/status_bar_icon.png')
        self.chart = NSImage.alloc().initByReferencingFile_('images/chart_150.png')
    	#self.icon.lockFocus()

        # init and draw menu
        self.menu = QrCodeMenu.alloc().init()
        self.menu.draw(self)

        # get a statusbar item
        statusbar = NSStatusBar.systemStatusBar()
        # Create the statusbar item
    	self.statusItem = statusbar.statusItemWithLength_(NSVariableStatusItemLength)
    	self.statusItem.setImage_(self.icon)
    	self.statusItem.setToolTip_('QR Code')
    	self.statusItem.setHighlightMode_(True)

        self.statusItem.setMenu_(self.menu)

    def applicationWillTerminate_(self, aNotification):
        pass


if __name__ == "__main__":
    app = NSApplication.sharedApplication()
    delegate = QrCodeMenuApp.alloc().init()
    app.setDelegate_(delegate)
    AppHelper.runEventLoop()
