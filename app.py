import os
import random
from flask import Flask, render_template, request, redirect, url_for, flash, session
from dotenv import load_dotenv
from user import UserOperation
from admin import AdminOperation
from encryption import encrypt   # import encrytion file
from validation import Validation
from myEmail import Email

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'tvd-secret-key-prod-mystic-falls-2026')

emailObj = Email(app) # Email Object created
userObj = UserOperation() # Create obj of useropertion (user module)
validObj = Validation()  # create obj of Validation class
adminObj = AdminOperation()


@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/about')
def about():
    
    return render_template('about.html')

@app.route('/characters')
def characters():
    
    return render_template('characters.html')

@app.route('/quiz')
def quiz():
    
    return render_template('quiz.html')

@app.route('/leaderboard')
def leaderboard():
    
    return render_template('leaderboard.html')

@app.route('/contect')
@app.route('/contact')
def contect():
    return "Contact Us"

@app.route('/greeting/<name>')  # /<name> = value pass karne ke liye
def greeting(name):
    return f"Good morning {name}"

@app.route('/userSignup',methods=['GET','POST'])
def userSignup():
    if request.method=='GET':
        return render_template('userSignup.html') #render ek baar in krte hai kisi file ko
    else:
        # return "post"
        firstName = request.form['firstName'] 
        lastName = request.form['lastName'] 
        email = request.form['email'] 
        mobile = request.form['mobile']
        password = request.form['password']  
        
        #-- empty validation--
        fieldList = [firstName,lastName,email,mobile,password]
        status = validObj.checkEmpty(fieldList)
        if status:
            flash("field can't be empty!!")
            return redirect(url_for('userSignup'))  #redirect already likha hai usse bss call kr rahe


        # --- mobile validation --
        status = validObj.checkMobile(mobile)
        if status:
            flash("mobile must be 10 digits")
            return redirect(url_for('userSignup'))

        #String validation
        status = validObj.checkStr(lastName)
        if status:
            flash("Last Name must be a string")
            return redirect(url_for('userSignup'))

        # ---encrypt password ---
        password = encrypt(password)
        # mobile = encrypt(mobile)

        #-----enail otp-----
        try:
            userObj.userInsert(firstName,lastName,email,mobile,password)
            user_otp = random.randint(1000,9999)
            session['userOTP'] = user_otp
            session['otpEmail'] = email
            subject ="TVD Quiz App: Email Verification"
            message = f"Hello {firstName}\n This is email verification mail. \nYour OTP is: {user_otp} \nThankyou\n TVD Quiz"

            emailObj.compose_mail(subject,email,message)
            return redirect(url_for('emailVerify', userEmail=email))
        except Exception as e:
            flash(f"Something went wrong with email:{e}")
            return redirect(url_for('userSignup'))
        # --insert---
        
        
    
@app.route('/emailVerify', methods=['GET', 'POST'])
def emailVerify():
    if request.method == 'GET':
        email = request.args.get('userEmail')
        return render_template('emailVerify.html',userEmail=email)
    else:
        try:
            otpInput = int(request.form.get('otp', 0))
        except (ValueError, TypeError):
            otpInput = 0
            
        userEmail = request.args.get('userEmail') or session.get('otpEmail')
        storedOTP = session.get('userOTP')
        if storedOTP and otpInput == int(storedOTP):
            session.pop('userOTP', None) #clear OTP after verification
            session.pop('otpEmail', None)
            flash("Successfully Registered.. Login Now")
            return redirect (url_for('userLogin'))
        else:
            if userEmail:
                userObj.userDelete(userEmail) #user acc deleted
            flash("Your email verification is failed. Try Again...")
            return redirect(url_for('userSignup'))


@app.route('/userLogin',methods=['GET','POST'])
def userLogin():
    if request.method=='GET':
        return render_template('userLogin.html')
    else:
        email = request.form['email']
        password = request.form['password']
    #-- empty validation--
    fieldList = [email,password]
    status = validObj.checkEmpty(fieldList)
    if status:
        flash("field can't be empty!!")
        return redirect(url_for('userLogin'))

    #------encrpt password-----
    password = encrypt(password)
    #------check user login-----
    status = userObj.userLogin(email,password)
    if status:
        return redirect(url_for('userDash'))
    else:
        flash("invalid email or password!!!!")
        return redirect(url_for('userLogin'))
    
@app.route('/userLogout')
def userLogout():
    session.clear()
    flash("logged out successfully!!!")
    return redirect(url_for('userLogin'))
    
@app.route('/userDash',methods=['GET','POST'])
def userDash():
    if 'userEmail' in session:
        if request.method=='GET':
            return render_template('userDash.html')
    else:
        flash("Please login to access this page!!")
        return redirect(url_for('userLogin'))


@app.route('/userProfile',methods=['GET','POST'])
def userProfile():
    if 'userEmail' in session:
        if request.method=='GET':
            data= userObj.userProfile()
            return render_template('userProfile.html', record=data)
        else:
            # return "post"
            firstName = request.form['firstName'] 
            lastName = request.form['lastName'] 
            mobile = request.form['mobile']
            
            #-- empty validation--
            fieldList = [firstName,lastName,mobile]
            status = validObj.checkEmpty(fieldList)
            if status:
                flash("field can't be empty!!")
                return redirect(url_for('userProfile'))  #redirect already likha hai usse bss call kr rahe


            # --- mobile validation --
            status = validObj.checkMobile(mobile)
            if status:
                flash("mobile must be 10 digits")
                return redirect(url_for('userProfile'))

            userObj.userUpdate(firstName,lastName,mobile)
            flash("Your Profile is Updated Successfully!!")
            return redirect(url_for('userProfile'))
    else:
        flash("Please login to access this page!!")
        return redirect(url_for('userLogin'))
    
@app.route('/userDelete',methods=['GET','POST'])
def userDelete():
    if 'userEmail' in session:
        if request.method=='GET':
            userObj.userDelete(session['userEmail'])
            flash("Your account is deleted successfully...hope to see you soon!!!")
            return redirect(url_for('userSignup'))
    else:
        flash("Please login to access this page!!")
        return redirect(url_for('userLogin'))
    
@app.route('/userPassword',methods=['GET','POST'])
def userPassword():
    if 'userEmail' in session:
        if request.method=='GET':
            return render_template('userPassword.html')
        else:
            oldPassword = request.form['oldPassword']
            newPassword = request.form['newPassword']
            oldPassword = encrypt(oldPassword)
            newPassword = encrypt(newPassword)
            status = userObj.userPassword(oldPassword,newPassword)
            if status:
                session.clear()
                flash ('your password is updated successfully!! Login Again...')
                return redirect(url_for('userLogin'))
                
            else:
                flash("your old password is invalid!!!")
                return redirect(url_for('userPassword'))
    else:
        flash("Please login to access this page!!")
        return redirect(url_for('userLogin'))

@app.route('/userPlayQuiz', methods=['GET', 'POST'])

def userPlayQuiz():

    if 'userEmail' in session:
        if request.method=='GET':
            return render_template('userPlayQuiz.html')
        else:
            level = request.form['level']
            quiz = userObj.userQuizQues(level)
            return render_template('userPlayQuiz.html',record=quiz,level=level)
    else:
        flash("Please login to access this page!!")
        return redirect(url_for('userLogin'))
    

@app.route('/userAnsCheck',methods=['GET','POST'])
def userAnsCheck():
    if 'userEmail' in session:
        if request.method=='POST':
            level = request.args.get('level')
            ans = request.form    #dictionary
            score = userObj.userAnsCheck(ans)
            userObj.scorecardInsert(level,score)
            return redirect(url_for('userScoreBoard',level=level))
    else:
        flash("Please login to access this page!!")
        return redirect(url_for('userLogin'))

@app.route('/userScoreBoard',methods=['GET','POST'])
def userScoreBoard():
    if 'userEmail' in session:
        if request.method=='GET':
            level = request.args.get('level') or '1'
            score = userObj.userScore(level)
            topRank = userObj.userTopRank(level)
            total = userObj.userTotal(level)
            return render_template('userScoreBoard.html',score=score,topRank=topRank,level=level,total=total) 
    else:
        flash("Please login to access this page!!")
        return redirect(url_for('userLogin'))

#-----------------------------------------------------------------
#---------------- Admin ------------------------------------------
#-----------------------------------------------------------------

@app.route('/adminLogin',methods=["POST","GET"])
def adminLogin():
    if request.method == 'GET':
        return render_template('adminLogin.html')
    else:
        user = request.form['user']
        password = request.form['password']
        status=adminObj.adminLogin(user,password)
        if status:
            return redirect(url_for('adminDash'))
        else:
            flash("invalid user or password!!!")
            return redirect(url_for('adminLogin'))

@app.route('/adminLogout')
def adminLogout():
    session.clear()
    flash("logged out successfully!!!")
    return redirect(url_for('adminLogin'))

@app.route('/adminDash',methods=['GET','POST'])
def adminDash():
    if 'admin' in session:
        if request.method=='GET':
            return render_template('adminDash.html')
    else:
        flash("Please login to access this page!!")
        return redirect(url_for('adminLogin'))

@app.route('/quizForm',methods=['POST','GET'])
def quizForm():
    if 'admin' in session:
        if request.method == 'GET':
            return render_template('quizForm.html')
        else:
            level = request.form['level']
            ques = request.form['ques']
            opt1 = request.form['opt1']
            opt2 = request.form['opt2']
            answer = request.form['answer']

            adminObj.quizInsert(level,ques,opt1,opt2,answer)
            flash("Question is Added Successfully!!")
            return redirect(url_for('quizForm'))
    else:
        flash("Please login to access this page!!")
        return redirect(url_for('adminLogin'))

@app.route('/quizView',methods=['GET','POST'])
def quizView():
    if 'admin' in session:
        if request.method=='GET':
            record = adminObj.quizView()
            return render_template('quizView.html',record=record)
    else:
        flash("Please login to access this page!!")
        return redirect(url_for('adminLogin'))

@app.route('/quizDelete',methods=['GET','POST'])
def quizDelete():
    if 'admin' in session:
        if request.method=='GET':
            quesID = request.args.get('quesID')
            adminObj.quizDelete(quesID)
            flash("Question is deleted successfully!!!")
            return redirect(url_for('quizView'))
    else:
        flash("Please login to access this page!!")
        return redirect(url_for('adminLogin'))

@app.route('/userRecord',methods=['GET','POST'])
def userRecord():
    if 'admin' in session:
        if request.method=='GET':
            record = adminObj.userRecord()
            return render_template('userRecord.html',record=record)
    else:
        flash("Please login to access this page!!")
        return redirect(url_for('adminLogin'))

import traceback

@app.errorhandler(500)
def internal_error(e):
    tb = traceback.format_exc()
    return f"<pre>500 Internal Server Error\n\n{tb}\n\nOriginal error: {e}</pre>", 500

@app.errorhandler(Exception)
def handle_exception(e):
    tb = traceback.format_exc()
    return f"<pre>Error: {type(e).__name__}\n\n{tb}\n\nDetails: {e}</pre>", 500


if __name__=='__main__':
    app.run(port=5001,debug=True)   # server activate  #debug=true :- auto save   # port= 5001  :- to change port

