import csv
from flask import Flask, render_template,request,redirect,url_for,session
import json
import MySQLdb
from flask_sqlalchemy import SQLAlchemy
import diseaseprediction
import mysql.connector
#import mySQLdb


with open('config.json','r') as c:
    params=json.load(c)["params"]

app = Flask(__name__)
app.secret_key = 'super-secret-key'
database=mysql.connector.connect(host='localhost',user='root',password='',database='disease_prediction')
database1=mysql.connector.connect(host='localhost',user='root',password='',database='disease_prediction')
#conn = MySQLdb.connect(host='localhost',user='root',password='',db='disease_prediction')
#cursor = conn.cursor()

with open('templates/Testing.csv', newline='') as f:

    reader = csv.reader(f)
    symptoms = next(reader)
    symptoms = symptoms[:len(symptoms)-1]

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/disease_prediction'
db = SQLAlchemy(app)

class patient(db.Model):
    '''
    sno,Gender,Age,Symptom1...7,Disease
    '''
    sno = db.Column(db.Integer, primary_key=True)
    Gender = db.Column(db.String(80),nullable=False)
    Age= db.Column(db.String(120),nullable=False)
    Symptom1=db.Column(db.String(120),nullable=True)
    Symptom2=db.Column(db.String(120),nullable=True)
    Symptom3=db.Column(db.String(120),nullable=True)
    Symptom4=db.Column(db.String(120),nullable=True)
    Symptom5=db.Column(db.String(120),nullable=True)
    Symptom6=db.Column(db.String(120),nullable=True)
    Symptom7=db.Column(db.String(120),nullable=True)
    Disease=db.Column(db.String(120),nullable=True)

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/dashboard')


@app.route('/', methods=['GET'])
def dropdown():
    lis=["SELECT * from table1","SELECT * from table2","SELECT * from table3"]
    s=[]
    for i in range(len(lis)):
        cursor=database.cursor(buffered=True)
        cursor.execute(lis[i])
        data=cursor.fetchall()
        s.append(data)
        cursor.close()
    database.commit()

    
    
    return render_template('includes/default.html', symptoms=symptoms,doctor=s[0],doctor1=s[1],doctor2=s[2])


@app.route("/dashboard",methods=['GET','POST'])
def dashboard():
    if 'user' in session and session['user']==params['admin_user']:
        data=patient.query.all()
        return render_template('dashboard.html',params=params,data=data)
    if request.method=='POST':
        username=request.form.get('uname')
        userpass=request.form.get('pass')
        if (username==params['admin_user'] and userpass==params['admin_pass']):
            session['user']=username
            data=patient.query.all()
            return render_template('dashboard.html',params=params,data=data)
    
    return render_template('login.html',params=params)

@app.route('/disease_predict', methods=['POST','GET'])
def disease_predict():
    selected_symptoms = []
    if(request.form['Symptom1']!="") and (request.form['Symptom1'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom1'])
    if(request.form['Symptom2']!="") and (request.form['Symptom2'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom2'])
    if(request.form['Symptom3']!="") and (request.form['Symptom3'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom3'])
    if(request.form['Symptom4']!="") and (request.form['Symptom4'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom4'])
    if(request.form['Symptom5']!="") and (request.form['Symptom5'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom5'])
    if(request.form['Symptom6']!="") and (request.form['Symptom6'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom6'])
    if(request.form['Symptom7']!="") and (request.form['Symptom7'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom7'])

    # disease_list = []
    # for i in range(7):
    #     disease = diseaseprediction.dosomething(selected_symptoms)
    #     disease_list.append(disease)
    # return render_template('disease_predict.html',disease_list=disease_list)
    disease = diseaseprediction.dosomething(selected_symptoms)
    if (request.method=='POST'):
        gender=request.form.get('gender')
        age=request.form.get('age')
        symptom1=request.form.get('Symptom1')
        symptom2=request.form.get('Symptom2')
        symptom3=request.form.get('Symptom3')
        symptom4=request.form.get('Symptom4')
        symptom5=request.form.get('Symptom5')
        symptom6=request.form.get('Symptom6')
        symptom7=request.form.get('Symptom7')
        '''
        sno,Gender,Age,Symptom1...7,Disease
        '''

        entry=patient(Gender=gender,Age=age,Symptom1=symptom1,Symptom2=symptom2,Symptom3=symptom3,Symptom4=symptom4,Symptom5=symptom5
            ,Symptom6=symptom6,Symptom7=symptom7,Disease=disease[0])
        db.session.add(entry)
        db.session.commit()
        

    return render_template('disease_predict.html',disease=disease,symptoms=symptoms)

# @app.route('/default')
# def default():
#         return render_template('includes/default.html')
 
@app.route('/find_doctor', methods=['POST'])
def get_location():
    location = request.form['doctor']
    
    return render_template('find_doctor.html',location=location,symptoms=symptoms)

@app.route('/drug', methods=['POST'])
def drugs():
    medicine = request.form['medicine']
    return render_template('homepage.html',medicine=medicine,symptoms=symptoms)

if __name__ == '__main__':
    app.run(debug=True)