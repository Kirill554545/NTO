import cv2
import numpy as np
import math

# Загрузка видеопотока (может быть заменено на чтение изображения или видеофайла)
cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
color_blue = (255, 0, 0)
color_yellow = (0, 255, 255)

while True:
    # Считывание кадра
    ret, frame = cap.read()
    if not ret:
        break

    # Преобразование кадра в оттенки серого
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Применение детектора границ Canny
    edges = cv2.Canny(gray, 50, 150)

    # Применение преобразования Хафа для обнаружения линий
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=10, maxLineGap=10)

    # Нарисовать обнаруженные линии на исходном изображении и вычислить углы
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Вычисление вектора линии
            usedEdge = np.array([x2 - x1, y2 - y1])

            # Вычисление угла между линией и горизонтальным вектором
            '''reference = np.array([1, 0])  # горизонтальный вектор, задающий горизонт
            if np.linalg.norm(reference) * np.linalg.norm(usedEdge) != 0:
                angle = 180.0 / math.pi * math.acos(
                    (reference[0] * usedEdge[0] + reference[1] * usedEdge[1]) / (
                            np.linalg.norm(reference) * np.linalg.norm(usedEdge)))

            # Вычисление центра линии
            center = ((x1 + x2) // 2, (y1 + y2) // 2)

            # Отображение маленького кружка в центре линии
            cv2.circle(frame, center, 5, color_yellow, 2)

            # Вывод величины угла наклона
            cv2.putText(frame, "%d" % int(angle), (center[0] + 20, center[1] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color_yellow, 2)'''

    # Показать результат
    cv2.imshow('Detected Lines', frame)

    # Остановка цикла при нажатии клавиши 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Освобождение ресурсов
cap.release()
cv2.destroyAllWindows()
