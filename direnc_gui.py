import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# --- VERİTABANI SINIFI ---
class Veritabani:
    def __init__(self):
        self.baglanti = sqlite3.connect("direncler.db")
        self.cursor = self.baglanti.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS envanter 
            (id INTEGER PRIMARY KEY, deger REAL, adet INTEGER)
        """)
        self.baglanti.commit()

    def envanter_getir(self):
        self.cursor.execute("SELECT deger, adet FROM envanter WHERE adet > 0")
        return {row[0]: row[1] for row in self.cursor.fetchall()}

    def stok_guncelle(self, deger, miktar):
        self.cursor.execute("UPDATE envanter SET adet = adet + ? WHERE deger = ?", (miktar, deger))
        # Eğer kayıt yoksa yeni ekle
        if self.cursor.rowcount == 0:
            self.cursor.execute("INSERT INTO envanter (deger, adet) VALUES (?, ?)", (deger, miktar))
        self.baglanti.commit()

# --- ANA UYGULAMA ARAYÜZÜ ---
class DirencApp:
    def __init__(self, root):
        self.db = Veritabani()
        self.root = root
        self.root.title("Direnç Hesaplayıcı & Envanter")
        self.root.geometry("450x550")
        
        # Arayüz Elemanları
        tk.Label(root, text="HEDEF DİRENÇ (Ohm):", font=('Arial', 10, 'bold')).pack(pady=5)
        self.ent_hedef = tk.Entry(root, font=('Arial', 12))
        self.ent_hedef.pack(pady=5)

        tk.Button(root, text="HESAPLA", command=self.hesapla, bg="#2c3e50", fg="white").pack(pady=10)

        self.lbl_sonuc = tk.Label(root, text="Öneri: -", font=('Arial', 11), fg="blue", wraplength=400)
        self.lbl_sonuc.pack(pady=20)

        self.btn_kullan = tk.Button(root, text="BU KOMBİNASYONU KULLAN (Stoktan Düş)", 
                                   state=tk.DISABLED, command=self.stoktan_dus, bg="#27ae60", fg="white")
        self.btn_kullan.pack(pady=5)

        tk.Frame(root, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, pady=20)

        # Envanter Ekleme Kısmı
        tk.Label(root, text="ENVANTERE EKLE", font=('Arial', 10, 'bold')).pack()
        tk.Label(root, text="Değer (Ohm):").pack()
        self.ent_ekle_val = tk.Entry(root)
        self.ent_ekle_val.pack()
        tk.Label(root, text="Adet:").pack()
        self.ent_ekle_adet = tk.Entry(root)
        self.ent_ekle_adet.pack()
        tk.Button(root, text="Stoka Ekle", command=self.stok_ekle).pack(pady=10)

        self.son_kullanilanlar = []

    def hesapla(self):
        try:
            hedef = float(self.ent_hedef.get())
            envanter = self.db.envanter_getir()
            
            # Basit Seri/Paralel Algoritması
            en_yakin_fark = float('inf')
            en_iyi_tarif = ""
            self.son_kullanilanlar = []

            flat_list = []
            for d, a in envanter.items(): flat_list.extend([d] * a)

            # İkili kombinasyonları tara
            import itertools
            for kombo in set(itertools.combinations(flat_list, 2)):
                r1, r2 = kombo
                # Seri
                s = r1 + r2
                if abs(s - hedef) < en_yakin_fark:
                    en_yakin_fark = abs(s - hedef)
                    en_iyi_tarif = f"{r1} + {r2} Seri Bağlantı (Toplam: {s} Ohm)"
                    self.son_kullanilanlar = [r1, r2]
                # Paralel
                p = (r1 * r2) / (r1 + r2)
                if abs(p - hedef) < en_yakin_fark:
                    en_yakin_fark = abs(p - hedef)
                    en_iyi_tarif = f"{r1} // {r2} Paralel Bağlantı (Toplam: {p:.2f} Ohm)"
                    self.son_kullanilanlar = [r1, r2]

            self.lbl_sonuc.config(text=f"ÖNERİ:\n{en_iyi_tarif}")
            self.btn_kullan.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Hata", "Lütfen geçerli bir sayı girin!")

    def stok_ekle(self):
        try:
            val = float(self.ent_ekle_val.get())
            adet = int(self.ent_ekle_adet.get())
            self.db.stok_guncelle(val, adet)
            messagebox.showinfo("Başarılı", f"{val} Ohm stok güncellendi.")
        except:
            messagebox.showerror("Hata", "Giriş değerlerini kontrol edin.")

    def stoktan_dus(self):
        for d in self.son_kullanilanlar:
            self.db.stok_guncelle(d, -1)
        messagebox.showinfo("Bilgi", "Seçilen dirençler stoktan düşüldü.")
        self.btn_kullan.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = DirencApp(root)
    root.mainloop()