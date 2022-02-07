#This allows the creation of sockets within a program.
from socket import * 

#To generate random numbers.
import random


#A declaration of a list to contain the answers that the other person should guesses.
answer=[] 
while True:
    rd = random.randint(0, 9) #0~9
    if(not rd in answer): #Not to draw the same number.
        answer.append(rd) 
        if len(answer) == 4:#When it fill in all four numbers, it exits the loop.
            break
str_answer=repr(answer[0])+repr(answer[1])+repr(answer[2])+repr(answer[3]) #Save answers as strings


#Put all numbers from 0123 to 9876 into the string guesslist[]
guesslist=[]
for i in range(0,10):
    for j in range(0,10):
        if i==j:
            continue
        for k in range(0,10):
            if i==k or j==k:
                continue
            for l in range(0,10):
                if i==l or j==l or k==l:
                    continue
                str_num=repr(i)+repr(j)+repr(k)+repr(l)
                guesslist.append(str_num) #Each of the numbers in the list is designed to have no equal number.

guess= random.choice(guesslist)


def check(arr,arr1): # arr : Array to be verified , arr1 : standard array
    st=0
    ba=0
    
    for i in range(0,4):
        if arr[i] == arr1[i]:
            st=st+1

    for i in range(0,4):
        for j in range(0,4):
            if i==j:
                continue
            elif arr[i]==arr1[j]:
                ba=ba+1

    return st,ba


def check_sb(arr,s,b):#arr:Array sent to opponent, s : Number of strikes received from opponent, b :Number of balls received from opponent
    rearr=[]
    rearr.append(int(arr[0]))
    rearr.append(int(arr[1]))
    rearr.append(int(arr[2]))
    rearr.append(int(arr[3]))

    for i in guesslist[:]:
        iarr=[]
        iarr.append(int(i[0]))
        iarr.append(int(i[1]))
        iarr.append(int(i[2]))
        iarr.append(int(i[3]))
        
        st,ba=check(rearr,iarr)
        if st!=s or ba!=b:
            guesslist.remove(i) #removes elements in the guesslist that do not satisfy the condition 
        
    return

start = input("Do you want a number baseball game? (Yes or No)") #Start Message
serverName='localhost' 
serverPort=12000 #port number
clientSocket=socket(AF_INET,SOCK_STREAM) #Create Client Sockets
flag=0 #Variables that tell you if the results came out
if start == 'No': 
    clientSocket.close() #end
elif start =='Yes':
    clientSocket.connect((serverName, serverPort)) #TCP
    send_msg='MAgame_request'
    print('To Server:'+send_msg[2:])
    clientSocket.send(send_msg.encode()) #send message
    receive_msg=clientSocket.recv(1024).decode() #receive message
    
    if receive_msg[0:2]=='MB': #start!
        print('From Server:'+receive_msg[2:])
        print('Answer:'+str_answer)
        strike=0
        ball=0
        send_msg='MC['+guess[0]+', '+guess[1]+', '+guess[2]+', '+guess[3]+']/['+repr(strike)+', '+repr(ball)+']'
        clientSocket.send(send_msg.encode()) #send first message
        print('To Server:'+send_msg[2:])

    while True :
        receive_msg=clientSocket.recv(1024).decode()
        if receive_msg[0:2]=='MC':
            if receive_msg[3]==receive_msg[6] or receive_msg[3]==receive_msg[9] or receive_msg[3]==receive_msg[12] or receive_msg[6]==receive_msg[9] or receive_msg[6]==receive_msg[12] or receive_msg[9]==receive_msg[12]:
                print('Wrong guess (same digits)!')
                break
            
            print('From Server:'+receive_msg[2:])
            receive_arr=[]
            receive_arr.append(int(receive_msg[3]))
            receive_arr.append(int(receive_msg[6]))
            receive_arr.append(int(receive_msg[9]))
            receive_arr.append(int(receive_msg[12]))

            strike,ball=check(receive_arr,answer)
            
            if receive_msg[16]=='4' and strike==4:
                print('Draw!')
                flag=1
                
            elif receive_msg[16]=='4':
                print('Client Win!')
                flag=1
            elif strike==4:
                guess='0000'
                print('Client Lose!')
                flag=1
            else:
                check_sb(guess,int(receive_msg[16]),int(receive_msg[19]))
                if not guesslist:
                    print('Wrong player!')
                    break
                guess= random.choice(guesslist)
    
            
            send_msg='MC['+guess[0]+', '+guess[1]+', '+guess[2]+', '+guess[3]+']/['+repr(strike)+', '+repr(ball)+']'
            clientSocket.send(send_msg.encode())
            print('To Server:'+send_msg[2:])
            if flag==1: #end
                break
        else: # error
            print('Wrong player!')
            break

clientSocket.close() #close socket