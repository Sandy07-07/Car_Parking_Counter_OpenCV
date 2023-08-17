import cv2
import pickle

# Dimensions of each box of the parking
width, height = 107, 48

# Get the current pos_list from the pickle file else create a new one
try:
    with open("CarParkPos", "rb") as f:
        pos_list = pickle.load(f)
except:
    pos_list = []


# To mark the space by clicking of mouse
def mouseClick(events, x, y, flags, params):
    # Draw a new rectangle on left click of mouse
    if events == cv2.EVENT_LBUTTONDOWN:
        pos_list.append((x, y))

    # Delete the existing rectangle on right click of mouse
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(pos_list):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                pos_list.pop(i)


while True:
    # As image needs to read multiple times to update the results
    img = cv2.imread("Car_Parking.png")

    # Create a rectangle for each space
    for pos in pos_list:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    # Show the image
    cv2.imshow("Image", img)

    # Capture mouse movement
    cv2.setMouseCallback("Image", mouseClick)

    # Give a delay
    cv2.waitKey(1)
