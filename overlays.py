import cv2
import numpy as np

cap = cv2.VideoCapture(2)
key_pressed = False
image = None
images = []
count = 0
count1 = 0

# Function to add overlay with needle

def add_overlay(image, angle, lat, long, elevation):
    color = (0, 0, 255)
    h, w = image.shape[:2]
    
    # Basic GPS Information Overlay
    image = cv2.putText(image, 'N', (70, 30), cv2.FONT_HERSHEY_TRIPLEX, 0.5, color, 1, cv2.LINE_AA)
    image = cv2.putText(image, 'W', (20, 75), cv2.FONT_HERSHEY_TRIPLEX, 0.5, color, 1, cv2.LINE_AA)
    image = cv2.putText(image, 'E', (120, 75), cv2.FONT_HERSHEY_TRIPLEX, 0.5, color, 1, cv2.LINE_AA)
    image = cv2.putText(image, 'S', (70, 120), cv2.FONT_HERSHEY_TRIPLEX, 0.5, color, 1, cv2.LINE_AA)
    
    image = cv2.putText(image, f'GPS: Latitude: {lat}', (200, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    image = cv2.putText(image, f'GPS: Longitude: {long}', (200, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    image = cv2.putText(image, f'Elevation: {elevation}', (200, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    
    # Read and Rotate Needle Image
    overlay_image = cv2.imread('/home/aditi/science/science/scripts/needle2.png', cv2.IMREAD_UNCHANGED)
    overlay_image = cv2.resize(overlay_image, (70, 70))
    row, col, _ = overlay_image.shape
    center = tuple(np.array([row, col]) / 2)
    rot_mat = cv2.getRotationMatrix2D(center, (-1.0) * angle, 1.0)
    overlay_image = cv2.warpAffine(overlay_image, rot_mat, (col, row))

    x_pos, y_pos = 40, 38
    needle_image = image.copy()

    for y in range(overlay_image.shape[0]):
        for x in range(overlay_image.shape[1]):
            if overlay_image[y, x, 3] > 0:
                needle_image[y + y_pos, x + x_pos] = overlay_image[y, x][:3]

    return needle_image

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    cv2.imshow("Video Feed", frame)
    key = cv2.waitKey(1)

    if key == ord('c'):
        key_pressed = True
        image = frame.copy()
        count += 1
        angle = 90
        lat, long, elevation = 12.9716, 77.5946, 300  # Example GPS Data
        image = add_overlay(image, angle, lat, long, elevation)
        cv2.imshow("Captured Image", image)
        
        image_filename = f"pic{count}.jpg"
        cv2.imwrite(image_filename, image)
        print(f"Image {count} captured and saved as {image_filename}")

    if key == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break