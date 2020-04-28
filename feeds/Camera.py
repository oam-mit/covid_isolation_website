import cv2

import time
import argparse
import math

import numpy as np
from PIL import Image
from keras.models import model_from_json
from .utils.anchor_generator import generate_anchors
from .utils.anchor_decode import decode_bbox
from .utils.nms import single_class_non_max_suppression
from .load_model.keras_loader import load_keras_model, keras_inference
import os
from distancing import settings
try:
    model = load_keras_model('model/face_mask_detection.json', 'model/face_mask_detection.hdf5')

  
except:
    pass
# anchor configuration
feature_map_sizes = [[33, 33], [17, 17], [9, 9], [5, 5], [3, 3]]
anchor_sizes = [[0.04, 0.056], [0.08, 0.11], [0.16, 0.22], [0.32, 0.45], [0.64, 0.72]]
anchor_ratios = [[1, 0.62, 0.42]] * 5

# generate anchors
anchors = generate_anchors(feature_map_sizes, anchor_sizes, anchor_ratios)

# for inference , the batch size is 1, the model output shape is [1, N, 4],
# so we expand dim for anchors to [1, anchor_num, 4]
anchors_exp = np.expand_dims(anchors, axis=0)

id2class = {0: 'Mask', 1: 'No Mask'}
# my changes
WIDTH = 57
# Perpendicular distance from the camera
DISTANCE = 38
#pixels covered by the object in the image
PIXELS = 480
# focus of the camera
# this value will be used in future calculations
FOCUS = PIXELS * DISTANCE / WIDTH
FOCUS
Face = (9,8)
faces = []

class Camera:
    def __init__(self,location):
        if type(location) is type(1):
            self.cam=cv2.VideoCapture(location)
        elif "." in location:
            self.cam=cv2.VideoCapture(location)
        else:
            self.cam=cv2.VideoCapture(os.path.join(settings.BASE_DIR,location))
        
    
    def turn_to_jpg(self,image):
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
    def __del__(self):
        self.cam.release()
    
    def run_on_video(self,video_path, conf_thresh):
        height = self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
        width = self.cam.get(cv2.CAP_PROP_FRAME_WIDTH)
        fps = self.cam.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        # writer = cv2.VideoWriter(output_video_name, fourcc, int(fps), (int(width), int(height)))
        total_frames = self.cam.get(cv2.CAP_PROP_FRAME_COUNT)
        if not self.cam.isOpened():
          
            raise ValueError("Video open failed.")
            return
        idx = 0
        
        start_stamp = time.time()
        status, img_raw = self.cam.read()
        img_raw = cv2.cvtColor(img_raw, cv2.COLOR_BGR2RGB)
        
        read_frame_stamp = time.time()

        if (status):
            self.inference(image=img_raw,
                        conf_thresh=conf_thresh,
                        iou_thresh=0.5,
                        target_shape=(260, 260),
                        draw_result=True,
                        show_result=False)
            
            return self.turn_to_jpg(image=img_raw[:, :, ::-1])
        inference_stamp = time.time()
                # writer.write(img_raw)
        write_frame_stamp = time.time()
        idx += 1
                # print("%d of %d" % (idx, total_frames))
                # print("read_frame:%f, infer time:%f, write time:%f" % (read_frame_stamp - start_stamp,
                                                                    # inference_stamp - read_frame_stamp,
                                                                    # write_frame_stamp - inference_stamp))
        # writer.release()
    
    def inference(self,image,conf_thresh=0.5,iou_thresh=0.4,target_shape=(160, 160),draw_result=True,show_result=True):
        '''
        Main function of detection inference
        :param image: 3D numpy array of image
        :param conf_thresh: the min threshold of classification probabity.
        :param iou_thresh: the IOU threshold of NMS
        :param target_shape: the model input size.
        :param draw_result: whether to daw bounding box to the image.
        :param show_result: whether to display the image.
        :return:
        '''
        # image = np.copy(image)
        
      
        faces = []
        output_info = []
        height, width, _ = image.shape
        image_resized = cv2.resize(image, target_shape)
        image_np = image_resized / 255.0  # 归一化到0~1
        image_exp = np.expand_dims(image_np, axis=0)
        # try:
        #     model = load_keras_model()
        #     print(type(model))
        # except:
        #     print("error in loading model")
        #     return image
        global model
        
        try:
            y_bboxes_output, y_cls_output = keras_inference(model, image_exp)
        except:
           
            return image
        # remove the batch dimension, for batch is always 1 for inference.
        y_bboxes = decode_bbox(anchors_exp, y_bboxes_output)[0]
        
        y_cls = y_cls_output[0]
        # To speed up, do single class NMS, not multiple classes NMS.
        bbox_max_scores = np.max(y_cls, axis=1)
        bbox_max_score_classes = np.argmax(y_cls, axis=1)

        # keep_idx is the alive bounding box after nms.
        
        keep_idxs = single_class_non_max_suppression(y_bboxes,
                                                    bbox_max_scores,
                                                    conf_thresh=conf_thresh,
                                                    iou_thresh=iou_thresh,
                                                    )
        

        for idx in keep_idxs:
            conf = float(bbox_max_scores[idx])
            class_id = bbox_max_score_classes[idx]
            bbox = y_bboxes[idx]
            # clip the coordinate, avoid the value exceed the image boundary.
            xmin = max(0, int(bbox[0] * width))
            ymin = max(0, int(bbox[1] * height))
            xmax = min(int(bbox[2] * width), width)
            ymax = min(int(bbox[3] * height), height)
            face_a=xmin
            face_b=abs(xmax-xmin)

            y = round((Face[0]*FOCUS/(face_b)),2)
            if face_a + face_b/2   < 320:
                P = 640 - 2*(face_a+ face_b/2 )
                # P_ = y * P /38
                w = round((P * y / (FOCUS)),2)
                x = -w/2
            elif face_a + face_b/2  > 320:
                P = 2*(face_a + face_b/2 ) - 640
                # P_ = y * P /38
                w = round((P *y / (FOCUS)),2)
                x=w/2
            else:
                x = 0
            faces.append((x,y))

            if draw_result:
                if class_id == 0:
                    color = (0, 255, 0)
                else:
                    color = (255, 0, 0)
                cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, 2)
                cv2.putText(image, "%s: %.2f" % (id2class[class_id], conf), (xmin + 2, ymin - 2),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, color)
            output_info.append([class_id, conf, xmin, ymin, xmax, ymax])

       
    #         global warning
        warning=[]
        for face in faces:
            warning.append([])
        if len(faces)>1:
            for a in range(len(faces)):
                for b in range(a + 1,len(faces)):
                    dist = (faces[a][0] - faces[b][0])**2 + ( faces[a][1] - faces[b][1])**2
                    dist = round(math.sqrt(dist),5)
                    if dist < 500:
                        warning[a].append(b)
                        warning[b].append(a)
                        cv2.putText(image,"distance is "+str(dist),(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,[0,0,255],2)
        str1 = ' '
        n = 0
        if len(faces)>0:
            if len(warning)>0:
                for war in range(len(warning)):
        #             n = n+1
                    str1 += '\n'
                    str1 += 'Person '
                    war3 = str(n)
                    str1 += war3
                    str1 += ' near to : '
                    for war2 in warning[war]:
                        str1 += str(war2)
                        str1 += ' , '
                    n = n+1
            y0, dy = 50, 20
            for i, line in enumerate(str1.split('\n')):
                y1 = y0 + i*dy
                y1 = int(y1)
                cv2.putText(image, line , (0,y1) ,cv2.FONT_HERSHEY_SIMPLEX,0.5,[0,0,255],2)
        if show_result:
            Image.fromarray(image).show()
       
        return output_info




