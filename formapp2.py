
from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sample'

mysql = MySQL(app)

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

        # Create a cursor
        cur = mysql.connection.cursor()

        # Insert data into the database
        cur.execute("""
            INSERT INTO your_table_name 
            (date_time, is_holiday, air_pollution_index, humidity, wind_speed, wind_direction,
             visibility_in_miles, dew_point, temperature, rain_p_h, snow_p_h, clouds_all,
             weather_type, weather_description, traffic_volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (date_time, is_holiday, air_pollution_index, humidity, wind_speed, wind_direction,
              visibility_in_miles, dew_point, temperature, rain_p_h, snow_p_h, clouds_all,
              weather_type, weather_description, traffic_volume))

        # Commit to the database
        mysql.connection.commit()

        # Close the cursor
        cur.close()

        # Return a response to the client
        return 'Data received and inserted into the database successfully'

if __name__ == '__main__':
    app.run(debug=True)
