import pickle
import pandas as pd
from flask import Flask, request, render_template

# Load the model
model_file = '../models/model.pkl'  # Adjust path if necessary

with open(model_file, 'rb') as input_file:
    model = pickle.load(input_file)

# Define the flask application
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    predicted_outcome = None  # Initialize the prediction variable

    if request.method == 'POST':
        # Get the input data from the form (adjust form field names as needed)
        try:
            glucose = float(request.form['Glucose'])
            insulin = float(request.form['Insulin'])
            bmi = float(request.form['BMI'])
            age = float(request.form['Age'])

            # Format the input data as a pandas DataFrame (model expects 2D array-like)
            input_data = pd.DataFrame([[glucose, insulin, bmi, age]], columns=['Glucose', 'Insulin', 'BMI', 'Age'])

            # Make the prediction using the model
            prediction = model.predict(input_data)

            # Convert the model's numeric output to a human-readable result
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