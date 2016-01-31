import sys, math
import base64
import Leap
import ctypes
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

def loadData(filename):
    f = open(filename, 'r')
    frames = []
    for data in f.readlines():
        dataDecoded = base64.b64decode( data )
        frame = Leap.Frame()        
        leap_byte_array = Leap.byte_array(len(dataDecoded))
        address = leap_byte_array.cast().__long__()
        ctypes.memmove(address, dataDecoded, len(dataDecoded))
        frame.deserialize((leap_byte_array, len(dataDecoded)))        
        frames.append( frame )
    return frames
        
def frameToVector(frame):
    vector = []
    
    hand = filter(lambda x: x.is_right, frame.hands)
    if hand == []:
        return None
    hand = hand[0]
    arm = hand.arm
         
    for finger in hand.fingers:                    
        for i in range(4):
            bone = finger.bone(i)
            
            pitch = bone.direction.pitch - arm.direction.pitch
            yaw = bone.direction.yaw - arm.direction.yaw
            vector.append(str(pitch))
            vector.append(str(yaw))
    
    return vector
    
def main():
    if len(sys.argv) != 3:
        print "USAGE: python2.7 dataExtractor.py <input.dat> <output.csv>"
        return
    
    inputFile = sys.argv[1]
    outputFile = sys.argv[2]
    
    frames = loadData(inputFile)    
    print "Read " + str(len(frames)) + " frames"
    
    vectors = []
    for frame in frames:
        vector = frameToVector(frame)
        if vector is None:
            continue
        vectors.append( ';'.join(vector) )
    
    f = open(outputFile, 'w')
    f.write('\n'.join(vectors))
    f.close()

if __name__ == '__main__':
    controller = Leap.Controller()
    main()
