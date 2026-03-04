from flask import Flask, render_template, request
import boto3
import pymysql
import os

app = Flask(__name__)

# AWS S3 configuration
S3_BUCKET = "shridevi-cloud-upload-app"
s3 = boto3.client('s3')

# RDS configuration
db = pymysql.connect(
    host="fileupload-db.cgdsgmaycs1c.us-east-1.rds.amazonaws.com",
    user="admin",
    password="Devops12345",
    database="fileupload"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']

    if file:
        filename = file.filename
        
        # Upload to S3
        s3.upload_fileobj(file, S3_BUCKET, filename)

        file_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{filename}"

        # Save metadata to RDS
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO uploads (filename, s3_url) VALUES (%s, %s)",
            (filename, file_url)
        )
        db.commit()

        return f"File uploaded successfully! <br> URL: {file_url}"

    return "No file uploaded"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
