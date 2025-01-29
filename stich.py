import cv2
import numpy as np
import os
import imutils as im

# Function to stitch frames into a panorama
def stitch_frames(frames):
    # Initialize stitcher
    stitcher = cv2.Stitcher_create()
    
    # Stitch frames
    status, stitched_img = stitcher.stitch(frames)
    
    if status == cv2.Stitcher_OK:
        return stitched_img
    else:
        print("Stitching failed!")
        return None

# Function to process video and stitch frames
def process_photos():
    # Open the video file
    # List to store frames
    frames = []
    image_dir_path = "site1"
    files = os.listdir(image_dir_path)
    for j in range(0, 3):
        i = files[j]
        imagePath = os.path.join(image_dir_path, i)
        frame = cv2.imread(imagePath)
        if frame is not None:  # Ensure the frame is read properly
            frames.append(frame)
        else:
            print(f"Failed to load image: {imagePath}")
    
    # Stitch frames into a panorama
    stitched_img = stitch_frames(frames)

    return stitched_img

# Function to resize image to 3:1 aspect ratio
def resize_to_aspect_ratio(image, aspect_ratio=(3, 1)):
    height, width = image.shape[:2]
    target_width = int(height * aspect_ratio[0] / aspect_ratio[1])
    
    # Resize the image while maintaining the aspect ratio
    resized_image = cv2.resize(image, (target_width, height))
    return resized_image

# Main function
def main():
    stitched_img = process_photos()

    if stitched_img is None:
        print("Stitching failed. Exiting program.")
        return

    stitched = cv2.copyMakeBorder(stitched_img, 10, 10, 10, 10, cv2.BORDER_CONSTANT, (0, 0, 0))
    
    if stitched is None:
        print("Error in stitched image.")
        return
    
    # Check if the image is in the expected format (3 channels, BGR)
    if len(stitched.shape) == 3 and stitched.shape[2] == 3:
        gray = cv2.cvtColor(stitched, cv2.COLOR_BGR2GRAY)
    else:
        print("Stitched image is not in the expected BGR format.")
        return
    
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = im.grab_contours(cnts)
    
    if cnts:  # Check if contours were found
        c = max(cnts, key=cv2.contourArea)
        mask = np.zeros(thresh.shape, dtype="uint8")
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)
        minRect = mask.copy()
        sub = mask.copy()
        while cv2.countNonZero(sub) > 1500:
            minRect = cv2.erode(minRect, None)
            sub = cv2.subtract(minRect, thresh)
        
        cnts = cv2.findContours(minRect.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = im.grab_contours(cnts)
        if cnts:
            c = max(cnts, key=cv2.contourArea)
            (x, y, w, h) = cv2.boundingRect(c)

            stitched = stitched[y:y + h, x:x + w]
            
            # Resize the image to a 3:1 aspect ratio
            stitched_resized = resize_to_aspect_ratio(stitched)
            
            print(y, h, x, w)
            print(stitched_resized.shape)
            
            # Display the resized stitched image
            cv2.imshow("Stitched Image (3:1 Aspect Ratio)", stitched_resized)
            
            # Save the image
            output_file = "stitched_image_3_1_aspect_ratio.jpg"
            cv2.imwrite(output_file, stitched_resized)
            print(f"Image saved as {output_file}")
            
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    else:
        print("No contours found.")

if __name__ == "__main__":
    main()
