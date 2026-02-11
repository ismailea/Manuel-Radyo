import tkinter as tk
from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

class SablonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pardus Hassas Şablon Atölyesi")
        self.root.geometry("450x550")
        self.root.configure(padx=20, pady=20)

        # Başlık
        tk.Label(root, text="KAĞIT ŞABLON ÜRETİCİ", font=('Arial', 14, 'bold'), fg="#2980b9").pack(pady=10)

        # --- GİRİŞLER ---
        frame_in = tk.LabelFrame(root, text=" Ölçüleri Girin (mm) ", padx=15, pady=15)
        frame_in.pack(fill="x", pady=10)

        tk.Label(frame_in, text="Plaka Yarıçapı (r):").grid(row=0, column=0, sticky="w")
        self.ent_r = tk.Entry(frame_in); self.ent_r.insert(0, "40"); self.ent_r.grid(row=0, column=1, pady=5)

        tk.Label(frame_in, text="Tel Çapı (w):").grid(row=1, column=0, sticky="w")
        self.ent_w = tk.Entry(frame_in); self.ent_w.insert(0, "0.5"); self.ent_w.grid(row=1, column=1, pady=5)

        tk.Label(frame_in, text="Bobin Tur Sayısı (N):").grid(row=2, column=0, sticky="w")
        self.ent_n = tk.Entry(frame_in); self.ent_n.insert(0, "42"); self.ent_n.grid(row=2, column=1, pady=5)

        tk.Label(frame_in, text="Kalem/Nüve Çapı (D):").grid(row=3, column=0, sticky="w")
        self.ent_d = tk.Entry(frame_in); self.ent_d.insert(0, "7.2"); self.ent_d.grid(row=3, column=1, pady=5)

        # --- BUTON ---
        tk.Button(root, text="PDF ŞABLONU OLUŞTUR", command=self.pdf_uret, 
                  bg="#27ae60", fg="white", font=('Arial', 11, 'bold'), height=2).pack(fill="x", pady=20)

        tk.Label(root, text="* Not: PDF'i yazdırırken 'Ölçeklendirme Yok'\nveya '%100' seçeneğini işaretlemeyi unutmayın!", 
                 font=('Arial', 9, 'italic'), fg="red").pack()

    def pdf_uret(self):
        try:
            r = float(self.ent_r.get())
            w = float(self.ent_w.get())
            n = int(self.ent_n.get())
            D = float(self.ent_d.get())

            # A4 Boyutlarında Çizim Alanı
            fig, ax = plt.subplots(figsize=(8.27, 11.69))
            ax.set_xlim(0, 210)
            ax.set_ylim(0, 297)
            ax.set_aspect('equal')
            ax.axis('off')

            # 1. KONDANSATÖR PLAKASI (Üst Kısım)
            ax.text(20, 270, "1. AYARLI KONDANSATÖR PLAKA ŞABLONU", fontweight='bold')
            wedge = patches.Wedge((105, 230), r, 0, 180, fill=False, edgecolor='black', linewidth=1.2)
            ax.add_patch(wedge)
            # Mil Deliği
            ax.add_patch(plt.Circle((105, 230), 1.5, fill=False, color='red', linestyle='--'))
            ax.text(105, 230 - r - 10, f"Yarıçap: {r}mm", ha='center')

            # 2. BOBİN SARIM CETVELİ (Alt Kısım - Kaleme Sarılacak Kağıt)
            ax.text(20, 150, "2. BOBİN SARIM VE TEL ÇAPI REHBERİ", fontweight='bold')
            # Kalem çevresi kadar uzunluk
            cevre = math.pi * D
            boy = n * w
            
            # Rehber Dikdörtgen (Kalem üzerine sarılacak parça)
            rect = patches.Rectangle((20, 60), cevre, boy, fill=False, edgecolor='blue', linestyle='-')
            ax.add_patch(rect)
            
            # Tur Çizgileri
            for i in range(n + 1):
                y_pos = 60 + (i * w)
                ax.plot([20, 20 + cevre], [y_pos, y_pos], color='blue', linewidth=0.3)

            ax.text(20, 50, f"Kalem Çevresi: {cevre:.1f}mm | Toplam Tur: {n} | Boy: {boy:.1f}mm", fontsize=8)
            ax.text(20, 35, "* Bu mavi parçayı kesin ve kaleme sarın. Çizgiler üzerinden teli sararak kusursuz bobin yapın.", fontsize=7, color='gray')

            # Çıktı Al
            file_path = "Atolye_Sablonu.pdf"
            plt.savefig(file_path, dpi=300)
            plt.close()
            messagebox.showinfo("Başarılı", f"Şablon '{file_path}' adıyla kaydedildi.\nBunu yazdırıp kesebilirsiniz!")

        except Exception as e:
            messagebox.showerror("Hata", f"Değerleri kontrol edin: {e}")

if __name__ == "__main__":
    import math
    root = tk.Tk(); app = SablonApp(root); root.mainloop()