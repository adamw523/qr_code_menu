import objc

from Foundation import *
from AppKit import *

ABOUT_TEXT = """Copyright Adam Wisniewski

"""

class AboutController(NSWindowController):
    aboutTextField = objc.IBOutlet()
    iconImageView = objc.IBOutlet()

    def __new__(cls):
        return cls.alloc().init()

    def init(self):
        self.initWithWindowNibName_("nibs/About")
        # self.showWindow()
        return self

    def showWindow(self):
        self.showWindow_(self)
        NSApp.activateIgnoringOtherApps_(True)

    def awakeFromNib(self):
        # NSWindowController.windowDidLoad(self)
        #super(AboutController, self).windowDidLoad()

    	# Set iamge
    	icon_128 = NSImage.alloc().initByReferencingFile_('images/icon_128.png')
    	self.iconImageView.setImage_(icon_128)

    	# Set text
    	self.aboutTextField.setStringValue_(ABOUT_TEXT)

