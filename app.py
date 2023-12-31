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

conn = mysql.connector.connect(**mysql_config)

def Baseurl(address):
    return url_for('static', filename=address)

@app.route('/')
def index():
    return render_template('basic-table.html', baseurl=Baseurl)

@app.route('/form')
def form():
    return render_template('form.html', baseurl=Baseurl)

@app.route('/chart_coba')
def chart_coba():
    return render_template('chart.html', baseurl=Baseurl)

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
        return redirect(url_for('sql_table'))
        # return 'Data received and inserted into the database successfully'

@app.route('/table')
def table():
    sql = "SELECT * FROM sample_v2"

    mycursor = conn.cursor(dictionary=True)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    return render_template('table.html', baseurl=Baseurl, data=myresult)

@app.route('/predict')
def predict_data():
    sql = "SELECT * FROM ( SELECT * FROM sample_v2 ORDER BY id DESC LIMIT 24 ) as SUBQUERY ORDER BY id"

    mycursor = conn.cursor(dictionary=True)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    df = pd.DataFrame(myresult)
    df.drop(columns=['id'], inplace=True)
    
    pred = predict(df)
    print(pred)

    return render_template('pred.html', baseurl=Baseurl, data=myresult, pred=pred)

@app.route('/chart')
def chart():
    sql = "SELECT * FROM sample"

    mycursor = conn.cursor(dictionary=True)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    Results = {}
    Results["date_time"] = [entry["date_time"] for entry in myresult]
    Results["traffic_volume"] = [entry["traffic_volume"] for entry in myresult]

    return render_template('chart.html', baseurl=Baseurl, results=Results)

@app.route('/chart_2')
def chart_2():
    sql = "SELECT * FROM ( SELECT * FROM second_half ORDER BY id DESC LIMIT 24 ) as SUBQUERY ORDER BY id"

    mycursor = conn.cursor(dictionary=True)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    df = pd.DataFrame(myresult)
    df.drop(columns=['id'], inplace=True)
    
    pred = int(predict(df)[0].round())

    Results = {}
    Results["date_time"] = [entry["date_time"] for entry in myresult]
    Results["traffic_volume"] = [entry["traffic_volume"] for entry in myresult]

    return render_template('chart_2.html', baseurl=Baseurl, results=Results, pred=pred, data=myresult)

@app.route('/chart_3')
def chart_3():
    sql = "SELECT * FROM ( SELECT * FROM df_train ORDER BY id DESC LIMIT 24 ) as SUBQUERY ORDER BY id"

    mycursor = conn.cursor(dictionary=True)
    mycursor.execute(sql)
    myresult_train = mycursor.fetchall()

    df_train = pd.DataFrame(myresult_train)
    df_train.drop(columns=['id'], inplace=True)
    
    sql = "SELECT * FROM ( SELECT * FROM df_prediction ORDER BY id DESC LIMIT 25 ) as SUBQUERY ORDER BY id"

    mycursor = conn.cursor(dictionary=True)
    mycursor.execute(sql)
    myresult_prediction = mycursor.fetchall()

    df_prediction = pd.DataFrame(myresult_prediction)
    df_prediction.drop(columns=['id'], inplace=True)

    # Columns to be dropped
    columns_to_drop = ['is_holiday', 'air_pollution_index', 'humidity', 'wind_speed',
                       'wind_direction', 'visibility_in_miles', 'dew_point', 'temperature',
                       'rain_p_h', 'snow_p_h', 'clouds_all', 'weather_type', 'weather_description']

    # Tail for the last 24 rows
    df_train_ = df_train.drop(columns=columns_to_drop).tail(24)
    df_prediction_ = df_prediction.tail(25)

    result_df = pd.merge(df_train_, df_prediction_, on='date_time', how='right')
    result_df.info()

    pred = int(predict(df_train)[0].round())

    Results = {}
    # Results["date_time"] = [entry["date_time"] for entry in myresult_train]
    # Results["traffic_volume"] = [entry["traffic_volume"] for entry in myresult_train]
    Results["date_time"] = result_df['date_time'].to_numpy().tolist()
    Results["traffic_volume"] = result_df['traffic_volume'].to_numpy().tolist()
    Results["prediction"] = result_df['prediction'].to_numpy().tolist()
    print(type(Results))
    print(Results)

    return render_template('chart_3.html', baseurl=Baseurl, results=Results, pred=pred, data=myresult_train)

if __name__ == '__main__':
    app.run(debug='True')