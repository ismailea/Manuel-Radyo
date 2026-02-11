import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import itertools

class RLCVeritabani:
    def __init__(self):
        self.baglanti = sqlite3.connect("rlc_envanter.db")
        self.cursor = self.baglanti.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS envanter 
            (id INTEGER PRIMARY KEY, tip TEXT, deger REAL, adet INTEGER)
        """)
        self.baglanti.commit()

    def envanter_getir(self, tip):
        self.cursor.execute("SELECT deger, adet FROM envanter WHERE tip = ? AND adet > 0", (tip,))
        return {row[0]: row[1] for row in self.cursor.fetchall()}

    def stok_guncelle(self, tip, deger, miktar):
        self.cursor.execute("SELECT adet FROM envanter WHERE tip = ? AND deger = ?", (tip, deger))
        if self.cursor.fetchone():
            self.cursor.execute("UPDATE envanter SET adet = adet + ? WHERE tip = ? AND deger = ?", (miktar, tip, deger))
        else:
            self.cursor.execute("INSERT INTO envanter (tip, deger, adet) VALUES (?, ?, ?)", (tip, deger, miktar))
        self.baglanti.commit()

class RLCApp:
    def __init__(self, root):
        self.db = RLCVeritabani()
        self.root = root
        self.root.title("Hassas RLC Envanter Çözücü")
        self.root.geometry("500x700")
        self.root.configure(padx=15, pady=15)

        # --- GİRİŞ PANELİ ---
        tk.Label(root, text="BİLEŞEN VE HEDEF", font=('Arial', 10, 'bold')).pack()
        
        self.combo_tip = ttk.Combobox(root, values=["Direnç (Ω)", "Kondansatör (µF)", "Bobin (mH)"], state="readonly")
        self.combo_tip.current(0); self.combo_tip.pack(pady=5)

        tk.Label(root, text="Hedef Değer:").pack()
        self.ent_hedef = tk.Entry(root, font=('Arial', 12)); self.ent_hedef.pack(pady=5)

        # --- TOLERANS AYARI ---
        tk.Label(root, text="Kabul Edilebilir Hata Payı (%):").pack()
        self.scale_tolerans = tk.Scale(root, from_=1, to=20, orient=tk.HORIZONTAL)
        self.scale_tolerans.set(5); self.scale_tolerans.pack(fill=tk.X, pady=5)

        tk.Button(root, text="KOMBİNASYON ARA", command=self.hesapla, bg="#34495e", fg="white", height=2).pack(fill=tk.X, pady=10)
        
        # --- SONUÇ PANELİ ---
        self.lbl_sonuc = tk.Label(root, text="Sonuç burada görünecek...", font=('Arial', 10, 'italic'), 
                                 bg="#ecf0f1", height=4, wraplength=400, relief=tk.GROOVE)
        self.lbl_sonuc.pack(fill=tk.X, pady=10)

        self.btn_kullan = tk.Button(root, text="BU KOMBİNASYONU KULLAN", state=tk.DISABLED, 
                                   command=self.stoktan_dus, bg="#27ae60", fg="white")
        self.btn_kullan.pack(fill=tk.X)

        # --- STOK YÖNETİMİ ---
        tk.Label(root, text="\nSTOK EKLEME", font=('Arial', 10, 'bold')).pack()
        frame_stok = tk.Frame(root)
        frame_stok.pack(pady=5)
        
        tk.Label(frame_stok, text="Değer:").grid(row=0, column=0)
        self.ent_ekle_val = tk.Entry(frame_stok, width=10); self.ent_ekle_val.grid(row=0, column=1, padx=5)
        
        tk.Label(frame_stok, text="Adet:").grid(row=0, column=2)
        self.ent_ekle_adet = tk.Entry(frame_stok, width=10); self.ent_ekle_adet.grid(row=0, column=3, padx=5)
        
        tk.Button(root, text="Envantere Kaydet", command=self.stok_ekle).pack(pady=5)

        self.son_kombinasyon = []

    def hesapla(self):
        try:
            hedef = float(self.ent_hedef.get())
            tolerans_yuzde = self.scale_tolerans.get() / 100
            tip_secili = self.combo_tip.get().split(" ")[0]
            envanter = self.db.envanter_getir(tip_secili)
            
            flat_list = []
            for d, a in envanter.items(): flat_list.extend([d] * a)
            
            en_yakin_fark = float('inf')
            en_iyi_cozum = None

            # Kombinasyonları dene (Tekli ve İkili)
            for n in [1, 2]:
                for kombo in set(itertools.combinations(flat_list, n)):
                    if n == 1:
                        deger, tarif = kombo[0], f"{kombo[0]} Ω (Tekli)"
                        self.test_ve_kaydet(deger, hedef, tolerans_yuzde, tarif, [kombo[0]])
                    else:
                        r1, r2 = kombo
                        if tip_secili in ["Direnç", "Bobin"]:
                            s, p = r1 + r2, (r1 * r2) / (r1 + r2)
                            self.test_ve_kaydet(s, hedef, tolerans_yuzde, f"{r1} + {r2} Seri", [r1, r2])
                            self.test_ve_kaydet(p, hedef, tolerans_yuzde, f"{r1} // {r2} Paralel", [r1, r2])
                        else: # Kondansatör
                            p, s = r1 + r2, (r1 * r2) / (r1 + r2)
                            self.test_ve_kaydet(p, hedef, tolerans_yuzde, f"{r1} // {r2} Paralel", [r1, r2])
                            self.test_ve_kaydet(s, hedef, tolerans_yuzde, f"{r1} + {r2} Seri", [r1, r2])

            if self.en_iyi_fark <= hedef * tolerans_yuzde:
                hata_yuzde = (self.en_iyi_fark / hedef) * 100
                self.lbl_sonuc.config(text=f"ÇÖZÜM: {self.en_iyi_tarif}\nSapma: %{hata_yuzde:.2f}", fg="green")
                self.btn_kullan.config(state=tk.NORMAL)
            else:
                self.lbl_sonuc.config(text="Belirlenen tolerans dahilinde\nuygun kombinasyon bulunamadı!", fg="red")
                self.btn_kullan.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Hata", "Lütfen değerleri kontrol edin!")

    en_iyi_fark = float('inf')
    en_iyi_tarif = ""
    def test_ve_kaydet(self, deger, hedef, tolerans, tarif, bilesenler):
        fark = abs(deger - hedef)
        if fark < self.en_iyi_fark:
            self.en_iyi_fark = fark
            self.en_iyi_tarif = f"{tarif} = {deger:.2f}"
            self.son_kombinasyon = bilesenler

    # Diğer metodlar (stok_ekle, stoktan_dus) önceki kodla aynı...
    def stok_ekle(self):
        try:
            tip = self.combo_tip.get().split(" ")[0]
            self.db.stok_guncelle(tip, float(self.ent_ekle_val.get()), int(self.ent_ekle_adet.get()))
            messagebox.showinfo("Başarılı", "Kayıt eklendi.")
        except: messagebox.showerror("Hata", "Giriş hatalı.")

    def stoktan_dus(self):
        tip = self.combo_tip.get().split(" ")[0]
        for d in self.son_kombinasyon: self.db.stok_guncelle(tip, d, -1)
        messagebox.showinfo("Tamam", "Stok güncellendi.")
        self.btn_kullan.config(state=tk.DISABLED)
        self.en_iyi_fark = float('inf') # Reset

if __name__ == "__main__":
    root = tk.Tk(); app = RLCApp(root); root.mainloop()