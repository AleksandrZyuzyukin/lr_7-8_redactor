import tkinter as tk
from tkinter import filedialog, messagebox


class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")

        self.file_path = None
        self.is_modified = False
        self.text_change_in_progress = False

        self.create_widgets()
        self.create_menu()
        self.bind_shortcuts()
        self.update_title()

        self.text_area.edit_modified(False)
        self.text_area.bind("<<Modified>>", self.on_text_modified)
        self.root.protocol("WM_DELETE_WINDOW", self.exit_editor)

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        self.text_area = tk.Text(
            frame,
            wrap="word",
            undo=True,
            font=("Arial", 12),
            yscrollcommand=scrollbar.set
        )
        self.text_area.pack(fill="both", expand=True)

        scrollbar.config(command=self.text_area.yview)

    def create_menu(self):
        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Новый\tCtrl+N", command=self.new_file)
        file_menu.add_command(label="Открыть...\tCtrl+O", command=self.open_file)
        file_menu.add_command(label="Сохранить\tCtrl+S", command=self.save_file)
        file_menu.add_command(label="Сохранить как...\tCtrl+Shift+S", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Выход\tCtrl+Q", command=self.exit_editor)

        menu_bar.add_cascade(label="Файл", menu=file_menu)
        self.root.config(menu=menu_bar)

    def bind_shortcuts(self):
        self.root.bind("<Control-n>", self.new_file_event)
        self.root.bind("<Control-o>", self.open_file_event)
        self.root.bind("<Control-s>", self.save_file_event)
        self.root.bind("<Control-S>", self.save_file_as_event)
        self.root.bind("<Control-Q>", self.exit_editor_event)
        self.root.bind("<Control-q>", self.exit_editor_event)

    def update_title(self):
        file_name = self.file_path if self.file_path else "Без имени"
        mark = "*" if self.is_modified else ""
        self.root.title(f"{mark}Простой текстовый редактор - {file_name}")

    def on_text_modified(self, event=None):
        if self.text_change_in_progress:
            self.text_area.edit_modified(False)
            return

        if self.text_area.edit_modified():
            self.is_modified = True
            self.update_title()
            self.text_area.edit_modified(False)

    def set_text_content(self, content):
        self.text_change_in_progress = True
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert("1.0", content)
        self.text_area.edit_modified(False)
        self.text_change_in_progress = False

    def get_text_content(self):
        return self.text_area.get("1.0", tk.END + "-1c")

    def confirm_save_if_needed(self):
        if not self.is_modified:
            return True

        answer = messagebox.askyesnocancel(
            "Несохранённые изменения",
            "Документ содержит несохранённые изменения.\nСохранить перед продолжением?"
        )

        if answer is None:
            return False

        if answer:
            return self.save_file()

        return True

    def new_file(self):
        if not self.confirm_save_if_needed():
            return

        self.set_text_content("")
        self.file_path = None
        self.is_modified = False
        self.update_title()

    def open_file(self):
        if not self.confirm_save_if_needed():
            return

        path = filedialog.askopenfilename(
            title="Открыть файл",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )

        if not path:
            return

        try:
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()

            self.set_text_content(content)
            self.file_path = path
            self.is_modified = False
            self.update_title()

        except Exception as e:
            messagebox.showerror("Ошибка открытия", f"Не удалось открыть файл:\n{e}")

    def save_file(self):
        if self.file_path:
            try:
                with open(self.file_path, "w", encoding="utf-8") as file:
                    file.write(self.get_text_content())

                self.is_modified = False
                self.update_title()
                return True

            except Exception as e:
                messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить файл:\n{e}")
                return False

        return self.save_file_as()

    def save_file_as(self):
        path = filedialog.asksaveasfilename(
            title="Сохранить как",
            defaultextension=".txt",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )

        if not path:
            return False

        try:
            with open(path, "w", encoding="utf-8") as file:
                file.write(self.get_text_content())

            self.file_path = path
            self.is_modified = False
            self.update_title()
            return True

        except Exception as e:
            messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить файл:\n{e}")
            return False

    def exit_editor(self):
        if self.confirm_save_if_needed():
            self.root.destroy()

    def new_file_event(self, event):
        self.new_file()
        return "break"

    def open_file_event(self, event):
        self.open_file()
        return "break"

    def save_file_event(self, event):
        self.save_file()
        return "break"

    def save_file_as_event(self, event):
        self.save_file_as()
        return "break"

    def exit_editor_event(self, event):
        self.exit_editor()
        return "break"


if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditor(root)
    root.mainloop()