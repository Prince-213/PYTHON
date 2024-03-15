import tkinter as tk
import customtkinter    
from PIL import Image, ImageTk
import threading
import cv2
from ultralytics import YOLO
from tkinter import filedialog as fd 



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.model1 = YOLO('./myset/best.pt')
        #model2 = YOLO('yolov8n-seg.pt')

        # Define the video files for the trackers
        self.video_file1 = 0 # Path to video file, 0 for webcam
        self.video_file2 = 1  # Path to video file, 0 for webcam, 1 for external camera
        
        self.tracker_thread1 = threading.Thread(target=self.run_tracker_in_thread, args=(self.video_file1, self.model1, 1), daemon=True)
        
        img = tk.PhotoImage(file='./network-eye-in-a-frame.png')
        self.iconphoto(False, img)
        self.title("Eye Disease Detection App")
        
        self.geometry("600x500")
        self.grid_columnconfigure((0, 1), weight=1)
        
        self.gap =  customtkinter.CTkLabel(self, text="", font=("Arial", 24, 'bold'), fg_color="transparent")
        self.gap.grid(row=0, column=1, padx=20,  sticky="ew", columnspan=2)
        
        self.label =  customtkinter.CTkLabel(self, text="Automated Data Labelling for Health Care using Deep Learning", font=("Arial", 22, 'bold'),  fg_color="transparent", justify="center", wraplength=400)
        self.label.grid(row=1, column=1, padx=60, pady=20,  sticky="ew", columnspan=2)
        
        self.my_image = customtkinter.CTkImage(light_image=Image.open("./network-eye-in-a-frame.png"),dark_image=Image.open("./network-eye-in-a-frame.png"),size=(80, 80))
        
        self.image_label = customtkinter.CTkLabel(self, image=self.my_image, text="")  # display image with a CTkLabel
        self.image_label.grid(row=2, column=0, padx=20, pady=20, sticky="ew", columnspan=2)
        
        
        
        # display image with a CTkLabel
        
        self.button = customtkinter.CTkButton(self, text="START REALTIME DETECTION", height=50,  font=("Arial", 18, 'bold'),  command=self.run)
        self.button.grid(row=3, column=0, padx=20, pady=20, sticky="ew", columnspan=2)
        
        self.button2 = customtkinter.CTkButton(self, text="SELECT IMAGE TO DETECT", height=50,  font=("Arial", 18, 'bold'),  command=self.filedetect)
        self.button2.grid(row=4, column=0, padx=20, pady=20, sticky="ew", columnspan=2)
        #self.checkbox_1 = customtkinter.CTkCheckBox(self, text="checkbox 1")
        #self.checkbox_1.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")
        #self.checkbox_2 = customtkinter.CTkCheckBox(self, text="checkbox 2")
        #self.checkbox_2.grid(row=1, column=1, padx=20, pady=(0, 20), sticky="w")
        
        self.courtsey =  customtkinter.CTkLabel(self, text="Author: Ilo Chinonyelum", font=("Arial", 18, ), fg_color="transparent")
        self.courtsey.grid(row=5, column=0, padx=20, pady=20, sticky="ew", columnspan=2)
    
    def select_file(self):
            filetypes = (
                ('pic files', '*.jpg'),
            )
    
            filename = fd.askopenfilename(
                title='Open a file',
                initialdir='/',
                filetypes=filetypes)
    
            print(filename)
            return filename





    def filedetect(self):
        path = self.select_file()
        
        model = YOLO('./thermal.pt')

        results = model([path], save=True, show=True, conf=0.55, iou=0.4)



        for result in results:
            boxes = result.boxes  # Boxes object for bounding box outputs
            masks = result.masks  # Masks object for segmentation masks outputs
            keypoints = result.keypoints  # Keypoints object for pose outputs
            probs = result.probs  # Probs object for classification outputs
            result.filname = 'result.jpg'
            print(result.path) # display to screen
            
    
    

    # Create the tracker threads
    
    #tracker_thread2 = threading.Thread(target=run_tracker_in_thread, args=(video_file2, model2, 2), daemon=True)

    # Start the tracker threads
    
    #tracker_thread2.start()

    # Wait for the tracker threads to finish
    #tracker_thread1.join()
    #tracker_thread2.join()

    def run(self):
        self.tracker_thread1.start()
        self.tracker_thread1.join()
        
    def button_callback(self):
        print("button pressed")
        
    def run_tracker_in_thread(self, filename, model, file_index):
        """
        Runs a video file or webcam stream concurrently with the YOLOv8 model using threading.

        This function captures video frames from a given file or camera source and utilizes the YOLOv8 model for object
        tracking. The function runs in its own thread for concurrent processing.

        Args:
            filename (str): The path to the video file or the identifier for the webcam/external camera source.
            model (obj): The YOLOv8 model object.
            file_index (int): An index to uniquely identify the file being processed, used for display purposes.

        Note:
            Press 'q' to quit the video display window.
        """
        video = cv2.VideoCapture(filename)  # Read the video file
        
        width, height = 1024, 720

# Set the width and height 
        video.set(cv2.CAP_PROP_FRAME_WIDTH, width) 
        video.set(cv2.CAP_PROP_FRAME_HEIGHT, height) 

        while True:
            ret, frame = video.read()  # Read the video frames

            # Exit the loop if no more frames in either video
            if not ret:
                break

            # Track objects in frames if available
            results = model.track(frame, persist=True, conf=0.43)
            res_plotted = results[0].plot()
            cv2.imshow(f"Tracking_Stream_{file_index}", res_plotted)

            key = cv2.waitKey(1)
            if key == ord('q'):
                break

        # Release video sources
        video.release()

    

app = App()
app.mainloop()