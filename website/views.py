import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import current_user
from .models import db, Patient, Patient_history
from werkzeug.utils import secure_filename
from tensorflow.keras.utils import load_img, img_to_array
import pickle

views = Blueprint('views', __name__)
# Corrected model path (using forward slashes for better cross-platform compatibility)
model_path = 'ML_portion/best_model.pkl'
# Load the model if it exists
if os.path.exists(model_path):
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
else:
    model = None
    print("Model file not found.")
@views.route('/')
def home():
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
    return render_template('home.html', user=current_user, diseases=diseases)

# Ensure only allowed file types can be uploaded
allowed_extensions = {'raw', 'png', 'jpg', 'jpeg'}

def allowed_fn(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def preprocess_image(image_path):
    img = load_img(image_path, target_size=(224, 224))  
    img_array = img_to_array(img)
    img_array = img_array / 255.0  
    img_array = img_array.reshape(1, 224, 224, 3)  
    return img_array

@views.route('/project-dashboard', methods=['GET', 'POST'])
def project_dashboard():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        phone_number = request.form.get('phone_number')
        doctor_id = request.form.get('doctor_id')
        file = request.files.get('photo')

        if not all([name, age, gender, phone_number, doctor_id]) or not file:
            flash('All fields are required', 'error')
            return redirect(url_for('views.project_dashboard'))

        if file and allowed_fn(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)  
            file.save(file_path)

            if model is not None:
                img_array = preprocess_image(file_path)
                prediction = model.predict(img_array)
                disease_class = prediction.argmax()
                class_names = ['Diabetic Retinopathy', 'Glaucoma', 'AMD','Normal']
                prediction_result = class_names[disease_class]
                flash(f'Prediction: {prediction_result}', 'success')
            else:
                prediction_result = "Model not available."
                flash('Model not available for prediction', 'error')

            # Save patient data
            new_patient = Patient(
                name=name,
                age=age,
                gender=gender,
                phone_number=phone_number,
                doctor_id=doctor_id,
                photo=filename
            )
            db.session.add(new_patient)
            db.session.commit()

            # Redirect to patient history with prediction result in query params
            return redirect(url_for('views.patient_history', patient_id=new_patient.id, prediction_result=prediction_result))
        else:
            flash('Invalid file type. Only images are allowed.', 'error')
            return redirect(url_for('views.project_dashboard'))

    return render_template('project-dashboard.html')

@views.route('/patient/<int:patient_id>/history', methods=['GET'])
def patient_history(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    history = Patient_history.query.filter_by(patient_id=patient_id).all()
    
    # Retrieve prediction_result from the query params
    prediction_result = request.args.get('prediction_result')
    
    return render_template('patient_history_and_result.html', patient=patient, history=history, prediction_result=prediction_result)
