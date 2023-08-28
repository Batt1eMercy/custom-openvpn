from tkinter import *
import subprocess, keyring, os, threading

OPENVPNPATH = 'C:\\Program Files\\OpenVPN\\bin\\openvpn.exe'
class OVpn():
        def save_cred(self):
                self.userName = userNameUi.get()
                self.userPass = userPassUi.get()
                self.configPath = configPathUi.get()

                if cred.configPath != "":
                        keyring.set_password("ovpn_config","config",cred.configPath)
                keyring.set_password("ovpn_cred", cred.userName, cred.userPass)

                configPathLabel["text"] = f"openvpn config path: \n Now: {keyring.get_password('ovpn_config','config')}"
                messageUi["text"] = f"settings saved"
        def connect(self):
                def rem_cred_file():
                        os.remove("cred.txt")
                try:
                        cwd = os.getcwd().replace("\\","\\\\")

                        configGet = keyring.get_password("ovpn_config","config")
                        configPath = configGet.replace("\\","\\\\")
                        print(configPath)

                        credGet = keyring.get_credential("ovpn_cred","")

                        with open(f"{cwd}\\cred.txt", "w") as credFile:
                                credFile.write(f"{credGet.username}\n{credGet.password}")
                        th = threading.Timer(0.1, rem_cred_file)
                        th.start()
                        openvpnCmd = subprocess.run(f"{OPENVPNPATH} \
                                                    --config \"{configPath}\" \
                                                    --auth-user-pass \"{cwd}\\cred.txt\"", stdin=subprocess.PIPE)
 
                except Exception as err:
                        os.remove(f"{cwd}\\cred.txt")
                        print(err)
                
main = Tk()
main.geometry('400x250')
cred = OVpn()
main.title("custom-openvpn")

savePassBtn = Button(main, width=20,
             height=2, text="Save",
             bg="white", fg="black",
             command=cred.save_cred)

connectBtn = Button(main, width=20,
             height=2, text="Connect",
             bg="white", fg="black",
             command=cred.connect)

                     
configPathUi = Entry(fg="black", bg="white", width=50) 
configPathLabel = Label(text=f"openvpn config path: \n Now: {keyring.get_password('ovpn_config','config')}")

userNameUi = Entry(fg="black", bg="white", width=50) 
userNameLable = Label(text="Username: ")

userPassUi = Entry(fg="black", bg="white", width=50, show='*') 
userPassLable = Label(text="Password: ")

messageUi = Label()

configPathLabel.pack()
configPathUi.pack()
userNameLable.pack()
userNameUi.pack()
userPassLable.pack()
userPassUi.pack()
savePassBtn.pack()
connectBtn.pack()
messageUi.pack()

main.mainloop()
