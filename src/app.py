import pickle
import pandas as pd
from flask import Flask, request, render_template

# Load the model
model_file = '../models/model.pkl'  

with open(model_file, 'rb') as input_file:
    model = pickle.load(input_file)

# Define the flask application
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    predicted_outcome = None  

    if request.method == 'POST':
       
        try:
            glucose = float(request.form['Glucose'])
            insulin = float(request.form['Insulin'])
            bmi = float(request.form['BMI'])
            age = float(request.form['Age'])

           
            input_data = pd.DataFrame([[glucose, insulin, bmi, age]], columns=['Glucose', 'Insulin', 'BMI', 'Age'])

            
            prediction = model.predict(input_data)

           
            if prediction[0] == 1:
                predicted_outcome = 'Diabetic'
            else:
                predicted_outcome = 'Not Diabetic'
        
        except ValueError:
            predicted_outcome = 'Invalid input, please enter numeric values only.'

    # Render the result page with the prediction
    return render_template('index.html', prediction=predicted_outcome)

if __name__ == "__main__":
    app.run(debug=True)

    #https://diabetes-prediction-h9nj.onrender.com