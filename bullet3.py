import customtkinter as ctk
import tkinter.messagebox as msg
import threading, time, platform, shutil
from datetime import datetime
import speech_recognition as sr

# Appearance and theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ================= CENTRAL AI AGENT ================= #
class CentralAIAgent:
    def __init__(self, ui):
        self.ui = ui

    def handle_request(self, software):
        threading.Thread(target=self._process, args=(software,), daemon=True).start()

    def _process(self, software):
        os_name = platform.system()
        self.ui.update_status(f"OS detected: {os_name}")

        if self.is_installed(software):
            msg.showinfo("Info", f"{software} already installed")
            self.ui.update_status(f"{software} already available ✔")
            self.ui.add_home_status(f"{software}: Installed")
            return

        self.download_agent(software)

    # -------- Child Agent A -------- #
    def download_agent(self, software):
        self.ui.update_status(f"Downloading {software}...")
        time.sleep(2)

        ok = msg.askyesno("Download Complete",
                          f"{software} downloaded.\nProceed to install?")
        if ok:
            self.install_agent(software)
        else:
            self.ui.update_status("Installation cancelled")
            self.ui.add_home_status(f"{software}: Download cancelled")

    # -------- Child Agent C -------- #
    def install_agent(self, software):
        self.ui.update_status(f"Installing {software}...")
        time.sleep(2)

        ok = msg.askyesno("Environment Setup",
                          f"Setup environment for {software}?")
        if ok:
            self.env_agent(software)
        else:
            self.ui.update_status("Environment skipped")
            self.ui.add_home_status(f"{software}: Install skipped")

    # -------- Child Agent D -------- #
    def env_agent(self, software):
        self.ui.update_status("Configuring environment...")
        time.sleep(1)
        self.ui.update_status(f"{software} ready ✅")
        msg.showinfo("Success", f"{software} installed & configured!")
        self.ui.add_home_status(f"{software}: Installed & Configured")

    # -------- Auto Environment Check -------- #
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
        self.geometry("1000x600")
        self.scheduled_tasks = []

        self.agent = CentralAIAgent(self)
        self.logged_user = None  # <-- store logged username
        self.build_login()

    # ---------------- LOGIN ---------------- #
    def build_login(self):
        self.clear()
        frame = ctk.CTkFrame(self)
        frame.pack(expand=True)

        ctk.CTkLabel(frame, text="AI Setup Assistant",
                     font=("Arial", 26)).pack(pady=15)

        self.user = ctk.CTkEntry(frame, placeholder_text="Username")
        self.user.pack(pady=5)

        self.pwd = ctk.CTkEntry(frame, placeholder_text="Password", show="*")
        self.pwd.pack(pady=5)

        ctk.CTkButton(frame, text="Login",
                      command=self.login).pack(pady=10)

    def login(self):
        username = self.user.get()
        password = self.pwd.get()

        # Hardcoded credentials for prototype
        if username == "admin" and password == "admin123":
            self.logged_user = username  # <-- save before destroying widgets
            self.build_main()
        else:
            msg.showerror("Error", "Invalid credentials")

    # ---------------- MAIN UI ---------------- #
    def build_main(self):
        self.clear()

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=180)
        self.sidebar.pack(side="left", fill="y", pady=10)

        for name, cmd in [
            ("Home", self.home),
            ("Install", self.install),
            ("Schedule", self.schedule),
            ("About", self.about),
            ("Settings", self.settings)
        ]:
            ctk.CTkButton(self.sidebar, text=name, command=cmd,
                          height=50, font=("Arial", 14)).pack(fill="x", pady=5, padx=5)

        # Content area
        self.content = ctk.CTkFrame(self)
        self.content.pack(expand=True, fill="both", padx=10, pady=10)

        # Status bar
        self.status = ctk.CTkLabel(self, text="Ready", anchor="w")
        self.status.pack(side="bottom", fill="x")

        self.home()

    # ---------------- PAGES ---------------- #
    def home(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text=f"Welcome {self.logged_user}!",
                     font=("Arial", 24)).pack(pady=20)
        ctk.CTkLabel(self.content,
                     text="Use the 'Install' tab to quickly setup Python, Git, and other tools.\n"
                          "Voice commands supported: e.g., 'Install Python'.\n"
                          "Check 'Schedule' tab to schedule installation tasks.",
                     font=("Arial", 14), justify="left").pack(pady=10)

        # Quick status summary
        self.home_status_frame = ctk.CTkFrame(self.content)
        self.home_status_frame.pack(pady=10, fill="x")
        ctk.CTkLabel(self.home_status_frame, text="Installed / Scheduled Status",
                     font=("Arial", 16)).pack(anchor="w")

    def add_home_status(self, text):
        if hasattr(self, "home_status_frame"):
            ctk.CTkLabel(self.home_status_frame, text=f"- {text}", font=("Arial", 12),
                         anchor="w").pack(fill="x")

    def install(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Install Software",
                     font=("Arial", 20)).pack(pady=10)

        ctk.CTkButton(self.content, text="🎙 Voice: Install Python",
                      command=self.voice_command, height=40, font=("Arial", 14)).pack(pady=5)

        ctk.CTkButton(self.content, text="Install Python",
                      command=lambda: self.agent.handle_request("Python"),
                      height=40, font=("Arial", 14)).pack(pady=5)

        ctk.CTkButton(self.content, text="Install Git",
                      command=lambda: self.agent.handle_request("Git"),
                      height=40, font=("Arial", 14)).pack(pady=5)

    def schedule(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Schedule Install",
                     font=("Arial", 20)).pack(pady=10)

        self.software = ctk.StringVar(value="Python")
        ctk.CTkOptionMenu(self.content, variable=self.software,
                          values=["Python", "Git"]).pack(pady=5)

        self.time_entry = ctk.CTkEntry(
            self.content, placeholder_text="YYYY-MM-DD HH:MM")
        self.time_entry.pack(pady=5)

        ctk.CTkButton(self.content, text="Schedule",
                      command=self.set_schedule, height=40, font=("Arial", 14)).pack(pady=5)

    def about(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="About Project",
                     font=("Arial", 22)).pack(pady=10)

        info_text = (
            "Project: AI Software Setup Assistant\n"
            "Developer: Mukesh Kanna S\n"
            "Year: 2025\n"
            "Description: Voice-driven multi-agent AI assistant for software installation,\n"
            "environment setup, and scheduler automation for engineering students.\n\n"
            "Features:\n"
            "- Real-time OS detection\n"
            "- Voice command support (English/Tamil)\n"
            "- Install Python, Git, and other tools\n"
            "- Child agents handle download, install, and environment setup\n"
            "- Scheduler for future installations\n"
            "- Status monitoring and popup confirmations\n\n"
            "Objective:\n"
            "Simplify software setup process for students and reduce manual errors."
        )

        ctk.CTkLabel(self.content, text=info_text,
                     font=("Arial", 14), justify="left").pack(pady=10)

    def settings(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Settings",
                     font=("Arial", 22)).pack(pady=10)

        ctk.CTkLabel(self.content, text="Theme Mode:",
                     font=("Arial", 14)).pack(pady=5)
        ctk.CTkOptionMenu(self.content,
                          values=["Light", "Dark"],
                          command=self.change_theme).pack(pady=5)

        ctk.CTkLabel(self.content, text="Voice Language:",
                     font=("Arial", 14)).pack(pady=5)
        ctk.CTkOptionMenu(self.content,
                          values=["English", "Tamil"],
                          command=self.change_language).pack(pady=5)

        ctk.CTkLabel(self.content, text="Future Suggestions:",
                     font=("Arial", 14)).pack(pady=5)
        ctk.CTkLabel(self.content,
                     text="- Automatic environment check\n- Advanced scheduling\n- Additional software support",
                     font=("Arial", 12), justify="left").pack(pady=5)

    # ---------------- VOICE ---------------- #
    def voice_command(self):
        self.update_status("Listening...")
        threading.Thread(target=self.listen_voice, daemon=True).start()

    def listen_voice(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                audio = r.listen(source, timeout=5)
                text = r.recognize_google(audio).lower()
                self.update_status(f"Heard: {text}")

                if "python" in text:
                    self.agent.handle_request("Python")
                elif "git" in text:
                    self.agent.handle_request("Git")
                else:
                    msg.showinfo("Info", "Software not recognized")

            except:
                msg.showerror("Error", "Voice recognition failed")
                self.update_status("Voice error")

    # ---------------- SCHEDULER ---------------- #
    def set_schedule(self):
        try:
            run_time = datetime.strptime(
                self.time_entry.get(), "%Y-%m-%d %H:%M")
            task = (run_time, self.software.get())
            self.scheduled_tasks.append(task)
            threading.Thread(
                target=self.wait_and_run,
                args=(run_time, self.software.get()),
                daemon=True
            ).start()
            msg.showinfo("Scheduled", f"{task[1]} scheduled at {task[0]}")
            self.add_home_status(f"{task[1]} scheduled for {task[0]}")
        except:
            msg.showerror("Error", "Invalid date/time format")

    def wait_and_run(self, run_time, software):
        while datetime.now() < run_time:
            time.sleep(1)
        self.agent.handle_request(software)

    # ---------------- HELPERS ---------------- #
    def update_status(self, msg_txt):
        self.status.configure(text=msg_txt)

    def change_theme(self, mode):
        ctk.set_appearance_mode(mode)
        self.update_status(f"Theme set to {mode}")

    def change_language(self, lang):
        self.update_status(f"Voice language set to {lang}")

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
