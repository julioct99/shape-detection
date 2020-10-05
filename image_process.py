# AUTOR: Julio Casallo Tamayo

import cv2
import numpy as np

C_W = 1     # Contour drawing width
CS_W = 2    # Contour success drawing width
F_S = 0.75  # Text font scale

# Color constants
PINK = (255, 0, 255)
YELLOW = (0, 255, 255)

def find_contorno(img,sal):
    salida = sal.copy()

    # Find contours
    _, hierarchy = cv2.threshold(img, 240, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(hierarchy, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # Iterate contours
    for contour in contours:

        # Calculate contour area
        area = cv2.contourArea(contour)

        # Draw contour
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        cv2.drawContours(salida, [approx], -1, PINK, C_W)
        x = approx.ravel()[0]
        y = approx.ravel()[1] - 5

        if area > 1000:
            # If TRIANGLE
            if len(approx) == 3:
                cv2.putText(salida, 'TRIANGLE', (x, y), cv2.FONT_HERSHEY_COMPLEX, F_S, YELLOW)
                cv2.drawContours(salida, [approx], -1, YELLOW, CS_W)
            # If RECTANGLE
            elif len(approx) == 4:
                (X, Y, W, H) = cv2.boundingRect(approx)
                # Se compara que la proporcion entre ancho y alto sea APROXIMADAMENTE 1
                proportion = float(W) / H
                if proportion > 0.9 and proportion < 1.1:
                    cv2.putText(salida, 'SQUARE', (x, y), cv2.FONT_HERSHEY_COMPLEX, F_S, YELLOW)
                    cv2.drawContours(salida, [approx], -1, YELLOW, CS_W)
                else:
                    cv2.putText(salida, 'RECTANGLE', (x, y), cv2.FONT_HERSHEY_COMPLEX, F_S, YELLOW)
                    cv2.drawContours(salida, [approx], -1, YELLOW, CS_W)  
            # If PENTAGON
            elif len(approx) == 5:
                cv2.putText(salida, 'PENTAGON', (x, y), cv2.FONT_HERSHEY_COMPLEX, F_S, YELLOW)
                cv2.drawContours(salida, [approx], -1, YELLOW, CS_W)
            # If HEXAGON
            elif len(approx) == 6:
                cv2.putText(salida, 'HEXAGON', (x, y), cv2.FONT_HERSHEY_COMPLEX, F_S, YELLOW)
                cv2.drawContours(salida, [approx], -1, YELLOW, CS_W)
            # If CIRCLE
            elif len(approx) > 10:
                cv2.putText(salida, 'CIRCLE', (x, y), cv2.FONT_HERSHEY_COMPLEX, F_S, YELLOW)
                cv2.drawContours(salida, [approx], -1, YELLOW, CS_W)

    return salida
