from flask import Flask, request,render_template
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
    diseases = [
        {
            "name": "Age-Related Macular Degeneration (AMD)",
            "description": "Age-Related Macular Degeneration (AMD) is a common eye condition that affects the macula, the central part of the retina responsible for sharp, straight-ahead vision. AMD usually occurs in people aged 50 and older and can lead to central vision loss. There are two types: dry AMD, which progresses slowly, and wet AMD, which is more severe but less common. Early diagnosis can help slow the progression of the disease."
        },
        {
            "name": "Glaucoma",
            "description": "Glaucoma is a group of eye conditions that damage the optic nerve, which is crucial for vision. This damage is often caused by abnormally high pressure in the eye. If untreated, glaucoma can lead to irreversible vision loss and even blindness. There are different types of glaucoma, including open-angle and angle-closure. Regular eye exams are essential, as glaucoma often shows no early symptoms."
        },
        {
            "name": "Diabetic Retinopathy",
            "description": "Diabetic Retinopathy is a complication of diabetes that affects the blood vessels of the retina, the light-sensitive tissue at the back of the eye. Over time, high blood sugar levels can damage these vessels, leading to vision problems, including blindness. Diabetic retinopathy progresses through stages, starting from mild non-proliferative changes to severe proliferative retinopathy. Managing blood sugar levels and early detection are key to preventing vision loss."
        }
    ]
    return render_template('home.html',diseases=diseases)

if __name__=='__main__':
    app.run(host='0.0.0.0', debug = True)

