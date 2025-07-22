from collections.abc import Iterator
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import mm, cm, inch
from math import atan, degrees

# Usage:
#   label = AveryLabels.AveryLabel(5160)
#   label.open( "labels5160.pdf" )
#   label.render( RenderAddress, 30 )
#   label.close()
#
# 'render' can either pass a callable, which receives the canvas object
# (with X,Y=0,0 at the lower right) or a string "form" name of a form
# previously created with canv.beginForm().


# labels across
# labels down
# label size w/h
# label gutter across/down
# page margins left/top
# page size w/h or name from reportlab.lib.pagesizes

labelInfo = {
    # 22x 32mm x 10mm mini labels
    3044: ( 2, 11, (32, 10), (2,2), (1, 1), (66.5*mm, 120.5*mm)),

    # 189x 25.4mm x 10mm mini labels
    4731: ( 7, 27, (25.4*mm, 10*mm), (2.5*mm, 0), (9*mm, 13.5*mm), A4),
    # 2.6 x 1 address labels
    5160: ( 3, 10, (187,  72), (11, 0), (14, 36), A4),
    5161: ( 2, 10, (288,  72), (0, 0), (18, 36), A4),
    # 4 x 2 address labels
    5163: ( 2,  5, (288, 144), (0, 0), (18, 36), A4),
    # 1.75 x 0.5 return address labels
    5167: ( 4, 20, (126,  36), (0, 0), (54, 36), A4),
    # 3.5 x 2 business cards
    5371: ( 2,  5, (252, 144), (0, 0), (54, 36), A4),

    # 48x 45.7x21.2mm 
    4778: (4, 12, (45.7*mm, 21.2*mm), (0.25*cm, 0), (1.1*cm, 2*cm), A4),

    # APLI 100984 40x 52.5x29.7mm 
    100984: (4, 10, (52.5*mm, 29.7*mm), (0, 0), (0, 0), A4),

    # Royal Green 1x0.375 (1138)
    1138: (7, 22, (1*inch, 0.375*inch), (0.1*inch,0.098*inch), (0.4375*inch, 0.24*inch), letter),
}

class AveryLabel:

    def __init__(self, label, **kwargs):
        data = labelInfo[label]
        self.across = data[0]
        self.down = data[1]
        self.size = data[2]
        self.labelsep = self.size[0]+data[3][0], self.size[1]+data[3][1]
        self.labelsTotalWidth = data[0] * data[2][0] + (data[0]-1) * data[3][0]
        self.margins = data[4]
        self.topDown = True
        self.debug = False
        self.pagesize = data[5]
        self.position = 0
        self.__dict__.update(kwargs)

    def open(self, filename):
        self.canvas = canvas.Canvas( filename, pagesize=self.pagesize )
        if self.debug:
            self.canvas.setPageCompression( 0 )
        self.canvas.setLineJoin(1)
        self.canvas.setLineCap(1)

    def topLeft(self, x=None, y=None):
        if x is None:
            x = self.position
        if y is None:
            if self.topDown:
                x,y = divmod(x, self.down)
            else:
                y,x = divmod(x, self.across)

        return (
            self.margins[0]+x*self.labelsep[0],
            self.pagesize[1] - self.margins[1] - (y+1)*self.labelsep[1]
        )

    def advance(self):
        self.position += 1
        if self.position == self.across * self.down:
            self.canvas.showPage()
            self.position = 0

    def close(self):
        if self.position:
            self.canvas.showPage()
        self.canvas.save()
        self.canvas = None

    def calculateRotationDegrees(self, rotateOffset):
        return degrees(atan(rotateOffset/self.labelsTotalWidth))

    # To render, you can either create a template and tell me
    # "go draw N of these templates" or provide a callback.
    # Callback receives canvas, width, height.
    #
    # Or, pass a callable and an iterator.  We'll do one label
    # per iteration of the iterator.

    def render( self, thing, count, offset=0, rotateOffset=0, *args ):
        assert callable(thing) or isinstance(thing, str)
        if isinstance(count, Iterator):
            return self.render_iterator( thing, count )

        canv = self.canvas
        canv.rotate(self.calculateRotationDegrees(rotateOffset))
        for i in range(offset+count):
            if i >= offset:
                canv.saveState()
                canv.translate( *self.topLeft() )
                if self.debug:
                    canv.setLineWidth( 0.25 )
                    canv.rect( 0, 0, self.size[0], self.size[1] )
                if callable(thing):
                    thing( canv, self.size[0], self.size[1], *args )
                elif isinstance(thing, str):
                    canv.doForm(thing)
                canv.restoreState()
            self.advance()

    def render_iterator( self, func, iterator ):
        canv = self.canvas
        for chunk in iterator:
            canv.saveState()
            canv.translate( *self.topLeft() )
            if self.debug:
                canv.setLineWidth( 0.25 )
                canv.rect( 0, 0, self.size[0], self.size[1] )
            func( canv, self.size[0], self.size[1], chunk )
            canv.restoreState()
            self.advance()
            
