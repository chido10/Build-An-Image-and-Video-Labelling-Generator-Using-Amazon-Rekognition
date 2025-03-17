import boto3
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
from io import BytesIO
import matplotlib
matplotlib.use('TkAgg')  # Add this line at the top after imports

def detect_labels(photo, bucket):
    try:
        # Create a Rekognition client
        client = boto3.client('rekognition', region_name='eu-west-2')

        # Detect labels in the photo
        response = client.detect_labels(
            Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
            MaxLabels=10)

        # Print detected labels
        print(f'Detected labels for {photo}')
        print()
        for label in response['Labels']:
            print(f"Label: {label['Name']}")
            print(f"Confidence: {label['Confidence']:.2f}%")
            print()

        # Load the image from S3
        s3 = boto3.client('s3', region_name='eu-west-2')
        img_data = s3.get_object(Bucket=bucket, Key=photo)['Body'].read()
        img = Image.open(BytesIO(img_data))

        # Create a new figure for each image
        plt.figure(figsize=(12, 8))
        plt.imshow(img)
        ax = plt.gca()
        
        for label in response['Labels']:
            for instance in label.get('Instances', []):
                bbox = instance['BoundingBox']
                left = bbox['Left'] * img.width
                top = bbox['Top'] * img.height
                width = bbox['Width'] * img.width
                height = bbox['Height'] * img.height
                rect = patches.Rectangle((left, top), width, height, linewidth=2, 
                                      edgecolor='r', facecolor='none')
                ax.add_patch(rect)
                label_text = f"{label['Name']} ({label['Confidence']:.2f}%)"
                plt.text(left, top - 5, label_text, color='r', fontsize=10, 
                        bbox=dict(facecolor='white', alpha=0.7))
        
        plt.title(f'Analysis Results - {photo}')
        plt.axis('off')
        plt.show(block=False)  # Changed to non-blocking
        plt.pause(5)  # Show the image for 5 seconds
        plt.close()  # Close the window after 5 seconds

        return len(response['Labels'])
    
    except Exception as e:
        print(f"Error processing {photo}: {str(e)}")
        return 0

def analyze_multiple_images():
    bucket = 'my-aws-practical-projects'
    photos = ['pic1.png', 'pic2.png']
    
    for photo in photos:
        print('=' * 50)
        label_count = detect_labels(photo, bucket)
        print(f"Total labels detected in {photo}: {label_count}")
        print('=' * 50)
        print()
        plt.pause(1)  # Add small pause between images

if __name__ == "__main__":
    analyze_multiple_images()
    print("Analysis complete. Press Enter to exit.")
    input()  # Wait for user input before closing