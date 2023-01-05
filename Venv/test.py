import wx
import matplotlib
import panda3d.core as core
from direct.showbase.ShowBase import ShowBase
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure

matplotlib.use('WXAgg')

class CanvasPanel(wx.Panel):
    def __init__(self, parent):
        #Defines Matplotlib display
        #Sets size and position of the Matplotlib display
        wx.Panel.__init__(self, parent, pos=wx.Point(800,0))
        
        #Configures the Matplotlib display
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.sizer = wx.FlexGridSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()
        
class Frame(wx.Frame):
    def __init__(self, *args, **kwargs):
        #Defines 3D display
        wx.Frame.__init__(self, *args, **kwargs)

class App(ShowBase):
    def __init__(self):
        #Configures main window
        ShowBase.__init__(self)
        self.startWx()
        self.frame = Frame(None, wx.ID_ANY, 'Matplotlib Test')
        self.frame.Show()
        self.frame.Layout()
        self.frame.Maximize()
        
        #Configures the 3D display
        wp = core.WindowProperties()
        wp.setOrigin(0,0)
        wp.setParentWindow(self.frame.GetHandle())
    
        base.openMainWindow(type = 'onscreen', props=wp, size=(800, 1000), aspectRatio = 1)
        
        panel = CanvasPanel(self.frame)
        panda = base.loader.loadModel('panda')
        panda.reparentTo(base.render)
        panda.setScale(10, 10, 10)
        panda.setPos(0, 500, -50)
        
App()