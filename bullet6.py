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

    def handle_request(self, software):
        threading.Thread(
            target=self._process,
            args=(software,),
            daemon=True
        ).start()

    def _process(self, software):
        os_name = platform.system()
        self.ui.safe_status(f"OS detected: {os_name}")

        if self.is_installed(software):
            self.ui.safe_home_log(f"{software} already installed ✔")
            msg.showinfo("Info", f"{software} already installed")
            return

        self.ui.safe_status(f"Downloading {software}...")
        time.sleep(2)

        self.ui.safe_status(f"Installing {software}...")
        time.sleep(2)

        self.ui.safe_status(f"{software} ready ✅")
        self.ui.safe_home_log(f"{software} installed successfully")
        msg.showinfo("Success", f"{software} installed & configured!")

    def is_installed(self, software):
        if software.lower() == "python":
            return shutil.which("python") is not None
        if software.lower() == "git":
            return shutil.which("git") is not None
        return False


# ================= MAIN APP ================= #
class AIInstallerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AI Software Setup Assistant")
        self.geometry("1100x650")

        self.username = ""
        self.agent = CentralAIAgent(self)

        self.build_login()

    # ---------------- LOGIN ---------------- #
    def build_login(self):
        self.clear()
        frame = ctk.CTkFrame(self)
        frame.pack(expand=True)

        ctk.CTkLabel(
            frame, text="AI Setup Assistant",
            font=("Arial", 30, "bold")
        ).pack(pady=20)

        self.user_entry = ctk.CTkEntry(
            frame, placeholder_text="Username", width=260
        )
        self.user_entry.pack(pady=8)

        self.pass_entry = ctk.CTkEntry(
            frame, placeholder_text="Password",
            show="*", width=260
        )
        self.pass_entry.pack(pady=8)

        ctk.CTkButton(
            frame, text="Login",
            height=45, width=180,
            font=("Arial", 16),
            command=self.login
        ).pack(pady=15)

    def login(self):
        if self.user_entry.get() and self.pass_entry.get():
            self.username = self.user_entry.get()
            self.build_main()
        else:
            msg.showerror("Error", "Enter username & password")

    # ---------------- MAIN UI ---------------- #
    def build_main(self):
        self.clear()

        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.pack(side="left", fill="y")

        for name, cmd in [
            ("🏠 Home", self.home),
            ("⬇ Install", self.install),
            ("⏰ Schedule", self.schedule),
            ("ℹ About", self.about),
            ("⚙ Settings", self.settings)
        ]:
            ctk.CTkButton(
                self.sidebar, text=name,
                height=45, font=("Arial", 18),
                command=cmd
            ).pack(fill="x", pady=6, padx=10)

        self.content = ctk.CTkFrame(self)
        self.content.pack(expand=True, fill="both", padx=10, pady=10)

        self.status = ctk.CTkLabel(
            self, text="Ready", anchor="w"
        )
        self.status.pack(side="bottom", fill="x")

        self.home()

    # ---------------- HOME ---------------- #
    def home(self):
        self.clear_content()

        ctk.CTkLabel(
            self.content,
            text=f"Welcome {self.username} 👋",
            font=("Arial", 30, "bold")
        ).pack(pady=10)

        ctk.CTkLabel(
            self.content,
            text=(
                f"Hi My Dear Nanbi's and Nanba's! \n"
                          "This AI Agent can reduce the time and working Complexities for Fresh Engineering Students. \n"
                          "It Working As User Friendly. \n"
                          "Use the 'Install' tab to quickly setup Python, Git, and other tools.\n"
                          "Voice commands supported: e.g., 'Install Python'.\n"
                          "Check 'Schedule' tab to schedule installation tasks."
            ),
            font=("Arial", 28),
            justify="left"
        ).pack(pady=10)

        self.home_status_frame = ctk.CTkFrame(self.content)
        self.home_status_frame.pack(fill="x", pady=15)

        ctk.CTkLabel(
            self.home_status_frame,
            text="Activity Log",
            font=("Arial", 18, "bold")
        ).pack(anchor="w", padx=10, pady=5)

    # ---------------- INSTALL ---------------- #
    def install(self):
        self.clear_content()

        ctk.CTkLabel(
            self.content, text="Install Software",
            font=("Arial", 22, "bold")
        ).pack(pady=10)

        ctk.CTkButton(
            self.content, text="🎙 Voice: Install Python",
            height=45, font=("Arial", 16),
            command=self.voice_command
        ).pack(pady=6)

        ctk.CTkButton(
            self.content, text="Install Python",
            height=45, font=("Arial", 16),
            command=lambda: self.agent.handle_request("Python")
        ).pack(pady=6)

        ctk.CTkButton(
            self.content, text="Install Git",
            height=45, font=("Arial", 16),
            command=lambda: self.agent.handle_request("Git")
        ).pack(pady=6)

    # ---------------- SCHEDULE ---------------- #
    def schedule(self):
        self.clear_content()

        ctk.CTkLabel(
            self.content, text="Schedule Installation",
            font=("Arial", 22, "bold")
        ).pack(pady=10)

        self.software = ctk.StringVar(value="Python")
        ctk.CTkOptionMenu(
            self.content,
            variable=self.software,
            values=["Python", "Git"]
        ).pack(pady=6)

        self.time_entry = ctk.CTkEntry(
            self.content,
            placeholder_text="YYYY-MM-DD HH:MM"
        )
        self.time_entry.pack(pady=6)

        ctk.CTkButton(
            self.content, text="Schedule",
            height=45,
            command=self.set_schedule
        ).pack(pady=10)

    # ---------------- ABOUT ---------------- #
    def about(self):
        self.clear_content()

        text = (
            "PROJECT NAME:\n"
            "AI-Based Software Setup Assistant\n\n"
            "DESCRIPTION:\n"
            "This project automates software installation using\n"
            "multi-agent AI architecture and voice commands.\n\n"
            "FEATURES:\n"
            "- Voice controlled installation\n"
            "- OS detection\n"
            "- Intelligent install check\n"
            "- Scheduler support\n"
            "- Modular AI agents\n\n"
            "DEVELOPER:\n"
            f"{self.username}\n\n"
            "TECH STACK:\n"
            "Python, CustomTkinter, SpeechRecognition\n\n"
            "USE CASE:\n"
            "Engineering students & freshers"
        )

        ctk.CTkLabel(
            self.content,
            text=text,
            font=("Arial", 20),
            justify="left"
        ).pack(padx=20, pady=20, anchor="w")

    # ---------------- SETTINGS ---------------- #
    def settings(self):
        self.clear_content()

        ctk.CTkLabel(
            self.content, text="Settings",
            font=("Arial", 22, "bold")
        ).pack(pady=10)

        ctk.CTkButton(
            self.content, text="Switch Dark / Light Theme",
            height=40,
            command=self.toggle_theme
        ).pack(pady=8)

        ctk.CTkOptionMenu(
            self.content,
            values=["English", "Tamil"],
            command=self.change_language
        ).pack(pady=8)

    def toggle_theme(self):
        mode = ctk.get_appearance_mode()
        ctk.set_appearance_mode("light" if mode == "Dark" else "dark")

    def change_language(self, lang):
        msg.showinfo("Language", f"{lang} selected (demo)")

    # ---------------- VOICE ---------------- #
    def voice_command(self):
        threading.Thread(
            target=self.listen_voice,
            daemon=True
        ).start()

    def listen_voice(self):
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                audio = r.listen(source, timeout=5)
                text = r.recognize_google(audio).lower()

            if "python" in text:
                self.agent.handle_request("Python")
            elif "git" in text:
                self.agent.handle_request("Git")
            else:
                msg.showinfo("Voice", "Software not recognized")

        except:
            msg.showerror("Error", "Voice recognition failed")

    # ---------------- HELPERS ---------------- #
    def safe_status(self, text):
        self.after(0, lambda: self.status.configure(text=text))

    def safe_home_log(self, text):
        def add():
            if hasattr(self, "home_status_frame"):
                ctk.CTkLabel(
                    self.home_status_frame,
                    text=f"- {text}",
                    font=("Arial", 12),
                    anchor="w"
                ).pack(anchor="w", padx=15)
        self.after(0, add)

    def set_schedule(self):
        try:
            run_time = datetime.strptime(
                self.time_entry.get(),
                "%Y-%m-%d %H:%M"
            )
            threading.Thread(
                target=self.wait_and_run,
                args=(run_time, self.software.get()),
                daemon=True
            ).start()
            msg.showinfo("Scheduled", "Task scheduled")
        except:
            msg.showerror("Error", "Invalid date/time")

    def wait_and_run(self, run_time, software):
        while datetime.now() < run_time:
            time.sleep(1)
        self.agent.handle_request(software)

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
