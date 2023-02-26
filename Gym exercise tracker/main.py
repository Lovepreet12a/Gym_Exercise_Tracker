from tkinter import *
from tkinter import ttk
from tkinter.font import BOLD
from webbrowser import BackgroundBrowser 
from PIL import Image, ImageTk
import os  
import numpy as np
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils 
mp_pose = mp.solutions.pose


class Gym_Exercise_Tracker:
    def __init__(self, root):
        self.root = root 
        self.root.geometry("1285x700+0+0")
        self.root.title("Gym Exercise Tracker")


         # First Image 
        img= Image.open(r"Boy1.jpg")
        img = img.resize((450,700), Image.ANTIALIAS)
        self.photoimg = ImageTk.PhotoImage(img)

        first_label = Label(self.root, image= self.photoimg)
        first_label.place(x=0, y= 0, width=450, height=700)

        # Second Image 
        img2= Image.open(r"Boy.jpg")
        img2 = img2.resize((500,700), Image.ANTIALIAS)
        self.photoimg2 = ImageTk.PhotoImage(img2)

        second_label = Label(self.root, image= self.photoimg2)
        second_label.place(x=450, y= 0, width=500, height=700)

        # Third Image 
        img3= Image.open(r"Girl.jpg")
        img3 = img3.resize((500,700), Image.ANTIALIAS)
        self.photoimg3 = ImageTk.PhotoImage(img3)

        third_label = Label(self.root, image= self.photoimg3)
        third_label.place(x=850, y= 0, width=450, height=700)


          # Title 
        title_label = Label(self.root, text= "Gym Exercise Tracker",
        font= ("times new roman", 25, BOLD), bg="darkblue", fg= "red")
        title_label.place(x=0, y=0, width=1285, height=45)

        # Button
        b1_1 = Button(second_label, text= "Track your workout", command= self.gym_tracker, cursor= "hand2",
        font= ("times new roman", 20, BOLD), bg="red", fg= "white")
        b1_1.place(x = 70, y= 560, width= 250, height= 55)
        

          

    def gym_tracker(self):
      def calculate_angle(a,b,c):
        a = np.array(a) # First point
        b = np.array(b) # Mid point
        c = np.array(c) # End point
        
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle= np.abs(radians*180.0/np.pi)

        if angle > 180.0:
            angle = 360.0-angle
      
        return angle
      cap = cv2.VideoCapture(0)

      #curl counter
      left_counter = 0
      left_stage = None

      right_counter = 0
      right_stage = None

      left_knee_counter = 0
      left_knee_stage = None

      # Setup mediapipe instances
      with mp_pose.Pose(min_detection_confidence= 0.5, min_tracking_confidence=0.5) as pose:
          
        while cap.isOpened():

          ret, frame = cap.read()
            
          # Recolor image
          image= cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
          image.flags.writeable= False
          
          # Make detections
          result = pose.process(image)
          
          # Recoloring image back to BGR
          image.flags.writeable= True
          image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
          
          
          # Extract landmarks
          try:
              landmarks= result.pose_landmarks.landmark
              # Get Coordinates for left arm
              left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y
              left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y
              left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y
              
              # Calculate angles
              left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
              
              # Visualization
              cv2.putText(image, str(left_angle), 
                        tuple(np.multiply(left_elbow, [640,480]).astype(int)),
                              cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA)
              
              
              # For Right arm
              # Get Coordinates for left arm
              right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y
              right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y
              right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y
              
              # Calculate angles
              right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
              
              # Visualization
              cv2.putText(image, str(right_angle), 
                        tuple(np.multiply(right_elbow, [640,480]).astype(int)),
                              cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA)
              
              
              # For Left knee
              # Get Coordinates for left knee
              left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y
              left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y
              left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y
              
              
              # Calculate angles
              left_knee_angle = calculate_angle(left_hip, left_knee, left_ankle)
              
              # Visualization
              cv2.putText(image, str(left_knee_angle), 
                        tuple(np.multiply(left_knee, [640,480]).astype(int)),
                              cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv2.LINE_AA)
              
              #left arm Curl counter logic
              if left_angle > 160:
                  left_stage = "down"
              if left_angle < 50 and  left_stage == "down":
                  left_stage = "up"
                  left_counter += 1
                  
              #right arm Curl counter logic
              if right_angle > 160:
                  right_stage = "down"
              if right_angle < 50 and  right_stage == "down":
                  right_stage = "up"
                  right_counter += 1
                  
              #left knee Curl counter logic
              if left_knee_angle < 150:
                  left_knee_stage = "down"
              if left_knee_angle > 150 and  left_knee_stage == "down":
                  left_knee_stage = "up"
                  left_knee_counter += 1
                  
              
          except:
              pass
          
          # Render curl counter
          # Setup status box for left arm
          # First rectangle
          cv2.rectangle(image, (0,0), (700,73), (245,117,66), -1)
          
          # Second rectangle
          cv2.rectangle(image, (0,300), (150,475), (0,0,255), -1)
          
          # REPS in first box
          cv2.putText(image, "LEFT REPS", (10,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0,0,0), 1, cv2.LINE_AA)
          
          cv2.putText(image, str(left_counter), (5,60), cv2.FONT_HERSHEY_SIMPLEX, 2,
                    (0,0,0), 2, cv2.LINE_AA)
          
          
          # Stage in first box
          cv2.putText(image, "Left Stage", (125,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0,0,0), 1, cv2.LINE_AA)
          
          cv2.putText(image, left_stage, (115,60), cv2.FONT_HERSHEY_SIMPLEX, 2,
                    (0,0,0), 2, cv2.LINE_AA)
          
          
          # Setup status box for right arm in second box
  #         cv2.rectangle(image, (600,0), (275,73), (245,117,66), -1)
          
          # REPS in first box
          cv2.putText(image, "RIGHT REPS", (345,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0,0,0), 1, cv2.LINE_AA)
          
          cv2.putText(image, str(right_counter), (350,60), cv2.FONT_HERSHEY_SIMPLEX, 2,
                    (0,0,0), 2, cv2.LINE_AA)
          
          
          # Stage in first box
          cv2.putText(image, "Right Stage", (460,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0,0,0), 1, cv2.LINE_AA)
          
          cv2.putText(image, right_stage, (450,60), cv2.FONT_HERSHEY_SIMPLEX, 2,
                    (0,0,0), 2, cv2.LINE_AA)
          
          
          # REPS in second box
          cv2.putText(image, "SQUAT REPS", (0,410), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0,0,0), 1, cv2.LINE_AA)
          
          cv2.putText(image, str(left_knee_counter), (10,470), cv2.FONT_HERSHEY_SIMPLEX, 2,
                    (0,0,0), 1, cv2.LINE_AA)
          
          
          # Stage in second box
          cv2.putText(image, "SQUAT STAGE", (0,320), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0,0,0), 1, cv2.LINE_AA)
          
          cv2.putText(image, left_knee_stage, (0,370), cv2.FONT_HERSHEY_SIMPLEX, 2,
                    (0,0,0), 1, cv2.LINE_AA)
          
          # Render detections
          mp_drawing.draw_landmarks(image, result.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245,117,66), thickness=2,
                                                        circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(245,66,230), thickness=2,
                                                        circle_radius=2))
          
          cv2.imshow("Mediapipe feed", image)

          if cv2.waitKey(10) == ord("q"):

              break
      cap.release()
      cv2.destroyAllWindows()
              

if __name__ == "__main__":
    root = Tk()
    obj= Gym_Exercise_Tracker(root)
    root.mainloop()
