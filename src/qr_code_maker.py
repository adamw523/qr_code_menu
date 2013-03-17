import qrcode
import qrcode.image.pure
import StringIO

from AppKit import *

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
