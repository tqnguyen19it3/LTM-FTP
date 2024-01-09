from ftplib import FTP

a = FTP('192.168.1.2') # Put your server ip address here
a.login('tqnguyen', '12345')
print(a.pwd())
print(a.dir())