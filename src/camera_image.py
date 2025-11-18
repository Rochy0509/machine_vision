import pyrealsense2 as rs
import numpy as np
import cv2
import os
import time


#querying cameras connected
ctx = rs.context()
devices = ctx.query_devices()

cameras = []
for device in devices:
    print(f"Devices connected: {device.get_info(rs.camera_info.name)}")
    cameras.append(device.get_info(rs.camera_info.serial_number))
print(cameras) #retrieving the serial number to connect to the cameras

#function to create pipeline for each camera
def pipeline_creation(serial_number):
    pipeline = rs.pipeline()
    config = rs.config()

    config.enable_device(serial_number)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    return pipeline, config

pipeline1, config1 = pipeline_creation(cameras[0])
pipeline2, config2 = pipeline_creation(cameras[1])


#Function to save images from cameras
def calibration_images(max_images=10):

    dirs = ['camera1', 'camera2']
    for d in dirs:
        os.makedirs(d, exist_ok=True)

    try:
        print("Starting pipeline 1...")
        pipeline1.start(config1)
        print("Pipeline 1 started successfully!")
        
        print("Starting pipeline 2...")
        pipeline2.start(config2)
        print("Pipeline 2 started successfully!")

        count1 = count2 = 0

        while count1 < max_images or count2 < max_images:
            #Capturing poses
            frames1 = pipeline1.wait_for_frames()
            frames2 = pipeline2.wait_for_frames()
            
            color_frame1 = frames1.get_color_frame()
            color_frame2 = frames2.get_color_frame()
            
            if color_frame1 and color_frame2:
                #convert to numpy
                img1 = np.asanyarray(color_frame1.get_data())
                img2 = np.asanyarray(color_frame2.get_data())

                #Display side by side
                cv2.imshow('Camera 1', img1)
                cv2.imshow('Camera 2', img2)

                k = cv2.waitKey(1) & 0xFF
                
                if k == ord('s'):

                    if count1 < max_images:
                        cv2.imwrite(f"camera1/image_{count1+1:02d}.png", img1)
                        count1 += 1
                    
                    if count2 < max_images:
                        cv2.imwrite(f"camera2/image_{count2+1:02d}.png", img2)
                        count2 += 1
                    
                    time.sleep(0.3)

                elif k == ord('q'):
                    break    

    except Exception as e:
        print(f'Error capturing or displaying frames: {e}')
    finally:
        try:
            pipeline1.stop()
            pipeline2.stop()
        except:
            pass
                        
        cv2.destroyAllWindows()

calibration_images(max_images=10)