import tkinter as tk
from tkinter import messagebox, ttk
import math

class AkilliBobinApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mekatronik Bobin Tasarım Asistanı")
        self.root.geometry("550x750")
        self.root.configure(padx=20, pady=20)

        # --- TASARIM MODU SEÇİMİ ---
        self.mod = tk.StringVar(value="duz") # 'duz' veya 'ters'
        
        tk.Label(root, text="TASARIM MODU", font=('Arial', 10, 'bold')).pack()
        frame_mod = tk.Frame(root)
        frame_mod.pack(pady=5)
        tk.Radiobutton(frame_mod, text="Çapa Göre Tur Hesapla", variable=self.mod, value="duz", command=self.arayuz_guncelle).grid(row=0, column=0, padx=10)
        tk.Radiobutton(frame_mod, text="Tura Göre Çap Öner (Akıllı)", variable=self.mod, value="ters", command=self.arayuz_guncelle).grid(row=0, column=1, padx=10)

        # --- GİRİŞ PANELİ ---
        self.frame_input = tk.LabelFrame(root, text=" Parametreler ", padx=15, pady=15)
        self.frame_input.pack(fill="x", pady=10)

        # Hedef Endüktans her iki modda da var
        tk.Label(self.frame_input, text="Hedef Endüktans (µH):").grid(row=0, column=0, sticky="w")
        self.ent_l = tk.Entry(self.frame_input); self.ent_l.insert(0, "15.0"); self.ent_l.grid(row=0, column=1, pady=5)

        tk.Label(self.frame_input, text="Tel Çapı (mm):").grid(row=1, column=0, sticky="w")
        self.ent_w = tk.Entry(self.frame_input); self.ent_w.insert(0, "0.5"); self.ent_w.grid(row=1, column=1, pady=5)

        # Dinamik Alanlar
        self.lbl_degisken = tk.Label(self.frame_input, text="Nüve Çapı (mm):")
        self.lbl_degisken.grid(row=2, column=0, sticky="w")
        self.ent_degisken = tk.Entry(self.frame_input); self.ent_degisken.insert(0, "7.2"); self.ent_degisken.grid(row=2, column=1, pady=5)

        # --- BUTON VE SONUÇ ---
        tk.Button(root, text="TASARLA", command=self.hesapla, bg="#2980b9", fg="white", font=('Arial', 11, 'bold'), height=2).pack(fill="x", pady=15)

        self.txt_sonuc = tk.Text(root, height=15, font=('Courier', 10), bg="#f8f9f9", padx=10, pady=10)
        self.txt_sonuc.pack(fill="x")

    def arayuz_guncelle(self):
        if self.mod.get() == "duz":
            self.lbl_degisken.config(text="Nüve Çapı (mm):")
            self.ent_degisken.delete(0, tk.END); self.ent_degisken.insert(0, "7.2")
        else:
            self.lbl_degisken.config(text="İstediğim Maks. Tur:")
            self.ent_degisken.delete(0, tk.END); self.ent_degisken.insert(0, "30")

    def hesapla(self):
        try:
            L = float(self.ent_l.get())
            W = float(self.ent_w.get())
            val = float(self.ent_degisken.get())
            
            self.txt_sonuc.config(state="normal")
            self.txt_sonuc.delete(1.0, tk.END)

            if self.mod.get() == "duz":
                # Klasik hesaplama (Önceki algoritmamız)
                n, boy = self.tur_bul(L, W, val)
                mesaj = f"SONUÇ (Çapa Göre):\n{'-'*30}\n• Tur Sayısı: {round(n,1)} tur\n• Bobin Boyu: {round(boy,2)} mm\n"
                if n > 60:
                    mesaj += "\n[!] UYARI: Tur sayısı çok yüksek! \nUsanmamak için daha kalın bir nüve deneyin."
            else:
                # Akıllı Çap Önerisi
                cap = self.cap_bul(L, W, val)
                mesaj = f"AKILLI ÖNERİ (Tura Göre):\n{'-'*30}\n"
                mesaj += f"• {val} turda {L} µH almak için \n  gereken çap: {round(cap, 2)} mm\n\n"
                mesaj += "Bu çapa en yakın malzemeler:\n"
                if cap < 10: mesaj += "- Kurşun Kalem (~7mm)\n- Matkap Ucu"
                elif cap < 16: mesaj += "- AA Pil (~14.5mm)\n- İşaretleme Kalemi"
                else: mesaj += "- 1/2 inç PVC Boru (~21mm)\n- Su borusu"

            self.txt_sonuc.insert(tk.END, mesaj)
            self.txt_sonuc.config(state="disabled")
        except:
            messagebox.showerror("Hata", "Lütfen değerleri kontrol edin.")

    def tur_bul(self, L, W, D):
        n = 1.0
        for _ in range(1000):
            l = n * W
            yeni_n = math.sqrt(L * (457 * D + 1016 * l)) / D
            if abs(yeni_n - n) < 0.001: break
            n = yeni_n
        return n, n * W

    def cap_bul(self, L, W, N):
        # Wheeler formülünden D'yi (çap) çekmek: 
        # L = (D^2 * N^2) / (457D + 1016*N*W) -> İkinci dereceden denklem oluşur
        # D^2 * N^2 - 457*L*D - 1016*L*N*W = 0
        a = N**2
        b = -457 * L
        c = -1016 * L * N * W
        
        # Diskriminant: b^2 - 4ac
        delta = b**2 - 4 * a * c
        D = (-b + math.sqrt(delta)) / (2 * a)
        return D

if __name__ == "__main__":
    root = tk.Tk(); app = AkilliBobinApp(root); root.mainloop()