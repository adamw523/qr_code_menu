from AppKit import *
from Foundation import *

from about_controller import *
from qr_code_menu import *
from qr_code_maker import *

class QrCodeMenuApp(NSObject):
    def init(self):
        self.aboutController = None
        return self

    @objc.IBAction
    def about_(self, sender):
        if not self.aboutController:
            self.aboutController = AboutController()
            print 'vc', self.aboutController, 'owner', self.aboutController.owner(), 'window', self.aboutController.window()
        
            # we want to get windows actions / menu selections
            self.aboutController.window().setDelegate_(self)
            self.aboutController.showWindow_(self.aboutController)
            NSApp.activateIgnoringOtherApps_(True)

    def validateUserInterfaceItem_(self, item):
        # keep menu items enabled even when windows are in focus
        return True

    @objc.IBAction
    def changeValue_(self, sender):
        print self.aboutController


    @objc.IBAction
    def menuActivated_(self, notification):
        # self.performSelectorInBackground_withObject_('updateImageInMenu:', None)
        pass

    @objc.IBAction
    def watchPasteboard_(self, notification):
        newPbstring = self.pb.stringForType_(NSStringPboardType)
        if newPbstring != self.pbstring:
            self.pbstring = newPbstring
            self.menu.setLoading()

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

