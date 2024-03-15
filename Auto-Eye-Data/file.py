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
        
        
        
        img = tk.PhotoImage(file='./network-eye-in-a-frame.png')
        self.iconphoto(False, img)
        self.title("Eye Disease Detection App")
        
        self.geometry("600x400")
        self.grid_columnconfigure((0, 1), weight=1)
        
        self.gap =  customtkinter.CTkLabel(self, text="", font=("Arial", 24, 'bold'), fg_color="transparent")
        self.gap.grid(row=0, column=1, padx=20,  sticky="ew", columnspan=2)
        
        self.label =  customtkinter.CTkLabel(self, text="Automated Data Labelling for Health Care using Deep Learning", font=("Arial", 22, 'bold'),  fg_color="transparent", justify="center", wraplength=400)
        self.label.grid(row=1, column=1, padx=60, pady=20,  sticky="ew", columnspan=2)
        
        self.my_image = customtkinter.CTkImage(light_image=Image.open("./network-eye-in-a-frame.png"),dark_image=Image.open("./network-eye-in-a-frame.png"),size=(80, 80))
        
        self.image_label = customtkinter.CTkLabel(self, image=self.my_image, text="")  # display image with a CTkLabel
        self.image_label.grid(row=2, column=0, padx=20, pady=20, sticky="ew", columnspan=2)
        
        
        
        # display image with a CTkLabel
        
        self.button = customtkinter.CTkButton(self, text="SELECT IMAGE TO DETECT", height=50,  font=("Arial", 18, 'bold'),  command=self.run)
        self.button.grid(row=3, column=0, padx=20, pady=20, sticky="ew", columnspan=2)
        #self.checkbox_1 = customtkinter.CTkCheckBox(self, text="checkbox 1")
        #self.checkbox_1.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")
        #self.checkbox_2 = customtkinter.CTkCheckBox(self, text="checkbox 2")
        #self.checkbox_2.grid(row=1, column=1, padx=20, pady=(0, 20), sticky="w")
        
        self.courtsey =  customtkinter.CTkLabel(self, text="Author: Ilo Chinonyelum", font=("Arial", 18, ), fg_color="transparent")
        self.courtsey.grid(row=4, column=0, padx=20, pady=20, sticky="ew", columnspan=2)
    
    

    # Create the tracker threads
    
    #tracker_thread2 = threading.Thread(target=run_tracker_in_thread, args=(video_file2, model2, 2), daemon=True)

    # Start the tracker threads
    
    #tracker_thread2.start()

    # Wait for the tracker threads to finish
    #tracker_thread1.join()
    #tracker_thread2.join()
    
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


# open button


    def run(self):
        path = self.select_file()
        
        model = YOLO('myset/best.pt')

        results = model([path], save=True, show=True, conf=0.55, iou=0.4)



        for result in results:
            boxes = result.boxes  # Boxes object for bounding box outputs
            masks = result.masks  # Masks object for segmentation masks outputs
            keypoints = result.keypoints  # Keypoints object for pose outputs
            probs = result.probs  # Probs object for classification outputs
            result.filname = 'result.jpg'
            print(result.path) # display to screen
            
    

app = App()
app.mainloop()