from AppKit import *
from Foundation import *

from about_controller import *
from change_controller import *
from qr_code_menu import *
from qr_code_maker import *

class QrCodeMenuApp(NSObject):
    def init(self):
        self.aboutController = None
        self.changeController = None
        return self

    @objc.IBAction
    def about_(self, sender):
        if not self.aboutController:
            self.aboutController = AboutController()
        
        self.aboutController.showWindow()        

    def validateUserInterfaceItem_(self, item):
        # keep menu items enabled even when windows are in focus
        return True

    @objc.IBAction
    def changeValue_(self, sender):
        currentPasteBaord = self.pb.stringForType_(NSStringPboardType)
        
        if not self.changeController:
            self.changeController = ChangeController(currentPasteBaord)

        self.changeController.setText(currentPasteBaord)
        self.changeController.showWindow()

    @objc.IBAction
    def clearPasteboard_(self, sender):
        pb = NSPasteboard.generalPasteboard()
        pb.declareTypes_owner_(NSArray.arrayWithObject_(NSStringPboardType), pb);
        pb.setString_forType_("", NSStringPboardType)

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

            if self.pbstring == "":
                self.menu.setEmpty()
                self.menu.setContentsText("Clipboard is Empty")
            else:
                # update image
                maker = QrCodeMaker()
                i = maker.imageFromText(repr(self.pbstring.encode("utf-8")))

                self.menu.setQrImage(i)

                # update menu text
                menuText = self.pbstring[:20]
                if len(self.pbstring) > 20: menuText += "..."
                self.menu.setContentsText(menuText)

                # update change controller if exists
                if self.changeController:
                    self.changeController.setText(self.pbstring)

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

