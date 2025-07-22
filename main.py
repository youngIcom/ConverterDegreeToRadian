import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import re
import math
import threading
from PIL import Image, ImageTk

class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lua Motion Converter")
        self.root.geometry("700x550")
        self.root.resizable(False, False)

        # Variabel untuk menyimpan path file
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()

        # --- Memuat Ikon ---
        self.icon_convert = self.create_icon("icons/B7.png", (40, 40))

        # --- Membuat Frame Utama ---
        main_frame = ttk.Frame(self.root, padding="25")
        main_frame.pack(fill=BOTH, expand=YES)

        # --- Logo di Kiri Judul --
        logo_frame = ttk.Frame(main_frame)
        logo_frame.pack(fill=X, pady=(0, 25))

        logo_label = ttk.Label(logo_frame, image=self.icon_convert)
        logo_label.pack(side=LEFT, padx=(0, 10))

        # --- Judul Aplikasi ---
        header = ttk.Label(logo_frame, text="Converter Lua (to Radian)", font=("Helvetica", 24, "bold"), bootstyle=PRIMARY)
        header.pack(side=LEFT)

        # --- Frame untuk Input & Output ---
        io_frame = ttk.Frame(main_frame)
        io_frame.pack(fill=X, pady=10)

        # --- Bagian File Input ---
        input_frame = ttk.Frame(io_frame)
        input_frame.pack(fill=X, expand=YES, pady=5)
        
        self.input_entry = ttk.Entry(input_frame, textvariable=self.input_path, font=("Helvetica", 11), state="readonly")
        self.input_entry.pack(side=LEFT, fill=X, expand=YES, padx=(0, 10))

        input_button = ttk.Button(input_frame, text=" Pilih File Input", compound=LEFT, command=self.pilih_file_input, bootstyle=(SUCCESS, OUTLINE))
        input_button.pack(side=LEFT)

        # --- Bagian File Output ---
        output_frame = ttk.Frame(io_frame)
        output_frame.pack(fill=X, expand=YES, pady=5)

        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_path, font=("Helvetica", 11), state="readonly")
        self.output_entry.pack(side=LEFT, fill=X, expand=YES, padx=(0, 10))

        output_button = ttk.Button(output_frame, text=" Simpan Hasil Ke", compound=LEFT, command=self.pilih_file_output, bootstyle=(SUCCESS, OUTLINE))
        output_button.pack(side=LEFT)

        # --- Tombol Konversi Utama ---
        self.convert_button = ttk.Button(main_frame, text="  KONVERSI SEKARANG", compound=LEFT, command=self.mulai_konversi, state="disabled", bootstyle=SUCCESS, padding=10)
        self.convert_button.pack(fill=X, pady=(20, 10))
        
        # --- Progress Bar ---
        self.progress_bar = ttk.Progressbar(main_frame, mode='indeterminate', bootstyle=(STRIPED, SUCCESS))
        self.progress_bar.pack(fill=X, pady=5)

        # --- Area Status / Log ---
        log_frame = ttk.LabelFrame(main_frame, text=" Log Aktivitas ", padding="10", bootstyle=INFO)
        log_frame.pack(fill=BOTH, expand=YES, pady=10)
        
        self.log_text = tk.Text(log_frame, height=8, state="disabled", wrap="word", font=("Courier New", 10), relief="flat")
        self.log_text.pack(fill=BOTH, expand=YES)
        self.log_text.tag_config("sukses", foreground="#00e676") # Hijau terang
        self.log_text.tag_config("error", foreground="#ff5252")  # Merah terang
        self.log_text.tag_config("info", foreground="#ff6b00")  # Biru terang

    def create_icon(self, path, size):
        """Mencoba memuat ikon dari file, jika gagal, buat ikon placeholder."""
        try:
            img = Image.open(path)
            img = img.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except FileNotFoundError:
            img = Image.new('RGBA', size, (0, 0, 0, 0))
            return ImageTk.PhotoImage(img)

    def log(self, message, tag=None):
        self.root.after(0, self._log_threadsafe, message, tag)

    def _log_threadsafe(self, message, tag):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, f"[ {threading.current_thread().name[:5]} ] {message}\n", tag)
        self.log_text.config(state="disabled")
        self.log_text.see(tk.END)

    def periksa_tombol_konversi(self):
        if self.input_path.get() and self.output_path.get():
            self.convert_button.config(state="normal")
        else:
            self.convert_button.config(state="disabled")

    def pilih_file_input(self):
        file_path = filedialog.askopenfilename(title="Pilih file tarian Lua", filetypes=[("Lua files", "*.lua")])
        if file_path:
            self.input_path.set(file_path)
            self.log(f"File input: {file_path}", "info")
            self.periksa_tombol_konversi()

    def pilih_file_output(self):
        file_path = filedialog.asksaveasfilename(title="Simpan file hasil konversi", defaultextension=".lua", filetypes=[("Lua files", "*.lua")])
        if file_path:
            self.output_path.set(file_path)
            self.log(f"File output: {file_path}", "info")
            self.periksa_tombol_konversi()
    
    def mulai_konversi(self):
        self.convert_button.config(state="disabled")
        self.progress_bar.start()
        self.log("\nMemulai proses konversi...", "info")
        thread = threading.Thread(target=self.proses_konversi, name="Worker", daemon=True)
        thread.start()

    def proses_konversi(self):
        try:
            with open(self.input_path.get(), "r") as f:
                content = f.read()
            frames = self._parse_frames(content)
            if not frames:
                raise ValueError("Format tidak sesuai. Tidak ada data 'angles' atau 'duration' yang ditemukan.")
            with open(self.output_path.get(), "w") as outfile:
                outfile.write("-- File ini dihasilkan oleh Premium Lua Motion Converter\n")
                outfile.write("local mot={};\nmot.servos={13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,};\nmot.keyframes = {\n")


                # rumus konversi dari derajat ke radian dimuat disini
                for frame in frames:
                    duration = frame["duration"]
                    angles_in_degrees = frame["angles"]
                    angles_in_radians = [angle * math.pi / 180 for angle in angles_in_degrees]
                    output_string = f"  {{\n    {duration}, -- duration\n{self._table_to_string(angles_in_radians)}\n  }},"
                    outfile.write(output_string + "\n")
                outfile.write("}\n\nreturn mot;\n")
            self.log("KONVERSI BERHASIL!", "sukses")
            self.root.after(100, lambda: messagebox.showinfo("Sukses", "Konversi file berhasil diselesaikan!"))
        except Exception as e:
            error_message = f"GAGAL: {e}"
            self.log(error_message, "error")
            self.root.after(100, lambda: messagebox.showerror("Error", error_message))
        finally:
            self.root.after(100, self._konversi_selesai)

    def _konversi_selesai(self):
        self.progress_bar.stop()
        self.convert_button.config(state="normal")

    def _parse_frames(self, content):
        pattern = re.compile(r"angles\s*=\s*vector\.new\(\s*\{([^\}]*)\}\)\s*\*\s*math\.pi\s*/\s*180\s*,\s*duration\s*=\s*([0-9\.]+)", re.MULTILINE)
        frames = []
        for angles_str, duration_str in pattern.findall(content):
            angles = [float(num) for num in re.findall(r'[-+]?\d*\.\d+|[-+]?\d+', angles_str)]
            duration = float(duration_str)
            frames.append({"duration": duration, "angles": angles})
        return frames

    def _table_to_string(self, tbl):
        result = "  {\n"
        for i, value in enumerate(tbl, 1):
            result += f"    {value:.10f},"
            if i % 5 == 0:
                result += "\n"
        if len(tbl) % 5 != 0:
            result += "\n"
        result += "  }"
        return result

if __name__ == "__main__":
    # Ganti 'superhero' dengan tema lain jika suka, misal:
    # 'litera', 'cosmo', 'flatly', 'journal', 'lumen', 'minty', 'pulse', 'sandstone', 'united', 'yeti'
    # 'cyborg', 'darkly', 'solar', 'superhero' (Tema Gelap)
    root = ttk.Window(themename="solar")
    app = ConverterApp(root)
    root.mainloop()