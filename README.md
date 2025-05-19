# -CodeAlpha_Project_Basic_Chatbot
Create a text-based chatbot that can have conversations with users. You can use natural language processing libraries like NLTK or spaCy to make your chatbot more conversational.

**LAN-Based Python Chat App with GUI, Emojis, File Sharing, and Enhanced UI**

---

**Project Description:**

This is a real-time, two-person LAN chat application built using Python. It features a graphical user interface (GUI) with enhanced interactivity and aesthetics using Tkinter. The app enables two users on the same network to communicate via chat with support for file sharing, emojis, and a modern, colorful UI.

**Key Features:**

* 💻 Socket Communication: Uses TCP sockets for real-time messaging.
* 🧑‍🤝‍🧑 Two-Person Chat: Designed for exactly two users to chat over LAN.
* 🌈 Color-coded UI: Sent messages in green, received messages in blue, timestamps in red.
* 🧠 Typing Indicator: Shows "Typing..." feedback while a user is typing.
* 📌 File Transfer: Send and receive files directly through the chat.
* 😀 Emoji Support: Use emoji shortcodes like "\:smile:" to send emojis.
* 🕒 Timestamp + Date: Each message includes the time and date it was sent.
* 📝 Chat History Logging: Messages are saved to a file named `chat_<username>.txt`.
* 🧹 Clear Chat: Button to clear chat messages from the screen.
* 🗑️ Modern GUI: Includes hover effects, colored backgrounds, and polished buttons.

**Technologies Used:**

* `socket` - For TCP communication.
* `threading` - To handle simultaneous send/receive actions.
* `tkinter` - For GUI elements.
* `emoji` - To support emoji shortcodes.
* `datetime` - For timestamps and dates.
* `os` - For managing file transfers and local storage.

**Folder Structure:**

```
chat_project/
|
|-- server.py            # Chat server file
|-- client.py            # Chat client with GUI
|-- chat_<username>.txt  # Generated per user to store chat logs
|-- received_<filename>  # Received file(s)
```

**Running Instructions:**

1. **Install Requirements:**

   ```bash
   pip install emoji
   ```

2. **Start Server:**
   Open a terminal and run:

   ```bash
   python server.py
   ```

   This will start the server and wait for two clients.

3. **Run Client(s):**
   Open another terminal (same or different machine on LAN):

   ```bash
   python client.py
   ```

   Enter your username when prompted.

   To connect over LAN, replace "localhost" in `client.py` with the server's IP address.

4. **Start Chatting:**
   Use the entry field to type messages, send emojis, or use buttons to send files or clear the chat.

**Tips:**

* Make sure all machines are on the same local network.
* Allow firewall access when prompted.
* Use two terminal windows or two machines for testing.
* Find server IP using `ipconfig` (Windows) or `ifconfig` (Linux/Mac).

**Sample IP Configuration for LAN:**

```python
ChatClient("192.168.1.10", 5555)
```



