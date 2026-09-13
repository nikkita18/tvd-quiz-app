
from db import get_connection
from flask import session


class AdminOperation:
    def connection(self):
        return get_connection()
    
    def adminLogin(self,user,password):
        if user=='admin' and password=='admin1234':
            session['admin']='admin'
            return True
        
        return False
        
    
    def quizInsert(self,level,ques,opt1,opt2,answer):
        db = self.connection()
        cur = db.cursor()
        sq = "insert into quiz (level,ques,opt1,opt2,answer) values(%s,%s,%s,%s,%s)"
        record = [level,ques,opt1,opt2,answer]
        cur.execute(sq,record)
        db.commit()  #save the database
        cur.close()
        db.close()
        
    def quizView(self):
        db = self.connection()
        cur = db.cursor()
        sq = "select quesID,level,ques,opt1,opt2,answer from quiz order by level"
        cur.execute(sq)
        row = cur.fetchall()
        return row
    
    def quizDelete(self,quesID):
        db = self.connection()
        cur = db.cursor()
        sq = "delete from quiz where quesID=%s"
        record = [quesID]
        cur.execute(sq,record)
        db.commit()  #save the database
        cur.close()
        db.close()
    
    def userRecord(self):
        db = self.connection()
        cur = db.cursor()
        sq = "select firstName,lastName,mobile,email from user"
        cur.execute(sq)
        row = cur.fetchall()
        return row

    
    
    
