import cv2
import requests
import numpy as np
import os
import time

# URL of the video stream
STREAM_URL = "http://192.168.234.121:5000/video1"  # Replace with your server's URL

# Create the site1 directory if it doesn't exist
site_directory = "site1"
if not os.path.exists(site_directory):
    os.makedirs(site_directory)

# Connect to the video stream
response = requests.get(STREAM_URL, stream=True)

if response.status_code == 200:
    print("Successfully connected to the stream. Press 's' to save images, 'q' to quit.")
    byte_stream = b''
    screenshot_count = 1

    for chunk in response.iter_content(chunk_size=1024):
        byte_stream += chunk
        start = byte_stream.find(b'\xFF\xD8')  # Start of JPEG
        end = byte_stream.find(b'\xFF\xD9')    # End of JPEG

        if start != -1 and end != -1:
            # Extract JPEG data
            jpg_data = byte_stream[start:end+2]
            byte_stream = byte_stream[end+2:]

            # Decode the JPEG image
            frame = cv2.imdecode(np.frombuffer(jpg_data, dtype=np.uint8), cv2.IMREAD_COLOR)

            if frame is not None:
                cv2.imshow('Camera Stream', frame)

                # Check for key presses
                key = cv2.waitKey(1) & 0xFF

                if key == ord('s'):  # Save image when 's' is pressed
                    file_name = f"{site_directory}/image{screenshot_count}.jpg"
                    cv2.imwrite(file_name, frame)
                    print(f"Saved: {file_name}")
                    screenshot_count += 1
                    time.sleep(0.1)  # Adjust the interval (in seconds) between captures if needed

                if key == ord('q'):  # Quit the program
                    print("Exiting...")
                    break
else:
    print(f"Failed to connect to stream. HTTP Status Code: {response.status_code}")

cv2.destroyAllWindows()
