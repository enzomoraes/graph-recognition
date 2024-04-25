import numpy as np
import cv2

# Function to update parameters when trackbars are moved
def update_params(x):
    global minDist, param1, param2, minRadius, maxRadius
    minDist = cv2.getTrackbarPos('minDist', 'Parameters')
    param1 = cv2.getTrackbarPos('param1', 'Parameters')
    param2 = cv2.getTrackbarPos('param2', 'Parameters')
    minRadius = cv2.getTrackbarPos('minRadius', 'Parameters')
    maxRadius = cv2.getTrackbarPos('maxRadius', 'Parameters')

# Initialize video capture from the webcam
cap = cv2.VideoCapture(0)  # 0 corresponds to the default webcam, change it if you have multiple cameras

# Create a window for parameter adjustment
cv2.namedWindow('Parameters')

# Create trackbars for parameter adjustment
cv2.createTrackbar('minDist', 'Parameters', 100, 500, update_params)
cv2.createTrackbar('param1', 'Parameters', 20, 100, update_params)
cv2.createTrackbar('param2', 'Parameters', 60, 300, update_params)
cv2.createTrackbar('minRadius', 'Parameters', 0, 100, update_params)
cv2.createTrackbar('maxRadius', 'Parameters', 0, 100, update_params)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Failed to capture frame")
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply bilateral filter for noise reduction
    blurred = cv2.bilateralFilter(gray, 10, 50, 50)

    # Detect circles using Hough Transform with updated parameters
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1, minDist,
                               param1=param1, param2=param2,
                               minRadius=minRadius, maxRadius=maxRadius)

    # Draw detected circles on the frame
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Frame', frame)

    # Check for user input to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()