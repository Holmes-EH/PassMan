import tkinter
from tkinter import ttk
from tkinter import messagebox
from database import Database
import random
import string
from security import user_pwd_context
import rncryptor
import pyperclip

database = Database("../passMan.db")


# App Gui interface configuration :
class PassMan(ttk.Frame):

    def __init__(self, parent):
        super(PassMan, self).__init__(parent)

        self.loggedIn = False

        # ttk Styling

        self.style = ttk.Style()
        self.style.theme_use("alt")
        self.style.configure("TButton", padding=6, relief="flat")
        self.style.configure("TButton", foreground="black", font="helvetica 16")
        self.style.configure("TButton", background="white")
        self.style.configure("mystyle.Treeview.Heading", relief="flat", font=("helvetica", 12))
        self.style.layout("mystyle.Treeview", [("mystyle.Treeview.treearea", {"sticky": "nswe"})])

        # ttk Main Frame

        self.content = ttk.Frame(self, width=500, height=300)

        # Menu buttons interface :

        self.menuButtons = ttk.Frame(self.content)

        self.mainLabel = ttk.Label(self.content, text="PASS MAN",
                                   font="helvetica 40 bold", justify="center")
        self.subLabel = ttk.Label(
            self.content, text="A convenient and secure credential manager", font="helvetica 10 italic", justify="center")
        self.menuButtons["padding"] = 20

        self.generatePwdBtn = ttk.Button(self.menuButtons, text="Generate secure password",
                                         style="TButton", command=self.newPwdDisplay)

        self.viewCredBtn = ttk.Button(self.menuButtons, text="View saved passwords",
                                      style="TButton", command=self.showAllCredentials)

        self.menuButtons.columnconfigure((0, 1), weight=1, pad=10)

        # Stored credential display :

        self.label = ttk.Label(self.content, text="STORED CREDENTIALS",
                               padding=20, font="helvetica 16 bold")

        self.tableFrame = ttk.Frame(self.content)
        self.tableFrame.columnconfigure((0), weight=1)
        self.tableFrame.rowconfigure((0), weight=1)

        self.tree = ttk.Treeview(self.tableFrame, columns=(
            "Login", "Password", "Date"), style="mystyle.Treeview", selectmode='browse')
        self.tree.column("#0", stretch=False)
        self.tree.column("Login", stretch=False)
        self.tree.column("Date", stretch=False)
        self.tree.heading("Date", text="Date Created")
        self.tree.heading("#0", text="Name")
        self.tree.heading("Login", text="Login")
        self.tree.heading("Password", text="Password")

        self.tree.tag_configure("odd", background="#EDEDED")
        self.tree.tag_configure("even", background="#D1D1D1")

        self.tree.bind("<Button-1>", self.showPassword)
        self.tree.bind("<Leave>", self.hidePasswords)
        self.tree.bind("<Double-1>", self.onTreeDoubleClick)

        self.vsb = ttk.Scrollbar(self.tableFrame, orient="vertical",
                                 command=self.tree.yview)

        self.tree.pack(side="left", expand=True, fill="both")
        self.vsb.pack(side="right", fill="y")

        self.tree.configure(yscrollcommand=self.vsb.set)

        self.quitBtn = ttk.Button(self.content, text="Quit",
                                  style="TButton", command=root.destroy)

        self.mainLabel.pack(pady=(20, 0))
        self.subLabel.pack(pady=(0, 20))
        self.content.pack(expand=True, fill="both")
        self.content.pack_propagate(0)

        # first Login Check
        # self.splash = tkinter.Toplevel(self.content)
        # self.splash.configure(background="#D9D9D9")
        # self.splash.columnconfigure((0, 1), weight=1, pad=20)

        if self.loggedIn == False:
            self.loginNotice = ttk.Frame(self.content)
            self.loginNowLabel = ttk.Label(self.loginNotice, text="You need to log in !",
                                           padding=20, font="helvetica 16 bold")
            self.logInNowButton = ttk.Button(self.loginNotice, text="Login",
                                             style="TButton", command=self.logInNow)
            self.loginNowLabel.pack(pady=(20, 0))
            self.logInNowButton.pack(pady=(0, 20))

            self.loginNotice.pack()

            self.content.bind("<Return>", lambda event: self.logInNow())

    # Menu buttons callback functions :
    def logInNow(self):
        pass
        if database.readMasterPwd() == None:
            # create master password

            self.create = tkinter.Toplevel(self)

            # Hide window before centering
            self.create.withdraw()

            self.create.configure(background="#D9D9D9")

            self.createLabel = ttk.Label(
                self.create, text="Create a Master Password :", padding=20, font="helvetica 16 bold")

            self.createMasterPassword = tkinter.StringVar()
            self.createMasterPwdEntry = ttk.Entry(
                self.create, textvariable=self.createMasterPassword, show="*", justify="center")

            self.createMasterPwdButton = ttk.Button(self.create, text="Save Master Password",
                                                    style="TButton", command=self.createMasterPwd)
            self.createLabel.pack(padx=20, pady=20)
            self.createMasterPwdEntry.pack(padx=20, pady=20)
            self.createMasterPwdButton.pack(padx=20, pady=20)

            self.createMasterPwdEntry.focus()

            self.createMasterPwdEntry.bind("<Return>", lambda event: self.loginCheck())

            # perform window centering
            self.create.update_idletasks()  # Update "requested size" from geometry manager

            x = (self.create.winfo_screenwidth() - self.create.winfo_reqwidth()) / 2
            y = (self.create.winfo_screenheight() - self.create.winfo_reqheight()) / 2
            self.create.geometry("+%d+%d" % (x, y))

            # window centered display it
            self.create.deiconify()

            self.create.lift()
        else:
            # login Frame :

            self.login = tkinter.Toplevel(self)

            # Hide window before centering
            self.login.withdraw()

            self.login.configure(background="#D9D9D9")

            self.loginLabel = ttk.Label(
                self.login, text="Enter master password :", font="helvetica 16 bold")
            self.masterPassword = tkinter.StringVar()
            self.masterPwdEntry = ttk.Entry(
                self.login, textvariable=self.masterPassword, justify="center", show="*")
            self.loginButton = ttk.Button(
                self.login, text="Login", style="TButton", command=self.loginCheck)

            self.loginLabel.pack(padx=20, pady=20)
            self.masterPwdEntry.pack(padx=20, pady=20)
            self.loginButton.pack(padx=20, pady=20)

            self.masterPwdEntry.focus()

            self.masterPwdEntry.bind("<Return>", lambda event: self.loginCheck())

            # perform window centering
            self.login.update_idletasks()  # Update "requested size" from geometry manager

            x = (self.login.winfo_screenwidth() - self.login.winfo_reqwidth()) / 2
            y = (self.login.winfo_screenheight() - self.login.winfo_reqheight()) / 2
            self.login.geometry("+%d+%d" % (x, y))

            # window centered display it
            self.login.deiconify()

            self.login.lift()

    def hidePasswords(self, event):
        self.tree.delete(*self.tree.get_children())
        self.showAllCredentials()
        pass

    def showPassword(self, event):
        item = self.tree.identify("item", event.x, event.y)
        id = self.tree.index(item)+1
        showColNum = int(self.tree.identify_column(event.x)[1:])

        def decryptPwd(encryptedPwd):
            try:
                masterPwd = self.masterPassword.get()
            except AttributeError:
                masterPwd = self.createMasterPassword.get()
            cryptor = rncryptor.RNCryptor()
            decryptedPwd = cryptor.decrypt(encryptedPwd, masterPwd)
            return decryptedPwd

        if showColNum == 2:
            pwd = database.readCred(id=id)[0][4]
            pwd = decryptPwd(pwd)
            self.tree.set(item, "Password", pwd)

        else:
            pass

    def onTreeDoubleClick(self, event):
        item = self.tree.identify("item", event.x, event.y)
        id = self.tree.index(item)+1
        colNum = int(self.tree.identify_column(event.x)[1:])-1
        valSelected = self.tree.item(item, "values")[colNum]

        def decryptPwd(encryptedPwd):
            try:
                masterPwd = self.masterPassword.get()
            except AttributeError:
                masterPwd = self.createMasterPassword.get()
            cryptor = rncryptor.RNCryptor()
            decryptedPwd = cryptor.decrypt(encryptedPwd, masterPwd)
            return decryptedPwd

        if colNum == 1:
            pwd = database.readCred(id=id)[0][4]
            pwd = decryptPwd(pwd)
            pyperclip.copy(pwd)
        else:
            pyperclip.copy(valSelected)

        messagebox.showinfo(message="Copied to clipboard !")

    def showAllCredentials(self):
        self.tree.delete(*self.tree.get_children())
        creds = database.readCred()

        for entry in creds:
            if entry[0] % 2 == 0:
                self.tree.insert("", "end", text=entry[2], values=(
                    entry[3], "**********", entry[1]), tags=("odd",))
            else:
                self.tree.insert("", "end", text=entry[2], values=(
                    entry[3], "**********", entry[1]), tags=("even",))

        # Hide window before centering
        root.withdraw()

        self.label.pack()
        self.tableFrame.pack(expand=True, fill="both")

        # perform window centering
        root.update_idletasks()  # Update "requested size" from geometry manager

        x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
        y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
        root.geometry("+%d+%d" % (x, y))

        # window centered display it
        root.deiconify()

    def newPwd(self, length=8):
        pwdCharSet = string.ascii_letters + string.digits + string.punctuation
        pwd = "".join(random.choice(pwdCharSet) for i in range(int(float(length))))

        return pwd

    def newPwdDisplay(self):
        newPwd = self.newPwd()

        # Generate new password Frame

        self.generateNew = tkinter.Toplevel(self)

        # Hide window before centering
        self.generateNew.withdraw()

        self.generateNew.configure(background="#D9D9D9")
        self.generateNew.columnconfigure((0, 1), weight=1, pad=20)

        self.generateNewLabel = ttk.Label(
            self.generateNew, text="New password :", font="helvetica 16 bold")
        self.generateNewPwdEntry = ttk.Entry(self.generateNew, justify="center")
        self.generateNewPwdEntry.insert(0, newPwd)
        self.generateNewPwdEntry.config(state="readonly", width=8)

        self.pwdLengthLabel = ttk.Label(self.generateNew, text="Password Length :")
        self.pwdLengthScale = ttk.Scale(
            self.generateNew, orient="horizontal", length=200, from_=8.0, to=50.0, command=self.generateNewPwdAgain)
        self.pwdLengthScaleLabels = ttk.Frame(self.generateNew)
        self.pwdLenghtScaleMinLabel = ttk.Label(
            self.pwdLengthScaleLabels, text="8", width=10, anchor="w")
        self.pwdLenghtScaleMaxLabel = ttk.Label(
            self.pwdLengthScaleLabels, text="50", width=10, anchor="e")
        self.pwdLenghtScaleMinLabel.grid(row=0, column=0)
        self.pwdLenghtScaleMaxLabel.grid(row=0, column=1)

        self.generateAgainLabel = ttk.Label(
            self.generateNew, text="Not satisfied ?", font="helvetica 16")
        self.generateAgainButton = ttk.Button(self.generateNew, text="Generate Again",
                                              style="TButton", command=self.generateNewPwdAgain)
        self.generateAgainEntry = ttk.Entry(self.generateNew, justify="center")

        self.savePwdLabel = ttk.Label(
            self.generateNew, text="Happy ?", font="helvetica 16")
        self.savePwdButton = ttk.Button(self.generateNew, text="Save",
                                        style="TButton", command=self.savePwd)

        self.generateNewLabel.grid(row=0, column=0, pady=(30, 0), columnspan=2)
        self.generateNewPwdEntry.grid(
            row=1, column=0, pady=(30, 10), ipady=10, columnspan=2)
        self.pwdLengthLabel.grid(row=2, column=0, pady=(10, 0))
        self.pwdLengthScale.grid(row=2, column=1, pady=(10, 0))
        self.pwdLengthScaleLabels.grid(row=3, column=1)
        self.generateAgainLabel.grid(row=4, column=0, pady=(30, 30))
        self.generateAgainButton.grid(row=4, column=1, pady=(30, 30))
        self.savePwdLabel.grid(row=5, column=0, pady=(0, 30))
        self.savePwdButton.grid(row=5, column=1, pady=(0, 30))

        # perform window centering
        self.generateNew.update_idletasks()  # Update "requested size" from geometry manager

        x = (self.generateNew.winfo_screenwidth() - self.generateNew.winfo_reqwidth()) / 2
        y = (self.generateNew.winfo_screenheight() - self.generateNew.winfo_reqheight()) / 2
        self.generateNew.geometry("+%d+%d" % (x, y))

        # window centered display it
        self.generateNew.deiconify()

    def generateNewPwdAgain(self, length=8):
        length = self.pwdLengthScale.get()
        newPwd = self.newPwd(int(float(length)))
        self.generateNewPwdEntry.config(state="normal")
        self.generateNewPwdEntry.delete(0, 'end')
        self.generateNewPwdEntry.insert(0, newPwd)
        self.generateNewPwdEntry.config(state="readonly", width=int(float(length)))

    def createMasterPwd(self):
        policy_config_path = "../config/config.ini"
        user_pwd_context.load_path(policy_config_path)

        if len(self.createMasterPwdEntry.get()) < 8:
            messagebox.showinfo(
                message="You must enter a password ! \n At least 8 characters long...",
                icon="warning",
                title="Invalid password")
        elif len(self.createMasterPwdEntry.get()) >= 8:
            hash = user_pwd_context.hash(self.createMasterPwdEntry.get())

            database.insertMasterPwd(hash)
            self.create.destroy()
            self.content.pack(expand=True, fill="both")

    def loginCheck(self, validating=False, enteredMasterPwdEntry=None):

        policy_config_path = "../config/config.ini"
        user_pwd_context.load_path(policy_config_path)

        hash = database.readMasterPwd()[0]
        # Depending on password validation situation (loging in or validation prior to db insertion), we may need to set the entry widget
        if enteredMasterPwdEntry == None:
            enteredMasterPwdEntry = self.masterPwdEntry

        enteredMasterPwd = enteredMasterPwdEntry.get()

        if len(enteredMasterPwd) < 8:
            messagebox.showinfo(
                message="You must enter your password ! \n It\"s at least 8 characters long...",
                icon="warning",
                title="Invalid password")
            enteredMasterPwdEntry.delete(0, "end")

        else:
            ok, new_hash = user_pwd_context.verify_and_update(enteredMasterPwd, hash)
            if not ok:
                # password did not match. do mean things
                messagebox.showinfo(
                    message="Wrong Password !",
                    icon="warning",
                    title="Wrong password")
                enteredMasterPwdEntry.delete(0, "end")
                pass

            else:
                # password matched

                if new_hash:
                    # old hash was deprecated by policy

                    # replace hash w/ new_hash for user account
                    database.updateMasterPwd(new_hash)

                    pass

                # do successful actions
                if validating == False:
                    self.login.destroy()
                    self.loginNotice.destroy()

                    self.loggedIn = True

                    self.content.pack_propagate(1)

                    self.menuButtons.pack(expand=True, fill="both")
                    self.viewCredBtn.grid(row=0, column=1)
                    self.generatePwdBtn.grid(row=0, column=0)
                    self.quitBtn.pack(pady=30)

                else:
                    # if not logging in, we are validating master password for inserting credential to db
                    return True

    def savePwd(self):
        newPwd = self.generateNewPwdEntry.get()

        self.generateNew.destroy()

        # Save credential Frame

        self.saveNew = tkinter.Toplevel(self)

        # Hide window before centering
        self.saveNew.withdraw()

        self.saveNew.configure(background="#D9D9D9")
        self.saveNew.columnconfigure((0, 1), weight=1, pad=20)
        self.saveNewWindowLabel = ttk.Label(
            self.saveNew, text="Save credentials", font="helvetica 16 bold")

        self.saveNewTitleLabel = ttk.Label(self.saveNew, text="Credential Title : ")
        self.saveNewTitle = tkinter.StringVar()
        self.saveNewTitleEntry = ttk.Entry(
            self.saveNew, textvariable=self.saveNewTitle, justify="center")

        self.saveNewLoginLabel = ttk.Label(self.saveNew, text="Login used (if any): ")
        self.saveNewLogin = tkinter.StringVar()
        self.saveNewLoginEntry = ttk.Entry(
            self.saveNew, textvariable=self.saveNewLogin, justify="center")

        self.saveNewPwdLabel = ttk.Label(self.saveNew, text="Password : ")
        self.saveNewPwdEntry = ttk.Entry(
            self.saveNew, justify="center")
        self.saveNewPwdEntry.insert(0, newPwd)
        self.saveNewPwdEntry.config(state="readonly")

        self.saveNewCredentialButton = ttk.Button(
            self.saveNew, text="Encrypt and Save", style="TButton", command=self.saveNewCredential)

        self.saveNewWindowLabel.grid(row=0, columnspan=2, pady=20)
        self.saveNewTitleLabel.grid(row=1, column=0, pady=20)
        self.saveNewTitleEntry.grid(row=1, column=1, pady=20)
        self.saveNewLoginLabel.grid(row=2, column=0, pady=20)
        self.saveNewLoginEntry.grid(row=2, column=1, pady=20)
        self.saveNewPwdLabel.grid(row=3, column=0, pady=20)
        self.saveNewPwdEntry.grid(row=3, column=1, pady=20)
        self.saveNewCredentialButton.grid(row=4, columnspan=2, pady=20)

        self.saveNewTitleEntry.focus()

        # perform window centering
        self.saveNew.update_idletasks()  # Update "requested size" from geometry manager

        x = (self.saveNew.winfo_screenwidth() - self.saveNew.winfo_reqwidth()) / 2
        y = (self.saveNew.winfo_screenheight() - self.saveNew.winfo_reqheight()) / 2
        self.saveNew.geometry("+%d+%d" % (x, y))

        # window centered display it
        self.saveNew.deiconify()

    def saveNewCredential(self):

        # Validate reentered master password

        def encryptAndSave(*args):
            newCredTitle = self.saveNewTitleEntry.get()
            newCredLogin = self.saveNewLoginEntry.get()
            newCredPwd = self.saveNewPwdEntry.get()
            masterPwdEntry = self.masterReenterEntry
            masterPwd = self.masterReenterEntry.get()

            if self.loginCheck(True, masterPwdEntry) == True:
                cryptor = rncryptor.RNCryptor()
                encypted_pwd = cryptor.encrypt(newCredPwd, masterPwd)
                database.insertCred(newCredTitle, newCredLogin, encypted_pwd)

                self.saveNew.destroy()

                self.showAllCredentials()

            else:
                self.masterReenterEntry.delete(0, "end")
                pass

        self.masterPwdReenter = tkinter.Toplevel(self.saveNew)

        # Hide window before centering
        self.masterPwdReenter.withdraw()

        self.masterPwdReenter.configure(background="#D9D9D9")

        self.masterReenterLabel = ttk.Label(
            self.masterPwdReenter, text="Please (Re)Enter your Master Password :")
        masterPwd = tkinter.StringVar()
        self.masterReenterEntry = ttk.Entry(
            self.masterPwdReenter, textvariable=masterPwd, justify="center", show="*")
        self.masterReenterValidate = ttk.Button(
            self.masterPwdReenter, text="OK", style="TButton", command=encryptAndSave)

        self.masterReenterLabel.pack(padx=20, pady=20)
        self.masterReenterEntry.pack(padx=20, pady=20)
        self.masterReenterValidate.pack(padx=20, pady=20)

        self.masterReenterEntry.focus()

        self.masterReenterEntry.bind("<Return>", encryptAndSave)

        # perform window centering
        self.masterPwdReenter.update_idletasks()  # Update "requested size" from geometry manager

        x = (self.masterPwdReenter.winfo_screenwidth() - self.masterPwdReenter.winfo_reqwidth()) / 2
        y = (self.masterPwdReenter.winfo_screenheight() -
             self.masterPwdReenter.winfo_reqheight()) / 2
        self.masterPwdReenter.geometry("+%d+%d" % (x, y))

        # window centered display it
        self.masterPwdReenter.deiconify()


# App Gui instanciation :
# def centerWindow(win):
#    win.eval('tk::PlaceWindow %s center' % win.winfo_pathname(win.winfo_id()))


if __name__ == "__main__":
    root = tkinter.Tk()
    # centerWindow(root)
    root.wm_title("Password Manager")

    root.withdraw()

    main = PassMan(root)
    main.pack(fill="both", expand=True)

    root.update_idletasks()  # Update "requested size" from geometry manager

    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
    y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
    root.geometry("+%d+%d" % (x, y))

    # This seems to draw the window frame immediately, so only call deiconify()
    # after setting correct window position
    root.deiconify()

    root.mainloop()
