# coding=utf-8
import objc

from Foundation import *
from AppKit import *

class ChangeController(NSWindowController):
    outputImageView = objc.IBOutlet()
    sourceTextField = objc.IBOutlet()

    def __new__(cls):
        return cls.alloc().init()

    def __init__(self):
        self.initWithWindowNibName_("nibs/Change")

    def control_textView_doCommandBySelector_(self, control, textView, selector):
        result = False
        #- (BOOL)control:(NSControl*)control textView:(NSTextView*)textView doCommandBySelector:(SEL)commandSelector
        if selector == 'insertNewline:':
            textView.insertNewlineIgnoringFieldEditor_(textView)
            result = True

        return result

    def windowDidLoad(self):
        NSWindowController.windowDidLoad(self)
        print "sourceTextField", self.sourceTextField
        self.sourceTextField.setDelegate_(self)