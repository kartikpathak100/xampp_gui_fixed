#!/usr/bin/env python3
"""
XAMPP Control Panel for macOS
A modern replacement for the broken manager-osx GUI.
Tested on macOS Sonoma/Sequoia with XAMPP 8.x.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import threading
import time
import webbrowser
import os

class XAMPPController:
    XAMPP_PATH = "/Applications/XAMPP/xamppfiles/xampp"
    HTDOCS_PATH = "/Applications/XAMPP/xamppfiles/htdocs"
    
    def __init__(self, root):
        self.root = root
        self.root.title("XAMPP Control Panel")
        self.root.geometry("500x420")
        self.root.resizable(False, False)
        
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f5f5f5")
        self.style.configure("TLabel", background="#f5f5f5", font=("Helvetica", 11))
        self.style.configure("TButton", font=("Helvetica", 11))
        self.style.configure("Header.TLabel", font=("Helvetica", 18, "bold"), foreground="#2c3e50")
        self.style.configure("Status.TLabel", font=("Helvetica", 10, "italic"))
        
        self.root.configure(bg="#f5f5f5")
        
        self._build_ui()
        self._start_status_monitor()
    
    def _build_ui(self):
        header = ttk.Label(self.root, text="XAMPP Control Panel", style="Header.TLabel")
        header.pack(pady=(15, 5))
        
        sub = ttk.Label(self.root, text="macOS Manager Replacement", style="Status.TLabel")
        sub.pack(pady=(0, 15))
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        services_frame = ttk.LabelFrame(main_frame, text="Services", padding="10")
        services_frame.pack(fill=tk.X, pady=5)
        
        self.apache_status = tk.StringVar(value="Checking...")
        ttk.Label(services_frame, text="Apache", width=12, anchor=tk.W).grid(row=0, column=0, padx=5, pady=5)
        self.apache_indicator = tk.Canvas(services_frame, width=12, height=12, highlightthickness=0)
        self.apache_indicator.grid(row=0, column=1, padx=5)
        self.apache_indicator.create_oval(2, 2, 10, 10, fill="gray")
        ttk.Label(services_frame, textvariable=self.apache_status, width=10).grid(row=0, column=2, padx=5)
        ttk.Button(services_frame, text="Start", width=8, command=self.start_apache).grid(row=0, column=3, padx=2)
        ttk.Button(services_frame, text="Stop", width=8, command=self.stop_apache).grid(row=0, column=4, padx=2)
        ttk.Button(services_frame, text="Restart", width=8, command=self.restart_apache).grid(row=0, column=5, padx=2)
        
        self.mysql_status = tk.StringVar(value="Checking...")
        ttk.Label(services_frame, text="MySQL", width=12, anchor=tk.W).grid(row=1, column=0, padx=5, pady=5)
        self.mysql_indicator = tk.Canvas(services_frame, width=12, height=12, highlightthickness=0)
        self.mysql_indicator.grid(row=1, column=1, padx=5)
        self.mysql_indicator.create_oval(2, 2, 10, 10, fill="gray")
        ttk.Label(services_frame, textvariable=self.mysql_status, width=10).grid(row=1, column=2, padx=5)
        ttk.Button(services_frame, text="Start", width=8, command=self.start_mysql).grid(row=1, column=3, padx=2)
        ttk.Button(services_frame, text="Stop", width=8, command=self.stop_mysql).grid(row=1, column=4, padx=2)
        ttk.Button(services_frame, text="Restart", width=8, command=self.restart_mysql).grid(row=1, column=5, padx=2)
        
        quick_frame = ttk.LabelFrame(main_frame, text="Quick Actions", padding="10")
        quick_frame.pack(fill=tk.X, pady=5)
        
        btn_frame = ttk.Frame(quick_frame)
        btn_frame.pack()
        
        ttk.Button(btn_frame, text="Start All", command=self.start_all, width=12).grid(row=0, column=0, padx=5, pady=2)
        ttk.Button(btn_frame, text="Stop All", command=self.stop_all, width=12).grid(row=0, column=1, padx=5, pady=2)
        ttk.Button(btn_frame, text="Restart All", command=self.restart_all, width=12).grid(row=0, column=2, padx=5, pady=2)
        
        links_frame = ttk.LabelFrame(main_frame, text="Open in Browser", padding="10")
        links_frame.pack(fill=tk.X, pady=5)
        
        link_frame = ttk.Frame(links_frame)
        link_frame.pack()
        
        ttk.Button(link_frame, text="localhost", command=self.open_localhost, width=12).grid(row=0, column=0, padx=5, pady=2)
        ttk.Button(link_frame, text="phpMyAdmin", command=self.open_phpmyadmin, width=12).grid(row=0, column=1, padx=5, pady=2)
        ttk.Button(link_frame, text="htdocs Folder", command=self.open_htdocs, width=12).grid(row=0, column=2, padx=5, pady=2)
        
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(bottom_frame, text="View Logs", command=self.show_logs, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="Edit Configs", command=self.open_configs, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="About", command=self.show_about, width=12).pack(side=tk.RIGHT, padx=5)
        
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _run_cmd(self, args):
        cmd = f'{" ".join(args)}'
        script = f'do shell script "{cmd}" with administrator privileges'
        try:
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True, text=True, timeout=30
            )
            return result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            return "", "Command timed out", 1
        except Exception as e:
            return "", str(e), 1
    
    def _run_cmd_no_admin(self, args):
        try:
            result = subprocess.run(
                args, capture_output=True, text=True, timeout=10
            )
            return result.stdout, result.stderr, result.returncode
        except Exception as e:
            return "", str(e), 1
    
    def _update_status(self):
        stdout, stderr, rc = self._run_cmd_no_admin([self.XAMPP_PATH, 'status'])
        output = stdout + stderr
        
        apache_running = "Apache" in output and "running" in output or "httpd" in output
        mysql_running = "MySQL" in output and "running" in output or "mysqld" in output
        
        self.apache_status.set("Running" if apache_running else "Stopped")
        self.mysql_status.set("Running" if mysql_running else "Stopped")
        
        color_apache = "#2ecc71" if apache_running else "#e74c3c"
        color_mysql = "#2ecc71" if mysql_running else "#e74c3c"
        
        self.apache_indicator.delete("all")
        self.apache_indicator.create_oval(2, 2, 10, 10, fill=color_apache, outline="")
        self.mysql_indicator.delete("all")
        self.mysql_indicator.create_oval(2, 2, 10, 10, fill=color_mysql, outline="")
    
    def _start_status_monitor(self):
        def monitor():
            while True:
                try:
                    self.root.after(0, self._update_status)
                except:
                    break
                time.sleep(3)
        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()
    
    def start_apache(self):
        self.status_bar.config(text="Starting Apache...")
        stdout, stderr, rc = self._run_cmd([self.XAMPP_PATH, 'startapache'])
        self.status_bar.config(text="Apache start complete")
        if rc != 0 and stderr:
            messagebox.showwarning("Apache", stderr[-500:])
        self._update_status()
    
    def stop_apache(self):
        self.status_bar.config(text="Stopping Apache...")
        stdout, stderr, rc = self._run_cmd([self.XAMPP_PATH, 'stopapache'])
        self.status_bar.config(text="Apache stop complete")
        self._update_status()
    
    def restart_apache(self):
        self.stop_apache()
        time.sleep(1)
        self.start_apache()
    
    def start_mysql(self):
        self.status_bar.config(text="Starting MySQL...")
        stdout, stderr, rc = self._run_cmd([self.XAMPP_PATH, 'startmysql'])
        self.status_bar.config(text="MySQL start complete")
        if rc != 0 and stderr:
            messagebox.showwarning("MySQL", stderr[-500:])
        self._update_status()
    
    def stop_mysql(self):
        self.status_bar.config(text="Stopping MySQL...")
        stdout, stderr, rc = self._run_cmd([self.XAMPP_PATH, 'stopmysql'])
        self.status_bar.config(text="MySQL stop complete")
        self._update_status()
    
    def restart_mysql(self):
        self.stop_mysql()
        time.sleep(1)
        self.start_mysql()
    
    def start_all(self):
        self.status_bar.config(text="Starting all services...")
        stdout, stderr, rc = self._run_cmd([self.XAMPP_PATH, 'start'])
        self.status_bar.config(text="All services started")
        self._update_status()
    
    def stop_all(self):
        self.status_bar.config(text="Stopping all services...")
        stdout, stderr, rc = self._run_cmd([self.XAMPP_PATH, 'stop'])
        self.status_bar.config(text="All services stopped")
        self._update_status()
    
    def restart_all(self):
        self.stop_all()
        time.sleep(2)
        self.start_all()
    
    def open_localhost(self):
        webbrowser.open('http://localhost')
    
    def open_phpmyadmin(self):
        webbrowser.open('http://localhost/phpmyadmin')
    
    def open_htdocs(self):
        subprocess.run(['open', self.HTDOCS_PATH])
    
    def show_logs(self):
        log_window = tk.Toplevel(self.root)
        log_window.title("XAMPP Logs")
        log_window.geometry("600x400")
        
        text = scrolledtext.ScrolledText(log_window, wrap=tk.WORD, font=("Menlo", 10))
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        logs = ["apache", "mysql", "php"]
        for log_name in logs:
            log_path = f"/Applications/XAMPP/xamppfiles/logs/{log_name}.log"
            text.insert(tk.END, f"\n{'='*50}\n{log_name.upper()} LOG\n{'='*50}\n\n")
            if os.path.exists(log_path):
                try:
                    with open(log_path, 'r') as f:
                        lines = f.readlines()[-100:]
                        text.insert(tk.END, ''.join(lines))
                except Exception as e:
                    text.insert(tk.END, f"Error reading log: {e}\n")
            else:
                text.insert(tk.END, f"Log file not found at {log_path}\n")
        
        text.config(state=tk.DISABLED)
    
    def open_configs(self):
        config_window = tk.Toplevel(self.root)
        config_window.title("XAMPP Configuration Files")
        config_window.geometry("400x250")
        
        configs = [
            ("Apache httpd.conf", "/Applications/XAMPP/xamppfiles/etc/httpd.conf"),
            ("Apache httpd-ssl.conf", "/Applications/XAMPP/xamppfiles/etc/extra/httpd-ssl.conf"),
            ("PHP php.ini", "/Applications/XAMPP/xamppfiles/etc/php.ini"),
            ("MySQL my.cnf", "/Applications/XAMPP/xamppfiles/etc/my.cnf"),
        ]
        
        for name, path in configs:
            frame = ttk.Frame(config_window, padding="5")
            frame.pack(fill=tk.X)
            ttk.Label(frame, text=name, width=20).pack(side=tk.LEFT)
            ttk.Button(frame, text="Open", command=lambda p=path: subprocess.run(['open', '-t', p])).pack(side=tk.RIGHT)
   
    def fix_permissions(self):
        script = 'do shell script "sudo chmod -R 777 /Applications/XAMPP/xamppfiles/temp/ && sudo chown -R daemon:daemon /Applications/XAMPP/xamppfiles/var/mysql/" with administrator privileges'
        subprocess.run(['osascript', '-e', script])
        messagebox.showinfo("Done", "Permissions fixed. Try starting MySQL again.")
    
    def show_about(self):
        messagebox.showinfo(
            "About XAMPP Control Panel",
            "XAMPP Control Panel for macOS\n\n"
            "A modern replacement for the broken manager-osx GUI.\n\n"
            "Features:\n"
            "- Start/Stop/Restart individual services\n"
            "- Real-time status indicators\n"
            "- Direct links to localhost and phpMyAdmin\n"
            "- Log viewer\n"
            "- Config file access\n\n"
            "Requires: macOS, XAMPP installed at /Applications/XAMPP"
        )

def main():
    root = tk.Tk()
    app = XAMPPController(root)
    root.mainloop()

if __name__ == "__main__":
    main()
