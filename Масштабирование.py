import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# Переменные для хранения предыдущего размера ограничивающего прямоугольника
prev_x = 0
prev_y = 0
prev_w = 0
prev_h = 0

# Создайте окно с именем 'frame'
cv2.namedWindow('frame', cv2.WINDOW_NORMAL)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([110, 50, 50])
    upper_blue = np.array([130, 255, 255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    centers = []

    for contour in contours:
        if cv2.mean(frame[contour[:, :, 1], contour[:, :, 0]])[0] > 10:
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                centers.append((cX, cY))

    if len(centers) > 1:
        x, y, w, h = cv2.boundingRect(np.array(centers))

        # Измените размер окна до размеров ограничивающего прямоугольника
        cv2.resizeWindow('frame', w, h)

        # Отобразите обрезанный кадр в окне с измененным размером
        cv2.imshow('frame', frame[y:y+h, x:x+w])

        # Сохраните текущий размер ограничивающего прямоугольника
        prev_x = x
        prev_y = y
        prev_w = w
        prev_h = h

        # Переместите окно
        cv2.moveWindow('frame', prev_x + 10, prev_y + 10)

    else:
        # Отобразите исходный кадр, если синих объектов не обнаружено
        cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()