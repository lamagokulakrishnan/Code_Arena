from flask import Flask, render_template,request,redirect,session,flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import mysql.connector

Project = Flask(__name__)
Project.secret_key = 'your_secret_key'

mydb=mysql.connector.connect(host="localhost",username="root",password="",database="codearena")

@Project.route("/")
def indexpage():
    return render_template("index.html")

@Project.route("/tasks")
def taskpage():
    return render_template("tasks.html")

@Project.route("/editor")
def editorpage():
    return render_template("editor.html")

@Project.route("/course")
def coursepage():
    return render_template("course.html")

@Project.route("/signin")
def signuppage():
    return render_template("signin.html")

@Project.route("/signin")
def signinpage():
    return render_template("signin.html")


# main Registration Form

@Project.route("/regis",methods=["post"])
def register():
    nme = request.form['name']
    mail = request.form['username']
    phno = request.form['phonenumber']
    passw =  request.form['password']
    conpass = request.form['confirmpassword']
    # print(nme,mail,phno,passw,conpass)
    if passw == conpass:
        a = mydb.cursor()
        b = "insert into signup (Name, Email, PhoneNumber, Password, Confirmpassword) values(%s,%s,%s,%s,%s)"
        c = (nme,mail,phno,passw,conpass)
        a.execute(b,c)
        mydb.commit()
        return render_template("signin.html", alert_message="Registration Successful")
    else:
        return render_template("signin.html", alert_message="Passwords do not match")
    
# Main Login Form

@Project.route("/log",methods=['post'])
def login():
    user = request.form['signinusername']
    passw = request.form['signinpassword']
    #print(user,passw)
    d = mydb.cursor()
    e = "select * from signup where Email = %s and ConfirmPassword = %s"
    f = (user,passw)
    d.execute(e,f)
    fo = d.fetchone()
    if fo:
        return render_template("index.html")
    elif(user == "Admin" and passw == "Admin@1213"):
        today = datetime.date.today()
        j =mydb.cursor()
        j.execute("select * FROM courseregistration WHERE Date = %s",(today , ))
        result = j.fetchall()
        return render_template("dbhome.html",courseusers = result)
    else:
        return render_template("signin.html", alert_message="Login failed. Please check your credentials and try again.")
    
# Course Registration Form

@Project.route("/coregis",methods =['post'])
def courseregis():
    cname = request.form['name']
    cemail= request.form['email']
    ccourse = request.form['course']
    cdate = request.form['date']
    ccity = request.form['city']
    cphnum = request.form['phone']
    cgender = request.form['gender']
    #print(cname,cemail,ccourse,cdate,ccity,cphnum,cgender)
    g = mydb.cursor()
    h = "insert into courseregistration (Name,Email,Course,Date,City,PhoneNumber,Gender) values(%s,%s,%s,%s,%s,%s,%s)"
    i = (cname,cemail,ccourse,cdate,ccity,cphnum,cgender)
    g.execute(h,i)
    mydb.commit()
    subject = "Course Registration Successful"
    body = f"Hello {cname},\n\nYour course registration for {ccourse} was successful!"
    email_sent = send_email(cemail, subject, body)

    if email_sent:
        flash("Registration successful! A confirmation email has been sent.", "success")
    else:
        flash("Registration successful, but failed to send confirmation email.", "warning")

    return redirect("/course")
    # return render_template("index.html")

# Course Database Collecting Frontend

@Project.route('/coursedetails')
def coursedetails():
    j =mydb.cursor()
    j.execute("select * FROM courseregistration")
    result = j.fetchall()
    return render_template("coursedb.html",courseusers = result)

# User Registers Database Collecting Frontend

@Project.route("/userregisdetails")
def userdetails():
    j =mydb.cursor()
    j.execute("select * FROM signup")
    result = j.fetchall()
    return render_template("database.html",newusers = result)

# course registors today database Collecting frontend

@Project.route("/currentdetails")
def currentdetails():
    today = datetime.date.today()
    j =mydb.cursor()
    j.execute("select * FROM courseregistration WHERE Date = %s",(today , ))
    result = j.fetchall()
    return render_template("dbhome.html",courseusers = result)

# mail connection
# Function to send email
def send_email(receiver_email, subject, body):
    sender_email = "lamagokulakrishnan@gmail.com"  # Enter your email ID here
    sender_password = "mhas ybvp hbxv aypi"    # Enter your email's app-specific password here
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# Run the Flask application
if __name__ == "__main__":
    Project.run(debug=True)

# Project.run()