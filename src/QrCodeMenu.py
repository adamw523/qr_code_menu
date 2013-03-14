import objc
import Cocoa
import qrcode
import qrcode.image.pure
import random
import StringIO

from AppKit import *
from Foundation import *
from multiprocessing import Process
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

        # track menu activation
        nc = NSNotificationCenter.defaultCenter()
        nc.addObserver_selector_name_object_(delegate, 'menuActivated:', NSMenuDidBeginTrackingNotification, self)

        self.chart = NSImage.alloc().initByReferencingFile_('images/chart_150.png')
        self.qrCodeItem.setImage_(self.chart)

    def setQrImage(self, image):
        self.qrCodeItem.setImage_(image)
        

class QrCodeMaker():
    def imageFromText(self, text):
        # create the image
        qr = qrcode.QRCode(image_factory=qrcode.image.pure.PymagingImage, 
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L, 
            box_size=4, 
            border=0)
        qr.add_data(text)
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
        # self.performSelectorInBackground_withObject_('updateImageInMenu:', None)
        pass

    @objc.IBAction
    def watchPasteboard_(self, notification):
        newPbstring = self.pb.stringForType_(NSStringPboardType)
        if newPbstring != self.pbstring:
            self.pbstring = newPbstring

            #TODO: need to figure out unicode
            #TODO: limit the size of the clipboard

            maker = QrCodeMaker()
            i = maker.imageFromText(repr(self.pbstring.encode("utf-8")))
            self.menu.setQrImage(i)
            # print u"New pastboard string: %s".encode("utf-8") % repr(self.pbstring)

        pass

    def applicationDidFinishLaunching_(self, notification):
        # init clipboard
        self.pb = NSPasteboard.generalPasteboard()
        self.pbstring = ""

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

        
        timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            1,
            self,
            'watchPasteboard:',
            None,
            True)
        NSRunLoop.currentRunLoop().addTimer_forMode_(timer, NSRunLoopCommonModes)

    def applicationWillTerminate_(self, aNotification):
        pass


if __name__ == "__main__":
    app = NSApplication.sharedApplication()
    delegate = QrCodeMenuApp.alloc().init()
    app.setDelegate_(delegate)
    AppHelper.runEventLoop()
