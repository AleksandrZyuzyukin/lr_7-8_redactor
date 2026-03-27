import tkinter as tk
from tkinter import filedialog, messagebox


class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Простой текстовый редактор")
        self.root.geometry("800x600")

        self.file_path = None

        self.create_widgets()
        self.create_menu()

    def create_widgets(self):
        self.text_area = tk.Text(self.root, wrap="word", undo=True, font=("Arial", 12))
        self.text_area.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(self.text_area)
        scrollbar.pack(side="right", fill="y")

        self.text_area.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text_area.yview)

    def create_menu(self):
        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Новый", command=self.new_file)
        file_menu.add_command(label="Открыть", command=self.open_file)
        file_menu.add_command(label="Сохранить", command=self.save_file)
        file_menu.add_command(label="Сохранить как", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.exit_editor)

        menu_bar.add_cascade(label="Файл", menu=file_menu)
        self.root.config(menu=menu_bar)

    def new_file(self):
        if self.confirm_save():
            self.text_area.delete(1.0, tk.END)
            self.file_path = None
            self.root.title("Простой текстовый редактор - Новый файл")

    def open_file(self):
        if not self.confirm_save():
            return

        path = filedialog.askopenfilename(
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        if path:
            try:
                with open(path, "r", encoding="utf-8") as file:
                    content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
                self.file_path = path
                self.root.title(f"Простой текстовый редактор - {path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть файл:\n{e}")

    def save_file(self):
        if self.file_path:
            try:
                with open(self.file_path, "w", encoding="utf-8") as file:
                    file.write(self.text_area.get(1.0, tk.END))
                messagebox.showinfo("Сохранение", "Файл успешно сохранён.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{e}")
        else:
            self.save_file_as()

    def save_file_as(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        if path:
            try:
                with open(path, "w", encoding="utf-8") as file:
                    file.write(self.text_area.get(1.0, tk.END))
                self.file_path = path
                self.root.title(f"Простой текстовый редактор - {path}")
                messagebox.showinfo("Сохранение", "Файл успешно сохранён.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{e}")

    def confirm_save(self):
        content = self.text_area.get(1.0, tk.END).strip()
        if content:
            answer = messagebox.askyesnocancel("Сохранение", "Сохранить текущий файл?")
            if answer is None:
                return False
            if answer:
                self.save_file()
        return True

    def exit_editor(self):
        if self.confirm_save():
            self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditor(root)
    root.mainloop()