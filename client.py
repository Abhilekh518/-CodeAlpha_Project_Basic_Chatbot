import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext, filedialog, messagebox
from datetime import datetime
import emoji
import os

class ChatClient:
    def __init__(self, host, port):
        self.username = simpledialog.askstring("Username", "Enter your name:")
        if not self.username:
            exit()

        # Root UI
        self.root = tk.Tk()
        self.root.title(f"💬 Chat - {self.username}")
        self.root.configure(bg="#1e1e2f")

        # Chat Display
        self.chat_display = scrolledtext.ScrolledText(self.root, state='disabled', width=60, height=20, font=("Arial", 12), bg="#2e2e3e", fg="#ffffff", insertbackground='white')
        self.chat_display.pack(padx=10, pady=(10, 0))

        # Entry Field
        self.msg_entry = tk.Entry(self.root, width=40, font=("Arial", 12), bg="#44475a", fg="white", insertbackground='white', relief='flat')
        self.msg_entry.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10))
        self.msg_entry.bind("<Return>", lambda event: self.send_message())
        self.msg_entry.bind("<FocusIn>", lambda e: self.msg_entry.config(bg="#6272a4"))
        self.msg_entry.bind("<FocusOut>", lambda e: self.msg_entry.config(bg="#44475a"))
        self.msg_entry.bind("<Key>", self.typing_status)

        # Send Button
        self.send_btn = tk.Button(self.root, text="📤 Send", command=self.send_message, bg="#50fa7b", fg="black", font=("Arial", 10, "bold"), relief="flat", padx=10)
        self.send_btn.pack(side=tk.LEFT, padx=(5, 0), pady=(0, 10))

        # File Button
        self.file_btn = tk.Button(self.root, text="📎 File", command=self.send_file, bg="#8be9fd", fg="black", font=("Arial", 10, "bold"), relief="flat", padx=10)
        self.file_btn.pack(side=tk.LEFT, padx=(5, 0), pady=(0, 10))

        # Clear Chat Button
        self.clear_btn = tk.Button(self.root, text="🧹 Clear", command=self.clear_chat, bg="#ff5555", fg="white", font=("Arial", 10, "bold"), relief="flat", padx=10)
        self.clear_btn.pack(side=tk.LEFT, padx=(5, 10), pady=(0, 10))

        # Typing Status Label
        self.status_label = tk.Label(self.root, text="", fg="lightgray", bg="#1e1e2f", font=("Arial", 9))
        self.status_label.pack(pady=(0, 10))

        # Chat Tags for colors
        self.chat_display.tag_config("me", foreground="limegreen")
        self.chat_display.tag_config("other", foreground="deepskyblue")
        self.chat_display.tag_config("timestamp", foreground="red")
        self.chat_display.tag_config("file", foreground="violet", font=("Arial", 10, "bold"))

        # Socket Setup
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        threading.Thread(target=self.receive_messages, daemon=True).start()

        self.chat_log_file = f"chat_{self.username}.txt"

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def send_message(self):
        msg = self.msg_entry.get()
        if msg:
            msg = emoji.emojize(msg, language='alias')
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            full_msg = f"[{timestamp}] {self.username}: {msg}"
            self.client_socket.send(full_msg.encode("utf-8"))
            self.display_message(full_msg, "me")
            self.log_chat(full_msg)
            self.msg_entry.delete(0, tk.END)

    def send_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            filename = os.path.basename(filepath)
            with open(filepath, "rb") as f:
                data = f.read()
            header = f"[FILE]{self.username}:{filename}:{len(data)}".encode("utf-8")
            self.client_socket.send(header + b"\n" + data)
            file_msg = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] You sent file: {filename}"
            self.display_message(file_msg, "file")
            self.log_chat(file_msg)

    def receive_messages(self):
        buffer = b""
        while True:
            try:
                data = self.client_socket.recv(4096)
                if not data:
                    break
                buffer += data
                if buffer.startswith(b"[FILE]"):
                    try:
                        header, filedata = buffer.split(b"\n", 1)
                        parts = header.decode("utf-8").split(":")
                        sender = parts[0].split("]")[1]
                        filename = parts[1]
                        length = int(parts[2])
                        with open(f"received_{filename}", "wb") as f:
                            f.write(filedata[:length])
                        msg = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {sender} sent file: {filename}"
                        self.display_message(msg, "file")
                        self.log_chat(msg)
                        buffer = filedata[length:]
                    except ValueError:
                        continue
                else:
                    msg = buffer.decode("utf-8")
                    buffer = b""
                    if not msg.startswith(f"{self.username}:"):
                        self.display_message(msg, "other")
                        self.log_chat(msg)
            except:
                break

    def display_message(self, msg, tag):
        self.chat_display.config(state='normal')
        if msg.startswith("["):
            try:
                end = msg.index("]") + 1
                self.chat_display.insert(tk.END, msg[:end] + " ", "timestamp")
                msg = msg[end:].strip()
            except:
                pass
        self.chat_display.insert(tk.END, msg + "\n", tag)
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)

    def log_chat(self, msg):
        with open(self.chat_log_file, "a", encoding="utf-8") as f:
            f.write(msg + "\n")

    def clear_chat(self):
        confirm = messagebox.askyesno("Clear Chat", "Are you sure you want to clear the chat history?")
        if confirm:
            self.chat_display.config(state='normal')
            self.chat_display.delete('1.0', tk.END)
            self.chat_display.config(state='disabled')
            open(self.chat_log_file, "w").close()

    def typing_status(self, event=None):
        self.status_label.config(text="Typing...")
        self.root.after(1000, lambda: self.status_label.config(text=""))

    def on_close(self):
        self.client_socket.close()
        self.root.destroy()

if __name__ == "__main__":
    ChatClient("localhost", 5555)
