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

def check(arr,arr1):
    st=0
    ba=0
    for i in range(0,4):
        if arr[i]==arr1[i]:
            st=st+1
    for i in range(0,4):
        for j in range(0,4):
            if i==j:
                continue
            elif arr[i]==arr1[j]:
                ba=ba+1
    return st,ba


def check_sb(arr,s,b):
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
        
        st,ba=check(iarr,rearr)
        if st!=s or ba!=b:
            guesslist.remove(i)

    return

start=0
serverPort = 12000 #port number
serverSocket=socket(AF_INET,SOCK_STREAM) #Create Server Sockets
serverSocket.bind(('',serverPort)) #Relate the serverport to the socket.
serverSocket.listen(1) #Allow the server to listen to TCP connection requests from clients.
print('The server is ready to receive a game request.')
connectionSocket,addr=serverSocket.accept() #Create TCP connections with handshake.

while True:
    receive_msg = connectionSocket.recv(1024).decode() #receive message
    if receive_msg[0:2]=='MA': 
        print('From Client:'+receive_msg[2:])
        send_msg='MBgame_grant'
        print('To Client:'+send_msg[2:])
        connectionSocket.send(send_msg.encode())
        print('Answer:'+str_answer)
    elif receive_msg[0:2]=='MC':
        print('From Client:'+receive_msg[2:])
        if receive_msg[16]=='4' :
            print('Server Win!')
            break
        elif receive_msg[3]==receive_msg[6] or receive_msg[3]==receive_msg[9] or receive_msg[3]==receive_msg[12] or receive_msg[6]==receive_msg[9] or receive_msg[6]==receive_msg[12] or receive_msg[9]==receive_msg[12]:
            print('Wrong guess (same digits)!')
            break
        
        
        receive_arr=[]
        receive_arr.append(int(receive_msg[3]))
        receive_arr.append(int(receive_msg[6]))
        receive_arr.append(int(receive_msg[9]))
        receive_arr.append(int(receive_msg[12]))
        
        strike,ball=check(receive_arr,answer)



        if strike ==4:
            check_sb(guess,int(receive_msg[16]),int(receive_msg[19]))
            guess= random.choice(guesslist)
            send_msg='MC['+guess[0]+', '+guess[1]+', '+guess[2]+', '+guess[3]+']/['+repr(strike)+', '+repr(ball)+']'
            connectionSocket.send(send_msg.encode())
            print('To Client:'+send_msg[2:])
            receive_msg = connectionSocket.recv(1024).decode()
            print('From Client:'+receive_msg[2:])
            if receive_msg[16]=='4':
                print('Draw!')
                break
            else:
                print('Server Lose!')
                break

        if start==0: #If I haven't sent any predictions yet
            start=1
        else:
            check_sb(guess,int(receive_msg[16]),int(receive_msg[19]))
            if not guesslist: #When the list is empty
                print('Wrong player!')
                break
            guess= random.choice(guesslist)
    
        send_msg='MC['+guess[0]+', '+guess[1]+', '+guess[2]+', '+guess[3]+']/['+repr(strike)+', '+repr(ball)+']'
        connectionSocket.send(send_msg.encode())
        print('To Client:'+send_msg[2:])
    else:# error
        print('Wrong player!')
        break
        
connectionSocket.close() #close socket
