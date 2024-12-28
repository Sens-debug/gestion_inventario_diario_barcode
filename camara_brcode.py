import cv2



class Camara(cv2.VideoCapture):
    def __init__(self):
        super().__init__(0)
    def get_frame(self):
        ret, frame = self.read()
        if ret:
            rgb_frame=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
            return rgb_frame  # Return the RGB frame for processing by the rest of the code  # 1:3 aspect ratio
        else: return None

    
    def release_cam (self):
        self.release()
        cv2.destroyAllWindows()



    