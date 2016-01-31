from wxPython.wx import *
import sys,math
import base64
#import binascii
#from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from skeletonHandWidget import *
from leapMotionListener import *

name = 'ball_glut'

class myFrame(wxFrame):
    def __init__(self, parent, title):
        wxFrame.__init__(self, parent, -1, title, wxDefaultPosition, wxSize(300,450), style= wxSYSTEM_MENU | wxCAPTION | wxCLOSE_BOX)
        #text = wxStaticText(self, label=title)

        self.filename = None
        self.dirname = None

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
        self.listBox.Bind(EVT_LISTBOX, self.selectionChanged )

    def isNewFrameSelected(self):
        return self.listBox.GetStringSelection() == "<New shot>"

    def onFrame(self, frame):
        if self.isNewFrameSelected():
            self.glCanvas.drawFrame(frame)
        return

    def OnNew(self, event):
        self.filename = None
        self.dirname = None
        self.listBox.Clear()
        self.listBox.Append("<New shot>")
        self.listBox.SetSelection(0)
        return

    def OnOpen(self, event):
        dirname = ""
        dlg = wxFileDialog(self, "Choose a file", dirname, "", "*.*", wxOPEN)
        if dlg.ShowModal() == wxID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            self.load(self.filename, self.dirname)
        dlg.Destroy()
        return

    def OnSave(self, event):
        if self.filename == None or self.dirname == None:
            self.OnSaveAs(event)
        else:
            self.save(self.filename, self.dirname)
        return

    def OnSaveAs(self, event):
        dirname = ""
        dlg = wxFileDialog(self, "Choose a file", dirname, "", "*.*", wxSAVE)
        if dlg.ShowModal() == wxID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            self.save(self.filename, self.dirname)
        dlg.Destroy()
        return

    def save(self, filename, dirname):
        f = open(dirname + "/" + filename, 'w')
        framesList = []
        for i in range(self.listBox.GetCount()):
            frame = self.listBox.GetClientData(i);
            if frame is None:
                continue
            serialized_tuple = frame.serialize
            serialized_data = serialized_tuple[0]
            serialized_length = serialized_tuple[1]
            data_address = serialized_data.cast().__long__()
            dataSerialized = (ctypes.c_ubyte * serialized_length).from_address(data_address)
            dataEncoded = base64.b64encode( dataSerialized )
            framesList.append( dataEncoded )
        f.write( '\n'.join(framesList) )
        f.close()

    def load(self, filename, dirname):
        f = open(dirname + "/" + filename, 'r')
        self.listBox.Clear()
        for data in f.readlines():
            dataDecoded = base64.b64decode( data )
            frame = Leap.Frame()
            leap_byte_array = Leap.byte_array(len(dataDecoded))
            address = leap_byte_array.cast().__long__()
            ctypes.memmove(address, dataDecoded, len(dataDecoded))
            frame.deserialize((leap_byte_array, len(dataDecoded)))

            frameName = "Frame " + str(frame.id)
            self.listBox.Append(frameName, frame)

        self.listBox.Append("<New shot>")

    def keyUp(self, event):
        if event.GetKeyCode() == WXK_SPACE:
            print "Key"
            frame = self.glCanvas.getScreen()
            frameName = "Frame " + str(frame.id)
            pos = self.listBox.GetCount() - 1
            self.listBox.Insert( frameName, pos, frame )
            self.listBox.EnsureVisible( self.listBox.GetCount() - 1 )

    def selectionChanged(self, event):
        if self.isNewFrameSelected():
            return
        frame = self.listBox.GetClientData( self.listBox.GetSelection() )
        self.glCanvas.drawFrame(frame)



if __name__ == '__main__':
    #init GUI
    app = wxPySimpleApp()
    frame = myFrame(None, "Hello world")
    frame.Show()

    #init leap motion
    listener = LeapMotionListener(frame)
    controller = Leap.Controller()
    controller.add_listener(listener)

    app.MainLoop()

    controller.remove_listener(listener)
