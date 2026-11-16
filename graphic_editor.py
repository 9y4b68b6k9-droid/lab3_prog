import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox


class DrawingApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Графический редактор — Лабораторная №3")
        self.root.geometry("800x600")

        self.current_color: str = "black"
        self.brush_size: int = 5
        self.last_x: int | None = None
        self.last_y: int | None = None
        self.is_drawing: bool = False

        self._create_menu()
        self._create_toolbar()
        self._create_canvas()
        self._bind_events()

    def _create_menu(self) -> None:
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Сохранить как...", command=self.save_image)
        file_menu.add_command(label="Загрузить...", command=self.load_image)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        menubar.add_cascade(label="Файл", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Очистить холст", command=self.clear_canvas)
        edit_menu.add_command(label="Выбрать цвет...", command=self.choose_color)
        menubar.add_cascade(label="Правка", menu=edit_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="О программе", command=self.show_about)
        menubar.add_cascade(label="Справка", menu=help_menu)

        self.root.config(menu=menubar)

    def _create_toolbar(self) -> None:
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.color_btn = tk.Button(
            toolbar,
            text="Цвет",
            bg=self.current_color,
            width=8,
            command=self.choose_color
        )
        self.color_btn.pack(side=tk.LEFT, padx=5, pady=2)

        tk.Label(toolbar, text="Толщина:").pack(side=tk.LEFT, padx=(10, 2))

        self.size_var = tk.IntVar(value=self.brush_size)
        size_spin = tk.Spinbox(
            toolbar,
            from_=1,
            to=20,
            textvariable=self.size_var,
            width=5,
            command=self._update_brush_size
        )
        size_spin.pack(side=tk.LEFT, padx=2, pady=2)

        tk.Button(
            toolbar,
            text="Очистить",
            command=self.clear_canvas
        ).pack(side=tk.LEFT, padx=10, pady=2)

    def _create_canvas(self) -> None:
        self.canvas = tk.Canvas(self.root, bg="white", cursor="pencil")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self._on_resize)

    def _bind_events(self) -> None:
        self.canvas.bind("<ButtonPress-1>", self._on_mouse_press)
        self.canvas.bind("<B1-Motion>", self._on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_mouse_release)

    def _on_mouse_press(self, event: tk.Event) -> None:
        self.is_drawing = True
        self.last_x = event.x
        self.last_y = event.y

    def _on_mouse_drag(self, event: tk.Event) -> None:
        if not self.is_drawing:
            return
        try:
            self.canvas.create_line(
                self.last_x, self.last_y,
                event.x, event.y,
                fill=self.current_color,
                width=self.brush_size,
                capstyle=tk.ROUND,
                smooth=True
            )
            self.last_x = event.x
            self.last_y = event.y
        except tk.TclError as e:
            messagebox.showerror("Ошибка рисования", f"Не удалось нарисовать линию: {e}")
            self.is_drawing = False

    def _on_mouse_release(self, event: tk.Event) -> None:
        self.is_drawing = False
        self.last_x = None
        self.last_y = None

    def _on_resize(self, event: tk.Event) -> None:
        pass

    def _update_brush_size(self) -> None:
        try:
            self.brush_size = self.size_var.get()
        except tk.TclError:
            self.brush_size = 3

    def choose_color(self) -> None:
        color = colorchooser.askcolor(title="Выберите цвет кисти")
        if color[1] is not None:
            self.current_color = color[1]
            self.color_btn.config(bg=self.current_color)

    def clear_canvas(self) -> None:
        try:
            self.canvas.delete("all")
            self.canvas.config(bg=self.current_color)
        except tk.TclError as e:
            messagebox.showerror("Ошибка", f"Не удалось очистить холст: {e}")

    def save_image(self) -> None:
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".ps",
                filetypes=[("PostScript files", "*.ps"), ("All files", "*.*")]
            )
            if not file_path:
                return
            self.canvas.postscript(file=file_path)
            messagebox.showinfo("Сохранено", f"Файл сохранён:\n{file_path}")
        except PermissionError:
            messagebox.showerror("Ошибка доступа", "Нет прав на запись в выбранную папку.")
        except OSError as e:
            messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить файл:\n{e}")
        except Exception as e:
            messagebox.showerror("Неизвестная ошибка", f"Что-то пошло не так:\n{e}")

    def load_image(self) -> None:
        messagebox.showinfo(
            "Загрузка",
            "Tkinter Canvas не поддерживает загрузку PostScript обратно.\n"
            "Этот метод можно расширить с помощью Pillow (PIL)."
        )

    def show_about(self) -> None:
        messagebox.showinfo(
            "О программе",
            "Графический редактор\n"
            "Лабораторная работа №3\n"
            "Вариант 10: рисование курсором мыши\n\n"
            "Технологии: Python, Tkinter, Git"
        )


def main() -> None:
    try:
        root = tk.Tk()
        app = DrawingApp(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Критическая ошибка", f"Программа не может запуститься:\n{e}")


if __name__ == "__main__":
    main()