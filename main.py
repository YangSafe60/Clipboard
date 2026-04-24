import customtkinter as ctk
import pyperclip
from PIL import Image, ImageTk, ImageGrab
import keyboard
import threading
import time
import win32api
import win32con
import win32clipboard
from io import BytesIO

class TabbedShadowClipboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Configuration ---
        self.title("Pro Shadow Clipboard")
        self.attributes("-topmost", True)
        self.overrideredirect(True)
        
        self.width = 380
        self.height = 550
        self.is_visible = False
        self.last_content = None
        self.current_tab = "text"
        self.ignore_next_update = False

        # --- Navbar (Tab Switcher) ---
        self.nav_frame = ctk.CTkFrame(self, fg_color="#1e1e1e", corner_radius=0, height=60)
        self.nav_frame.pack(side="top", fill="x")
        self.nav_frame.pack_propagate(False)

        self.btn_text_tab = ctk.CTkButton(self.nav_frame, text="📑 CLIPS", width=140, height=40,
                                          fg_color="#0e639c", hover_color="#1177bb", font=("Arial", 12, "bold"),
                                          command=lambda: self.show_tab("text"))
        self.btn_text_tab.pack(side="left", padx=(40, 5), pady=10)

        self.btn_img_tab = ctk.CTkButton(self.nav_frame, text="🖼️ PICS", width=140, height=40,
                                         fg_color="#333", hover_color="#444", font=("Arial", 12, "bold"),
                                         command=lambda: self.show_tab("img"))
        self.btn_img_tab.pack(side="left", padx=(5, 40), pady=10)

        # --- Main Screens (Scrollable Pages) ---
        self.text_page = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.img_page = ctk.CTkScrollableFrame(self, fg_color="transparent")
        
        # Start on Clips tab
        self.text_page.pack(padx=10, pady=5, fill="both", expand=True)

        # --- Footer ---
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.pack(side="bottom", fill="x", pady=15)

        self.btn_clear = ctk.CTkButton(footer_frame, text="🗑️ Clear Current View", 
                                       fg_color="#d9534f", hover_color="#c9302c", 
                                       command=self.clear_history)
        self.btn_clear.pack()

        # Hide window on startup
        self.withdraw()

        # --- Background Services ---
        threading.Thread(target=self.clipboard_listener, daemon=True).start()
        keyboard.add_hotkey('alt+v', self.toggle_window)

    def show_tab(self, tab_type):
        """Switches between Text and Image screens."""
        self.current_tab = tab_type
        if tab_type == "text":
            self.img_page.pack_forget()
            self.text_page.pack(padx=10, pady=5, fill="both", expand=True)
            self.btn_text_tab.configure(fg_color="#0e639c")
            self.btn_img_tab.configure(fg_color="#333")
        else:
            self.text_page.pack_forget()
            self.img_page.pack(padx=10, pady=5, fill="both", expand=True)
            self.btn_img_tab.configure(fg_color="#0e639c")
            self.btn_text_tab.configure(fg_color="#333")

    def send_to_clipboard(self, clip_type, data):
        """Copies item back to Windows and prevents the app from re-capturing it."""
        self.ignore_next_update = True 
        
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            if clip_type == win32clipboard.CF_DIB:
                output = BytesIO()
                data.convert("RGB").save(output, "BMP")
                data_bytes = output.getvalue()[14:]
                win32clipboard.SetClipboardData(clip_type, data_bytes)
            else:
                win32clipboard.SetClipboardText(str(data), win32clipboard.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
        except Exception as e:
            print(f"Copy Error: {e}")
        finally:
            try: win32clipboard.CloseClipboard()
            except: pass
        
        self.hide_window()

    def clipboard_listener(self):
        """Monitors clipboard in a separate thread."""
        while True:
            try:
                img = ImageGrab.grabclipboard()
                if isinstance(img, Image.Image):
                    img_id = hash(img.tobytes())
                    if img_id != self.last_content:
                        self.last_content = img_id
                        if self.ignore_next_update:
                            self.ignore_next_update = False
                        else:
                            self.after(0, self.add_to_history, img, "IMAGE")
                else:
                    content = pyperclip.paste()
                    if content and content.strip() and content != self.last_content:
                        self.last_content = content
                        if self.ignore_next_update:
                            self.ignore_next_update = False
                        else:
                            self.after(0, self.add_to_history, content, "TEXT")
            except: pass
            time.sleep(0.4)

    def add_to_history(self, content, type):
        """Creates a new entry in the appropriate tab."""
        target_page = self.text_page if type == "TEXT" else self.img_page
        icon = "📑" if type == "TEXT" else "🖼️"
        copy_type = win32clipboard.CF_UNICODETEXT if type == "TEXT" else win32clipboard.CF_DIB

        item_frame = ctk.CTkFrame(target_page, fg_color="#2b2b2b")
        item_frame.pack(fill="x", pady=4, padx=5, side="top")
        item_frame.tkraise()

        content_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        content_frame.pack(side="left", fill="both", expand=True, padx=10)

        if type == "TEXT":
            display_text = (content[:75] + '...') if len(content) > 75 else content
            ctk.CTkLabel(content_frame, text=display_text, wraplength=200, 
                         justify="left", font=("Consolas", 10)).pack(side="left", pady=12)
        else:
            thumb = content.copy()
            thumb.thumbnail((120, 120))
            img_tk = ImageTk.PhotoImage(thumb)
            lbl = ctk.CTkLabel(content_frame, image=img_tk, text="")
            lbl.image = img_tk 
            lbl.pack(side="left", pady=8)

        # Action Buttons side-by-side
        btn_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        btn_frame.pack(side="right", padx=10)

        ctk.CTkButton(btn_frame, text=icon, width=40, height=35, fg_color="#0e639c", 
                      command=lambda: self.send_to_clipboard(copy_type, content)).pack(side="left", padx=2)
        
        ctk.CTkButton(btn_frame, text="🗑️", width=40, height=35, fg_color="#444", 
                      hover_color="#d9534f", command=item_frame.destroy).pack(side="left", padx=2)

    def toggle_window(self):
        if self.is_visible: self.hide_window()
        else: self.show_window()

    def show_window(self):
        try:
            # Anchor to Bottom Right
            monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromPoint((0,0), win32con.MONITOR_DEFAULTTOPRIMARY))
            work_area = monitor_info['Work']
            x = work_area[2] - self.width - 15
            y = work_area[3] - self.height - 15
            self.geometry(f"{self.width}x{self.height}+{x}+{y}")
            self.deiconify()
            self.lift()
            self.focus_force()
            self.is_visible = True
        except: pass

    def hide_window(self):
        self.withdraw()
        self.is_visible = False

    def clear_history(self):
        """Wipes current tab and flushes Windows clipboard to prevent ghost re-adds."""
        if self.current_tab == "text":
            for child in self.text_page.winfo_children(): child.destroy()
        else:
            for child in self.img_page.winfo_children(): child.destroy()
        
        # Reset memory
        self.last_content = None
        
        # Flush Windows Clipboard
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.CloseClipboard()
        except: pass

if __name__ == "__main__":
    app = TabbedShadowClipboard()
    app.mainloop()