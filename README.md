# Build-An-Image-and-Video-Labelling-Generator-Using-Amazon-Rekognition

#### Architectural Diagram
![image](https://github.com/user-attachments/assets/66e07768-1c5d-49ee-a0be-396443d2fc30)

### Introduction to AWS Rekognition
Amazon Rekognition is a cloud-based image and video analysis service that adds computer vision capabilities to applications without requiring deep learning expertise. It uses pre-trained deep learning models to identify thousands of objects, scenes, faces, text, and even inappropriate content in images and videos. With simple API calls, you can detect and label objects or scenes in an image, recognize faces and compare them, read text in images, and more. Rekognition’s face analysis can identify attributes like emotions, age range, or gender of faces in photos, and its face search can match faces against a known collection for user verification or security. 
Rekognition’s capabilities cover both Image Analysis (photos) and Video Analysis (frame-by-frame). For images, it can label objects (e.g. "Person", "Car", "Animals"), detect faces/celebrity identities, find text (OCR), and moderate unsafe content. For videos, it can track objects over time, detect activities, and flag inappropriate content in video frames. These features enable a wide range of use cases. For example, you can build searchable media libraries by extracting labels from images/videos (making them searchable by content). In security or authentication, Rekognition can do face-based user verification – confirming a user’s identity by comparing their face to a reference image. Other use cases include content moderation (detecting nudity or violence in user-uploaded media), people counting in footage, detecting personal protective equipment in workplace images, and more. Because Rekognition is fully managed and continuously learning from new data, developers can leverage these advanced vision features via APIs without building or training models themselves. This tutorial will walk through how to set up and use AWS Rekognition for analysing images and videos, with examples and best practices for integration, optimization, and troubleshooting.
 ![image](https://github.com/user-attachments/assets/06099266-5833-4f04-a392-590d5410ed67)


### Setting Up AWS Rekognition and IDE
Before using Rekognition, you need to set up your AWS environment. Start by creating an AWS account if you don't have one. Sign in to the AWS Console and choose a region that supports Rekognition (the service is available in many regions – see the AWS region table for Rekognition).
 ![image](https://github.com/user-attachments/assets/113c09fc-02a7-4f10-8bf0-7d06913aa735)

Next, create an S3 bucket to store images and videos that you want to analyse. 
 ![image](https://github.com/user-attachments/assets/ec50a42d-0a97-4e1a-93d3-011025e00d41)


Amazon Rekognition can only process images in JPEG or PNG format and videos in MP4 or MOV format (H.264 codec), so ensure your media files meet these requirements. Configure IAM roles and permissions: Rekognition will require proper AWS Identity and Access Management (IAM) permissions to access images/videos from S3 and to perform analysis. If you are calling Rekognition from an AWS Lambda function or EC2 instance, you should create an IAM execution role for that service. For example, to use Rekognition in a Lambda, go to the IAM console and create a new role with Lambda as the trusted entity. On the role creation screen, select AWS service Lambda as the use case. Creating a new IAM role for Lambda in the AWS IAM Console (selecting Lambda as the service). After selecting Lambda as the trusted service in the IAM role wizard, attach the necessary policies that grant access to Rekognition and S3. In the permissions step, search for and attach AmazonRekognitionFullAccess (which allows using all Rekognition APIs). Also attach AmazonS3FullAccess or a more restrictive S3 policy (for example, read-only access to specific buckets) so the role can read images from (and if needed, write results to) S3. For tighter security, you could use AmazonS3ReadOnlyAccess instead of full access if the function only needs to read objects. After attaching policies, complete the role creation and note the role name. Attaching Rekognition and S3 access policies to the IAM role. If you are using Rekognition from your own computer (e.g. through the AWS CLI or Boto3 SDK), you can create an IAM user instead. Give the IAM user programmatic access (an Access Key ID and Secret) and attach the same AmazonRekognitionFullAccess and appropriate S3 access policies to that user. Configure your AWS credentials (for example by running aws configure for the AWS CLI or setting up your ~/.aws/credentials for SDKs) so that your calls to AWS Rekognition are authenticated. With IAM in place, you can now enable and access Rekognition in the AWS Console. There is no special “enable” switch for Rekognition – if your account is active and you have permissions, the service is ready to use. Navigate to the Amazon Rekognition console from the AWS Management Console. The Rekognition console provides a demo interface for some features: for example, you can upload an image and have the console detect objects and faces as a quick test. (The console’s capabilities are somewhat limited to demos for image detection and managing Custom Labels projects; most production use of Rekognition is via the API/SDK.) Ensure the IAM user/role you’re using has permission for Rekognition console actions. The first time you use certain features (like Amazon Rekognition Custom Labels), the console might prompt to create an S3 bucket for storing training data or results – allow it or configure permissions as needed. At this point, your AWS environment is set up: you have an S3 bucket for input media, and an IAM identity with rights to use Rekognition and S3 (and if using Lambda, an execution role with those rights). 
However, in this project we want to use AWS CLI from our own private environment using Our IDE (Vscode) to perform this task and so we will be using our AWS credentials to authenticate our requests. To set this up, we need to configure the AWS CLI with our access keys.
First, we need to create an IAM user with the right permissions. We will log into the AWS Management Console and search for IAM.
![image](https://github.com/user-attachments/assets/22163d0f-29fd-473d-9840-8e24685bc156)

In the IAM dashboard, navigate to Users and click "Create User". After providing username, click Next.  
![image](https://github.com/user-attachments/assets/9c0139de-b841-41d1-ba5b-b6c18bca2512)

For permissions, we will select "Attach policies directly" and attach the "AdministratorAccess" policy. We should note that using Administrator Access gives full access to all AWS services, which isn't ideal from a security perspective. In a production environment, we should follow the principle of least privilege and only grant the specific permissions needed for my task.
 ![image](https://github.com/user-attachments/assets/6db9c2e2-2ea4-4c89-825e-61ca426f23b3)
![image](https://github.com/user-attachments/assets/4a92f72c-0af7-4b38-a643-633956c23746)

 
After creating the user, we will generate access keys by clicking on "Create Access Key” and selecting "Command Line Interface (CLI)" as the use case. 
![image](https://github.com/user-attachments/assets/83f92a8e-091a-4130-8038-18aa130bbba2)
![image](https://github.com/user-attachments/assets/b7fcfe40-cf53-4935-9e1c-849b547b76b2)


 
 
We added a description explaining that these keys are for my local Rekognition project, then create the access key.
 ![image](https://github.com/user-attachments/assets/c69f8fb2-8dbd-42f2-aad1-c11f0b2b7ce7)


AWS will provide us with an Access Key ID and Secret Access Key. We need to keep these confidential since they grant access to our AWS account. This means that if we configure my IDE to use AWS, we will be giving it full access into my account. Some important security practices include:
•	Never storing keys in plain text or in code repositories
•	Disabling keys when no longer needed
•	Using least-privilege permissions when possible
•	Rotating keys regularly

Now we have set our IAM to configure the AWS CLI, open terminal in VSCode and run:
aws configure

When prompted, enter Access Key ID, Secret Access Key, preferred region (making sure it matches my S3 bucket region), and output format. The interaction will look something like:
AWS Access Key ID: [Ienter my key here]
AWS Secret Access Key: [Ienter my secret key here]
Default region name: us-east-1 or eu-west-2
Default output format: None
![image](https://github.com/user-attachments/assets/29d3d118-5d21-4561-ac56-2dd2ebe96873)

 
With AWS CLI configured, we can now move on to writing Python code that will extract images from my S3 bucket and use Rekognition's detect_labels operation to generate labels with their confidence scores.

### Image Analysis with AWS Rekognition
With the setup done, let’s start with image analysis. The basic workflow is: Upload an image to S3.
 ![image](https://github.com/user-attachments/assets/ca55df6a-82c6-4534-815f-35a9ed685aab)


Afterwards, call the Rekognition API (using AWS SDK or AWS CLI) to analyse that image. Make sure image/s are in an S3 bucket that your IAM role/user can access. (The image should be JPEG or PNG and ideally at a decent resolution for best results – AWS recommends at least VGA 640x480 for accuracy.) We can use Rekognition’s label detection API to identify objects and scenes in this image. Amazon Rekognition can detect a wide variety of objects, animals, scenes, and concepts in an image. We’ll use the AWS SDK for Python (Boto3) in our examples. 
#### Setting Up the Working Environment
First, we will set up our working environment, activate it, and install dependencies which contain all the necessary packages we will be using for this task. This includes Boto3 for AWS services, matplotlib for visualization, and pillow for image processing.
•	Step 1: Create and Activate a Virtual Environment
To create a clean, isolated environment for our project, we'll use Python's built-in venv module:
#Create a virtual environment named 'venv'
python -m venv venv
#### Activate the virtual environment
venv\Scripts\activate

•	Step 2: Install Required Dependencies
With the virtual environment activated, we'll install the necessary packages:
#Install packages from requirements.txt file
pip install -r requirements.txt

#### Alternatively, install individual packages
pip install boto3 matplotlib pillow

 ![image](https://github.com/user-attachments/assets/0f839b4a-0dc6-439d-9d1d-e89f0d50b190)


As shown in the screenshots, once activated, the command prompt will display (venv) at the beginning of the line, indicating that the virtual environment is active and then the installation process with dependency resolution and successful installation of packages including boto3 (AWS SDK for Python), matplotlib (for data visualization), and pillow (for image processing).

## Project Structure
Our project directory contains:
.vscode - A folder in VS Code for workspace settings and configurations.
Venv – Active environment
Amazon Rekognition.py - Main Python script
requirements.txt - List of dependencies
![image](https://github.com/user-attachments/assets/2acbe679-754d-4a4a-9966-89370343f1c6)

 

#### Implementation
•	Creating the Image Recognition Script
The main script uses AWS Rekognition service to detect labels (objects, scenes, concepts) in images:
 ![image](https://github.com/user-attachments/assets/8d5617ae-04f6-40d8-8789-9cf30ea79bd3)

#### Executing the Script
To run the script, we use the following command in PowerShell
 ![image](https://github.com/user-attachments/assets/d7d438f1-b9d1-4946-a79b-a08fb18b69c0)

Note: As seen in the screenshots, when executing a file with spaces in the name, we need to enclose the filename in quotes.

#### Results and Analysis
•	First Image Analysis (pic1.png)
 ![image](https://github.com/user-attachments/assets/a6e6eb07-93b4-4030-b7b8-f86c66d35cdb)

The above image shows the image before analysis.
The analysis of the first image (pic1.png) detected the following labels with confidence scores:
 ![image](https://github.com/user-attachments/assets/c00e62d7-5b18-443c-9525-374fb7e89c45)

 ![image](https://github.com/user-attachments/assets/bfb892cd-30bd-4752-b103-8a90b8e5980b)

Now the result shows a collage of various people with bounding boxes identifying each person in the image.

•	Second Image Analysis (pic2.png)
 ![image](https://github.com/user-attachments/assets/623ffedc-ed98-4a33-8634-9c4c7142b7b2)

The analysis of the second image (pic2.png) detected the following labels with confidence scores:
Vegetation (99.95%)
Animal (99.84%)
Zoo (99.84%)
Jungle (99.81%)
Elephant (98.17%)
Wildlife (98.17%)
Collage (95.63%)
Bear (91.92%)
Zebra (90.29%)
Rainforest (80.98%)
 ![image](https://github.com/user-attachments/assets/06cbb706-ea5d-467e-ad2f-33e8839f7fd5)

The visualization shows wildlife images with bounding boxes identifying an elephant, a zebra, and what appears to be a bear, along with their confidence scores. The Elephant is perfectly recognized but others were slightly recognized due to the resemblaces.

### Video Analysis with AWS Rekognition
Store Video in Amazon S3
We will Upload the video file (video1.mp4) to our Amazon S3 bucket.
Note that the s3 bucket contains the video file (8.1 MB) and will store the results
 ![image](https://github.com/user-attachments/assets/6ba11424-6455-45d6-9e93-a87018d6bcb2)

#### Run the Video Analysis Script
Run the Python script for video analysis:
 ![image](https://github.com/user-attachments/assets/d2c48397-f124-4663-9aae-e355bc0d3290)

The script starts analysing "video1.mp4"
A job ID is generated: "16728c032958e5a6721ddff01c721b573cdc4a87ee263486cf702f5db29a939"
However, the analysis fails with error: "Unsupported codec/format"
#### Install FFmpeg for Video Conversion
Install FFmpeg using Chocolatey package manager:
 ![image](https://github.com/user-attachments/assets/32bfd551-f48b-4dab-b8e8-05d62ad50bb1)

If you get permission errors, reopen PowerShell as Administrator
Accept the installation prompts
FFmpeg will install to "C:\ProgramData\chocolatey\lib\ffmpeg\tools"
#### Convert the Video to a Compatible Format
Navigate to your video directory:
Convert the video to a compatible format (H.264 codec with AAC audio):
 ![image](https://github.com/user-attachments/assets/7482a1f9-31de-402b-a48d-8429c74e3fa6)

Move the converted video to your project folder:
 ![image](https://github.com/user-attachments/assets/92fc4b1d-06af-4aa8-b7ca-659175e8e9b5)

Then the converted video was uploaded to the designated s3 bucket
![image](https://github.com/user-attachments/assets/acf94898-2979-4415-8e4d-7688a21b509c)

 
#### Update and Run the Video Analysis Code
The Python script includes:
•	Starting a video analysis job with Amazon Rekognition
•	Monitoring job status with polling
•	Processing results when the job succeeds
•	Organizing detected labels by timestamp
•	Handling errors gracefully
#### Key components of the code:
•	analyze_video () function that handles video analysis
•	Job status monitoring through a while loop
•	Results processing that organizes labels by timestamp
•	Confidence scores included with each label
 ![image](https://github.com/user-attachments/assets/66a6d5aa-7d76-417e-ad13-23d02870604d)

View Analysis Results
When successful, the script outputs detected labels with confidence scores:
    ![image](https://github.com/user-attachments/assets/853aacf4-c19f-4472-9c4c-e769e1a8d4c3)
![image](https://github.com/user-attachments/assets/985743a7-b85c-4189-92d0-eb15c22c6809)
![image](https://github.com/user-attachments/assets/1f2f211e-a950-47d1-841a-31b3423c5346)
![image](https://github.com/user-attachments/assets/1ea95242-f7cc-40f2-9e2e-af784abcc5e7)
![image](https://github.com/user-attachments/assets/fcf90899-0286-4860-a3e2-a76fb1b75056)
![image](https://github.com/user-attachments/assets/2ca1b99c-7f94-4050-9a41-457b62081f90)
![image](https://github.com/user-attachments/assets/4af06ff0-c500-4f4e-963d-a18c0a44f381)
![image](https://github.com/user-attachments/assets/df562368-b558-4dfa-8a2e-d2cec0b2cae8)
![image](https://github.com/user-attachments/assets/e0dc6440-3c26-4cc7-9a14-9230fc0bbab8)
![image](https://github.com/user-attachments/assets/4e262fe1-f15f-4e17-be54-f8dc0f30304b)
![image](https://github.com/user-attachments/assets/f24e8cd7-9969-4b54-a39f-0c9939610ede)

     ![image](https://github.com/user-attachments/assets/b6c9157f-0c5c-4e56-ac11-6bd51f84bc1e)

 
 

 

 

 

 

 

•	Labels are organized by timestamp throughout the video
•	The system captures snapshots at regular intervals from the video, identifying objects within bounding boxes for each frame analysed.
•	The total number of labels detected (1000) is displayed at the end



### Project Overview
This project demonstrated how to leverage AWS Rekognition for Image and video analysis, specifically focusing on object detection and label identification. By converting video formats and using AWS's powerful AI services, we were able to extract meaningful insights from image and video content.

### Key Takeaways
•	Format Compatibility: AWS Rekognition requires specific video formats (H.264 codec in MP4/MOV containers) for successful analysis. Converting videos with FFmpeg is an essential step when working with various source formats.
•	Asynchronous Processing: Video analysis is performed asynchronously in AWS Rekognition, requiring job monitoring and result fetching strategies in your application code.
•	Rich Metadata: The service provides detailed information including confidence scores, timestamps, and label categorization, enabling sophisticated video content analysis.
•	Cost Efficiency: By properly formatting videos before submission, you avoid failed analysis jobs and unnecessary AWS charges.

### Technical Implementation
The solution involved several AWS services and tools working together:
•	Amazon S3 for video storage
•	AWS Rekognition for AI-powered video analysis
•	FFmpeg for video format conversion
•	Python with boto3 SDK for orchestrating the workflow

### Future Enhancements
This project could be extended by:
•	Implementing a web interface to display video analysis results
•	Creating automated workflows for batch video processing
•	Integrating with notification systems for analysis completion alerts
•	Developing custom label detection for specific use cases
#### Related Projects for Readers
1. Real-time Video Moderation System
Create a content moderation system using AWS Rekognition's DetectModerationLabels API to identify inappropriate content in live video streams. This project could include a web interface showing moderation decisions in real-time and an alert system for flagged content.
2. Video Searchable Library
Build a searchable video library where users can find moments in videos by describing what they're looking for (e.g., "find all scenes with cars"). This would leverage Rekognition for object detection and a database to store and query video metadata.
3. Automated Sports Highlight Generator
Develop a system that automatically generates sports highlights by analysing game footage. Use Rekognition to detect key moments like goals, celebrations, or penalties, then compile these into highlight reels without manual editing.
4. Security Camera Analytics Dashboard
Create a comprehensive security monitoring solution that analyses footage from multiple cameras. Build a dashboard showing person detection, object tracking, and unusual activity alerts, all powered by AWS Rekognition's video analysis capabilities.
Each of these projects builds upon the foundation established in this tutorial while exploring different applications of video analysis technology, providing readers with exciting paths to continue their AWS AI journey.
