import numpy as np
import cv2

C_W = 1     # Contour drawing width
CS_W = 2    # Contour success drawing width

# Color constants
PINK = (255, 0, 255)
YELLOW = (0, 255, 255)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # Gray
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Gaussian Filter (Blur)
    gauss = cv2.GaussianBlur(gray, (5, 5), 1)

    # Canny
    canny = cv2.Canny(gauss, 100, 200)

    # Find contours
    _, hierarchy = cv2.threshold(canny, 240, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(hierarchy, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # Iterate contours
    for contour in contours:

        # Calculate contour area
        area = cv2.contourArea(contour)

        # Draw contour
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        cv2.drawContours(frame, [approx], -1, PINK, C_W)
        x = approx.ravel()[0]
        y = approx.ravel()[1] - 5

        if area > 1000:
            # If TRIANGLE
            if len(approx) == 3:
                cv2.putText(frame, 'TRIANGLE', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, YELLOW)
                cv2.drawContours(frame, [approx], -1, YELLOW, CS_W)
            # If RECTANGLE
            elif len(approx) == 4:
                cv2.putText(frame, 'RECTANGLE', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, YELLOW)
                cv2.drawContours(frame, [approx], -1, YELLOW, CS_W)
            # If PENTAGON
            # elif len(approx) == 5:
            #     cv2.putText(frame, 'PENTAGON', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, YELLOW)
            #     cv2.drawContours(frame, [approx], -1, YELLOW, CS_W)
            # If HEXAGON
            # elif len(approx) == 6:
            #     cv2.putText(frame, 'HEXAGON', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, YELLOW)
            #     cv2.drawContours(frame, [approx], -1, YELLOW, CS_W)
            # If CIRCLE
            elif len(approx) > 10:
                cv2.putText(frame, 'CIRCLE', (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, YELLOW)
                cv2.drawContours(frame, [approx], -1, YELLOW, CS_W)

    # Show images
    cv2.imshow('frame', frame)
    cv2.imshow('canny', canny)

    # Wait for key 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
