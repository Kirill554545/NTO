import cv2
import numpy as np
import time
import open3d as o3d


# Функция для калибровки проекции на неровной поверхности
def calibrate_projection(img, depth_map):
    pcd = o3d.geometry.PointCloud.create_from_depth_image(depth_map, intrinsic=o3d.camera.PinholeCameraIntrinsic(
        width=img.shape[1], height=img.shape[0], fx=500, fy=500, cx=img.shape[1] / 2, cy=img.shape[0] / 2),
                                                          depth_scale=0.1, depth_trunc=10)
    o3d.visualization.draw_geometries([pcd])


# Открытие видеопотока с камеры
cap = cv2.VideoCapture(0)

# Чтение диспаритетной карты. В реальном времени может потребоваться другой метод для получения карты глубины
depth_map = cv2.imread('depth_map.jpg', cv2.IMREAD_GRAYSCALE)

while True:
    ret, frame = cap.read()

    if ret:
        # Показ изображения с камеры
        cv2.imshow('Camera Image', frame)

        # Калибровка проекции на неровной поверхности
        calibrate_projection(frame, depth_map)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
