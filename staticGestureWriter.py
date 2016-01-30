from wxPython.wx import *
import sys,math
#from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from skeletonHandWidget import *
from leapMotionListener import *

name = 'ball_glut'

class myFrame(wxFrame):
    def __init__(self, parent, title):
        wxFrame.__init__(self, parent, -1, title, wxDefaultPosition, wxSize(300,450), style= wxSYSTEM_MENU | wxCAPTION | wxCLOSE_BOX)
        #text = wxStaticText(self, label=title)
        
        fileMenu = wxMenu()
        newItem = fileMenu.Append(wxID_NEW, "New")
        openItem = fileMenu.Append(wxID_OPEN, "Open")
        saveItem = fileMenu.Append(wxID_SAVE, "Save")
        saveAsItem = fileMenu.Append(wxID_SAVEAS, "Save as")
        bar = wxMenuBar()
        bar.Append(fileMenu, "File")
        self.SetMenuBar(bar)
        self.Bind(EVT_MENU, self.OnNew, newItem)
        self.Bind(EVT_MENU, self.OnOpen, openItem)
        self.Bind(EVT_MENU, self.OnSave, saveItem)
        self.Bind(EVT_MENU, self.OnSaveAs, saveAsItem)

        panel = wxPanel(self, -1)
        self.listBox = wxListBox(panel, -1, choices=["<New shot>"], style=wxLB_SINGLE)
        #self.listBox.Append("hello3")
        self.listBox.SetMaxSize((300, 150))
        self.listBox.SetMinSize((300, 150))
        self.listBox.SetSelection(0)
        self.glCanvas = myGLCanvas(panel, wxSize(300,300))
        self.glCanvas.SetMaxSize((300, 300))
        self.glCanvas.SetMinSize((300, 300))
        box = wxBoxSizer(wxVERTICAL)
        box.Add(self.glCanvas, 1 )
        #box.Add(wxButton(panel, -1, 'Button2'), 1 )
        box.Add(self.listBox, 0.5 )
        panel.SetSizer(box)
        self.Centre()
        
        self.Bind(EVT_KEY_UP, self.keyUp)
        
    def OnNew(self, event):
        return
        
    def OnOpen(self, event):
        dirname = ""
        dlg = wxFileDialog(self, "Choose a file", dirname, "", "*.*", wxOPEN)
        if dlg.ShowModal() == wxID_OK:
            filename = dlg.GetFilename()
            dirname = dlg.GetDirectory()
        dlg.Destroy()
        return
    
    def OnSave(self, event):
        return
    
    def OnSaveAs(self, event):
        return
        
    def keyUp(self, event):
        if event.GetKeyCode() == WXK_SPACE:
            print "Key"
            frame = self.glCanvas.getScreen()
            frameName = "Frame " + str(frame.id)
            pos = self.listBox.GetCount() - 1
            self.listBox.Insert( frameName, pos, frame )
            self.listBox.EnsureVisible( self.listBox.GetCount() - 1 )
        

if __name__ == '__main__':
    #init GUI
    app = wxPySimpleApp()
    frame = myFrame(None, "Hello world")
    frame.Show()
    
    #init leap motion
    listener = LeapMotionListener(frame.glCanvas)
    controller = Leap.Controller()
    controller.add_listener(listener)
    
    app.MainLoop()
    
    controller.remove_listener(listener)
