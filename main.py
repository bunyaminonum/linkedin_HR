from info import GetInfo
import tkinter as tk
from tkinter import messagebox

class LinkedInScraperGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("LinkedIn Scraper")

        # Ekran boyutunu al
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Pencere boyutunu ve konumunu ayarla
        window_width = 400
        window_height = 200
        window_x = (screen_width - window_width) // 2
        window_y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

        # Padding ayarları
        self.root.configure(padx=50, pady=50)

        # Giriş bilgileri etiketleri ve giriş kutuları
        email_label = tk.Label(self.root, text="Email:")
        email_label.pack()

        self.email_entry = tk.Entry(self.root, width=30)
        self.email_entry.pack()

        password_label = tk.Label(self.root, text="Password:")
        password_label.pack()

        self.password_entry = tk.Entry(self.root, show="*", width=30)
        self.password_entry.pack()

        # Başlat düğmesi
        self.start_button = tk.Button(self.root, text="Başlat", command=self.start_scraper, state="disabled")
        self.start_button.pack()

        # Entry kutuları izleme
        self.email_entry.bind("<KeyRelease>", self.check_entry_fields)
        self.password_entry.bind("<KeyRelease>", self.check_entry_fields)

    def check_entry_fields(self, event):
        # Giriş kutularının boş olup olmadığını kontrol et
        email = self.email_entry.get()
        password = self.password_entry.get()

        if email and password:
            self.start_button.config(state="normal")
        else:
            self.start_button.config(state="disabled")

    def start_scraper(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            tk.messagebox.showerror("Hata", "Email ve password alanı boş olamaz!")
            return

        # LinkedIn Scraper nesnesini oluştur
        scraper = GetInfo(email, password)

        # İşlemi başlat
        scraper.start()

        # İşlem tamamlandığında bilgi mesajı göster
        tk.messagebox.showinfo("LinkedIn Scraper", "Scraper tamamlandı!")

    def run(self):
        self.root.mainloop()


# Uygulamayı çalıştır
if __name__ == "__main__":
    gui = LinkedInScraperGUI()
    gui.run()
