from AppKit import *
from Foundation import *

from qr_code_menu import *
from qr_code_maker import *

class QrCodeMenuApp(NSObject):
    @objc.IBAction
    def about_(self, sender):
        self.icon_128 = NSImage.alloc().initByReferencingFile_('images/icon_128.png')


        print 'mainbundle', NSBundle.mainBundle()

        self.vc = NSWindowController.alloc().initWithWindowNibName_("nibs/About")
        print 'vc', self.vc
        self.vc.showWindow_(self.vc)

    
        NSApp.activateIgnoringOtherApps_(True)

        return

        print "About stuff", sender

        graphicsRect = NSMakeRect(300.0, 550.0, 300.0, 457.0)
        #Make window
        self.aboutWindow = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            graphicsRect,
            NSTitledWindowMask |
            NSClosableWindowMask |
            NSResizableWindowMask,
            NSBackingStoreBuffered, False)
        
        self.aboutWindow.center()

        # Set handler for window
        self.aboutWindow.setTitle_("About QR Code Menu")
        #myDelegate = WindowDelegate.alloc( ).init( )
        #myWindow.setDelegate_(myDelegate)

        # Create button, and add to window
        #button = NSButton.alloc().init()
        #myWindow.contentView().addSubview_(button)
        #button.setFrame_(NSMakeRect(10.0, 35.0, 45.0, 40.0))

        # Set handler for button; note that the function is called by string name
        #buttonHandler = ButtonHandler.alloc().init()
        #button.setTarget_(buttonHandler)
        #button.setAction_("doSomething")

        # Zoom button
        self.aboutWindow.standardWindowButton_(NSWindowZoomButton).setHidden_(True)
        # Display window
        self.aboutWindow.display()
        # window.(makeKeyAndOrderFront(myWindow))
        self.aboutWindow.makeKeyAndOrderFront_(self.aboutWindow)
        NSApp.activateIgnoringOtherApps_(True)
        #myWindow.orderFrontRegardless()


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

