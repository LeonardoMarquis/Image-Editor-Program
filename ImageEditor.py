import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

import Manager
import Filters


class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Imagens - Lab. Programação")
        self.root.geometry("1100x750")
        self.root.configure(bg="#FFFFFF")

        self.original_path = None
        self.editing_image = None
        self.image_preview = None
        self.downloader = Manager.Download()

        self.filters = {
            "Gray Scale": Filters.GrayFilter(),
            "Black and White": Filters.BlackWhiteFilter(),
            "Negative": Filters.NegativeFilter(),
            "Blur": Filters.BlurredFilter(),
            "Contour": Filters.ContourFilter(),
            "Cartoon": Filters.CartoonFilter()
        }

        self.build_screen()

    def build_screen(self):
        # ===== TOP BAR =====
        top_frame = tk.Frame(self.root, bg="#EAF2FF", pady=10)
        top_frame.pack(fill="x")

        tk.Button(
            top_frame,
            text="Open Local File",
            command=self.local_search,
            bg="#1E90FF",
            fg="white",
            activebackground="#1873CC",
            relief="flat"
        ).pack(side="left", padx=10)

        tk.Label(
            top_frame,
            text="Or URL:",
            bg="#EAF2FF",
            fg="#1E90FF"
        ).pack(side="left")

        self.entry_url = tk.Entry(top_frame, width=40)
        self.entry_url.pack(side="left", padx=5)

        tk.Button(
            top_frame,
            text="Download",
            command=self.url_download,
            bg="#1E90FF",
            fg="white",
            activebackground="#1873CC",
            relief="flat"
        ).pack(side="left", padx=5)

        self.save_btn = tk.Button(
            top_frame,
            text="Save Final Image",
            command=self.disk_save,
            state="disabled",
            bg="#FFF3B0",
            fg="#333333",
            relief="flat"
        )
        self.save_btn.pack(side="right", padx=10)

        # ===== MAIN AREA =====
        main_frame = tk.Frame(self.root, bg="#FFFFFF")
        main_frame.pack(expand=True, fill="both")

        # ===== SIDEBAR =====
        sidebar = tk.Frame(main_frame, width=220, bg="#F5F5F5", padx=10, pady=10)
        sidebar.pack(side="left", fill="y")

        tk.Label(
            sidebar,
            text="Filters",
            font=("Arial", 13, "bold"),
            bg="#F5F5F5",
            fg="#1E90FF"
        ).pack(pady=10)

        for name, obj in self.filters.items():
            tk.Button(
                sidebar,
                text=name,
                width=18,
                command=lambda f=obj: self.generate_preview(f),
                bg="#FFFFFF",
                fg="#1E90FF",
                activebackground="#EAF2FF",
                relief="flat"
            ).pack(pady=4)

        self.confirm_btn = tk.Button(
            sidebar,
            text="Confirm Filter",
            command=self.confirm_filter,
            state="disabled",
            bg="#FFF3B0",
            fg="#333333",
            relief="flat",
            width=18
        )
        self.confirm_btn.pack(pady=25)

        # ===== IMAGE AREA =====
        self.image_frame = tk.Frame(main_frame, bg="#EAF2FF")
        self.image_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        self.lbl_imagem = tk.Label(
            self.image_frame,
            text="No image loaded",
            bg="#EAF2FF",
            fg="#1E90FF",
            font=("Arial", 14)
        )
        self.lbl_imagem.pack(expand=True)

    # ========= FUNCTIONS (sem mudanças) =========

    def display_on_screen(self, pil_img):
        max_width, max_height = 850, 550
        img_copy = pil_img.copy()
        img_copy.thumbnail((max_width, max_height))

        img_tk = ImageTk.PhotoImage(img_copy)
        self.lbl_imagem.configure(image=img_tk, text="")
        self.lbl_imagem.image = img_tk

    def carregar_imagem(self, image_path):
        try:
            Manager.Image(image_path)
            self.original_path = image_path
            self.editing_image = Image.open(image_path)
            self.image_preview = None

            self.display_on_screen(self.editing_image)
            self.save_btn.config(state="normal")
            self.confirm_btn.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def local_search(self):
        image_path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png")])
        if image_path:
            self.carregar_imagem(image_path)

    def url_download(self):
        url = self.entry_url.get()
        if not url:
            return

        try:
            self.root.config(cursor="wait")
            self.root.update()

            image_path = self.downloader.download_img(url)
            self.carregar_imagem(image_path)

        except Exception as e:
            messagebox.showerror("Download Error", str(e))
        finally:
            self.root.config(cursor="")

    def generate_preview(self, filtro_obj):
        if not self.editing_image:
            return

        try:
            self.root.config(cursor="wait")
            self.root.update()

            self.editing_image.save("temp.png")
            result_image = filtro_obj.simple_process("temp.png")

            self.image_preview = result_image
            self.display_on_screen(result_image)

            self.confirm_btn.config(state="normal")

        except Exception as e:
            messagebox.showerror("Filter Error!", str(e))
        finally:
            self.root.config(cursor="")

    def confirm_filter(self):
        if self.image_preview:
            self.editing_image = self.image_preview
            self.image_preview = None
            self.confirm_btn.config(state="disabled")
            messagebox.showinfo("Filter applied", "Filter applied successfully!")

    def disk_save(self):
        if not self.editing_image:
            return

        image_path = filedialog.asksaveasfilename(defaultextension=".jpg")
        if image_path:
            self.editing_image.save(image_path)
            messagebox.showinfo("Saved", "Image successfully saved!")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()
