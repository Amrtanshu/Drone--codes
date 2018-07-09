import cv2
import urllib 
import numpy as np
import time


start=time.time()
stream=urllib.urlopen('http://10.42.0.178:8081/frame.h264')
bytes=''
f=0
end=0
totalframes =0

while True:

    bytes+=stream.read(150000)
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')
 
    if a!=-1 and b!=-1:
        jpg = bytes[a:b+2]
        bytes= bytes[b+2:]
        i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_GRAYSCALE)
        end = time.time()
        totalframes=totalframes+1
        f=f+1
        if cv2.waitKey(1) ==27:
            exit(0)
        cv2.imshow('IMAGE',i)

elapsed_time=end-start
print elapsed_time ,5/elapsed_time


def get_aruco(img,aruco_id):
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    corners,marker_ids,reject = cv2.aruco.detectMarkers(gray,dictionary)
    if (marker_ids)>0:
        if aruco_id in marker_ids:
            marker_ids=((marker_ids)[:,0]).tolist().index(aruco_id)
            corners = np.asarray(corners)
            corners=(corners[marker_ids][0,:])
            centres=np.mean(corners,axis=0)
            return (centres)
    else:
        return(-1,-1)

def get_errors(x,y,centre):

    
    dist[0]=y-centre[0]
    dist[1]=x-centre[1]
    return dist

dist=np.zeros(2)  
y,x,z=img.shape
x=x/2
y=y/2

while True:
    ret, img
    ret,img = cap.read()
    centre = get_aruco(img,aruco_id)
    if centre[0]!=-1:
        dist = get_errors(x,y,centre)
        cv2.line(img,(centre[0],centre[1]),(x,y),(255,0,0),5)
    cv2.imshow("output",img)
    out.write(img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
