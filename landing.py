import cv2
import numpy as np

def is_flat_surface(contour, epsilon=0.02):
    # Аппроксимируем контур, чтобы упростить его
    approx = cv2.approxPolyDP(contour, epsilon * cv2.arcLength(contour, True), True)
    
    return len(approx) == 4

def find_landing_zone(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # уменьшение шумов
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Детектируем края (edges)
    edges = cv2.Canny(blurred, 50, 150)

    # Находим контуры на изображении
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    landing_zones = []

    # Проверяем каждый контур
    for contour in contours:
        area = cv2.contourArea(contour)

        # Игнорируем слишком маленькие или слишком большие контуры
        if area < 1000 or area > 50000:
            continue

        # Проверяем, является ли контур плоской и ровной зоной (примерно прямоугольник)
        if is_flat_surface(contour):
            landing_zones.append(contour)

    return landing_zones

def process_video_stream(video_source=0):
    cap = cv2.VideoCapture(video_source)

    if not cap.isOpened():
        print("Ошибка при открытии видеопотока.")
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Не удалось получить кадр.")
            break

        # поиск посадочных зон в кадре
        landing_zones = find_landing_zone(frame)

        # отображение посадочных зон
        for zone in landing_zones:
    
            cv2.drawContours(frame, [zone], -1, (0, 255, 0), 3)

        cv2.imshow("Landing Zone Detection", frame)

        # Выход по нажатию клавиши 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    process_video_stream(0) 