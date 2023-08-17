import cv2
import pickle
import cvzone
import numpy as np

# Adding the video
cap = cv2.VideoCapture("Car_Parking.mp4")

# Uploading the previously loaded positions
with open("CarParkPos", "rb") as f:
    pos_list = pickle.load(f)

# Dimensions of each box of the parking
width, height = 107, 48


# Checking the Parking Space
def check_Parking_Space(imgPro):
    # Counter for number of free spaces in park
    space_counter = 0

    for pos in pos_list:
        x, y = pos

        # Crop the image for each parking space
        img_crop = imgPro[y:y+height, x:x+width]

        # Count the number white line pixels
        count = cv2.countNonZero(img_crop)

        # Display the number of non-zeros with each park space
        cvzone.putTextRect(img, str(count), (x, y+height-3), scale=1, thickness=2, offset=1, colorR=(0, 0, 255))

        # Checking of Car presence if non-zero count value above 800
        if count < 800:
            color = (0, 255, 0)
            thickness = 5
            space_counter += 1
        else:
            color = (0, 0, 255)
            thickness = 2

        # Drawing the rectangle around each park space
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)

    # Displaying the number of spaces available
    cvzone.putTextRect(img, f"Free :- {space_counter}/{len(pos_list)}", (100, 50), scale=3, thickness=5, offset=20, colorR=(0, 200, 0))


while True:
    # Loop the video continuously
    # Current frame == Total number of frames
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        # Again set the frame to 0 to start form first
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # Capturing the Video frame by frame
    success, img = cap.read()

    # Converting frame to GrayScale
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Add blur to the image
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)

    # Convert image to Binary image
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)

    # Convert Binary image to Median Binary Image
    imgMedian = cv2.medianBlur(imgThreshold, 5)

    # Dilate the Median Image to make the white lines thicker
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    # For displaying the positions
    check_Parking_Space(imgDilate)

    # For displaying the video frame by frame
    cv2.imshow("Image", img)
    cv2.waitKey(5)
