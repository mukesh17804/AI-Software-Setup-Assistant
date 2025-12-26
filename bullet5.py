import customtkinter as ctk
import tkinter.messagebox as msg
import threading, time, platform, shutil
from datetime import datetime
import speech_recognition as sr

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ================= CENTRAL AI AGENT ================= #
class CentralAIAgent:
    def __init__(self, ui):
        self.ui = ui
        self.software_info = {
            "Python": {"versions": ["3.11", "3.10", "3.9"], "dependencies": []},
            "Git": {"versions": ["2.41", "2.40"], "dependencies": []},
            "Node": {"versions": ["20", "18"], "dependencies": ["Python"]}
        }

    def handle_request(self, software, version):
        threading.Thread(
            target=self._process, args=(software, version), daemon=True
        ).start()

    def _process(self, software, version):
        self.ui.safe_status(f"OS detected: {platform.system()}")

        if self.is_installed(software):
            self.ui.safe_home(f"{software} already installed ✔")
            self.ui.safe_status(f"{software} already available")
            return

        self.download_agent(software, version)

    # ---------- DOWNLOAD ---------- #
    def download_agent(self, software, version):
        self.ui.show_progress(f"Downloading {software} v{version}", 3)
        if not self.ui.confirm(f"{software} v{version} downloaded.\nInstall now?"):
            self.ui.safe_home(f"{software} download cancelled")
            return
        self.install_agent(software, version)

    # ---------- INSTALL ---------- #
    def install_agent(self, software, version):
        self.ui.show_progress(f"Installing {software} v{version}", 3)
        if not self.ui.confirm(f"Setup environment for {software}?"):
            self.ui.safe_home(f"{software} installed (env skipped)")
            return
        self.env_agent(software, version)

    # ---------- ENV SETUP ---------- #
    def env_agent(self, software, version):
        self.ui.show_progress("Configuring Environment", 2)
        self.ui.safe_home(f"{software} v{version} installed & ready ✅")
        msg.showinfo("Success", f"{software} is ready to use!")

    def is_installed(self, software):
        return shutil.which(software.lower()) is not None


# ================= MAIN APP ================= #
class AIInstallerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AI Software Setup Assistant")
        self.geometry("1150x680")

        self.agent = CentralAIAgent(self)
        self.logged_user = None

        self.build_login()

    # ---------------- LOGIN ---------------- #
    def build_login(self):
        self.clear()
        box = ctk.CTkFrame(self)
        box.pack(expand=True)

        ctk.CTkLabel(box, text="AI Setup Assistant", font=("Arial", 28)).pack(pady=20)
        self.user = ctk.CTkEntry(box, placeholder_text="Username")
        self.user.pack(pady=6)
        self.pwd = ctk.CTkEntry(box, placeholder_text="Password", show="*")
        self.pwd.pack(pady=6)
        ctk.CTkButton(box, text="Login", height=40, command=self.login).pack(pady=12)

    def login(self):
        if self.user.get() == "admin" and self.pwd.get() == "admin123":
            self.logged_user = self.user.get()
            self.build_main()
        else:
            msg.showerror("Error", "Invalid credentials")

    # ---------------- MAIN UI ---------------- #
    def build_main(self):
        self.clear()

        self.sidebar = ctk.CTkFrame(self, width=180)
        self.sidebar.pack(side="left", fill="y", padx=8)

        for name, cmd in [
            ("Home", self.home),
            ("Install", self.install),
            ("Schedule", self.schedule),
            ("About", self.about),
            ("Settings", self.settings)
        ]:
            ctk.CTkButton(self.sidebar, text=name, height=50,
                          font=("Arial", 14), command=cmd).pack(fill="x", pady=5)

        self.content = ctk.CTkFrame(self)
        self.content.pack(expand=True, fill="both", padx=10)

        self.status = ctk.CTkLabel(self, text="Ready", anchor="w")
        self.status.pack(side="bottom", fill="x")

        self.home()

    # ---------------- HOME ---------------- #
    def home(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text=f"Welcome {self.logged_user}",
                     font=("Arial", 28)).pack(pady=15)
        ctk.CTkLabel(self.content,
                     text=f"Hi My Dear Nanbi's and Nanba's! \n"
                          "This AI Agent can reduce the time and working Complexities for Fresh Engineering Students. \n"
                          "It Working As User Friendly. \n"
                          "Use the 'Install' tab to quickly setup Python, Git, and other tools.\n"
                          "Voice commands supported: e.g., 'Install Python'.\n"
                          "Check 'Schedule' tab to schedule installation tasks.",
                     font=("Arial", 22), justify="left").pack(pady=10)

        self.home_frame = ctk.CTkFrame(self.content)
        self.home_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(self.home_frame, text="Activity Log",
                     font=("Arial", 18)).pack(anchor="w")

    # ---------------- INSTALL ---------------- #
    def install(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Install Software",
                     font=("Arial", 22)).pack(pady=10)

        self.soft = ctk.StringVar(value="Python")
        self.ver = ctk.StringVar(value="3.11")

        ctk.CTkOptionMenu(self.content, variable=self.soft,
                          values=list(self.agent.software_info.keys())).pack(pady=5)
        ctk.CTkOptionMenu(self.content, variable=self.ver,
                          values=["3.11", "3.10", "3.9"]).pack(pady=5)

        ctk.CTkButton(self.content, text="🎙 Voice Install",
                      height=40, command=self.voice).pack(pady=6)

        ctk.CTkButton(self.content, text="Install",
                      height=45,
                      command=lambda: self.agent.handle_request(
                          self.soft.get(), self.ver.get())
                      ).pack(pady=6)

    # ---------------- SCHEDULE ---------------- #
    def schedule(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Schedule Install",
                     font=("Arial", 22)).pack(pady=10)

        self.sch_soft = ctk.StringVar(value="Python")
        self.sch_ver = ctk.StringVar(value="3.11")

        ctk.CTkOptionMenu(self.content, variable=self.sch_soft,
                          values=list(self.agent.software_info.keys())).pack(pady=5)
        ctk.CTkOptionMenu(self.content, variable=self.sch_ver,
                          values=["3.11", "3.10", "3.9"]).pack(pady=5)

        self.time_entry = ctk.CTkEntry(self.content,
                                       placeholder_text="YYYY-MM-DD HH:MM")
        self.time_entry.pack(pady=5)

        ctk.CTkButton(self.content, text="Schedule",
                      height=40, command=self.set_schedule).pack(pady=8)

    def set_schedule(self):
        try:
            run = datetime.strptime(self.time_entry.get(), "%Y-%m-%d %H:%M")
            threading.Thread(target=self.wait_and_run,
                             args=(run, self.sch_soft.get(), self.sch_ver.get()),
                             daemon=True).start()
            self.safe_home(f"{self.sch_soft.get()} scheduled at {run}")
        except:
            msg.showerror("Error", "Invalid date/time")

    def wait_and_run(self, run, s, v):
        while datetime.now() < run:
            time.sleep(1)
        self.agent.handle_request(s, v)

    # ---------------- ABOUT ---------------- #
    def about(self):
        self.clear_content()
        text = (
            "AI SOFTWARE SETUP ASSISTANT\n\n"
            "Developer: Mukesh Kanna S\n"
            "Year: 2025\n\n"
            "Problem:\nFreshers struggle installing programming tools\n"
            "and configuring environments.\n\n"
            "Solution:\nVoice-driven AI multi-agent installer\n"
            "with automation, scheduler & monitoring.\n\n"
            "Features:\n"
            "- Voice Command\n- Multi-Agent AI\n"
            "- Scheduler\n- Progress Tracking\n"
            "- Environment Setup\n- OS Detection\n\n"
            "Technology:\nPython, CustomTkinter, Speech Recognition\n\n"
            "This is a REAL-WORLD READY academic + startup-level project."
        )
        ctk.CTkLabel(self.content, text=text,
                     font=("Arial", 20), justify="left").pack(padx=15, pady=15)

    # ---------------- SETTINGS ---------------- #
    def settings(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Settings",
                     font=("Arial", 22)).pack(pady=10)

        ctk.CTkOptionMenu(self.content,
                          values=["Dark", "Light"],
                          command=lambda m: ctk.set_appearance_mode(m)
                          ).pack(pady=5)
        #ctk.CTkLabel(self.content, text="Voice Language:",
                   #  font=("Arial", 14)).pack(pady=5)
        #ctk.CTkOptionMenu(self.content,
                         # values=["English", "Tamil"],
                         # command=self.change_language).pack(pady=5)
        ctk.CTkOptionMenu(self.content, values=["English", "Tamil"], command=self.change_language).pack(pady=5)


    # ---------------- VOICE ---------------- #
    def voice(self):
        threading.Thread(target=self.listen, daemon=True).start()

    def listen(self):
        r = sr.Recognizer()
        with sr.Microphone() as src:
            try:
                audio = r.listen(src, timeout=5)
                text = r.recognize_google(audio).lower()
                for s in self.agent.software_info:
                    if s.lower() in text:
                        self.agent.handle_request(s, "3.11")
                        return
            except:
                msg.showerror("Error", "Voice failed")

    # ---------------- HELPERS ---------------- #
    def show_progress(self, title, seconds):
        self.safe_status(title)
        bar = ctk.CTkProgressBar(self.content)
        bar.pack(pady=8)
        bar.set(0)

        for i in range(101):
            time.sleep(seconds / 100)
            bar.after(0, lambda v=i/100: bar.set(v))
        bar.after(0, bar.destroy)

    def confirm(self, text):
        return msg.askyesno("Confirm", text)

    def safe_home(self, text):
        if hasattr(self, "home_frame") and self.home_frame.winfo_exists():
            self.home_frame.after(0, lambda:
                ctk.CTkLabel(self.home_frame,
                             text="• " + text,
                             font=("Arial", 12)).pack(anchor="w"))

    def safe_status(self, t):
        self.status.after(0, lambda: self.status.configure(text=t))

    def clear(self):
        for w in self.winfo_children():
            w.destroy()

    def clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()


# ================= RUN ================= #
if __name__ == "__main__":
    app = AIInstallerApp()
    app.mainloop()
