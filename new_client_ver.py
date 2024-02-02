'''
  ETTTP_TicTacToe_skeleton.py
 
  34743-02 Information Communications
  Term Project on Implementation of Ewah Tic-Tac-Toe Protocol
 
  Skeleton Code Prepared by JeiHee Cho
  May 24, 2023
 
 '''

import random
import tkinter as tk
from socket import *
import _thread

SIZE=1024

class TTT(tk.Tk):
    def __init__(self, target_socket,src_addr,dst_addr, client=True):
        super().__init__()
        
        self.my_turn = -1

        self.geometry('500x800')

        self.active = 'GAME ACTIVE'
        self.socket = target_socket
        
        self.send_ip = dst_addr
        self.recv_ip = src_addr
        
        self.total_cells = 9
        self.line_size = 3
        
        
        # Set variables for Client and Server UI
        ############## updated ###########################
        if client:
            self.myID = 1   #0: server, 1: client
            self.title('34743-02-Tic-Tac-Toe Client')
            self.user = {'value': self.line_size+1, 'bg': 'blue',
                     'win': 'Result: You Won!', 'text':'O','Name':"ME"}
            self.computer = {'value': 1, 'bg': 'orange',
                             'win': 'Result: You Lost!', 'text':'X','Name':"YOU"}   
        else:
            self.myID = 0
            self.title('34743-02-Tic-Tac-Toe Server')
            self.user = {'value': 1, 'bg': 'orange',
                         'win': 'Result: You Won!', 'text':'X','Name':"ME"}   
            self.computer = {'value': self.line_size+1, 'bg': 'blue',
                     'win': 'Result: You Lost!', 'text':'O','Name':"YOU"}
        ##################################################

            
        self.board_bg = 'white'
        self.all_lines = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6))

        self.create_control_frame()

    def create_control_frame(self):
        '''
        Make Quit button to quit game 
        Click this button to exit game

        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.control_frame = tk.Frame()
        self.control_frame.pack(side=tk.TOP)

        self.b_quit = tk.Button(self.control_frame, text='Quit',
                                command=self.quit)
        self.b_quit.pack(side=tk.RIGHT)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def create_status_frame(self):
        '''
        Status UI that shows "Hold" or "Ready"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.status_frame = tk.Frame()
        self.status_frame.pack(expand=True,anchor='w',padx=20)
        
        self.l_status_bullet = tk.Label(self.status_frame,text='O',font=('Helevetica',25,'bold'),justify='left')
        self.l_status_bullet.pack(side=tk.LEFT,anchor='w')
        self.l_status = tk.Label(self.status_frame,font=('Helevetica',25,'bold'),justify='left')
        self.l_status.pack(side=tk.RIGHT,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def create_result_frame(self):
        '''
        UI that shows Result
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.result_frame = tk.Frame()
        self.result_frame.pack(expand=True,anchor='w',padx=20)
        
        self.l_result = tk.Label(self.result_frame,font=('Helevetica',25,'bold'),justify='left')
        self.l_result.pack(side=tk.BOTTOM,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def create_debug_frame(self):
        '''
        Debug UI that gets input from the user
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.debug_frame = tk.Frame()
        self.debug_frame.pack(expand=True)
        
        self.t_debug = tk.Text(self.debug_frame,height=2,width=50)
        self.t_debug.pack(side=tk.LEFT)
        self.b_debug = tk.Button(self.debug_frame,text="Send",command=self.send_debug)
        self.b_debug.pack(side=tk.RIGHT)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    
    def create_board_frame(self):
        '''
        Tic-Tac-Toe Board UI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.board_frame = tk.Frame()
        self.board_frame.pack(expand=True)

        self.cell = [None] * self.total_cells
        self.setText=[None]*self.total_cells
        self.board = [0] * self.total_cells
        self.remaining_moves = list(range(self.total_cells))
        for i in range(self.total_cells):
            self.setText[i] = tk.StringVar()
            self.setText[i].set("  ")
            self.cell[i] = tk.Label(self.board_frame, highlightthickness=1,borderwidth=5,relief='solid',
                                    width=5, height=3,
                                    bg=self.board_bg,compound="center",
                                    textvariable=self.setText[i],font=('Helevetica',30,'bold'))
            self.cell[i].bind('<Button-1>',
                              lambda e, move=i: self.my_move(e, move))
            r, c = divmod(i, self.line_size)
            self.cell[i].grid(row=r, column=c,sticky="nsew")
            
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def play(self, start_user=1):
        '''
        Call this function to initiate the game
        
        start_user: if its 0, start by "server" and if its 1, start by "client"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.last_click = 0
        self.create_board_frame()
        self.create_status_frame()
        self.create_result_frame()
        self.create_debug_frame()
        self.state = self.active
        if start_user == self.myID:
            self.my_turn = 1    
            self.user['text'] = 'X'
            self.computer['text'] = 'O'
            self.l_status_bullet.config(fg='green')
            self.l_status['text'] = ['Ready']
        else:
            self.my_turn = 0
            self.user['text'] = 'O'
            self.computer['text'] = 'X'
            self.l_status_bullet.config(fg='red')
            self.l_status['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def quit(self):
        '''
        Call this function to close GUI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.destroy()
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def my_move(self, e, user_move):    
        '''
        Read button when the player clicks the button
        
        e: event
        user_move: button number, from 0 to 8 
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        
        # When it is not my turn or the selected location is already taken, do nothing
        if self.board[user_move] != 0 or not self.my_turn:
            return
        # Send move to peer 
        valid = self.send_move(user_move)
        
        # If ACK is not returned from the peer or it is not valid, exit game
        if not valid:
            self.quit()
            
        # Update Tic-Tac-Toe board based on user's selection
        self.update_board(self.user, user_move)
        
        # If the game is not over, change turn
        if self.state == self.active:    
            self.my_turn = 0
            self.l_status_bullet.config(fg='red')
            self.l_status ['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def get_move(self):
        '''
        Function to get move from other peer
        Get message using socket, and check if it is valid
        If is valid, send ACK message
        If is not, close socket and quit
        '''
        ###################  Fill Out  #######################
        msg = self.socket.recv(SIZE).decode() # get message using socket

        ip_address = self.recv_ip 
        msg_valid_check = check_msg(msg, ip_address) #ETTTP 형식으로 메세지를 받았는지 check_msg 함수를 통해 확인한다.
         
        
        if not msg_valid_check: # Message is not valid
            self.socket.close()   
            quit(self)
            
        else:  # If message is valid - send ack, update board and change turn

            ack_msg = "ACK" 
            self.socket.send(ack_msg.encode()) 

            start_index = msg.find("(") #받은 메세지에서 좌표 부분만 추출한다. 이는 send_debug함수와 동일한 과정으로 이루어지기 때문에 생략한다.
            end_index = msg.find(")")

            if start_index != -1 and end_index != -1:
                coordinates = msg[start_index+1:end_index]
                n1, n2 = coordinates.strip("()").split(",")

                n1 = int(n1)
                n2 = int(n2)
                if n1 == 0:
                    loc = n2
                elif n1 == 1:
                    loc = 2*n1+n2+1
                elif n1 == 2:
                    loc = 3*n1+n2

            # received next-move
            
            ######################################################   
            
            
            #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
            self.update_board(self.computer, loc, get=True)
            if self.state == self.active:  
                self.my_turn = 1
                self.l_status_bullet.config(fg='green')
                self.l_status ['text'] = ['Ready']
            #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                

    def send_debug(self):
        '''
        Function to send message to peer using input from the textbox
        Need to check if this turn is my turn or not
        '''

        if not self.my_turn:
            self.t_debug.delete(1.0,"end")
            return
        # get message from the input box
        d_msg = self.t_debug.get(1.0,"end")
        d_msg = d_msg.replace("\\r\\n","\r\n")   # msg is sanitized as \r\n is modified when it is given as input
        self.t_debug.delete(1.0,"end")
        
        ###################  Fill Out  #######################
       
    
        start_index = d_msg.find("(") #저장한 메세지에서 좌표로 표현되는 선택할 위치를 뽑아준다.
        end_index = d_msg.find(")")   #(n1,n2)만 뽑아 내기 위해 (로 시작하는 부분에서 )로 끝나는 부분을 인덱스로 표싷나다,

        if start_index != -1 and end_index != -1: # (n1,n2)형식으로 표현이 되고 있다면, 보드에 표현하기 위해서 좌표값을 이용하여 loc값을 수정해준다
            coordinates = d_msg[start_index+1:end_index]
            n1, n2 = coordinates.strip("()").split(",") # (n1,n2) 형식에서 각각의 숫자만 빼서 n1과 n2라는 변수에 저장해둔다.

            n1 = int(n1) #문자열 형식으로 저장되어 있는 변수를 int형식으로 변환한다.
            n2 = int(n2)
            if n1 == 0:
                loc = n2 #(0,0)->loc=0, (0,1)->loc=1,(0,2)->loc=2를 계산하는 식
            elif n1 == 1:
                loc = 2*n1+n2+1 #(1,0)->loc=0, (1,1)->loc=1,(1,2)->loc=2를 계산하는 식
            elif n1 == 2:
                loc = 3*n1+n2 #(2,0)->loc=0, (2,1)->loc=1,(2,2)->loc=2를 계산하는 식
        
        
        if self.board[loc] != 0: # 선택한 위치가 이미 선택이 되어있다면 프로그램을 종료해야함
            self.socket.close()#소켓을 닫고, quit함수를 호출해서 종료한다.
            self.quit()
        self.socket.send(d_msg.encode()) #메세지를 peer로 전송한다.
        ack, addr = self.socket.recvfrom(SIZE)
        
        if ack.decode() != "ACK": #메세지를 받은 peer에서 ACK를 보냈는지 (정확하게 수신되었는지)
            return False
        

        ######################################################  
        
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.update_board(self.user, loc)
            
        if self.state == self.active:    # always after my move
            self.my_turn = 0
            self.l_status_bullet.config(fg='red')
            self.l_status ['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
            
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
        
    def send_move(self,selection):
        '''
        Function to send message to peer using button click
        selection indicates the selected button
        '''
        row,col = divmod(selection,3) #색칠할 부분의 행 번호와 렬 번호를 추출한다.
        ###################  Fill Out  #######################

        # send message and check ACK
        msg = f"SEND ETTTP/1.0\r\nHost:{self.send_ip}\r\nNew-Move:({row},{col})\r\n\r\n"#host ip와 추출한 행렬을 대입하여 메세징한다.
        self.socket.send(msg.encode()) #소켓을 통해서 보낸다.

        ack_msg = self.socket.recv(SIZE).decode()#peer측에서 잘 받았는지 확인하기 위한 ACK 받아온다.

        if ack_msg == "ACK":
            return True
        else:
            self.socket.close()
            quit(self)

        ######################################################  

    
    def check_result(self,winner,get=False):
        '''
        Function to check if the result between peers are same
        get: if it is false, it means this user is winner and need to report the result first
        '''
        # no skeleton
        ###################  Fill Out  #######################

        if get:  #내가 졌을 때 (result를 받아서 처리한다.)
            opponent_result = self.socket.recv(SIZE).decode().strip()
            if opponent_result == str(self):
                return True
            else:
                return False
        else:   #내가 이겼을 때 (result를 보내서 처리한다.)
            self.socket.send(self.encode())
            opponent_result = self.socket.recv(SIZE).decode().strip()
            if opponent_result == str(winner['Name']):
                return True
            else:
                return False

        ######################################################  

        
    #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
    def update_board(self, player, move, get=False):
        '''
        This function updates Board if is clicked
        
        '''
        self.board[move] = player['value']
        self.remaining_moves.remove(move)
        self.cell[self.last_click]['bg'] = self.board_bg
        self.last_click = move
        self.setText[move].set(player['text'])
        self.cell[move]['bg'] = player['bg']
        self.update_status(player,get=get)

    def update_status(self, player,get=False):
        '''
        This function checks status - define if the game is over or not
        '''
        winner_sum = self.line_size * player['value']
        for line in self.all_lines:
            if sum(self.board[i] for i in line) == winner_sum:
                self.l_status_bullet.config(fg='red')
                self.l_status ['text'] = ['Hold']
                self.highlight_winning_line(player, line)
                correct = self.check_result(player['Name'],get=get)
                if correct:
                    self.state = player['win']
                    self.l_result['text'] = player['win']
                else:
                    self.l_result['text'] = "Somethings wrong..."

    def highlight_winning_line(self, player, line):
        '''
        This function highlights the winning line
        '''
        for i in line:
            self.cell[i]['bg'] = 'red'

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# End of Root class

def check_msg(msg, recv_ip):
    '''
    Function that checks if received message is ETTTP format
    '''
    ###################  Fill Out  #######################

    if not msg.startswith("SEND ETTTP/1.0\r\n"):
        return False #입력받은 메세지가 ETTTP 형식인지 확인
    
    ip_start = msg.find("Host:") + len("Host:")# host IP 추출
    ip_end = msg.find("\r\n", ip_start)
    if ip_start == -1 or ip_end == -1:
        return False
    
    received_ip = msg[ip_start:ip_end].strip()
    if received_ip == recv_ip: #추출한 IP가 수신 IP 주소와 일치하는지 확인
        return True

    return False
    ######################################################  


if __name__ == '__main__':

    SERVER_IP = '127.0.0.1'
    MY_IP = '127.0.0.1'
    SERVER_PORT = 12000
    SIZE = 1024
    SERVER_ADDR = (SERVER_IP, SERVER_PORT)

    with socket(AF_INET, SOCK_STREAM) as client_socket:
        client_socket.connect(SERVER_ADDR)
        #RECEIVE WHO WILL START FIRST FROM THE SERVER
        start = client_socket.recv(SIZE).decode()
        #SEND ACK
        client_socket.send(str("ACK").encode())

        #게임 시작
        root = TTT(target_socket=client_socket, src_addr=MY_IP, dst_addr=SERVER_IP)
        root.play(start_user=start)
        root.mainloop()
        client_socket.close() # 게임 종료-> 클라이언트 소켓을 닫는다.
