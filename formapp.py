from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/process_data', methods=['POST'])
def process_data():
    if request.method == 'POST':
        # Access form data using request.form
        date_time = request.form['date_time']
        is_holiday = request.form['is_holiday']
        air_pollution_index = int(request.form['air_pollution_index'])
        humidity = int(request.form['humidity'])
        wind_speed = int(request.form['wind_speed'])
        wind_direction = int(request.form['wind_direction'])
        visibility_in_miles = int(request.form['visibility_in_miles'])
        dew_point = int(request.form['dew_point'])
        temperature = float(request.form['temperature'])
        rain_p_h = float(request.form['rain_p_h'])
        snow_p_h = float(request.form['snow_p_h'])
        clouds_all = int(request.form['clouds_all'])
        weather_type = request.form['weather_type']
        weather_description = request.form['weather_description']
        traffic_volume = int(request.form['traffic_volume'])

        # Now you can process or store the data as needed

        # For demonstration, let's print the data
        print(f'Date and Time: {date_time}')
        print(f'Is Holiday: {is_holiday}')
        print(f'Air Pollution Index: {air_pollution_index}')
        print(f'Humidity: {humidity}')
        print(f'Wind Speed: {wind_speed}')
        print(f'Wind Direction: {wind_direction}')
        print(f'Visibility in Miles: {visibility_in_miles}')
        print(f'Dew Point: {dew_point}')
        print(f'Temperature: {temperature}')
        print(f'Rain (mm/h): {rain_p_h}')
        print(f'Snow (mm/h): {snow_p_h}')
        print(f'Clouds (Percentage): {clouds_all}')
        print(f'Weather Type: {weather_type}')
        print(f'Weather Description: {weather_description}')
        print(f'Traffic Volume: {traffic_volume}')

        # Return a response to the client
        return 'Data received and processed successfully'

if __name__ == '__main__':
    app.run(debug=True)
