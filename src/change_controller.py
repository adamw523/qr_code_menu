# coding=utf-8
import objc

from Foundation import *
from AppKit import *

from qr_code_maker import *

class ChangeController(NSWindowController):
    outputImageView = objc.IBOutlet()
    sourceTextField = objc.IBOutlet()
    myMenu = objc.IBOutlet()

    def __new__(cls, text):
        return cls.alloc().initWithText(text)

    def initWithText(self, text):
        self.text = text
        self.qrImageText = None
        return self.init()

    def __init__(self, pb):
        self.initWithWindowNibName_("nibs/Change")

        # start timer for updating image if text changes
        timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            1, self, 'watchAndUpdateText:', None, True)
        NSRunLoop.currentRunLoop().addTimer_forMode_(timer, NSRunLoopCommonModes)

    def controlTextDidChange_(self, notification):
        self.text = self.sourceTextField.stringValue()

    def control_textView_doCommandBySelector_(self, control, textView, selector):
        result = False
        #- (BOOL)control:(NSControl*)control textView:(NSTextView*)textView doCommandBySelector:(SEL)commandSelector
        if selector == 'insertNewline:':
            textView.insertNewlineIgnoringFieldEditor_(textView)
            result = True

        return result

    def setText(self, text):
        self.text = text
        if self.sourceTextField and self.sourceTextField.stringValue() != text:
            self.sourceTextField.setStringValue_(text)

    def showWindow(self):
        self.showWindow_(self)
        NSApp.activateIgnoringOtherApps_(True)
        self.window().setLevel_(NSFloatingWindowLevel)
        self.updateView()

    def updateView(self):
        self.updateQrCode()
        
    def updateQrCode(self):
        # create a qr code image
        maker = QrCodeMaker()
        i = maker.imageFromText(self.text)

        # set the output view to the image
        self.outputImageView.setImage_(i)
        self.qrImageText = self.text

    def watchAndUpdateText_(self, notification):
        if self.qrImageText != self.text:
            self.updateQrCode()

    def windowDidLoad(self):
        NSWindowController.windowDidLoad(self)
        self.sourceTextField.setDelegate_(self)

        # set menu so copy and paste work
        NSApp.setMainMenu_(self.myMenu)

        # set initial text
        self.sourceTextField.setStringValue_(self.text)