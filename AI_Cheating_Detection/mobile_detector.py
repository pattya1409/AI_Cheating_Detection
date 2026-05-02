import cv2
import os

class MobileDetector:
    """
    Attempts to load MobileNet-SSD Caffe model from models/ folder.
    If models are not present, the detector will gracefully disable itself.
    To enable mobile detection, download these two files and place them in 'models/':
     - MobileNetSSD_deploy.prototxt
     - MobileNetSSD_deploy.caffemodel
    Links (use a browser to download):
     - https://github.com/chuanqi305/MobileNet-SSD
    """
    def __init__(self, model_dir='models'):
        proto = os.path.join(model_dir, 'MobileNetSSD_deploy.prototxt')
        model = os.path.join(model_dir, 'MobileNetSSD_deploy.caffemodel')
        self.enabled = False
        if os.path.exists(proto) and os.path.exists(model):
            try:
                self.net = cv2.dnn.readNetFromCaffe(proto, model)
                # Class id for 'person' is 15 in the original MobileNet-SSD; many models don't have 'mobile' label.
                # We will treat detected 'person' holding something close to face/hands as a heuristic later if needed.
                self.enabled = True
            except Exception as e:
                print('Warning: Failed to load object detection model:', e)
                self.enabled = False
        else:
            print('Mobile detection model files not found in models/. Mobile detection disabled.')
            self.net = None

    def detect(self, frame, conf_threshold=0.5):
        """
        Returns True if a high-confidence detection (any object) is found.
        If model is not enabled returns False.
        """
        if not self.enabled or self.net is None:
            return False

        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
        self.net.setInput(blob)
        detections = self.net.forward()
        for i in range(detections.shape[2]):
            confidence = float(detections[0,0,i,2])
            if confidence > conf_threshold:
                return True
        return False
