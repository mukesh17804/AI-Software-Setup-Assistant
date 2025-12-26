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
        # Define software versions and dependencies
        self.software_info = {
            "Python": {"versions": ["3.11", "3.10", "3.9"], "dependencies": []},
            "Git": {"versions": ["2.41", "2.40"], "dependencies": []},
            "Node": {"versions": ["20", "18"], "dependencies": ["Python"]}
        }

    def handle_request(self, software, version=None):
        threading.Thread(target=self._process, args=(software, version), daemon=True).start()

    def _process(self, software, version):
        os_name = platform.system()
        self.ui.update_status(f"OS detected: {os_name}")

        # Dependency check
        dependencies = self.software_info.get(software, {}).get("dependencies", [])
        for dep in dependencies:
            if not self.is_installed(dep):
                self.ui.add_home_status(f"Dependency {dep} not found, installing first...")
                self._process(dep, None)

        selected_version = version if version else self.software_info.get(software, {}).get("versions", [None])[0]

        if self.is_installed(software):
            self.ui.add_home_status(f"{software} already installed")
            self.ui.update_status(f"{software} already available ✔")
            return

        self.download_agent(software, selected_version)

    # -------- Child Agent A -------- #
    def download_agent(self, software, version):
        self.ui.update_status(f"Downloading {software} v{version}...")
        time.sleep(2)

        ok = msg.askyesno("Download Complete",
                          f"{software} v{version} downloaded.\nProceed to install?")
        if ok:
            self.install_agent(software, version)
        else:
            self.ui.update_status("Installation cancelled")
            self.ui.add_home_status(f"{software} v{version}: Download cancelled")

    # -------- Child Agent B -------- #
    def install_agent(self, software, version):
        self.ui.update_status(f"Installing {software} v{version}...")
        time.sleep(2)

        ok = msg.askyesno("Environment Setup",
                          f"Setup environment for {software} v{version}?")
        if ok:
            self.env_agent(software, version)
        else:
            self.ui.update_status("Environment skipped")
            self.ui.add_home_status(f"{software} v{version}: Install skipped")

    # -------- Child Agent C -------- #
    def env_agent(self, software, version):
        self.ui.update_status("Configuring environment...")
        time.sleep(1)
        self.ui.update_status(f"{software} v{version} ready ✅")
        msg.showinfo("Success", f"{software} v{version} installed & configured!")
        self.ui.add_home_status(f"{software} v{version}: Installed & Configured")

    # -------- Auto Environment Check -------- #
    def is_installed(self, software):
        if software.lower() == "python": return shutil.which("python") is not None
        if software.lower() == "git": return shutil.which("git") is not None
        if software.lower() == "node": return shutil.which("node") is not None
        return False


# ================= MAIN APP ================= #
class AIInstallerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AI Software Setup Assistant")
        self.geometry("1100x650")
        self.scheduled_tasks = []

        self.agent = CentralAIAgent(self)
        self.logged_user = None
        self.build_login()

    # ---------------- LOGIN ---------------- #
    def build_login(self):
        self.clear()
        frame = ctk.CTkFrame(self)
        frame.pack(expand=True)

        ctk.CTkLabel(frame, text="AI Setup Assistant", font=("Arial", 26)).pack(pady=15)
        self.user = ctk.CTkEntry(frame, placeholder_text="Username")
        self.user.pack(pady=5)
        self.pwd = ctk.CTkEntry(frame, placeholder_text="Password", show="*")
        self.pwd.pack(pady=5)
        ctk.CTkButton(frame, text="Login", command=self.login).pack(pady=10)

    def login(self):
        username = self.user.get()
        password = self.pwd.get()
        if username == "admin" and password == "admin123":
            self.logged_user = username
            self.build_main()
        else:
            msg.showerror("Error", "Invalid credentials")

    # ---------------- MAIN UI ---------------- #
    def build_main(self):
        self.clear()
        self.sidebar = ctk.CTkFrame(self, width=180)
        self.sidebar.pack(side="left", fill="y", pady=10)
        for name, cmd in [("Home", self.home), ("Install", self.install), ("Schedule", self.schedule),
                          ("About", self.about), ("Settings", self.settings)]:
            ctk.CTkButton(self.sidebar, text=name, command=cmd, height=50, font=("Arial", 14)).pack(fill="x", pady=5, padx=5)

        self.content = ctk.CTkFrame(self)
        self.content.pack(expand=True, fill="both", padx=10, pady=10)
        self.status = ctk.CTkLabel(self, text="Ready", anchor="w")
        self.status.pack(side="bottom", fill="x")
        self.home()

    # ---------------- PAGES ---------------- #
    def home(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text=f"Welcome {self.logged_user}!", font=("Arial", 24)).pack(pady=20)
        ctk.CTkLabel(self.content,
                     text="Use 'Install' tab to setup software.\nVoice commands supported.\nCheck 'Schedule' tab to schedule tasks.",
                     font=("Arial", 14), justify="left").pack(pady=10)
        self.home_status_frame = ctk.CTkFrame(self.content)
        self.home_status_frame.pack(pady=10, fill="x")
        ctk.CTkLabel(self.home_status_frame, text="Installed / Scheduled Status", font=("Arial", 16)).pack(anchor="w")

    # Thread-safe UI updates
    def add_home_status(self, text):
        if hasattr(self, "home_status_frame"):
            self.home_status_frame.after(0, lambda: ctk.CTkLabel(
                self.home_status_frame, text=f"- {text}", font=("Arial", 12), anchor="w").pack(fill="x"))

    def install(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Install Software", font=("Arial", 20)).pack(pady=10)

        self.selected_software = ctk.StringVar(value="Python")
        self.selected_version = ctk.StringVar(value=None)
        ctk.CTkOptionMenu(self.content, variable=self.selected_software,
                          values=list(self.agent.software_info.keys())).pack(pady=5)
        self.version_menu = ctk.CTkOptionMenu(self.content, variable=self.selected_version, values=[])
        self.version_menu.pack(pady=5)

        def update_versions(choice):
            versions = self.agent.software_info[choice]["versions"]
            self.version_menu.configure(values=versions)
            if versions:
                self.selected_version.set(versions[0])
        update_versions("Python")
        self.selected_software.trace("w", lambda *args: update_versions(self.selected_software.get()))

        ctk.CTkButton(self.content, text="🎙 Voice Install", command=self.voice_command, height=40, font=("Arial", 14)).pack(pady=5)
        ctk.CTkButton(self.content, text="Install Selected Software",
                      command=lambda: self.agent.handle_request(self.selected_software.get(), self.selected_version.get()),
                      height=40, font=("Arial", 14)).pack(pady=5)

    def schedule(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Schedule Install", font=("Arial", 20)).pack(pady=10)
        self.software = ctk.StringVar(value="Python")
        self.software_version = ctk.StringVar(value=None)
        self.software_menu = ctk.CTkOptionMenu(self.content, variable=self.software, values=list(self.agent.software_info.keys()))
        self.software_menu.pack(pady=5)
        self.version_sched_menu = ctk.CTkOptionMenu(self.content, variable=self.software_version, values=[])
        self.version_sched_menu.pack(pady=5)
        def update_versions_sched(choice):
            versions = self.agent.software_info[choice]["versions"]
            self.version_sched_menu.configure(values=versions)
            if versions:
                self.software_version.set(versions[0])
        update_versions_sched("Python")
        self.software.trace("w", lambda *args: update_versions_sched(self.software.get()))
        self.time_entry = ctk.CTkEntry(self.content, placeholder_text="YYYY-MM-DD HH:MM")
        self.time_entry.pack(pady=5)
        ctk.CTkButton(self.content, text="Schedule",
                      command=self.set_schedule, height=40, font=("Arial", 14)).pack(pady=5)

    def about(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="About Project", font=("Arial", 22)).pack(pady=10)
        info_text = (
            "Project: AI Software Setup Assistant\nDeveloper: Mukesh Kanna S\nYear: 2025\n"
            "Voice-driven multi-agent AI assistant for software installation,\n"
            "environment setup, multi-version support, dependencies management, and scheduler automation.\n\n"
            "Features:\n- Real-time OS detection\n- Voice command support\n- Multi-version selection\n"
            "- Dependency management\n- Scheduler\n- Status monitoring\n- Popup confirmations\n\n"
            "Objective: Simplify software setup process for students."
        )
        ctk.CTkLabel(self.content, text=info_text, font=("Arial", 14), justify="left").pack(pady=10)

    def settings(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Settings", font=("Arial", 22)).pack(pady=10)
        ctk.CTkLabel(self.content, text="Theme Mode:", font=("Arial", 14)).pack(pady=5)
        ctk.CTkOptionMenu(self.content, values=["Light", "Dark"], command=self.change_theme).pack(pady=5)
        ctk.CTkLabel(self.content, text="Voice Language:", font=("Arial", 14)).pack(pady=5)
        ctk.CTkOptionMenu(self.content, values=["English", "Tamil"], command=self.change_language).pack(pady=5)

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
                for software in self.agent.software_info.keys():
                    if software.lower() in text:
                        version = None
                        for v in self.agent.software_info[software]["versions"]:
                            if v in text:
                                version = v
                        self.agent.handle_request(software, version)
                        return
                msg.showinfo("Info", "Software not recognized")
            except:
                msg.showerror("Error", "Voice recognition failed")
                self.update_status("Voice error")

    def set_schedule(self):
        try:
            run_time = datetime.strptime(self.time_entry.get(), "%Y-%m-%d %H:%M")
            software = self.software.get()
            version = self.software_version.get()
            task = (run_time, software, version)
            self.scheduled_tasks.append(task)
            threading.Thread(target=self.wait_and_run, args=(run_time, software, version), daemon=True).start()
            msg.showinfo("Scheduled", f"{software} v{version} scheduled at {run_time}")
            self.add_home_status(f"{software} v{version} scheduled for {run_time}")
        except:
            msg.showerror("Error", "Invalid date/time format")

    def wait_and_run(self, run_time, software, version):
        while datetime.now() < run_time:
            time.sleep(1)
        self.agent.handle_request(software, version)

    # ---------------- HELPERS ---------------- #
    def update_status(self, msg_txt):
        self.status.configure(text=msg_txt)
    def change_theme(self, mode): ctk.set_appearance_mode(mode); self.update_status(f"Theme set to {mode}")
    def change_language(self, lang): self.update_status(f"Voice language set to {lang}")
    def clear(self): [w.destroy() for w in self.winfo_children()]
    def clear_content(self): [w.destroy() for w in self.content.winfo_children()]

# ================= RUN ================= #
if __name__ == "__main__":
    app = AIInstallerApp()
    app.mainloop()
