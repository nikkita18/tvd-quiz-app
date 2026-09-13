class Validation:
    def checkEmpty(self,fieldList):
        for f in fieldList:
            if f =='': #    '' :- means empty
                return True
        return False


    def checkMobile(self,data):
        if len(data)!=10 or not data.isdigit():
            return True
        return False
    
    # h.w  :- string validation 
    def checkStr(self,data):
        if not data.isalpha():
            return True
        return False