import tkinter as tk
from tkinter import messagebox, ttk
import math

class AyarliKapasitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mekatronik Kondansatör Atölyesi")
        self.root.geometry("550x750")
        self.root.configure(padx=20, pady=20)

        # Başlık
        tk.Label(root, text="HEDEF ODAKLI KONDANSATÖR TASARIMI", font=('Arial', 12, 'bold'), fg="#16a085").pack(pady=10)

        # --- GİRİŞ PANELİ ---
        frame_input = tk.LabelFrame(root, text=" Tasarım Hedefleri ", padx=15, pady=15)
        frame_input.pack(fill="x", pady=10)

        # Hedef Kapasite
        tk.Label(frame_input, text="Hedef Maks. Kapasite (pF):").grid(row=0, column=0, sticky="w")
        self.ent_target_pf = tk.Entry(frame_input); self.ent_target_pf.insert(0, "100"); self.ent_target_pf.grid(row=0, column=1, pady=5)

        # Plaka Sayısı (Kullanıcı kaç plaka kesmeye üşenmez?)
        tk.Label(frame_input, text="Kullanılacak Plaka Sayısı:").grid(row=1, column=0, sticky="w")
        self.ent_n = tk.Entry(frame_input); self.ent_n.insert(0, "4"); self.ent_n.grid(row=1, column=1, pady=5)

        # Plakalar Arası Boşluk
        tk.Label(frame_input, text="Plakalar Arası Boşluk (d - mm):").grid(row=2, column=0, sticky="w")
        self.ent_d = tk.Entry(frame_input); self.ent_d.insert(0, "1.0"); self.ent_d.grid(row=2, column=1, pady=5)

        # Yalıtkan
        tk.Label(frame_input, text="Araya Ne Koyacaksın? (Yalıtkan):").grid(row=3, column=0, sticky="w")
        self.dielektrikler = {"Hava (Boşluk)": 1.0, "İnce Dosya Kağıdı": 3.7, "PVC Bant / Plastik": 3.0}
        self.combo_mat = ttk.Combobox(frame_input, values=list(self.dielektrikler.keys()), state="readonly")
        self.combo_mat.current(0); self.combo_mat.grid(row=3, column=1, pady=5)

        # --- HESAPLA BUTONU ---
        tk.Button(root, text="YAPIM KILAVUZUNU OLUŞTUR", command=self.hesapla_tersine, 
                  bg="#2c3e50", fg="white", font=('Arial', 10, 'bold'), height=2).pack(fill="x", pady=15)

        # --- ÇIKTI REHBERİ ---
        self.txt_rehber = tk.Text(root, height=20, font=('Courier', 10), bg="#fdfefe", padx=10, pady=10)
        self.txt_rehber.pack(fill="x")

    def hesapla_tersine(self):
        try:
            target_pf = float(self.ent_target_pf.get())
            n = int(self.ent_n.get())
            d_mm = float(self.ent_d.get())
            k = self.dielektrikler[self.combo_mat.get()]

            if n < 2: raise ValueError("En az 2 plaka (1 sabit, 1 hareketli) gereklidir.")

            # Sabitler
            epsilon_0 = 8.854e-12
            d_m = d_mm / 1000
            target_f = target_pf * 1e-12

            # Formül: C = (epsilon_0 * k * A * (n-1)) / d
            # A (alan_m2) = (C * d) / (epsilon_0 * k * (n-1))
            alan_m2 = (target_f * d_m) / (epsilon_0 * k * (n - 1))
            alan_mm2 = alan_m2 * 1_000_000

            # Yarım daire yarıçapı: A = (pi * r^2) / 2  => r = sqrt(2A / pi)
            r = math.sqrt((2 * alan_mm2) / math.pi)

            rehber = (
                f"{' YAPIM KILAVUZU: ' + str(target_pf) + ' pF ':=^40}\n\n"
                f"1. ADIM (MALZEMELER):\n"
                f"- Toplam {n} adet alüminyum plaka kesin.\n"
                f"- Plaka Yarıçapı: {round(r, 1)} mm olmalı.\n"
                f"- Mil olarak bir adet M3-M4 vida/somun seti.\n\n"
                f"2. ADIM (HESAP DETAYI):\n"
                f"- Plaka Sayısı: {n} ({n//2} Sabit, {n - n//2} Hareketli)\n"
                f"- Plaka Aralığı: {d_mm} mm (Pul/Rondela ile ayarla)\n"
                f"- Yalıtkan: {self.combo_mat.get()}\n\n"
                f"3. ADIM (MONTAJ):\n"
                f"- Sabit plakaları gövdeye paralel dizin.\n"
                f"- Dönen plakaları mil üzerine dizin.\n"
                f"- Plakalar birbirine ASLA değmemeli.\n"
                f"- Plakalar tam iç içeyken kapasite: {target_pf} pF\n"
                f"- Plakalar tamamen açıkken kapasite: ~3-8 pF\n\n"
                f"{' RADYO İPUCU ':-^40}\n"
                f"Eğer {round(r,1)} mm çok büyük gelirse,\n"
                f"plaka sayısını (N) artırarak çapı\n"
                f"küçültebilirsiniz."
            )

            self.txt_rehber.config(state="normal")
            self.txt_rehber.delete(1.0, tk.END)
            self.txt_rehber.insert(tk.END, rehber)
            self.txt_rehber.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Hata", f"Hatalı giriş: {e}")

if __name__ == "__main__":
    root = tk.Tk(); app = AyarliKapasitorApp(root); root.mainloop()