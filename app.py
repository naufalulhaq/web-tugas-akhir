from flask import Flask, render_template, url_for, request, redirect
import mysql.connector
import pandas as pd
from mlutils import predict

app = Flask(__name__, static_folder='src')

mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'tugas_akhir',
}

conn = mysql.connector.connect(**mysql_config)

holiday_dict = {'08-10': 'Columbus Day',
                '12-11': 'Veterans Day',
                '22-11': 'Thanksgiving Day',
                '25-12': 'Christmas Day',
                '01-01': 'New Years Day',
                '18-02': 'Washingtons Birthday',
                '27-05': 'Memorial Day',
                '04-07': 'Independence Day',
                '22-08': 'State Fair',
                '02-09': 'Labor Day',
                '14-10': 'Columbus Day',
                '11-11': 'Veterans Day',
                '28-11': 'Thanksgiving Day',
                '20-01': 'Martin Luther King Jr Day',
                '17-02': 'Washingtons Birthday',
                '26-05': 'Memorial Day',
                '03-07': 'Independence Day',
                '27-08': 'State Fair',
                '07-09': 'Labor Day',
                '12-10': 'Columbus Day',
                '26-11': 'Thanksgiving Day',
                '15-02': 'Washingtons Birthday',
                '30-05': 'Memorial Day',
                '25-08': 'State Fair',
                '05-09': 'Labor Day',
                '10-10': 'Columbus Day',
                '24-11': 'Thanksgiving Day',
                '26-12': 'Christmas Day',
                '02-01': 'New Years Day',
                '16-01': 'Martin Luther King Jr Day',
                '20-02': 'Washingtons Birthday'}

def Baseurl(address):
    return url_for('static', filename=address)

def push_predict():
    sql = "SELECT * FROM ( SELECT * FROM df_train_2 ORDER BY id DESC LIMIT 24 ) as SUBQUERY ORDER BY id"
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    myresult_prediction = cursor.fetchall()

    df = pd.DataFrame(myresult_prediction)
    df.drop(columns=['id'], inplace=True)

    date_time = str(pd.to_datetime(df['date_time'].iloc[-1]) + pd.to_timedelta('1 hour'))
    pred = int(predict(df))

    insert_query = """INSERT INTO df_prediction_2 (date_time, prediction) 
             VALUES (%s, %s)"""

    cursor.execute(insert_query, (date_time, pred))
    conn.commit()

    cursor.close()

    # return render_template('test.html', pred=pred, date_time=date_time)
    return redirect(url_for('dashboard'))

@app.route('/')
def dashboard():
    sql = """SELECT date_time, traffic_volume, weather_description, weather_type, 
            is_holiday, clouds_all, snow_p_h, rain_p_h, temperature, dew_point, 
            visibility_in_miles, wind_direction, wind_speed, humidity, 
            air_pollution_index FROM ( SELECT 
                id, date_time, traffic_volume, weather_description, weather_type, 
                is_holiday, clouds_all, snow_p_h, rain_p_h, temperature, dew_point, 
                visibility_in_miles, wind_direction, wind_speed, humidity, 
                air_pollution_index FROM df_train_2 ORDER BY id DESC LIMIT 24 ) 
                as SUBQUERY ORDER BY id"""

    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    myresult_train = cursor.fetchall()
    cursor.close()

    df_train = pd.DataFrame(myresult_train)
    # df_train.drop(columns=['id'], inplace=True)
    
    sql = "SELECT * FROM ( SELECT * FROM df_prediction_2 ORDER BY id DESC LIMIT 25 ) as SUBQUERY ORDER BY id"

    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    myresult_prediction = cursor.fetchall()
    cursor.close()

    df_prediction = pd.DataFrame(myresult_prediction)
    df_prediction.drop(columns=['id'], inplace=True)

    result_df = pd.merge(df_train, df_prediction, on='date_time', how='right')
    result_df['date_time']=result_df['date_time'].str[:-6]

    Results = {}
    Results["date_time"] = result_df['date_time'].to_numpy().tolist()
    Results["traffic_volume"] = result_df['traffic_volume'].to_numpy().tolist()
    Results["prediction"] = result_df['prediction'].to_numpy().tolist()

    return render_template('dashboard.html', baseurl=Baseurl, results=Results, data=myresult_train)

@app.route('/form')
def form():
    return render_template('form.html', baseurl=Baseurl)

@app.route('/process_data', methods=['POST'])
def process_data():
    if request.method == 'POST':
        # Access form data using request.form
        date_time = str(pd.to_datetime(request.form['date_time']))
        # is_holiday = request.form['is_holiday']
        is_holiday = holiday_dict.get((pd.to_datetime(request.form['date_time'])).strftime('%d-%m'), 'Not a Holiday')
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
            INSERT INTO df_train_2 
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
        # return redirect(url_for('push_predict'))
        return push_predict()
        # return 'Data received and inserted into the database successfully'

@app.route('/table')
def table():
    sql = """SELECT date_time, traffic_volume, weather_description, weather_type, 
             is_holiday, clouds_all, snow_p_h, rain_p_h, temperature, dew_point, 
             visibility_in_miles, wind_direction, wind_speed, humidity, 
             air_pollution_index FROM sample_v2"""

    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    myresult = cursor.fetchall()

    cursor.close()

    return render_template('table.html', baseurl=Baseurl, data=myresult)

if __name__ == '__main__':
    app.run(debug='True')