from flask import Flask, request, redirect, render_template ,jsonify, url_for, session
from mysql.connector import connect, Error
import bcrypt, os

app = Flask(__name__)
app.secret_key = 'secret_key'


db_name = os.environ.get('DB_NAME')
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_host = os.environ.get('DB_HOST')

cnx = connect(user= db_user,
              password=db_password,
              host=db_host,
              database=db_name)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get the user input
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']


        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        # Insert the user details into the database
        cursor = cnx.cursor()
        sql_query = "INSERT INTO users (email, password, name) VALUES (%s, %s, %s)"
        cursor.execute(sql_query, (email, hashed_password, name))
        cnx.commit()
        cursor.close()
                
        

        return redirect('/')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Get the user name and password from the request
    if request.method == 'POST':

        username = request.form['name']
        password = request.form['password']

        with cnx.cursor() as cursor:
            query = "SELECT * FROM users WHERE name = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()

        if user:
            if bcrypt.checkpw(password.encode(), user[3].encode()):
                session['user_id']=user[0]
                return render_template('login_success.html', user=user[1])

            else:
                error = "Incorrect username or password"
                return render_template('login.html', error=error)
        else:
            error = "Incorrect username or password"
            return render_template('login.html', error=error)
    
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)