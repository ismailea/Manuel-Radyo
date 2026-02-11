import tkinter as tk
from tkinter import messagebox, ttk
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class ManuelRadyoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Manuel Radyo: El Yapımı RF Atölyesi")
        self.root.geometry("600x500")
        self.root.configure(padx=20, pady=20)

        # Başlık ve Karşılama
        tk.Label(root, text="MANUEL RADYO", font=('Arial', 18, 'bold'), fg="#e67e22").pack(pady=5)
        tk.Label(root, text="Hassas RF Tasarım ve Tamir Paneli", font=('Arial', 10, 'italic')).pack(pady=10)

        # Menü Çerçevesi
        btn_frame = tk.Frame(root)
        btn_frame.pack(expand=True)

        # --- BUTONLAR (Modüller) ---
        # 1. RLC ve Envanter
        tk.Button(btn_frame, text="📦 RLC Envanter & Kombinasyon", width=35, height=2, 
                  command=self.ac_rlc, bg="#34495e", fg="white").grid(row=0, column=0, padx=10, pady=10)

        # 2. Bobin Tasarımı
        tk.Button(btn_frame, text="🌀 Akıllı Bobin Tasarımı (Kalem Odaklı)", width=35, height=2, 
                  command=self.ac_bobin, bg="#2980b9", fg="white").grid(row=1, column=0, padx=10, pady=10)

        # 3. Kondansatör Tasarımı
        tk.Button(btn_frame, text="🛸 Ayarlı Kondansatör Atölyesi", width=35, height=2, 
                  command=self.ac_kapasitor, bg="#16a085", fg="white").grid(row=2, column=0, padx=10, pady=10)

        # 4. Şablon Üretici
        tk.Button(btn_frame, text="📄 PDF Şablon & Cetvel Üretici", width=35, height=2, 
                  command=self.ac_sablon, bg="#8e44ad", fg="white").grid(row=3, column=0, padx=10, pady=10)

        # Alt Bilgi
        tk.Label(root, text="Babana sevgilerle... | Pardus RF Edition", font=('Arial', 8), fg="gray").pack(side="bottom")

    # Modül Pencere Fonksiyonları (Önceki kodları bu fonksiyonların içine yerleştirebilirsin)
    def ac_rlc(self):
        messagebox.showinfo("Modül", "RLC Envanter Modülü Başlatılıyor...")
        # Buraya RLCApp sınıfını çağırabilirsin

    def ac_bobin(self):
        messagebox.showinfo("Modül", "Akıllı Bobin Tasarımcısı Başlatılıyor...")
        # Buraya AkilliBobinApp sınıfını çağırabilirsin

    def ac_kapasitor(self):
        messagebox.showinfo("Modül", "Kondansatör Atölyesi Başlatılıyor...")

    def ac_sablon(self):
        messagebox.showinfo("Modül", "Hassas Şablon Üretici Başlatılıyor...")

if __name__ == "__main__":
    root = tk.Tk()
    app = ManuelRadyoApp(root)
    root.mainloop()