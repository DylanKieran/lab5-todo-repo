from flask import Flask
from flask import render_template
from flask_mysqldb import MySQL
from flask_prometheus import monitor

mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'c15321906'
app.config['MYSQL_DB'] = 'todo'
app.config['MYSQL_HOST'] = '35.195.79.6'
mysql.init_app(app)

@app.route('/')
@app.route('/<task>')
def statichtml(task=None):
    return render_template('index.html', task=task)

@app.route("/list")
def hello(): # Name of the method
    cur = mysql.connection.cursor() #create a connection to the SQL instance
    cur.execute('''SELECT * FROM itemstodo''') # execute an SQL statment
    rv = cur.fetchall() #Retreive all rows returend by the SQL statment
    return render_template('index.html', name=str(rv))     #Return the data in a string format

@app.route("/add/<task>/<taskDescription>")
def add(task=None, taskDescription=None):
    cur= mysql.connection.cursor()
    insert_stmt = (
                 "INSERT INTO itemstodo (task, taskDescription) "
                 "VALUES (%s, %s)")
    data=(task,taskDescription)
    cur.execute(insert_stmt, data)
    mysql.connection.commit()
    return render_template('index.html', name="New Record is added to the database")  

@app.route("/update/<task>/<taskDescription>")
def update(task=None, taskDescription=None):
    cur=mysql.connection.cursor()
    update_stmt = (
        "UPDATE itemstodo SET task = %s " 
        "WHERE taskDescription = %s")
    data=(task,taskDescription)
    cur.execute(update_stmt, data)
    mysql.connection.commit()
    return render_template('index.html', name="User recored was updated")      #Return the data in a string format

@app.route("/delete/<task>")
def delete(task=None):
    cur=mysql.connection.cursor()
    delstatmt = "DELETE FROM itemstodo WHERE task = ' {} ' ".format(name)
    print(delstatmt)

    cur.execute(delstatmt)
    mysql.connection.commit()
    return render_template('index.html', name="User recored was deleted")      #Return the data in a string format

if __name__ == "__main__":
        monitor(app, port=8000)
        app.run(host='0.0.0.0', port='5000')

