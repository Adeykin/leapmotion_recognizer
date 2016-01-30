import numpy as np
from wxPython.glcanvas import wxGLCanvas
from wxPython.wx import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class myGLCanvas(wxGLCanvas):
    def __init__(self, parent, size):
        glutInit(sys.argv)
        wxGLCanvas.__init__(self, parent,-1, size=size)
        EVT_PAINT(self, self.OnPaint)
        self.init = 0
        self.lastFrame = None
        self.haveFrame = False
        return

    def OnPaint(self,event):
        dc = wxPaintDC(self)
        self.SetCurrent()
        if not self.init:
            self.InitGL()
            self.init = 1
        self.OnDraw()
        return

    def OnDraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        color = [1.0,0.,0.,1.]
        #glMaterialfv(GL_FRONT,GL_DIFFUSE,color)
        #glutSolidSphere(2,20,20)
        
        self.drawGrid()
        if self.haveFrame == True:
            hand = filter(lambda x: x.is_right, self.lastFrame.hands)            
            self.drawHand(hand)
                    

        glPopMatrix()
        self.SwapBuffers()
        return
        
    def drawGrid(self):
        glColor(0.0,0.3,0.0,0.0)
        glBegin(GL_LINES)
        for i in np.linspace(-250,250, num=11):
            # xz
            glVertex3d(i,    0, -250)
            glVertex3d(i,    0,  250)
            glVertex3d(-250, 0,    i)
            glVertex3d( 250, 0,    i)
        for i in np.linspace(0,500, num=11):
            # xy
            glVertex3d(-250, i, -250)
            glVertex3d( 250, i, -250)
            glVertex3d(-250+i, 0,    -250)
            glVertex3d(-250+i, 500,  -250)
            # zy
            glVertex3d(-250, 500, -250+i)
            glVertex3d(-250,   0, -250+i)
            glVertex3d(-250, i, -250)
            glVertex3d(-250, i,  250)
        glEnd()
        
    def drawHand(self,hand):
        if hand == []:
            return
            
        hand = hand[0]
        
        glColor(1.0,0.0,0.0,0.0)          
        for finger in hand.fingers:                    
            bones = [hand.arm.wrist_position] + [finger.bone(0).prev_joint] + [finger.bone(i).next_joint for i in range(4)] 
            glBegin(GL_LINE_STRIP)
            for bone in bones:
                glVertex(bone.x, bone.y, bone.z)
            glEnd()
            
        glPointSize(3)
        glBegin(GL_POINTS)
        glVertex(hand.arm.wrist_position.x, hand.arm.wrist_position.y, -250)
        glVertex(-250, hand.arm.wrist_position.y, hand.arm.wrist_position.z)
        glVertex(hand.arm.wrist_position.x, 0, hand.arm.wrist_position.z)
        glEnd()

    def InitGL(self):
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClearDepth(1.0)

        glOrtho(-400,400,-100,600,-400,400)
        glRotated(30, 1,0,0)
        glRotated(-30, 0,1,0)
        return
        
    def drawFrame(self, frame):
        self.lastFrame = frame;
        self.haveFrame = True
        self.Refresh()
        #print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
        #      frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))
        EVT_PAINT(self, self.OnPaint)
        return
        
    def getScreen(self):
        return self.lastFrame
