import cv2
import os

def images_to_video(input_folder, output_video):
    images = [img for img in os.listdir(input_folder) if img.endswith(".png")]

    frame = cv2.imread(os.path.join(input_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*'mp4v'), 1, (width,height))

    for image in images:
        video.write(cv2.imread(os.path.join(input_folder, image)))

    cv2.destroyAllWindows()
    video.release()

input_folder = "img"
output_video = "video.mp4"

images_to_video(input_folder, output_video)
