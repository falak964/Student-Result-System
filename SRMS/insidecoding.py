

pass1 =input("Enter Password: ")
l,u,p,d=0,0,0,0
if len(pass1)>=8:
    for i in pass1:
        if(i.islower()):
            l+=1   
        elif(i.isupper()):
            u+=1 
        elif(i.isdigit()):
            d+=1 
        elif(i=='@'or i=='&'or i=='#' or i=='!' or i=='_'):
            p+=1 
    if(l>=1 and u>=1 and d>=1 and p>=1):
        print("Valid Password")
    else:
        print("Invalid Password")
else:
    print("Invalid Password")

    
FirstName = 'Shubham'
LastName= "kumbhar"
fn = 0
ln = 0
for i in FirstName:
    if i.isupper() or i.islower():
        fn+=1 
for i in LastName:
    if i.isupper() or i.islower():
        ln+=1 
if fn == len(FirstName) and ln == len(LastName):
    print("OK")
else:
    print("Error")



contact="1234567288"
s = 0
for i in contact:
    if i.isdigit():
        s+=1
if s==10:
    print("Continue")
else:
    print("error")




k=pass1[-10:-1]
j=k+"m"
print(j)

if(j!="@gmail.com"):
    print("error")
else:
    print("Ok")