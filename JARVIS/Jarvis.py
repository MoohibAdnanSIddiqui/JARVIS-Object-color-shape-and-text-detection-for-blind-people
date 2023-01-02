import time
import pyttsx3 
import cvlib as cv
from cvlib.object_detection import draw_bbox
import datetime
import cv2 
from pytesseract import pytesseract
import numpy as np
import speech_recognition as sr 
from tkinter import *
from PIL import ImageTk, Image


engine = pyttsx3.init() 
def speak(audio): 
    engine.say (audio) 
    engine.runAndWait() 
def wishMe() : 
    time2 = int (datetime.datetime.now().hour) 
    if time2 >= 0 and time2 < 12: 
        speak ("Good Morning, Hi i'm your voice assistance.") 
    elif time2 >= 12 and time2 < 18: 
        speak ("Good Afternoon, Hi i'm your voice assistance.") 
    else: 
        speak ("Good Evening, Hi i'm your voice assistance.") 
    
def takeCommand(): 
        r = sr. Recognizer() 
        
        with sr.Microphone () as source:
            print("Hello i'm your Voice Assistant . How can i help you Sir / Mam .") 
            print("I'm listening to what you're saying...") 
            r.pause_threshold = 1
            audio = r.listen(source, timeout=3, phrase_time_limit=3)
            
        try: 
            print ("Recognizing...") 
            query = r.recognize_google (audio, language='en-in') 
            print (f"You said: {query} \n") 
        
        except Exception as e: 
            print ("Would you mind repeating that?") 
            return "None" 
        return query 
def show_frames():
    cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image = img)
    label.imgtk = imgtk
    label.configure(image=imgtk)
    label.after(5, show_frames)
    label.place(anchor='center',relx=0.5,rely=0.5)



wishMe() 

from datetime import datetime

while True:

    query = takeCommand().lower() 

    if 'open locker' in query: 
        r = sr. Recognizer() 

        with sr.Microphone () as source: 
            print("I'm listening to what you're saying plz tell me your password...") 
            r.pause_threshold = 1
            audio = r.listen(source, timeout=3, phrase_time_limit=5)
        
        try: 
            print ("Recognizing...") 
            password = r.recognize_google (audio, language='en-in') 
            print (f"You said: {password} \n") 

        except Exception as e: 
            print ("Would you mind repeating that?")

        while True: 
            if password == "hello":
                speak("password open")
            
        
    elif 'shape' in query:
        speak("shape detection")
        camera = cv2.VideoCapture(0)
        while True:
            _,image=camera.read()
            cv2.imshow('Shape Detection',image)
            if cv2.waitKey(1) & 0xFF==ord("s"):
                cv2.imwrite('shapesample.jpg',image)
                break
        camera.release()
        cv2.destroyAllWindows()
        img = cv2.imread('shapesample.jpg')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(
            threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        i = 0
        for contour in contours:
            if i == 0:
                i = 1
                continue

            
            approx = cv2.approxPolyDP(
                contour, 0.01 * cv2.arcLength(contour, True), True)
            cv2.drawContours(img, [contour], 0, (0, 0, 255), 5)
            M = cv2.moments(contour)
            if M['m00'] != 0.0:
                x = int(M['m10']/M['m00'])
                y = int(M['m01']/M['m00'])

            if len(approx) == 3:
                cv2.putText(img, 'Triangle', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2) ,speak("Triangle")
                            
            elif len(approx) == 4:
                cv2.putText(img, 'Quadrilateral', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2),speak("Quadrilateral")

            elif len(approx) == 5:
                cv2.putText(img, 'Pentagon', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2),speak("Pentagon")

            elif len(approx) == 6:
                cv2.putText(img, 'Hexagon', (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2),speak("Hexagon")

                
        cv2.imshow('shapes', img)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    elif "object" in query:
        speak("Object detection")
        camera = cv2.VideoCapture(0)
        while True:
            _,image=camera.read()
            cv2.imshow('Object Detection',image)
            if cv2.waitKey(1) & 0xFF==ord("s"):
                cv2.imwrite('objectsample.jpg',image)
                break
        camera.release()
        cv2.destroyAllWindows()

        from IPython.display import Image, display
        def detect_and_draw_box(filename, model="yolov5x", confidence=0.6):
            img_filepath = f'{filename}'
            img = cv2.imread(img_filepath)
            bbox, label, conf = cv.detect_common_objects(img, confidence=confidence, model=model)
            for l, c in zip(label, conf):
                ac = round(c, 2)
                accuracy_percent = ac*100
                print(accuracy_percent)
                if accuracy_percent>40:
                    print(f"Detected object: {l} with accuray of {accuracy_percent}n")
                    speak(str(l)+"found with a accuracy of"+str(accuracy_percent)+"percent")
                output_image = draw_bbox(img, bbox, label, conf)
                cv2.imshow("object detection", output_image)
        detect_and_draw_box("objectsample.jpg", confidence=0.2)
    elif 'colour' in query:
        speak("Color Detection")
        camera = cv2.VideoCapture(0)
        while True:
            _,image=camera.read()
            cv2.imshow('Color Detection',image)
            if cv2.waitKey(1) & 0xFF==ord("s"):
                cv2.imwrite('colorsample.jpg',image)
                break
        camera.release()
        cv2.destroyAllWindows()
        while(1):
            imageFrame = cv2.imread("colorsample.jpg")
            hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
            red_lower = np.array([165, 95, 125], np.uint8)
            red_upper = np.array([180, 255, 255], np.uint8)
            red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

            green_lower = np.array([25, 52, 72], np.uint8)
            green_upper = np.array([102, 255, 255], np.uint8)
            green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

            blue_lower = np.array([94, 80, 2], np.uint8)
            blue_upper = np.array([120, 255, 255], np.uint8)
            blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)
            
            kernal = np.ones((5, 5), "uint8")
            
            # For red color
            red_mask = cv2.dilate(red_mask, kernal)
            res_red = cv2.bitwise_and(imageFrame, imageFrame,
                                    mask = red_mask)
            
            # For green color
            green_mask = cv2.dilate(green_mask, kernal)
            res_green = cv2.bitwise_and(imageFrame, imageFrame,
                                        mask = green_mask)
            
            # For blue color
            blue_mask = cv2.dilate(blue_mask, kernal)
            res_blue = cv2.bitwise_and(imageFrame, imageFrame,
                                    mask = blue_mask)

            # Creating contour to track red color
            contours, hierarchy = cv2.findContours(red_mask,
                                                cv2.RETR_TREE,
                                                cv2.CHAIN_APPROX_SIMPLE)
            
            for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if(area > 300):
                    x, y, w, h = cv2.boundingRect(contour)
                    imageFrame = cv2.rectangle(imageFrame, (x, y),
                                            (x + w, y + h),
                                            (0, 0, 255), 2)
                    
                    cv2.putText(imageFrame, "Red Colour", (x, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                                (0, 0, 255))	
                    speak("red color detected")
                    print("red")

            # Creating contour to track green color
            contours, hierarchy = cv2.findContours(green_mask,
                                                cv2.RETR_TREE,
                                                cv2.CHAIN_APPROX_SIMPLE)
            
            for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if(area > 300):
                    x, y, w, h = cv2.boundingRect(contour)
                    imageFrame = cv2.rectangle(imageFrame, (x, y),
                                            (x + w, y + h),
                                            (0, 255, 0), 2)
                    
                    cv2.putText(imageFrame, "Green Colour", (x, y),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1.0, (0, 255, 0))
                    speak("green color detected")
                    print("green")

            # Creating contour to track blue color
            contours, hierarchy = cv2.findContours(blue_mask,
                                                cv2.RETR_TREE,
                                                cv2.CHAIN_APPROX_SIMPLE)
            for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if(area > 300):
                    x, y, w, h = cv2.boundingRect(contour)
                    imageFrame = cv2.rectangle(imageFrame, (x, y),
                                            (x + w, y + h),
                                            (255, 0, 0), 2)
                    
                    cv2.putText(imageFrame, "Blue Colour", (x, y),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1.0, (255, 0, 0))
                    speak("blue color detected")
                    print("blue")
                    
            cv2.imshow("Color Detection ", imageFrame)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
    
    elif 'time' in query:          
        strTime = datetime.today().strftime("%H:%M %p")
        window = Tk()
        window.title("Time")
        window.geometry('1600x1000')
        frame = Frame(window, width=600, height=400)
        frame.place(anchor='center', relx=0.5, rely=0.5)
        img = ImageTk.PhotoImage(Image.open("obj.jpg"))
        label = Label(frame, image = img)
        label.pack()
        window.iconbitmap("favicon.ico")
        lbl = Label(window, text="               TIME                     ",font=("annai MN", 30,'bold'))
        lbl1=Label(window,text="Current Time "+str(strTime),font=("Arial Bold", 30,'bold'))
        window.wm_attributes('-fullscreen', 'false')
        lbl.place(anchor='center', relx=0.5, rely=0.08)
        lbl1.place(anchor='center', relx=0.5, rely=0.3)
        label =Label(window)
        label.place(anchor='center',relx=0.6,rely=0.5)
        window.mainloop()
        print (f"The current time is {strTime}") 
        speak (f"The current time is {strTime}")

    elif 'text' in query: 
        speak("text detection")
        camera = cv2.VideoCapture(0)
        while True:
            _,image=camera.read()
            cv2.imshow('Text Detection',image)
            if cv2.waitKey(1) & 0xFF==ord("s"):
                cv2.imwrite('sample.jpg',image)
                break
        camera.release()
        cv2.destroyAllWindows()

        im = Image.open("sample.jpg")

        text = pytesseract.image_to_string(im, lang = 'eng')

        speak(text)
    elif 'open camera' in query:
        speak("opening camera")
        window = Tk()
        window.title("Camera")
        window.geometry('1600x1000')
        frame = Frame(window, width=600, height=400)
        frame.place(anchor='center', relx=0.5, rely=0.5)
        img = ImageTk.PhotoImage(Image.open("obj.jpg"))
        label = Label(frame, image = img)
        label.pack()
        window.iconbitmap("favicon.ico")
        lbl = Label(window, text="                CAMERA                       ",font=("annai MN", 30,'bold'))
        window.wm_attributes('-fullscreen', 'false')
        lbl.place(anchor='center', relx=0.5, rely=0.08)

        label =Label(window)
        cap= cv2.VideoCapture(0)

        
        show_frames()
        window.mainloop()
    elif 'thank you' in query: 
        speak ("My pleasure sir") 
            

    elif 'bye' in query:
        window = Tk()
        window.title("Bye. See you soon")
        window.geometry('1600x1000')
        frame = Frame(window, width=600, height=400)
        frame.place(anchor='center', relx=0.5, rely=0.5)
        img = ImageTk.PhotoImage(Image.open("obj.jpg"))
        label = Label(frame, image = img)
        label.pack()
        window.iconbitmap("favicon.ico")
        lbl = Label(window, text="                       Bye. See you soon                              ",font=("annai MN", 50,'bold'))
        window.wm_attributes('-fullscreen', 'false')
        lbl.place(anchor='center', relx=0.5, rely=0.5)
        label =Label(window)
        cap= cv2.VideoCapture(0)
        window.mainloop()
        speak ("Bye. See you soon") 
        quit()