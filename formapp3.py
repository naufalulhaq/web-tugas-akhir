from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Configure MySQL
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'tugas_akhir',
}

conn = mysql.connector.connect(**mysql_config)

@app.route('/')
def index():
    return render_template('form2.html')

@app.route('/table')
def sql_table():
    # Get filter and sort parameters from the request
    filter_column = request.args.get('filter_column', None)
    filter_value = request.args.get('filter_value', None)
    sort_column = request.args.get('sort_column', None)
    sort_order = request.args.get('sort_order', 'ASC')

    # Construct SQL query with optional filter and sort
    sql = "SELECT * FROM sample"
    if filter_column and filter_value:
        sql += f" WHERE {filter_column} = '{filter_value}'"
    if sort_column:
        sql += f" ORDER BY {sort_column} {sort_order}"

    mycursor = conn.cursor(dictionary=True)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return render_template('table3.html', data=myresult)


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
        cursor = conn.cursor()

        # Insert data into the database
        insert_query = """
            INSERT INTO sample 
            (date_time, is_holiday, air_pollution_index, humidity, wind_speed, wind_direction,
             visibility_in_miles, dew_point, temperature, rain_p_h, snow_p_h, clouds_all,
             weather_type, weather_description, traffic_volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, (date_time, is_holiday, air_pollution_index, humidity, wind_speed,
                                      wind_direction, visibility_in_miles, dew_point, temperature, rain_p_h,
                                      snow_p_h, clouds_all, weather_type, weather_description, traffic_volume))

        # Commit to the database
        conn.commit()

        # Close the cursor
        cursor.close()

        # Return a response to the client
        return 'Data received and inserted into the database successfully'

if __name__ == '__main__':
    app.run(debug=True)
