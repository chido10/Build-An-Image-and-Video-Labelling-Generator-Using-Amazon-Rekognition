import boto3
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def analyze_video_frames(video_path, bucket, fps=1):
    # Open the video
    cap = cv2.VideoCapture(video_path)
    rekognition = boto3.client('rekognition', region_name='eu-west-2')
    frame_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        # Only analyze every nth frame based on fps
        if frame_count % int(cap.get(cv2.CAP_PROP_FPS) / fps) == 0:
            # Convert frame to jpg
            _, buffer = cv2.imencode('.jpg', frame)
            image_bytes = buffer.tobytes()
            
            # Detect labels with bounding boxes
            response = rekognition.detect_labels(
                Image={'Bytes': image_bytes},
                MaxLabels=10,
                MinConfidence=60
            )
            
            # Draw bounding boxes
            plt.figure(figsize=(15, 10))
            plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            ax = plt.gca()
            
            for label in response['Labels']:
                for instance in label.get('Instances', []):
                    bbox = instance['BoundingBox']
                    left = bbox['Left'] * frame.shape[1]
                    top = bbox['Top'] * frame.shape[0]
                    width = bbox['Width'] * frame.shape[1]
                    height = bbox['Height'] * frame.shape[0]
                    
                    # Draw rectangle
                    rect = patches.Rectangle(
                        (left, top), width, height,
                        linewidth=2, edgecolor='r', facecolor='none'
                    )
                    ax.add_patch(rect)
                    
                    # Add label
                    plt.text(
                        left, top - 2,
                        f"{label['Name']} ({label['Confidence']:.1f}%)",
                        color='red',
                        bbox=dict(facecolor='white', alpha=0.8)
                    )
            
            plt.title(f'Frame {frame_count} - Time: {frame_count/cap.get(cv2.CAP_PROP_FPS):.2f}s')
            plt.axis('off')
            plt.show()
            
        frame_count += 1
    
    cap.release()

# Use the function
video_path = "video1_converted.mp4"  # Path to your converted video
bucket = "my-aws-practical-projects"
analyze_video_frames(video_path, bucket, fps=1)  # Analyze 1 frame per second