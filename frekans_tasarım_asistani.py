import tkinter as tk
from tkinter import messagebox, ttk
import math

class RadyoTersineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Radyo İstasyonu Tasarım Asistanı")
        self.root.geometry("550x750")
        self.root.configure(padx=20, pady=20)

        # Başlık
        tk.Label(root, text="FREKANSTAN KONDANSATÖRE TASARIM", font=('Arial', 12, 'bold'), fg="#27ae60").pack(pady=10)

        # --- GİRİŞ PANELİ ---
        frame_input = tk.LabelFrame(root, text=" Hedef İstasyon ve Mevcut Bobin ", padx=15, pady=15)
        frame_input.pack(fill="x", pady=10)

        tk.Label(frame_input, text="Hedef Frekans Değeri:").grid(row=0, column=0, sticky="w")
        self.ent_freq = tk.Entry(frame_input); self.ent_freq.insert(0, "103.1"); self.ent_freq.grid(row=0, column=1, pady=5)
        
        self.combo_birim = ttk.Combobox(frame_input, values=["MHz (FM Bandı)", "kHz (MW/Orta Dalga)"], state="readonly", width=15)
        self.combo_birim.current(0); self.combo_birim.grid(row=0, column=2, padx=5)

        tk.Label(frame_input, text="Elimdeki Bobin (L - µH):").grid(row=1, column=0, sticky="w")
        self.ent_l = tk.Entry(frame_input); self.ent_l.insert(0, "1.5"); self.ent_l.grid(row=1, column=1, pady=5)

        # --- FİZİKSEL KISITLAMALAR ---
        tk.Label(frame_input, text="Plaka Sayısı (N):").grid(row=2, column=0, sticky="w")
        self.ent_n = tk.Entry(frame_input); self.ent_n.insert(0, "2"); self.ent_n.grid(row=2, column=1, pady=5)

        tk.Label(frame_input, text="Plaka Arası Boşluk (mm):").grid(row=3, column=0, sticky="w")
        self.ent_d = tk.Entry(frame_input); self.ent_d.insert(0, "0.5"); self.ent_d.grid(row=3, column=1, pady=5)

        # --- BUTON ---
        tk.Button(root, text="İSTASYONU YAKALAYACAK PLAKAYI TASARLA", command=self.hesapla, 
                  bg="#2c3e50", fg="white", font=('Arial', 10, 'bold'), height=2).pack(fill="x", pady=15)

        # --- SONUÇ REHBERİ ---
        self.txt_sonuc = tk.Text(root, height=18, font=('Courier', 10), bg="#f4f6f7", padx=10, pady=10)
        self.txt_sonuc.pack(fill="x")

    def hesapla(self):
        try:
            # 1. Frekanstan Kapasite (C) bulma: C = 1 / (4 * pi^2 * f^2 * L)
            f_val = float(self.ent_freq.get())
            if "MHz" in self.combo_birim.get():
                f = f_val * 1e6
            else:
                f = f_val * 1e3
            
            L = float(self.ent_l.get()) * 1e-6
            
            # Rezonans formülünden C çekilir
            C_farad = 1 / (4 * (math.pi**2) * (f**2) * L)
            C_pf = C_farad * 1e12

            # 2. Kapasiteden Plaka Çapı bulma
            n = int(self.ent_n.get())
            d_mm = float(self.ent_d.get())
            epsilon_0 = 8.854e-12
            d_m = d_mm / 1000
            
            # Alan: A = (C * d) / (epsilon_0 * (n-1))
            alan_m2 = (C_farad * d_m) / (epsilon_0 * (n - 1))
            alan_mm2 = alan_m2 * 1e6
            r = math.sqrt((2 * alan_mm2) / math.pi)

            res = (
                f"{' İSTASYON YAKALAMA PLANI ':=^40}\n\n"
                f"• Hedef İstasyon    : {f_val} {self.combo_birim.get().split(' ')[0]}\n"
                f"• Gereken Kapasite  : {round(C_pf, 2)} pF\n\n"
                f"{' PLAKA ÖLÇÜLERİ ':-^40}\n"
                f"• Plaka Yarıçapı    : {round(r, 2)} mm\n"
                f"• Toplam Plaka      : {n} Adet\n"
                f"• Plaka Aralığı     : {d_mm} mm\n\n"
                f"NOT: Bu frekansı yakalamak için\n"
                f"plakalar tam iç içeyken bu ölçülerde\n"
                f"olmalıdır. Plakaları çevirdikçe\n"
                f"diğer kanallara geçebilirsiniz."
            )
            self.txt_sonuc.config(state="normal")
            self.txt_sonuc.delete(1.0, tk.END)
            self.txt_sonuc.insert(tk.END, res)
            self.txt_sonuc.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Hata", "Lütfen değerleri kontrol edin. Bobin değeri frekans için çok küçük veya büyük olabilir.")

if __name__ == "__main__":
    root = tk.Tk(); app = RadyoTersineApp(root); root.mainloop()