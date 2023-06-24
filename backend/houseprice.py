from flask import Flask, request, jsonify
import numpy as np
import pickle
from sklearn import preprocessing


app = Flask(__name__)

# Load the pre-trained model
model = pickle.load(open('housepricemodel.sav', 'rb'))

@app.route('/predict', methods=['POST'])
def predict():
    # Get the values from the API call
    data = request.get_json()
    values = data['values']

    # Preprocess the input values
    processed_values = preprocess(values)

    # Make predictions using the pre-trained model
    predictions = model.predict(processed_values)

    # Prepare the response
    response = {'predictions': predictions.tolist()}

    return jsonify(response)

def preprocess(values):
    label_encoder = preprocessing.LabelEncoder()

    # Separate numeric and categorical columns
    numeric_values = []
    categorical_values = []

    for value in values:
        if value.isdigit():
            numeric_values.append(float(value))
        else:
            categorical_values.append(value)

    # Convert numeric values to float
    numeric_values = np.array(numeric_values).reshape(1, -1).astype(float)

    # Apply label encoding to categorical values
    categorical_values = np.array(categorical_values).reshape(1, -1)

    for i in range(categorical_values.shape[1]):
        categorical_values[:, i] = label_encoder.fit_transform(categorical_values[:, i])

    # Concatenate the processed numeric and categorical values
    processed_values = np.hstack((numeric_values, categorical_values))

    return processed_values



if __name__ == '__main__':
    app.run(debug=True)
