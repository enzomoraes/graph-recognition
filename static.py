import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

# Function to update parameters when "Apply" button is clicked
def update_params():
    global minDist, param1, param2, minRadius, maxRadius, cap, frame_copy
    
    # Get parameter values from text entry widgets
    minDist = int(minDist_entry.get())
    param1 = int(param1_entry.get())
    param2 = int(param2_entry.get())
    minRadius = int(minRadius_entry.get())
    maxRadius = int(maxRadius_entry.get())

    # Create a copy of the original frame
    frame_copy = cap.copy()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2GRAY)

    # Apply bilateral filter for noise reduction
    blurred = cv2.GaussianBlur(gray, (7, 7), 1.5)

    # Detect circles using Hough Transform with updated parameters
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT_ALT, 1, minDist,
                               param1=param1, param2=param2,
                               minRadius=minRadius, maxRadius=maxRadius)

    # Draw detected circles on the frame copy
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            cv2.circle(frame_copy, (i[0], i[1]), i[2], (0, 255, 0), 2)

    # Display the resulting frame
    display_image(frame_copy)

# Function to display image in Tkinter window
def display_image(image):
    image = rescale_image(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor=tk.NW, image=image)
    canvas.image = image

def rescale_image(image):
    wProportion = WINDOW_WIDTH / image.shape[1]
    hProportion = WINDOW_HEIGHT / image.shape[0]
    
    width = int(image.shape[1] * wProportion)
    height = int(image.shape[0] * hProportion)
    dimensions = (width, height)

    return cv2.resize(image, dimensions, interpolation=cv2.INTER_AREA)

# Load the image
cap = cv2.imread('grafo2.jpeg')

# Initialize parameters
minDist = 204
param1 = 21
param2 = 62
minRadius = 18
maxRadius = 0

# Create a copy of the original frame
frame_copy = cap.copy()

# Create Tkinter window
root = tk.Tk()
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
root.title("Circle Detection Parameters")

# Create canvas to display image
canvas = tk.Canvas(root, width=frame_copy.shape[1], height=frame_copy.shape[0])
canvas.pack()

# Create labels and entry widgets for parameters
minDist_label = tk.Label(root, text="minDist:")
minDist_label.place(x=10, y=10)
minDist_entry = tk.Entry(root)
minDist_entry.insert(0, str(minDist))
minDist_entry.place(x=70, y=10)

param1_label = tk.Label(root, text="param1:")
param1_label.place(x=10, y=40)
param1_entry = tk.Entry(root)
param1_entry.insert(0, str(param1))
param1_entry.place(x=70, y=40)

param2_label = tk.Label(root, text="param2:")
param2_label.place(x=10, y=70)
param2_entry = tk.Entry(root)
param2_entry.insert(0, str(param2))
param2_entry.place(x=70, y=70)

minRadius_label = tk.Label(root, text="minRadius:")
minRadius_label.place(x=10, y=100)
minRadius_entry = tk.Entry(root)
minRadius_entry.insert(0, str(minRadius))
minRadius_entry.place(x=70, y=100)

maxRadius_label = tk.Label(root, text="maxRadius:")
maxRadius_label.place(x=10, y=130)
maxRadius_entry = tk.Entry(root)
maxRadius_entry.insert(0, str(maxRadius))
maxRadius_entry.place(x=70, y=130)

# Create "Apply" button
apply_button = tk.Button(root, text="Apply", command=update_params)
apply_button.place(x=10, y=160)

# Display initial image
display_image(frame_copy)

# Start Tkinter event loop
root.mainloop()
