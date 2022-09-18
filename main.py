from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.videoplayer import VideoPlayer
import socket, cv2, pickle, struct, pafy
from kivy.uix.video import Video
from kivy.uix.videoplayer import VideoPlayer


class Screen_Welcome (Screen):
    pass
class Screen_Home (Screen):
    pass
class Screen_LiveStreaming (Screen):
    pass
class Screen_VideoPlayer (Screen):
    pass
class Screen_YouTubePlayer (Screen):
    pass
class Screen_ChatRoom (Screen):
    pass
class Screen_Manager (ScreenManager):
    pass

window_size = Window.size
x = int(window_size[0]) 
y = int(window_size[1]) 

class Streamer(MDApp):
    def build(self):
        window_size = Window.size
        x = int(window_size[0]) 
        y = int(window_size[1])

        self.theme_cls.theme_style= 'Light'
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.accent_palette = 'Orange'
        return Builder.load_file('main.kv')
    def forward(self):
        x="A2.mp4" 
        self.root.get_screen('Home').ids.Video.source = x
    def backward(self):
        x="A6.mp4" 
        self.root.get_screen('Home').ids.Video.source = x
    def VideoPlay(self):
        x= str(self.root.get_screen('VideoPlayer').ids.Video_path.text) 
        self.root.get_screen('VideoPlayer').ids.Video.source = x
    def YouTubePlay(self):
        url = self.root.get_screen('YoutubePlayer').ids.url.text
        data = pafy.new(url )
        data = data.getbest(preftype="mp4")
        cap = cv2.VideoCapture()   #Here parameter 0 is a path of any video use for webcam
        cap.open(data.url)

        #it is 4 byte code which is use to specify the video codec
        fourcc = cv2.VideoWriter_fourcc(*"XVID")  # *"XVID"
        #It contain 4 parameter , name, codec,fps,resolution
        output = cv2.VideoWriter("output.avi",fourcc,20.0,(640,480),0)

        while(cap.isOpened()):
            ret, frame = cap.read()   #here read the frame
            
            if ret==True:
                
                gray  = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                #here flip is used to lip the video at recording time
                #frame = cv2.flip(frame,0)
                #output.write(gray)
                
                #cv2.imshow("Gray Frame",gray)
                cv2.imshow('Colorframe',frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):   #press to exit
                    break
            else:
                break
            
        # Release everything if job is finished
        cap.release()
        output.release()
        cv2.destroyAllWindows()
    def responce(self):
        y = self.root.get_screen('ChatRoom').ids.message.text
        return y
    def ChatRooms(self):
        import time, socket, sys
        print('Setup Server...')
        time.sleep(1)
        #Get the hostname, IP Address from socket and set Port
        soc = socket.socket()
        host_name = socket.gethostname()
        ip = socket.gethostbyname(host_name)
        port = 1234
        soc.bind((host_name, port))
        print(host_name, '({})'.format(ip))
        #name = input('Enter name: ')
        name = self.root.get_screen('ChatRoom').ids.message.text
        self.root.get_screen('ChatRoom').ids.message.hint_text = "Enter the message..."
        self.root.get_screen('ChatRoom').ids.message.text =""
        soc.listen(1) #Try to locate using socket
        print('Waiting for incoming connections...')
        connection, addr = soc.accept()
        print("Received connection from ", addr[0], "(", addr[1], ")\n")
        print('Connection Established. Connected From: {}, ({})'.format(addr[0], addr[0]))
        #get a connection from client side
        client_name = connection.recv(1024)
        client_name = client_name.decode()
        print(client_name + ' has connected.')
        print('Press [bye] to leave the chat room')
        connection.send(name.encode())
        while True:
            message = input('Me> ')
            if message == '[bye]':
                message = 'Good Night...'
                connection.send(message.encode())
                print("\n")
                break
            connection.send(message.encode())
            message = connection.recv(1024)
            message = message.decode()
            print(client_name, '>', message)

    def LiveStream(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        port = 9999
        print("Host_ip: ",host_ip,port)

        socket_address = (host_ip, port)

        server_socket.bind(socket_address)

        server_socket.listen(5)
        print("Listening at:",socket_address)
        while True:
            client_socket,addr = server_socket.accept()
            print("GOT Connection from:",addr)
            if client_socket:
                vid = cv2.VideoCapture(1)
                while(vid.isOpened()):
                    img,frame = vid.read()
                    cv2.imshow('Transmitting video...',frame)
                    key  = cv2.waitKey(24) & 0xFF
                    if key == ord('q'):
                        client_socket.close()
                    a = pickle.dumps(frame)
                    message = struct.pack("Q",len(a))+a
                    client_socket.sendall(message)
        
                    
        

Streamer().run()