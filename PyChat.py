import time,os,datetime
from tkinter import *
from tkinter import messagebox
class afterlogin():
    def __init__(self,username_signin):
        self.username_signin=username_signin
        self.realname_username()
        self.lstart()
    def realname_username(self):
        namer=open(r"personal_user_database/"+self.username_signin+"/database/"+self.username_signin+".txt","r+")
        self.Real_Name=namer.readlines()[0]
    def friend_detector(self,given,work=None):
        if given==None:
            messagebox.showerror("Violation!","Please select your Friend.")
        else:
            if work=="to_send":
                self.var=given
            else:
                self.mess_reading=given
            self.root1.destroy()
    def friend_list_displayer(self,message="These are Your Friends!",work="only_display"):
        self.root1 = Tk()
        self.root1.config(bg="#fad6a5")
        self.root1.geometry("320x400")
        list_of_friends=os.listdir(r'personal_user_database')
        list_of_friends.remove(self.username_signin)
        if work=="to_send":
            Label(self.root1,text=message+"           \n"+"-"*160,bg="#fad6a5").pack()
        if work=="read_mess":
            Label(self.root1,text=message+"           \n"+"-"*160,bg="#fad6a5").pack()
        self.canvas = Canvas(self.root1, height=200,bg="#fad6a5")
        self.frame = Frame(self.canvas)
        self.scrollbar = Scrollbar(self.root1, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw", tags="frame")
        self.frame.bind("<Configure>", lambda x: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.root1.bind("<Down>", lambda x: self.canvas.yview_scroll(3, 'units'))
        self.root1.bind("<Up>", lambda x: self.canvas.yview_scroll(-3, 'units'))
        self.root1.bind("<MouseWheel>", lambda x: self.canvas.yview_scroll(int(-1*(x.delta/40)), "units"))
        friend_list=[]
        list_of_mess=[]
        for x in list_of_friends:
            file=open(r'personal_user_database/'+x+'/database/'+x+'.txt','r+')
            friend_name=file.readlines()[0]
            friend_name=friend_name.rstrip("\n")
            y=friend_name+"   <"+x+">"
            bi=open(r"personal_user_database/"+x+"/bio/bio.txt","r")
            bio=bi.read()
            if bio=="":
                bio="No Bio to Show"
            if work=="only_display":
                y=y+"\n    Bio: "+bio
                friend_list.append(y)
            else:
                list_of_mess.append(y)
        if work=="only_display":
            def display_send():
                self.root1.destroy()
                self.messenger()
            self.root1.title("Friend List")
            self.root1.iconbitmap(r'pictures\friends.ico')
            self.root1.geometry("625x380")
            self.root1.maxsize(width=625,height=380)
            self.labels_mess = [Label(self.frame, text=str("    "+i+"\n"+'-'*100),bg="#b4ffff",justify=LEFT) for i in friend_list]
            for l in self.labels_mess: l.pack(fill=X)            
            button_send_a_message=Button(self.root1,text="Send a Message",command=display_send,bg="#fecaca")
            button_send_a_message.pack()
            button_send_a_message.place(x=510,y=50)
            button_quit=Button(self.root1,text="Back",command=self.root1.destroy,bg="#fecaca",width=12)
            button_quit.pack()
            button_quit.place(x=510,y=150)
        if work=="to_send" or work=="read_mess":
            self.root1.geometry("700x470")
            self.root1.maxsize(width=700,height=470)
            if work=="to_send":
                self.root1.title("Select to Send")
                self.root1.iconbitmap(r'pictures\selecttosend.ico')
            else:
                self.root1.title("Select to Read")
                self.root1.iconbitmap(r'pictures\selecttoreacd.ico')
            text=None
            def protocolhandler():
                    self.friend_detector(text)
            def btn_to_send(btn):
                text=btn.cget("text")
                text=text.split("<")
                text=text[1]
                text=text.rstrip(">")
                self.friend_detector(text,work)
            self.buttons = [Button(self.frame, text=str(i),bg="#b4ffff",padx=130) for i in list_of_mess]
            for l in self.buttons: l.pack(fill=X)
            for I in self.buttons:
                I.config(command=lambda btn=I: btn_to_send(btn))
            self.root1.protocol("WM_DELETE_WINDOW", protocolhandler)
            button_quit=Button(self.root1,text="Cancel",command=self.root1.destroy,width=12,bg="#fecaca")
            button_quit.pack()
            button_quit.place(x=585,y=235)
        self.root1.mainloop()
    def messenger(self,var=""):
        def protocolhandler():
            messagebox.showerror("Don't Quit","Go Back and Write Something.")
        self.var=var
        if self.var=="":
            self.friend_list_displayer("Select the friend whom you want to send message","to_send")
        if self.var!="":
            if "\n" in self.var:
                self.var=self.var.split("\n")[1]
                self.var=self.var.rstrip(" ")
                self.var=self.var.rstrip(">")
                self.var=self.var.lstrip(" ")
                self.var=self.var.lstrip("<")
            root=Tk()
            root.geometry("535x245")
            root.maxsize(width=535,height=245)
            root.config(bg="#fad6a5")
            scrollbar=Scrollbar(root)
            scrollbar.pack(side=RIGHT,fill=Y)
            name_of_receiver=open(r'personal_user_database/'+self.var+'/database/'+self.var+'.txt',"r+")
            name_of_receiver=name_of_receiver.readlines()[0]
            root.title("Message for    "+name_of_receiver)
            root.iconbitmap(r'pictures\writing.ico')
            text=Text(root, yscrollcommand = scrollbar.set ,height=15,width=55,bg="#dcffd2")
            text.pack(side=RIGHT,fill=BOTH )
            scrollbar.config( command = text.yview )
            def message_collecter():
                t=text.get("1.0", "end-1c")
                if t!="":
                    check=os.listdir(r'message_godown')
                    if not((self.username_signin+'$'+self.var in check) or (self.var+'$'+self.username_signin in check)):
                            os.mkdir(r'message_godown/'+self.username_signin+'$'+self.var)
                            inbox=open(r'message_godown/'+self.username_signin+'$'+self.var+'/'+self.username_signin+'$'+self.var+'.txt' ,"a+")
                            inbox.close()
                    check=os.listdir(r'message_godown')
                    if (self.username_signin+'$'+self.var not in check):
                        try:
                            inbox=open(r'message_godown/'+self.var+'$'+self.username_signin+'/'+self.username_signin+'$'+self.var+'.txt' ,"r+")
                            inbox=open(r'message_godown/'+self.var+'$'+self.username_signin+'/'+self.username_signin+'$'+self.var+'.txt' ,"a+")
                            inbox=open(r'message_godown/'+self.var+'$'+self.username_signin+'/'+self.username_signin+'$'+self.var+'.txt' ,"r+")
                            previous_message=inbox.read()
                            inbox=open(r'message_godown/'+self.var+'$'+self.username_signin+'/'+self.username_signin+'$'+self.var+'.txt' ,"r+")
                            inbox.truncate()
                            inbox.flush()
                            inbox.close()
                            inbox=open(r'message_godown/'+self.var+'$'+self.username_signin+'/'+self.username_signin+'$'+self.var+'.txt' ,"a+")
                            inbox.write(self.username_signin+"::>   "+t+"\n")
                            inbox=open(r'message_godown/'+self.var+'$'+self.username_signin+'/'+self.username_signin+'$'+self.var+'.txt' ,"a+")
                            inbox.write(previous_message)
                            inbox.flush()
                            inbox.close()
                        except:
                            inbox=open(r'message_godown/'+self.var+'$'+self.username_signin+'/'+self.var+'$'+self.username_signin+'.txt' ,"r+")
                            previous_message=inbox.read()
                            inbox=open(r'message_godown/'+self.var+'$'+self.username_signin+'/'+self.var+'$'+self.username_signin+'.txt' ,"r+")
                            inbox.truncate()
                            inbox.flush()
                            inbox.close()
                            inbox=open(r'message_godown/'+self.var+'$'+self.username_signin+'/'+self.var+'$'+self.username_signin+'.txt' ,"a+")
                            inbox.write(self.username_signin+"::>   "+t+"\n")
                            inbox=open(r'message_godown/'+self.var+'$'+self.username_signin+'/'+self.var+'$'+self.username_signin+'.txt' ,"a+")
                            inbox.write(previous_message)
                            inbox.flush()
                            inbox.close()
                    else:
                        try:
                            inbox=open(r'message_godown/'+self.username_signin+'$'+self.var+'/'+self.username_signin+'$'+self.var+'.txt' ,"r+")
                            inbox=open(r'message_godown/'+self.username_signin+'$'+self.var+'/'+self.username_signin+'$'+self.var+'.txt' ,"a+")
                            inbox=open(r'message_godown/'+self.username_signin+'$'+self.var+'/'+self.username_signin+'$'+self.var+'.txt' ,"r+")
                            previous_message=inbox.read()
                            inbox=open(r'message_godown/'+self.username_signin+'$'+self.var+'/'+self.username_signin+'$'+self.var+'.txt' ,"r+")
                            inbox.truncate()
                            inbox.flush()
                            inbox.close()
                            inbox=open(r'message_godown/'+self.username_signin+'$'+self.var+'/'+self.username_signin+'$'+self.var+'.txt' ,"a+")
                            inbox.write(self.username_signin+"::>   "+t+"\n")
                            inbox=open(r'message_godown/'+self.username_signin+'$'+self.var+'/'+self.username_signin+'$'+self.var+'.txt' ,"a+")
                            inbox.write(previous_message)
                            inbox.flush()
                            inbox.close()
                        except:
                            inbox=open(r'message_godown/'+self.username_signin+'$'+self.var+'/'+self.var+'$'+self.username_signin+'.txt' ,"r+")
                            previous_message=inbox.read()
                            inbox=open(r'message_godown/'+self.username_signin+'$'+self.var+'/'+self.var+'$'+self.username_signin+'.txt' ,"r+")
                            inbox.truncate()
                            inbox.flush()
                            inbox.close()
                            inbox=open(r'message_godown/'+self.username_signin+'$'+self.var+'/'+self.var+'$'+self.username_signin+'.txt' ,"a+")
                            inbox.write(self.username_signin+"::>   "+t+"\n")
                            inbox=open(r'message_godown/'+self.username_signin+'$'+self.var+'/'+self.var+'$'+self.username_signin+'.txt' ,"a+")
                            inbox.write(previous_message)
                            inbox.flush()
                            inbox.close()
                    messagebox.showinfo("Success","Message Send Successfully")
                    root.destroy()
                else:
                    messagebox.showerror("Don't Quit","Go Back and Write Something.")
            button=Button(root, text="Send", command=message_collecter,bg="#fecaca",padx=20)
            button.pack()
            button.place(y=70)
            button1=Button(root,text="Cancel",command=root.destroy,bg="#fecaca",padx=15)
            button1.pack()
            button1.place(y=120)
            root.protocol("WM_DELETE_WINDOW", protocolhandler)
            root.mainloop()
    def inboxer(self):
        self.mess=Tk()
        self.mess.title("Inbox")
        self.mess.iconbitmap(r'pictures\inbox.ico')
        self.mess.config(bg="#fad6a5")
        varct=0
        first_line_message_list=[]
        for x in os.listdir(r'message_godown'):
            if self.username_signin in x:
                varct+=1
                reader=open(r'message_godown/'+x+'/'+x+'.txt',"r+")
                inboxer_message=reader.readlines()[0]
                if inboxer_message.startswith(self.username_signin):
                    inboxer_message=inboxer_message.replace(self.username_signin,'You')
                reader.close()
                inboxer_message=inboxer_message.rstrip("\n")
                x=x.split("$")
                x.remove(self.username_signin)
                x=x[0]
                reader1=open(r'personal_user_database/'+x+'/database/'+x+'.txt',"r+")
                inboxer_name=reader1.readlines()[0]
                inboxer_name=inboxer_name.rstrip("\n")
                first_line_message_list.append(inboxer_name+" ||   "+inboxer_message+"\n"+"-"*150)
        if varct==0:
            self.mess.geometry("380x150")
            self.mess.maxsize(height=150,width=380)
            def first_message():
                self.mess.destroy()
                self.messenger()
            Label(self.mess,text="There are no Messages yet, Try sending messages to your friends\n"+"-"*500+"\n",bg="#fad6a5").pack()
            button_new=Button(self.mess,text="Send Your New Message",command=first_message,bg="#fecaca")
            button_new.pack()
            button_new.place(x=50,y=80)
            button_cancel=Button(self.mess,text="Cancel",command=self.mess.destroy,bg="#fecaca")
            button_cancel.pack()
            button_cancel.place(x=270,y=80)
        else:
            def see_n_reply():
                self.mess.destroy()
                self.messenger()
            self.mess.geometry("550x250")
            self.mess.maxsize(height=250,width=550)
            canvas1=Canvas(self.mess, height=200,bg="#fad6a5")
            frame1=Frame(canvas1)
            scrollbar1=Scrollbar(self.mess,orient="vertical", command=canvas1.yview)
            canvas1.configure(yscrollcommand=scrollbar1.set)
            scrollbar1.pack(side="left", fill="y")
            canvas1.pack(side="left", fill="both", expand=True)
            canvas1.create_window((4,4), window=frame1, anchor="nw", tags="frame")
            frame1.bind("<Configure>", lambda x: canvas1.configure(scrollregion=canvas1.bbox("all")))
            self.mess.bind("<Down>", lambda x: canvas1.yview_scroll(3, 'units'))
            self.mess.bind("<Up>", lambda x: canvas1.yview_scroll(-3, 'units'))
            self.mess.bind("<MouseWheel>", lambda x: canvas1.yview_scroll(int(-1*(x.delta/40)), "units"))
            labels_mess1=[Label(frame1,text=str(i),justify=LEFT,bg="#dcffd2") for i in first_line_message_list]
            for l in labels_mess1: l.pack(anchor=W)
            button1_reply=Button(self.mess,text="Reply\nSomeone",command=see_n_reply,bg="#fecaca",padx=6)
            button1_reply.pack()
            button1_reply.place()
            button1_later=Button(self.mess,text="Reply Later",command=self.mess.destroy,bg="#fecaca")
            button1_later.pack()
            button1_later.place(x=480,y=100)
        self.mess.mainloop()
    def lstart(self):
        AfterLogin=Tk()
        AfterLogin.title("Profile")
        AfterLogin.iconbitmap(r'pictures\profile.ico')
        AfterLogin.config(bg="#fad6a5")
        AfterLogin.geometry("350x220")
        AfterLogin.maxsize(height=220,width=350)
        def direct_quit2():
            messagebox.showerror("Violation","Please go through the options")
        def C1():
            AfterLogin.destroy()
            self.messenger()
            self.lstart()
        def C2():
            AfterLogin.destroy()
            self.inboxer()
            self.lstart()
        def C3():
            AfterLogin.destroy()
            self.friend_list_displayer()
            self.lstart()
        def C4():
            AfterLogin.destroy()
            self.mess_reading=""
            self.friend_list_displayer("Select the friend to read message","read_mess")
            if self.mess_reading!="":
                message_list=os.listdir(r'message_godown')
                y=self.username_signin+'$'+self.mess_reading
                filer=open(r'personal_user_database/'+self.mess_reading+'/database/'+self.mess_reading+'.txt',"r+")
                messaged_name=filer.readlines()[0]
                if y not in message_list:
                    y=self.mess_reading+'$'+self.username_signin
                try:
                    file_mess_final=[]
                    file_mess=open(r'message_godown/'+y+'/'+y+'.txt',"r+")
                    for x in file_mess.readlines():
                        x=x.rstrip("\n")
                        if x.startswith(self.username_signin):
                            gonna_append=x.replace(self.username_signin,"You")
                        else:
                            gonna_append=x
                        file_mess_final.append(gonna_append+"\t"*10)
                    global tempo
                    def color_donate(i):
                        color_filer=os.listdir(r'personal_user_database')
                        if i.startswith("You"):
                            return("#e2d6de")
                        if [(i.startswith(x)) for x in color_filer]:
                            return("#d2f8d2")
                    rooted=Tk()
                    def start_chat():
                        rooted.destroy()
                        self.messenger(self.mess_reading)
                    rooted.title("Messages with   "+messaged_name)
                    rooted.iconbitmap(r'pictures\readmessages.ico')
                    rooted.config(bg="#fad6a5")
                    rooted.geometry("920x340")
                    rooted.maxsize(width=920,height=340)
                    canvas_mess = Canvas(rooted, height=200,bg="#fad6a5")
                    frame_mess = Frame(canvas_mess,bg="#fad6a5")
                    scrollbar = Scrollbar(rooted, orient="vertical", command=canvas_mess.yview)
                    canvas_mess.configure(yscrollcommand=scrollbar.set)
                    scrollbar.pack(side="right", fill="y")
                    canvas_mess.pack(side="left", fill="both", expand=True)
                    canvas_mess.create_window((4,4), window=frame_mess, anchor="nw", tags="frame_mess")
                    frame_mess.bind("<Configure>", lambda x: canvas_mess.configure(scrollregion=canvas_mess.bbox("all")))
                    rooted.bind("<Down>", lambda x: canvas_mess.yview_scroll(3, 'units'))
                    rooted.bind("<Up>", lambda x: canvas_mess.yview_scroll(-3, 'units'))
                    rooted.bind("<MouseWheel>", lambda x: canvas_mess.yview_scroll(int(-1*(x.delta/40)), "units"))
                    labels = [Message(frame_mess, text=str(i),justify=LEFT,width=770,bg=color_donate(i)) for i in file_mess_final]
                    for l in labels: l.pack(fill=X)
                    button_mess=Button(rooted,text="Seen",command=rooted.destroy,bg="#fecaca",width=15)
                    button_mess.pack()
                    button_mess.place(x=785,y=140)
                    button_send=Button(rooted,text="Reply",command=start_chat,bg="#fecaca",width=15)
                    button_send.pack()
                    button_send.place(x=785,y=60)
                    rooted.mainloop()
                except:
                    def start_chat():
                        rooted1.destroy()
                        self.messenger(self.mess_reading)
                    rooted1=Tk()
                    rooted1.geometry("390x150")
                    rooted1.config(bg="#fad6a5")
                    rooted1.maxsize(height=150,width=390)
                    rooted1.title("No Chat with   "+messaged_name)
                    Label(rooted1,text="You haven't started any Chat with "+messaged_name+"."+"\nProceed Chatting\n"+"-"*500+"\n",bg="#fad6a5").pack()
                    messaged_name=messaged_name.split(" ")[0]
                    button_new=Button(rooted1,text="Let's Chat",command=start_chat,bg="#fecaca")
                    button_new.pack()
                    button_new.place(x=50,y=80)
                    button_cancel=Button(rooted1,text="Not now",command=rooted1.destroy,bg="#fecaca")
                    button_cancel.pack()
                    button_cancel.place(x=270,y=80)
                    rooted1.mainloop()
            self.lstart()
        def C5():
            def p_handler():
                messagebox.showerror("Don't Quit","Please Go by either 'Yes' or 'No'")
            def for_no():
                confirm_logout.destroy()
            def for_yes():
            	confirm_logout.destroy()
            	AfterLogin.destroy()
            	start=homepage()
            confirm_logout=Tk()
            confirm_logout.title("Log Out")
            confirm_logout.iconbitmap(r'pictures\logout.ico')
            confirm_logout.geometry("250x100")
            confirm_logout.config(bg="#fad6a5")
            confirm_logout.maxsize(height=100,width=250)
            Label(confirm_logout,text="Are you sure want to Log Out??\n"+"-"*140,bg="#fad6a5").pack()
            button_yes=Button(confirm_logout,text="Yes",command=for_yes,bg="#fecaca",padx=25)
            button_yes.pack()
            button_yes.place(x=30,y=55)
            button_no=Button(confirm_logout,text="No",command=for_no,bg="#fecaca",padx=25)
            button_no.pack()
            button_no.place(x=155,y=55)
            confirm_logout.protocol("WM_DELETE_WINDOW", p_handler)
            confirm_logout.mainloop()
        def C6():
            set_ac=Tk()
            def temp_pass():
                set_ac.destroy()
                Temp_pass=Tk()
                Temp_pass.title("Change Password")
                Temp_pass.iconbitmap(r'pictures\changepassword.ico')
                Temp_pass.configure(bg="#fad6a5")
                Temp_pass.geometry("260x130")
                Temp_pass.maxsize(height=130,width=260)
                Temp_pass_label=Label(Temp_pass,text="Confirm current Password",bg="#fad6a5")
                Temp_pass_label.pack()
                Temp_pass_entry=Entry(Temp_pass,show="*")
                Temp_pass_entry.pack()
                Temp_pass_npass_label=Label(Temp_pass,text="Enter new Password",bg="#fad6a5")
                Temp_pass_npass_label.pack()
                Temp_pass_npass_entry=Entry(Temp_pass,show="*")
                Temp_pass_npass_entry.pack()
                Temp_pass_cancel=Button(Temp_pass,text="Cancel",command=Temp_pass.destroy,bg="#fecaca")
                Temp_pass_cancel.pack()
                def npass_save():
                    f=open(r"personal_user_database/"+self.username_signin+"/database/"+self.username_signin+".txt","r+")
                    a=f.readlines()
                    if a[2]==Temp_pass_entry.get():
                        def valid_new_pass(var):
                            if not(var.isalnum()):
                                messagebox.showerror('Error','Extra characters are not allowed in your New Password.')
                                return(False)
                            if len(var)<6:
                                messagebox.showerror('Error','New Password is very small, give a big one.')
                                return(False)
                            else:
                                return(True)
                        while True:
                            if valid_new_pass(Temp_pass_npass_entry.get()):
                                break
                            return
                        a[2]=Temp_pass_npass_entry.get()
                        f.seek(0)
                        f.truncate()
                        f.seek(0)
                        f.writelines(a)
                        f.close()
                        messagebox.showinfo('Success','Password Successfully Changed.')
                        Temp_pass.destroy()
                    else:
                        messagebox.showerror('Error','Old Password is incorrect.')
                Temp_pass_Save=Button(Temp_pass,text="save and Exit",command=npass_save,bg="#fecaca")
                Temp_pass_Save.pack()
                Temp_pass.mainloop()
            def temp_bio():
                set_ac.destroy()
                bi=open(r"personal_user_database/"+self.username_signin+"/bio/bio.txt","a+")
                bi=open(r"personal_user_database/"+self.username_signin+"/bio/bio.txt","r+")
                bio=bi.read()
                if bio=="":
                    bio="No bio to show! Start Editing"
                Temp_bio=Tk()
                Temp_bio.title("Current Bio")
                Temp_bio.iconbitmap(r'pictures\bio.ico')
                Temp_bio.configure(bg="#fad6a5")
                Temp_bio.geometry("350x220")
                Temp_bio.maxsize(height=220,width=350)                
                def edit_bio():
                    Temp_bio.destroy()
                    Edit_bio=Tk()
                    Edit_bio.title("Edit Bio")
                    Edit_bio.iconbitmap(r'pictures\editbio.ico')
                    Edit_bio.configure(bg="#fad6a5")
                    Edit_bio.geometry("350x460")
                    Edit_bio.maxsize(height=460,width=350)
                    edit_text=Text(Edit_bio)
                    edit_text.pack()
                    def save_bio():
                        saving_data=edit_text.get("1.0", "end-1c")
                        bi=open(r"personal_user_database/"+self.username_signin+"/bio/bio.txt","w")
                        bi.write(saving_data)
                        bi.flush()
                        messagebox.showinfo("Done","Successfully Updated")
                        Edit_bio.destroy()
                    edit_text_button1=Button(Edit_bio,text="Save and Exit",command=save_bio,bg="#fecaca")
                    edit_text_button1.pack()
                    edit_text_button2=Button(Edit_bio,text="Cancel",command=Edit_bio.destroy,bg="#fecaca")
                    edit_text_button2.pack()
                    Edit_bio.mainloop()
                mess_bio=Message(Temp_bio,text=bio,bg="#9ed2dc")
                mess_bio.pack()
                edit_bio_start=Button(Temp_bio,text="Edit",command=edit_bio,padx=10,bg="#fecaca")
                edit_bio_start.pack()
                edit_bio_start.place(x=80,y=180)
                edit_bio_cancel=Button(Temp_bio,text="Cancel",command=Temp_bio.destroy,bg="#fecaca")
                edit_bio_cancel.pack()
                edit_bio_cancel.place(x=200,y=180)
                Temp_bio.mainloop()
            set_ac.title("Settings")
            set_ac.iconbitmap(r'pictures\settings.ico')
            set_ac.configure(bg = "#fad6a5")
            set_ac.geometry("200x150")
            set_ac.maxsize(height=150,width=200)
            change_pass=Button(set_ac,text="Change Password",command=temp_pass,bg="#fecaca")
            change_pass.pack()
            change_pass.place(x=40,y=25)
            change_bio=Button(set_ac,text="Change Bio",command=temp_bio,bg="#fecaca",padx=10)
            change_bio.pack()
            change_bio.place(x=45,y=75)
            set_ac.mainloop()
        pres_time=datetime.datetime.now()
        if 12<pres_time.hour<17:
        	greet_val="Good Afternoon"
        elif 0<=pres_time.hour<5 or 17<=pres_time.hour<=24:
        	greet_val="Good Evening"
        else:
        	greet_val="Good Morning"
        greeting_username=Label(text=greet_val+", "+self.Real_Name+"_"*70,bg="#b7f2a2")
        greeting_username.pack()
        label_inf1=Label(text="Stay Chatting with your Friends",bg="#fad6a5")
        label_inf1.pack()
        label_inf1.place(x=10,y=44)
        SendMess=Button(text="Send Message",command=C1,bg="#fecaca")
        SendMess.pack()
        SendMess.place(x=190,y=40)
        label_inf2=Label(text="Recieved Messages",bg="#fad6a5")
        label_inf2.pack()
        label_inf2.place(x=10,y=80)
        SeeInbox=Button(text="See my Inbox",command=C2,padx=3,bg="#fecaca")
        SeeInbox.pack()
        SeeInbox.place(x=190,y=80)
        Credits=Button(text="Read Messages",command=C4,bg="#fecaca")
        Credits.pack()
        Credits.place(x=10,y=120)
        Feedback=Button(text="See my Friend list",command=C3,bg="#fecaca")
        Feedback.pack()
        Feedback.place(x=120,y=120)
        Settings=Button(text="Settings",command=C6,padx=4,bg="#fecaca")
        Settings.pack()
        Settings.place(x=40,y=160)
        Exit=Button(text="Log Out ",command=C5,bg="#fecaca")
        Exit.pack()
        Exit.place(x=160,y=160)
        AfterLogin.protocol("WM_DELETE_WINDOW",direct_quit2)
        AfterLogin.mainloop()
class signin(object):
    def __init__(self):
        self.username_signin()
    def username_signin(self):    
        self.window_signin = Tk()
        self.window_signin.title('Sign In')
        self.window_signin.iconbitmap(r'pictures\signin.ico')
        self.window_signin.geometry("350x220")
        self.window_signin.config(bg="#fad6a5")
        self.window_signin.maxsize(height=220,width=350)
        def confirmation():
            self.username=entry1.get()
            password = entry2.get()
            if self.username=="" or password=="":
                messagebox.showerror('Error','Blank Username or Password')
                return
            file=open("username.txt","a+")
            file=open("username.txt","r+")
            if "$"+self.username+"$" in file.read():
                file=open(r"personal_user_database/"+self.username+"/database/"+self.username+".txt","r+")
                password_verify=file.readlines()[2]
                file=open(r"personal_user_database/"+self.username+"/database/"+self.username+".txt","r+")
                user_Name=file.readlines()[0]
                if password_verify==password:
                    t="Welcome Back, "+self.username
                    messagebox.showinfo('Ready to Rock and Roll!!',t)
                    self.window_signin.destroy()
                    username_signin=self.username
                    start=afterlogin(username_signin)
                else:
                    messagebox.showerror("Password Incorrect",user_Name+"Your password is incorrect")
            else:
                messagebox.showinfo('info','Invalid Login')
        def let_close():
            self.window_signin.destroy()
            start=homepage()
        def sign_up_proceed():
            self.window_signin.destroy()
            start=signUp()
        def direct_quit1():
            messagebox.showerror("Violation","Please go through the options")
        frame = Frame(self.window_signin,bg="#fad6a5")
        f=open(r"username.txt","r")
        if len(f.readlines())==0:
            def retrive_home():
                self.window_signin.destroy()
                start=homepage()
            label_frst=Label(self.window_signin,text='You are the first user. please go by Signing Up',bg="#fad6a5")
            label_frst.pack()
            label_frst.place(x=30,y=50)
            sign_up_button=Button(self.window_signin,text="Sign Up",command=sign_up_proceed,bg="#fecaca")
            sign_up_button.pack()
            sign_up_button.place(x=100,y=100)
            sign_up_cancel=Button(text="cancel",command=retrive_home,bg="#fecaca",padx=5)
            sign_up_cancel.pack()
            sign_up_cancel.place(x=180,y=100)
        else:
            Label1 = Label(self.window_signin,text = 'Username:',bg="#fad6a5")
            Label1.pack(padx=15,pady= 5)
            entry1 = Entry(self.window_signin,bd =5)
            entry1.pack(padx=15, pady=5)
            Label2 = Label(self.window_signin,text = 'Password: ',bg="#fad6a5")
            Label2.pack(padx = 15,pady=6)
            entry2 = Entry(self.window_signin, bd=5,show="*")
            entry2.pack(padx = 15,pady=7)
            btn = Button(frame, text = 'Sign In',command=confirmation,bg="#fecaca")
            btn.pack(side = RIGHT , padx =5)
            btnn=Button(frame,text="Cancel",command=let_close,bg="#fecaca")
            btnn.pack(side=LEFT,padx=1)
            frame.pack(padx=100,pady = 19)
        self.window_signin.protocol("WM_DELETE_WINDOW",direct_quit1)
        self.window_signin.mainloop()
class profile(object):
    def __init__(self,name,username,password):
        self.name=name
        self.username=username
        self.password=password
        self.create_file()
    def redirect_home(self):
        if self.var1.get()==0:
            messagebox.showerror("Violation!","Please accept all the Conditions")
        else:
            self.B1.configure(bg = "#dbc9c3")
            messagebox.showinfo("Signed Up Successfull","Thanks for being in this Platform\nPlease go next  by Signing In")
            self.window.destroy()
            start=homepage()
    def create_file(self):
        os.mkdir(r'personal_user_database/'+self.username)
        os.mkdir(r'personal_user_database/'+self.username+"/messages")
        os.mkdir(r'personal_user_database/'+self.username+"/bio")
        file=open(r"personal_user_database/"+self.username+"/bio/bio.txt","a+")
        file.close()
        os.mkdir(r'personal_user_database/'+self.username+"/database")
        file=open(r"personal_user_database/"+self.username+"/database/"+self.username+".txt",mode="a+")
        file.write(self.name+"\n"+self.username+"\n"+self.password)
        file.flush()
        file.close()
        self.mention_in_database()
    def mention_in_database(self):    
        file=open("username.txt",mode="a+")
        file.write("$"+self.username+"$\n")
        file.flush()
        self.displayer_guru()        
    def displayer_guru(self):
        def protocolhandler():
            messagebox.showerror("Don't Quit","Please Go through the Procedure")
        self.window=Tk()
        self.window.geometry('500x450')
        self.window.maxsize(height=500,width=450)
        self.window.config(bg="#fad6a5")
        self.window.title("Account Details!")
        self.window.iconbitmap(r'pictures\accountdetails.ico')
        var="Please note your following Accounts Details\n"+"_"*120+"\n\n\n"
        Label(self.window,text=var,bg="#fad6a5").pack()
        count=0  
        file=open(r"personal_user_database/"+self.username+"/database/"+self.username+".txt",mode="r+")
        for x in file.readlines():
            if count==0:
                Label(self.window,text="\nName:\t\t"+x,bg="#C5EF94",padx=650).pack()
            if count==1:
                Label(self.window,text="\nUsername:\t"+x,bg="#F58C6B",padx=650).pack()
            if count==2:
                Label(self.window,text="\nPassword:\t"+x+"\n",bg="#76CFC9",padx=650).pack()
            count+=1    
        self.var1=IntVar()
        Checkbutton(self.window,text="\n\nI agree all the terms and conditions.\n\n",variable=self.var1,bg="#fad6a5").pack()
        self.B1=Button(text="Accept and Continue !",command=self.redirect_home,bg="#f2e9e6")
        self.B1.pack()
        self.window.protocol("WM_DELETE_WINDOW", protocolhandler)
        self.window.mainloop()
class signUp(object):
    def __init__(self):
        self.WinSignup()
    def blank(self):
        if self.entry_First.get()=="" or self.entry_Last.get()=="" or self.entry_User.get()=="" or \
           self.nPass.get()=="" or self.cPass.get()=="":
          return(True)
        else:
            return(False)
    def valid_name(self,var,var1):
        if not(var.isalpha()) or not(var.isalnum()) or var.isspace():
            messagebox.showerror('Error',"Extra characters are not allowed like 'Spaces', 'Digits', 'Symbols' in your "+var1)
        if len(var)<3:
            messagebox.showerror('Error',"Your "+var1+" is very small, give a big one.")
    def valid_pass(self,var):
        if not(var.isalnum()):
            messagebox.showerror('Error','Extra characters are not allowed.')
            return(False)
        elif len(var)<6:
            messagebox.showerror('Error','Password is very small, give a big one.')
            return(False)
        else:
            return(True)
    def cnf_pass(self,var):
        if self.nPass.get()!=var:
            messagebox.showerror('Error','Wrong Password, Please re-enter')
            return(False)
        else:
            return(True)
    def unq_user(self,Usrnm):
        f=open("username.txt",mode="a+")
        f=open("username.txt","r+")
        if "$"+Usrnm+"$" in f.read():
            messagebox.showerror('Error','This User id is already taken, Please try another combination')
            return(False)
        elif Usrnm[0].isdigit():
            messagebox.showerror('Error','Username must not start with a digit.')
            return(False)
        elif not(Usrnm.islower()):
            messagebox.showerror('Error','Username must contain only lowercase letters.')
            return(False)
        elif not(Usrnm.isalnum()):
            messagebox.showerror('Error','Extra characters are not allowed.')
            return(False)
        elif len(Usrnm)<6:
            messagebox.showerror('Error','Username is very small, give a big one.')
            return(False)
        else:
            return(True)
    def Confirm(self):
        if self.blank():
            messagebox.showerror('Error','All fields are Mandatory')
            return
        self.valid_name(self.entry_First.get(),"First Name")
        self.valid_name(self.entry_Last.get(),"Last Name")
        while True:
            if self.unq_user(self.entry_User.get()):
                break
            return
        while True:
            if self.valid_pass(self.nPass.get()):
                break
            return
        while True:
            if self.cnf_pass(self.cPass.get()):
                break
            return
        a,b,c,d=self.entry_First.get(),self.entry_Last.get(),self.entry_User.get(),self.cPass.get()
        self.WinDow.destroy()
        profile(a+" "+b,c,d)
    def close_back(self):
        self.WinDow.destroy()
        start=homepage()
    def direct_quit(self):
        messagebox.showerror("Violation","Please go through the options")
    def WinSignup(self):
        self.WinDow=Tk()
        self.WinDow.geometry("700x300")
        self.WinDow.maxsize(height=300,width=700)
        self.WinDow.config(bg="#fad6a5")
        self.WinDow.title("Hurry! Create New Account")
        self.WinDow.iconbitmap(r'pictures\signup.ico')
        frame = Frame(self.WinDow)
        First = Label(self.WinDow,text = 'Enter Your First Name',bg="#fad6a5")
        First.pack(padx=15,pady= 5)
        First.place(x=70,y=30)
        self.entry_First = Entry(self.WinDow,bd =5)
        self.entry_First.pack(padx=15, pady=5)
        self.entry_First.place(x=70,y=55)
        Last = Label(self.WinDow,text = 'Enter Your Last Name',bg="#fad6a5")
        Last.pack(padx=15,pady= 5)
        Last.place(x=500,y=30)
        self.entry_Last = Entry(self.WinDow,bd =5)
        self.entry_Last.pack(padx=15, pady=5)
        self.entry_Last.place(x=500,y=55)
        User = Label(self.WinDow,text = 'Build your unique Username',bg="#fad6a5")
        User.pack(padx=15,pady= 5)
        User.place(x=275,y=100)
        self.entry_User = Entry(self.WinDow,bd =5)
        self.entry_User.pack(padx=15, pady=5)
        self.entry_User.place(x=290,y=125)
        NPassword = Label(self.WinDow,text = 'Generate Your Password',bg="#fad6a5")
        NPassword.pack(padx = 15,pady=6)
        NPassword.place(x=70,y=150)
        self.nPass = Entry(self.WinDow, bd=5,show="*")
        self.nPass.pack(padx = 15,pady=7)
        self.nPass.place(x=70,y=175)
        CPassword = Label(self.WinDow,text = 'Confirm Your Password',bg="#fad6a5")
        CPassword.pack(padx = 15,pady=6)
        CPassword.place(x=500,y=150)
        self.cPass = Entry(self.WinDow, bd=5,show="*")
        self.cPass.pack(padx = 15,pady=7)
        self.cPass.place(x=500,y=175)
        btn = Button(text = 'Sign Up',command=self.Confirm,padx=25,bg="#fecaca")
        btn.pack()
        btn.place(x=230,y=250)
        btn1=Button(text = 'Cancel',command=self.close_back,padx=25,bg="#fecaca")
        btn1.pack()
        btn1.place(x=380,y=250)
        frame.pack()
        self.WinDow.protocol("WM_DELETE_WINDOW",self.direct_quit)
        self.WinDow.mainloop()
class virtual_win_feed(object):
    def __init__(self):
        self.Wi=Tk()
        self.Wi.title("Feedback")
        self.Wi.iconbitmap(r'pictures\feedbacks.ico')
        self.Wi.config(bg="#fad6a5")
        def feed_collector():
            data_feed=self.feed.get("1.0", "end-1c")
            messagebox.showinfo("Thanks!","Thanks for your Feeds!\nWe will response you Soon!")
            self.Wi.destroy()
            feed_file=open('feedbacks.txt',"a+")
            feed_file.write(data_feed+"\n"+"_"*100+"\n")
            feed_file.flush()
            feed_file.close()
        self.feed=Text(self.Wi,height=15,width=55)
        self.feed.pack()
        self.feed_send=Button(self.Wi,text="Send",command=feed_collector,bg="#fecaca",padx=5)
        self.feed_send.pack()
        self.Wi.mainloop()
class credits_win(object):
    def __init__(self):
        self.Cwi=Toplevel()
        self.Cwi.title("Credits")
        self.Cwi.iconbitmap(r'pictures\credits.ico')
        self.Cwi.geometry("450x400")
        self.Cwi.maxsize(width=400,height=450)
        self.Cwi.config(bg="#9ed2dc")
        cred_mess='''
_______________________________________________________________________________________________
                   This Project is an Exprimental approach towards making a Chat Room
_______________________________________________________________________________________________
                        Here, "python" language is used under complete development.
________________________________________________________________________________________________
                                                      © All Rights Reserved
________________________________________________________________________________________________
                                    Thanks to ®hkonvict team and python 3.4.
________________________________________________________________________________________________
                                                            Thank you all.
________________________________________________________________________________________________'''
        mess_cred=Message(self.Cwi,text=cred_mess,bg="#9ed2dc",padx=100,width=600)
        mess_cred.pack()
        image = PhotoImage(file=r"pictures\python_sign.gif")
        label = Label(self.Cwi,image=image)
        label.pack()
        self.Cwi.mainloop()        
class homepage(object):
    def __init__(self):
        home=Tk()
        home.title('Py Chat')
        home.iconbitmap(r'pictures\hk.ico')
        home.geometry("400x300")
        home.config(bg="#fad6a5")
        home.maxsize(height=300,width=400)
        def C1():
            home.destroy()
            start=signUp()
        def C2():
            home.destroy()
            start=signin()
        def C3():
            temp=virtual_win_feed()
        def C4():
            temp=credits_win()
        def C5():
            messagebox.showinfo("Good Luck!","Have a Great Day!")
            home.destroy()
        label01=Label(text="______________________________________\nNew to PyChat, Create an Account",bg="#fad6a5")
        label01.pack()
        SignUp=Button(text="Create an Account",command=C1,bg="#fecaca")
        SignUp.pack()
        label02=Label(text="__________________________________________\nAlready have an account, Please Sign In",bg="#fad6a5")
        label02.pack()
        LogIn=Button(text="Sign In",command=C2,bg="#fecaca")
        LogIn.pack()
        labeldash=Label(text="___________________________________________",bg="#fad6a5")
        labeldash.pack()
        Feedback=Button(text="Leave Feedback",command=C3,bg="#fecaca")
        Feedback.pack()
        Feedback.place(x=90,y=150)
        Credits=Button(text="Credits",command=C4,bg="#fecaca")
        Credits.pack()
        Credits.place(x=240,y=150)
        Exit=Button(text="Exit",command=C5,padx=5,bg="#fecaca")
        Exit.pack()
        Exit.place(x=180,y=210)
        home.mainloop()
start=homepage()
