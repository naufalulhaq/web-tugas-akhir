from flask import Flask, render_template

app = Flask(__name__)

@app.route('/table')
@app.route('/test')
def sql_table():
    return render_template('test.html')
    # return render_template('sql-data.html')
def testi():
    return render_template('test.html')

if __name__ == '__main__':
    app.run()