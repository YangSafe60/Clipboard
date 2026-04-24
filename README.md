# 📋 Clipboard

A high-performance Windows clipboard manager built in Python that tracks your history of text and images. It provides a sleek, "shadow" interface that stays hidden until needed, allowing you to quickly recall and manage your copied data.

---

## 📋 Features

* **Dual-Category History**: Automatically separates copied content into **📑 CLIPS** (Text) and **🖼️ PICS** (Images).
* **Stealth Mode**: Hidden by default. Use the global hotkey `Alt + V` to toggle the clipboard overlay instantly.
* **Smart Monitoring**: Runs a background listener thread that captures clipboard changes without interfering with your workflow.
* **Image Thumbnails**: Preview copied images directly within the UI before re-copying them.
* **Clean UI/UX**: Built with a dark-themed, modern interface that anchors to the bottom-right of your workspace.
* **One-Click Recall**: Click the icon next to any history item to push it back to the active Windows clipboard.
* **Memory Efficient**: Prevents duplicate entries and avoids "feedback loops" when the app itself modifies the clipboard.

---

## 🛠️ Technologies

* **Python 3.10+**
* **CustomTkinter**: Modern, high-DPI GUI components.
* **PyWin32 (win32clipboard, win32api)**: Native Windows API integration for advanced clipboard handling and window management.
* **Pillow (PIL)**: Image processing, thumbnail generation, and DIB (Device Independent Bitmap) conversion.
* **Pyperclip**: Cross-platform text clipboard utilities.
* **Keyboard**: Global hotkey listening.
* **Threading**: Background monitoring to ensure the GUI remains responsive.

---

## 📦 Installation

### 1. Requirements
Ensure you are running **Windows** (the application relies on `win32api` and `win32clipboard`).

### 2. Clone the repository
```bash
git clone https://github.com/YangSafe60/Clipboard
cd Clipboard
```

### 3. Install dependencies
```bash
pip install customtkinter pyperclip Pillow keyboard pywin32
```

### 4. Run the application
```bash
python main.py
```

---

## 📖 How to Use

1.  **Launch**: Run the script. The app starts hidden in the background.
2.  **Toggle Visibility**: Press **`Alt + V`** to show the clipboard manager at the bottom-right of your screen.
3.  **Browse History**: Switch between the **CLIPS** and **PICS** tabs to see your recent activity.
4.  **Re-Copy**: Click the **📑** or **🖼️** button on an entry to make it your active clipboard content.
5.  **Delete/Clear**: Use the **🗑️** button on specific items to remove them, or use **"Clear Current View"** at the bottom to wipe the current tab.
6.  **Hide**: Press **`Alt + V`** again or perform a copy action to automatically hide the window.

---

## 🗂️ Project Structure

```text
ProShadowClipboard/
├── shadow_clipboard.py      # Main Application (Logic, UI, & Listener)
├── README.md                # Documentation
```

---

## 🐛 Troubleshooting

| Issue | Cause | Solution |
| :--- | :--- | :--- |
| **Hotkey not working** | Permissions or focus issue. | Try running the terminal/IDE as **Administrator**. |
| **Images not appearing** | Unsupported image format. | Ensure the image is copied as a standard Bitmap/DIB (standard for most PrintScreens). |
| **Window won't show** | Monitor resolution change. | Restart the app to recalibrate the bottom-right anchor coordinates. |
| **High CPU usage** | Sleep timer too low. | The script uses a 0.4s sleep interval; increase `time.sleep()` in `clipboard_listener` if needed. |

---

## 📝 Important Notes

* **Windows Only**: This application utilizes `win32con` and `win32api`, making it strictly compatible with Windows OS.
* **Data Persistence**: This version stores history in memory. Closing the application will clear your clipboard history.
* **Topmost Attribute**: The window is set to stay on top of all other applications when visible to ensure easy access.

---

## 🤝 Contributing

1. **Fork** the project.
2. Create your **Feature Branch** (`git checkout -b feature/AmazingFeature`).
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`).
4. **Push** to the branch (`git push origin feature/AmazingFeature`).
5. Open a **Pull Request**.

---

## 📄 License

Distributed under the **MIT License**.

**Developed by:** YangSafe60