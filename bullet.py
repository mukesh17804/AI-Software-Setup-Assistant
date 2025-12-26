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
        threading.Thread(target=self._process, args=(software,), daemon=True).start()

    def _process(self, software):
        os_name = platform.system()
        self.ui.update_status(f"OS detected: {os_name}")

        if self.is_installed(software):
            msg.showinfo("Info", f"{software} already installed")
            self.ui.update_status(f"{software} already available ✔")
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

    # -------- Child Agent D -------- #
    def env_agent(self, software):
        self.ui.update_status("Configuring environment...")
        time.sleep(1)
        self.ui.update_status(f"{software} ready ✅")
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
        self.geometry("1000x600")

        self.agent = CentralAIAgent(self)
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
        if self.user.get() and self.pwd.get():
            self.build_main()
        else:
            msg.showerror("Error", "Invalid credentials")

    # ---------------- MAIN UI ---------------- #
    def build_main(self):
        self.clear()

        self.sidebar = ctk.CTkFrame(self, width=180)
        self.sidebar.pack(side="left", fill="y")

        for name, cmd in [
            ("Home", self.home),
            ("Install", self.install),
            ("Schedule", self.schedule),
            ("About", self.about),
            ("Settings", self.settings)
        ]:
            ctk.CTkButton(self.sidebar, text=name,
                          command=cmd).pack(fill="x", pady=5)

        self.content = ctk.CTkFrame(self)
        self.content.pack(expand=True, fill="both")

        self.status = ctk.CTkLabel(self, text="Ready", anchor="w")
        self.status.pack(side="bottom", fill="x")

        self.home()

    # ---------------- PAGES ---------------- #
    def home(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Welcome",
                     font=("Arial", 22)).pack(pady=20)

    def install(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Install Software",
                     font=("Arial", 20)).pack(pady=10)

        ctk.CTkButton(self.content, text="🎙 Voice: Install Python",
                      command=self.voice_command).pack(pady=5)

        ctk.CTkButton(self.content, text="Install Python",
                      command=lambda: self.agent.handle_request("Python")).pack(pady=5)

        ctk.CTkButton(self.content, text="Install Git",
                      command=lambda: self.agent.handle_request("Git")).pack(pady=5)

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
                      command=self.set_schedule).pack(pady=5)

    def about(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="About Project",
                     font=("Arial", 20)).pack(pady=10)
        ctk.CTkLabel(
            self.content,
            text=("AI-based voice driven software setup assistant\n"
                  "for engineering freshers using multi-agent AI."),
            justify="left"
        ).pack()

    def settings(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Settings",
                     font=("Arial", 20)).pack(pady=10)
        ctk.CTkLabel(self.content,
                     text="Theme & language handled internally").pack()

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
            threading.Thread(
                target=self.wait_and_run,
                args=(run_time, self.software.get()),
                daemon=True
            ).start()
            msg.showinfo("Scheduled", "Task scheduled successfully")
        except:
            msg.showerror("Error", "Invalid date/time format")

    def wait_and_run(self, run_time, software):
        while datetime.now() < run_time:
            time.sleep(1)
        self.agent.handle_request(software)

    # ---------------- HELPERS ---------------- #
    def update_status(self, msg_txt):
        self.status.configure(text=msg_txt)

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
