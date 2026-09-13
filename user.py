from db import get_connection
from flask import session
from datetime import date

class UserOperation:
    def connection(self):
        return get_connection()
    

    def userInsert(self,firstName,lastName,email,mobile,password):
        db = self.connection()
        cur = db.cursor()
        sq = "insert into user (firstName,lastName,email,mobile,password) values(%s,%s,%s,%s,%s)"
        record = [firstName,lastName,email,mobile,password]
        cur.execute(sq,record)
        db.commit()  #save the database
        cur.close()
        db.close()
        return


    def userDelete(self,email):
        db = self.connection()
        cur = db.cursor()
        sq = "delete from user where email=%s"
        record = [email]
        cur.execute(sq,record)
        db.commit()  #save the database
        cur.close()
        db.close()
        return
    
    def userLogin(self,email,password):
        db = self.connection()
        cur = db.cursor()
        sq = "select firstName, email from user where email=%s and password=%s"
        record = [email,password]
        cur.execute(sq,record)
        row= cur.fetchall()
        cur.close()
        db.close()
        if row:
            session['userName'] = row[0][0]
            session['userEmail'] = row[0][1]
            return True
        return False

    def userProfile(self):
        db = self.connection()
        cur = db.cursor()
        sq = "select firstName,lastName,email,mobile from user where email=%s"
        record = [session['userEmail']]
        cur.execute(sq,record)
        row= cur.fetchall()
        cur.close()
        db.close()
        return row

    def userUpdate(self,firstName,lastName,mobile):
        db = self.connection()
        cur = db.cursor()
        sq = "update user set firstName=%s,lastName=%s,mobile=%s where email=%s"
        record = [firstName,lastName,mobile,session['userEmail']]
        cur.execute(sq,record)
        db.commit()
        session['userName'] = firstName
        cur.close()
        db.close()
        return

    def userPassword(self,oldPassword,newPassword):
        db = self.connection()
        cur = db.cursor()
        sq = "select * from user where email=%s and password=%s"
        record = [session['userEmail'],oldPassword]
        cur.execute(sq,record)
        row = cur.fetchall()
        if row:
            sq = "update user set password=%s where email=%s"
            record= [newPassword,session['userEmail']]
            cur.execute(sq,record)
            db.commit()
            cur.close()
            db.close()
            return True
        else:
            cur.close()
            db.close()
            return False

    def userQuizQues(self,level):
        db = self.connection()
        cur = db.cursor()
        sq = "select quesID,ques,opt1,opt2 from quiz where level=%s"
        record=[level]
        cur.execute(sq,record)
        row = cur.fetchall()
        cur.close()
        db.close()
        return row

    def userAnsCheck(self,ans):
        db = self.connection()
        cur = db.cursor()
        count = 0
        for quesID,answer in ans.items():
            try:
                qid = int(quesID)
            except (ValueError, TypeError):
                continue
            sq = "select * from quiz where quesID=%s and answer=%s"
            record=[qid,answer]
            cur.execute(sq,record)
            row = cur.fetchall()
            
            if row:
                count += 1

        cur.close()
        db.close()
        return count

    def scorecardInsert(self,level,score):
        db = self.connection()
        cur = db.cursor()
        playDate = date.today()
        sq = "insert into scorecard (userEmail,level,score,playDate) values(%s,%s,%s,%s)"
        record = [session['userEmail'],level,score,playDate]
        cur.execute(sq,record)
        db.commit() 
        cur.close()
        db.close()
        return
    
    def userScore(self,level):
        db = self.connection()
        cur = db.cursor()
        sq = "select score from scorecard where userEmail=%s and level=%s "
        record = [session['userEmail'],level]
        cur.execute(sq,record)
        row = cur.fetchall()
        if row:
            for r in row:
                pass
            return r[0]
        else:
            return None
    
    def userTopRank(self,level):
        db = self.connection()
        cur = db.cursor()
        sq = "select firstName,score,DENSE_RANK() OVER (order by score DESC) as 'rank' from scorecard s,user u where s.userEmail=u.email and level=%s limit 3"
        record = [level]
        cur.execute(sq,record)
        row = cur.fetchall()
        return row
    
    def userTotal(self,level):
        db = self.connection()
        cur = db.cursor()
        sq = "select count(*) from scorecard where level=%s"
        record = [level]
        cur.execute(sq,record)
        row = cur.fetchall()
        if row:
            return row[0][0]
        else:
            return 0