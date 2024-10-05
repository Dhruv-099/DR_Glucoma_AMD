from flask import Flask, request
'''
import boto3
def upload_file():
    if 'file' not in request.files:
        return "No file part"    
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    # Upload to AWS S3
    s3 = boto3.client('s3')
    s3.upload_fileobj(file, 'your-bucket-name', file.filename)
    
    return "File uploaded successfully"
'''

app = Flask(__name__)
@app.route("/")

def re():
    return render_template('home.html')

if __name__=='main':
    app.run(host='0.0.0.0', debug = True)

