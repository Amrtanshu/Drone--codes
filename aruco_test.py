
import numpy as np
import cv2


fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))


dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
aruco_id=23

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

cap = cv2.VideoCapture(1)

ret ,img=cap.read()
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


 
