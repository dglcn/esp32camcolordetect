import cv2
import urllib.request
import numpy as np
 
def nothing(x):
    pass
 
# Change the IP address below according to the
# IP shown in the Serial monitor of Arduino code
url = 'http://192.168.64.190'
 
cv2.namedWindow("live transmission", cv2.WINDOW_AUTOSIZE)
 
cv2.namedWindow("Tracking")
cv2.createTrackbar("LH", "Tracking", 0, 255, nothing)
cv2.createTrackbar("LS", "Tracking", 0, 255, nothing)
cv2.createTrackbar("LV", "Tracking", 0, 255, nothing)
cv2.createTrackbar("UH", "Tracking", 255, 255, nothing)
cv2.createTrackbar("US", "Tracking", 255, 255, nothing)
cv2.createTrackbar("UV", "Tracking", 255, 255, nothing)

while True:
    try:
        # Adding timeout to urlopen
        img_resp = urllib.request.urlopen(url, timeout=10)
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        frame = cv2.imdecode(imgnp, -1)
        
        # Check if frame is valid
        if frame is None:
            print("Tidak dapat membaca frame dari URL")
            continue  # Skip this iteration if frame is empty

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
        l_h = cv2.getTrackbarPos("LH", "Tracking")
        l_s = cv2.getTrackbarPos("LS", "Tracking")
        l_v = cv2.getTrackbarPos("LV", "Tracking")
 
        u_h = cv2.getTrackbarPos("UH", "Tracking")
        u_s = cv2.getTrackbarPos("US", "Tracking")
        u_v = cv2.getTrackbarPos("UV", "Tracking")
 
        l_b = np.array([l_h, l_s, l_v])
        u_b = np.array([u_h, u_s, u_v])
    
        mask = cv2.inRange(hsv, l_b, u_b) 
        res = cv2.bitwise_and(frame, frame, mask=mask)
 
        cv2.imshow("live transmission", frame)
        cv2.imshow("mask", mask)
        cv2.imshow("res", res)
    except Exception as e:
        print(f"Error: {e}")
        continue  # Skip iteration if there's an error (e.g., timeout, frame issues)

    key = cv2.waitKey(5)
    if key == ord('q'):
        break
    
cv2.destroyAllWindows()
