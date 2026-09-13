import hashlib    #buit-in module

def encrypt(data):
    data = hashlib.sha256(data.encode())
    data = data.hexdigest()   # convert hexacode into string
    return data