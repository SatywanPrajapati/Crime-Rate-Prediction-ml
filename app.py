from flask import Flask, request, render_template
import pickle
import math
import os

# Load model
model_path = os.path.join(os.path.dirname(__file__), 'Model', 'model.pkl')
model = pickle.load(open(model_path, 'rb'))

app = Flask(__name__)

# Home route
@app.route('/')
def index():
    return render_template("index.html")


# Prediction route
@app.route('/predict', methods=['POST'])
def predict_result():

    try:
        # Dictionaries
        city_names = {
            '0': 'Araria', '1': 'Arwal', '2': 'Aurangabad', '3': 'Banka', '4': 'Begusarai',
            '5': 'Bhagalpur', '6': 'Bhojpur', '7': 'Buxar', '8': 'Darbhanga', '9': 'East Champaran (Motihari)',
            '10': 'Gaya', '11': 'Gopalganj', '12': 'Jamui', '13': 'Jehanabad', '14': 'Kaimur (Bhabua)',
            '15': 'Katihar', '16': 'Khagaria', '17': 'Kishanganj', '18': 'Lakhisarai', '19': 'Madhepura',
            '20': 'Madhubani', '21': 'Munger', '22': 'Muzaffarpur', '23': 'Nalanda', '24': 'Nawada',
            '25': 'Patna', '26': 'Purnia', '27': 'Rohtas', '28': 'Saharsa', '29': 'Samastipur',
            '30': 'Saran (Chhapra)', '31': 'Sheikhpura', '32': 'Sheohar', '33': 'Sitamarhi', '34': 'Siwan',
            '35': 'Supaul', '36': 'Vaishali (Hajipur)', '37': 'West Champaran (Bettiah)'
        }

        crimes_names = {
            '0': 'Attempt to Murder', '1': 'Burglary', '2': 'Cruelty by Husband/Relatives',
            '3': 'Dacoity', '4': 'Dowry Deaths', '5': 'Kidnapping & Abduction',
            '6': 'Murder', '7': 'Rape', '8': 'Riots', '9': 'Robbery',
            '10': 'Theft', '11': 'Total Violent Crimes'
        }

        population = {
            '0': 63.50, '1': 85.00, '2': 87.00, '3': 21.50, '4': 163.10, '5': 23.60,
            '6': 77.50, '7': 21.70, '8': 30.70, '9': 29.20, '10': 21.20, '11': 141.10,
            '12': 20.30, '13': 29.00, '14': 184.10, '15': 25.00, '16': 20.50, '17': 50.50,
            '18': 28.12, '19': 7.01, '20': 25.41, '21': 20.35, '22': 29.71, '23': 30.38,
            '24': 27.28, '25': 17.06, '26': 39.37, '27': 50.99, '28': 43.91, '29': 25.62,
            '30': 17.6, '31': 11.13, '32': 16.26, '33': 30.71, '34': 16.67,
            '35': 17.1, '36': 10.01, '37': 19.95
        }

        # Input (convert to int)
        city_code = int(request.form["city"])
        crime_code = int(request.form['crime'])
        year = int(request.form['year'])

        # Get population
        pop = population[str(city_code)]

        # Adjust population by year
        year_diff = year - 2018
        pop = pop + 0.01 * year_diff * pop

        # Prediction
        crime_rate = model.predict([[year, city_code, pop, crime_code]])[0]

        # Mapping names
        city_name = city_names[str(city_code)]
        crime_type = crimes_names[str(crime_code)]

        # Crime category
        if crime_rate <= 10:
            crime_status = "Very Low Crime Area"
        elif crime_rate <= 40:
            crime_status = "Low Crime Area"
        elif crime_rate <= 70:
            crime_status = "Middle Crime Area"
        else:
            crime_status = "High Crime Area"

        # Cases calculation
        cases = math.ceil(crime_rate * pop)

        return render_template(
            'result.html',
            city_name=city_name,
            crime_type=crime_type,
            year=year,
            crime_status=crime_status,
            crime_rate=round(crime_rate, 2),
            cases=cases,
            population=round(pop, 2)
        )

    except Exception as e:
        return f"Error: {str(e)}"


# Run app
if __name__ == '__main__':
    app.run(debug=True)
