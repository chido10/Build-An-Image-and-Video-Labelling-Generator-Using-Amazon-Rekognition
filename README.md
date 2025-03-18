# Build-An-Image-and-Video-Labelling-Generator-Using-Amazon-Rekognition

## Architectural Diagram
![image](https://github.com/user-attachments/assets/66e07768-1c5d-49ee-a0be-396443d2fc30)

*This diagram illustrates an image/video analysis workflow using AWS Rekognition. It shows how a developer, using local tools (Python SDK and AWS CLI), connects to AWS cloud services to process media files. The workflow begins with authentication through IAM, followed by uploading media to S3 storage. The core functionality displays how Amazon Rekognition analyzes these files from S3 and returns various results like labels, object detection, face recognition, and text extraction. The diagram clearly separates the local development environment from the AWS cloud platform, showing the complete data flow from media upload to analysis results.*

---

## Introduction to AWS Rekognition
**Amazon Rekognition** is a cloud-based image and video analysis service that adds computer vision capabilities to your applications without requiring deep learning expertise. It uses pre-trained deep learning models to identify thousands of objects, scenes, faces, text, and even inappropriate content in images and videos.

**Key Features:**
- **Image Analysis:** Detect labels (objects, scenes, concepts), faces, celebrity identities, text, and unsafe content in photos.  
- **Video Analysis:** Track objects over time, detect activities, and flag inappropriate content in frames.  
- **Face Analysis:** Identify attributes like emotions, age range, and gender.  
- **Use Cases:**  
  - Searchable media libraries (extracting labels to make content searchable)  
  - Security and authentication (face-based user verification)  
  - Content moderation  
  - People counting in footage  
  - Detecting personal protective equipment in workplace images

Because Rekognition is fully managed, developers can leverage these vision features via APIs without building or training models.

![image](https://github.com/user-attachments/assets/06099266-5833-4f04-a392-590d5410ed67)

---

## Setting Up AWS Rekognition and IDE

1. **Create an AWS Account** if you don’t already have one.  
2. **Choose a Region** that supports Rekognition (check the [AWS Region Table](https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/) for availability).
3. **Create an S3 Bucket** to store images and videos for analysis.  
   - Rekognition supports JPEG/PNG for images, MP4/MOV (H.264 codec) for videos.
4. **Configure IAM Roles/Permissions:**  
   - If calling Rekognition from AWS Lambda or EC2, create an **IAM execution role** with permissions for Rekognition and S3.  
   - If calling from your local machine (via AWS CLI or Boto3), create an **IAM user** with programmatic access and attach policies like **AmazonRekognitionFullAccess** and **AmazonS3ReadOnlyAccess**.  
5. **Configure AWS Credentials:**  
   - Use `aws configure` in your terminal or set up `~/.aws/credentials` for SDKs.  
   - Make sure your region matches the S3 bucket’s region.  

In this project, we’ll mainly use **AWS CLI** from a local environment (VS Code) with credentials for Rekognition access.

![image](https://github.com/user-attachments/assets/113c09fc-02a7-4f10-8bf0-7d06913aa735)  
![image](https://github.com/user-attachments/assets/ec50a42d-0a97-4e1a-93d3-011025e00d41)

---

## Using AWS CLI and IAM
1. **Create an IAM User:**  
   - Navigate to **IAM** → **Users** → **Create User**.  
   - Provide a username, select “Attach policies directly,” and attach **AdministratorAccess** (for demo).  
   - Ideally, use **least-privilege** policies in production.
2. **Generate Access Keys:**  
   - Under “Security Credentials,” create an **Access Key** for CLI usage.  
   - Download or securely store these keys (Access Key ID and Secret).
3. **Configure AWS CLI in VSCode**  
   ```bash
   aws configure
   ```
   - Enter your **Access Key ID** and **Secret Access Key**.  
   - Set default region (e.g., `us-east-1`) and default output (e.g., `json`).  

![image](https://github.com/user-attachments/assets/22163d0f-29fd-473d-9840-8e24685bc156)  
![image](https://github.com/user-attachments/assets/9c0139de-b841-41d1-ba5b-b6c18bca2512)  
![image](https://github.com/user-attachments/assets/6db9c2e2-2ea4-4c89-825e-61ca426f23b3)  
![image](https://github.com/user-attachments/assets/c69f8fb2-8dbd-42f2-aad1-c11f0b2b7ce7)  
![image](https://github.com/user-attachments/assets/29d3d118-5d21-4561-ac56-2dd2ebe96873)

---

## Image Analysis with AWS Rekognition

### Workflow
1. Upload an image (JPEG or PNG) to **Amazon S3**.  
2. Call **Rekognition’s detect_labels** API (via AWS SDK or AWS CLI) to analyze the image.  
3. Retrieve labels, confidence scores, bounding boxes, etc.

### Environment Setup
1. **Virtual Environment**  
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
2. **Install Dependencies**  
   ```bash
   pip install boto3 matplotlib pillow
   ```
   or use a **requirements.txt** with the needed packages.

![image](https://github.com/user-attachments/assets/0f839b4a-0dc6-439d-9d1d-e89f0d50b190)

---

### Project Structure
```
.
├── .vscode/            # VS Code settings
├── venv/               # Python virtual environment
├── Amazon Rekognition.py
├── requirements.txt
└── ... (other files/folders)
```
![image](https://github.com/user-attachments/assets/2acbe679-754d-4a4a-9966-89370343f1c6)

---

### Implementation

**Image Recognition Script** (pseudocode/example):
```python
import boto3

def detect_labels_in_image(bucket, image_key):
    client = boto3.client('rekognition')
    response = client.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': image_key
            }
        },
        MaxLabels=10
    )
    return response
```

#### Running the Script
```bash
python "Amazon Rekognition.py"
```
(Enclose the script name in quotes if it contains spaces.)

---

### Results and Analysis

**First Image (pic1.png)**  
- Labels detected (example): People, Person, Crowd, etc.  
- Bounding boxes drawn around each recognized person.

![image](https://github.com/user-attachments/assets/a6e6eb07-93b4-4030-b7b8-f86c66d35cdb)  
![image](https://github.com/user-attachments/assets/c00e62d7-5b18-443c-9525-374fb7e89c45)  
![image](https://github.com/user-attachments/assets/bfb892cd-30bd-4752-b103-8a90b8e5980b)

**Second Image (pic2.png)**  
- Detected labels: Vegetation, Animal, Elephant, Bear (less certain), Zebra, etc.  
- Confidence scores vary based on the image quality and how closely objects match Rekognition’s trained dataset.

![image](https://github.com/user-attachments/assets/623ffedc-ed98-4a33-8634-9c4c7142b7b2)  
![image](https://github.com/user-attachments/assets/06cbb706-ea5d-467e-ad2f-33e8839f7fd5)

---

## Video Analysis with AWS Rekognition

### Preparing Video for Analysis
1. **Upload the Video** (e.g., `video1.mp4`) to **S3**.  
2. Ensure it’s in a **compatible format** (H.264 codec in MP4 or MOV).  
   - If you get “Unsupported codec/format,” you’ll need to **install FFmpeg** and convert.

![image](https://github.com/user-attachments/assets/6ba11424-6455-45d6-9e93-a87018d6bcb2)

#### Converting with FFmpeg
```bash
choco install ffmpeg
ffmpeg -i input_video.mkv -c:v libx264 -c:a aac output_video.mp4
```
Then re-upload the **converted video** to S3.

![image](https://github.com/user-attachments/assets/7482a1f9-31de-402b-a48d-8429c74e3fa6)  
![image](https://github.com/user-attachments/assets/acf94898-2979-4415-8e4d-7688a21b509c)

---

### Running the Video Analysis Script
Typical workflow with Python and Boto3:

1. **Start** a video analysis job (`start_label_detection`)  
2. **Poll** for job status (`get_label_detection`)  
3. **Retrieve** results once the job is complete (asynchronous processing)

```python
# Pseudocode
def analyze_video(bucket, video_key):
    rekog = boto3.client('rekognition')
    response = rekog.start_label_detection(
        Video={
            'S3Object': {
                'Bucket': bucket,
                'Name': video_key
            }
        }
    )
    job_id = response['JobId']
    
    # Poll job status until "SUCCEEDED"
    # Then call rekog.get_label_detection(JobId=job_id) to retrieve results
```

![image](https://github.com/user-attachments/assets/d2c48397-f124-4663-9aae-e355bc0d3290)

---

### Viewing Analysis Results
- Detected labels are grouped by timestamps in the video.  
- Confidence scores and bounding boxes are included.  
- The total number of labels found is returned at the end.

![image](https://github.com/user-attachments/assets/853aacf4-c19f-4472-9c4c-e769e1a8d4c3)  
![image](https://github.com/user-attachments/assets/b6c9157f-0c5c-4e56-ac11-6bd51f84bc1e)

**Notes:**
- **Asynchronous Processing:** Video analysis jobs run in the background.  
- **Job Monitoring:** You must poll for job completion before fetching results.  
- **Cost:** Each request is billed, so convert videos to supported formats to avoid failed jobs.

---

## Project Overview
This project demonstrates how to leverage **AWS Rekognition** for image and video analysis—detecting objects, scenes, and faces, plus generating detailed metadata like timestamps and bounding boxes.

### Key Takeaways
- **Format Compatibility:** Rekognition needs H.264 in MP4/MOV for videos.  
- **Asynchronous Processing:** Video analysis requires polling the job ID.  
- **Rich Metadata:** Rekognition outputs confidence scores, timestamps, bounding boxes.  
- **Cost Efficiency:** Proper formatting avoids failed analyses.

### Technical Implementation
- **Amazon S3** for storing images/videos.  
- **AWS Rekognition** for AI-powered analysis.  
- **FFmpeg** for video format conversion.  
- **Python Boto3 SDK** to orchestrate.

---

## Future Enhancements
1. **Web Interface** to display analysis results in real-time.  
2. **Batch Processing Workflows** (e.g., using AWS Step Functions) for large-scale video libraries.  
3. **Notifications** on analysis completion (SNS or EventBridge).  
4. **Custom Label Detection** for specific industry use cases (using Rekognition Custom Labels).

---

### Related Projects for Readers
1. **Real-time Video Moderation System**  
   - Use `DetectModerationLabels` to identify inappropriate content in live streams.  
   - Integrate a web interface for real-time decisions and alerts.
2. **Video Searchable Library**  
   - Extract metadata to build a search index (e.g., “find all scenes with cars”).
3. **Automated Sports Highlight Generator**  
   - Identify key events (e.g., goals, fouls) and compile highlights automatically.
4. **Security Camera Analytics Dashboard**  
   - Analyze multiple camera feeds for person detection, object tracking, and anomalies.

---

**By combining AWS Rekognition, S3, and supporting tools, you can unlock advanced image and video analysis capabilities in your applications—without deep expertise in computer vision or machine learning.**
