import objc
import Cocoa
from AppKit import *
from Foundation import *
from PyObjCTools import AppHelper

from qr_code_menu import *
from qr_code_menu_app import *

if __name__ == "__main__":
    app = NSApplication.sharedApplication()
    delegate = QrCodeMenuApp.alloc().init()
    app.setDelegate_(delegate)
    AppHelper.runEventLoop()
