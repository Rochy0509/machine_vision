import cv2
import numpy as np
import glob
import os

#chessboard's size printed for calibrating cameras
chessboard_size = (10, 7) #10 inner corners horizontally and 7 vertically

#prepare points
obj_p = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
obj_p[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

#lists to store the chessboard points


#load images
images1 = sorted(glob.glob('camera1/*.png'))
images2 = sorted(glob.glob('camera2/*.png'))

def drawing_corners(img_path, output_dir, camera_name):
    
    objpoints = []
    imgpoints = []

    os.makedirs(output_dir, exist_ok=True)

    #processing images
    for i, fname in enumerate(img_path):

        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        #finding chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)
        
        if ret: 
            objpoints.append(obj_p)
            imgpoints.append(corners)

            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), 
                                       (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
            
            img_with_corners = cv2.drawChessboardCorners(img.copy(), chessboard_size, corners2, ret)
            
             # Save annotated image
            filename = os.path.basename(fname)
            output_path = os.path.join(output_dir, f"calibrated_{filename}")
            cv2.imwrite(output_path, img_with_corners)

    return objpoints, imgpoints

objpoints1, imgpoints1 = drawing_corners(images1, 'camera1/calibration', 'Camera 1')
objpoints2, imgpoints2 = drawing_corners(images2, 'camera2/calibration', 'Camera 2')

def intrinsic_calculation(objpoint, imgpoint):

    ret, mtx, dist, rvecs, tvec = cv2.calibrateCamera(objpoint, imgpoint, (640, 480), None, None)
    
    return ret, mtx, dist, rvecs, tvec

ret1, mtx1, dist1, rvecs1, tvecs1 = intrinsic_calculation(objpoints1, imgpoints1)
ret2, mtx2, dist2, rvecs2, tvecs2 = intrinsic_calculation(objpoints2, imgpoints2)

print("\nCamera1 Intrinsic Matrix:")
print(mtx1)
print("\nCamera1 Len distortion:")
print(dist1)
print("\nCamera2 Intrinsic Matrix:")
print(mtx2)
print("\nCamera2 Len distortion:")
print(dist2)

