import calendar
from datetime import date, datetime
import tkinter as tk
from tkinter import messagebox, ttk

try:
    import plant
except ModuleNotFoundError:
    plant = None


DATE_FORMAT = "%Y-%m-%d"


class ScrollableFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.canvas = tk.Canvas(
            self,
            bg="#eef5ee",
            highlightthickness=0,
            bd=0,
        )
        self.scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview,
        )
        self.content = ttk.Frame(self.canvas, style="App.TFrame")

        self.window_id = self.canvas.create_window(
            (0, 0),
            window=self.content,
            anchor="nw",
        )
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.content.bind("<Configure>", self._update_scroll_region)
        self.canvas.bind("<Configure>", self._update_content_width)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _update_scroll_region(self, _event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _update_content_width(self, event):
        self.canvas.itemconfigure(self.window_id, width=event.width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


class DatePicker(tk.Toplevel):
    def __init__(self, parent, date_var):
        super().__init__(parent)
        self.date_var = date_var
        self.selected_date = self.get_initial_date()
        self.year = self.selected_date.year
        self.month = self.selected_date.month

        self.title("اختيار التاريخ")
        self.configure(bg="#ffffff")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.build_calendar()
        self.update_idletasks()
        self.center_over_parent(parent)

    def get_initial_date(self):
        try:
            return datetime.strptime(self.date_var.get(), DATE_FORMAT).date()
        except ValueError:
            return date.today()

    def center_over_parent(self, parent):
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        width = self.winfo_width()
        height = self.winfo_height()
        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")

    def build_calendar(self):
        for child in self.winfo_children():
            child.destroy()

        wrapper = tk.Frame(self, bg="#ffffff", padx=14, pady=14)
        wrapper.pack(fill="both", expand=True)

        header = tk.Frame(wrapper, bg="#ffffff")
        header.pack(fill="x", pady=(0, 10))

        tk.Button(
            header,
            text="<",
            command=self.previous_month,
            bg="#e7f0e8",
            fg="#17351f",
            relief="flat",
            width=4,
            font=("Segoe UI", 11, "bold"),
        ).pack(side="left")

        title = f"{calendar.month_name[self.month]} {self.year}"
        tk.Label(
            header,
            text=title,
            bg="#ffffff",
            fg="#17351f",
            font=("Segoe UI", 13, "bold"),
        ).pack(side="left", expand=True)

        tk.Button(
            header,
            text=">",
            command=self.next_month,
            bg="#e7f0e8",
            fg="#17351f",
            relief="flat",
            width=4,
            font=("Segoe UI", 11, "bold"),
        ).pack(side="right")

        days_frame = tk.Frame(wrapper, bg="#ffffff")
        days_frame.pack()

        day_names = ["Sat", "Fri", "Thu", "Wed", "Tue", "Mon", "Sun"]
        for column, day_name in enumerate(day_names):
            tk.Label(
                days_frame,
                text=day_name,
                bg="#ffffff",
                fg="#5b7161",
                width=5,
                font=("Segoe UI", 9, "bold"),
            ).grid(row=0, column=column, padx=2, pady=2)

        month_days = calendar.Calendar(firstweekday=5).monthdayscalendar(
            self.year,
            self.month,
        )
        today = date.today()

        for row_index, week in enumerate(month_days, start=1):
            for column_index, day_number in enumerate(week):
                if day_number == 0:
                    tk.Label(days_frame, text="", bg="#ffffff", width=5).grid(
                        row=row_index,
                        column=column_index,
                        padx=2,
                        pady=2,
                    )
                    continue

                current_date = date(self.year, self.month, day_number)
                is_today = current_date == today
                is_selected = current_date == self.selected_date
                bg_color = "#287346" if is_selected else "#dcebe0" if is_today else "#f6faf6"
                fg_color = "#ffffff" if is_selected else "#17351f"

                tk.Button(
                    days_frame,
                    text=str(day_number),
                    command=lambda picked=current_date: self.pick_date(picked),
                    bg=bg_color,
                    fg=fg_color,
                    activebackground="#cfe2d3",
                    activeforeground="#17351f",
                    relief="flat",
                    width=5,
                    font=("Segoe UI", 10),
                ).grid(row=row_index, column=column_index, padx=2, pady=2)

        footer = tk.Frame(wrapper, bg="#ffffff")
        footer.pack(fill="x", pady=(12, 0))

        tk.Button(
            footer,
            text="اليوم",
            command=lambda: self.pick_date(date.today()),
            bg="#e7f0e8",
            fg="#17351f",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=12,
            pady=6,
        ).pack(side="right", padx=(6, 0))

        tk.Button(
            footer,
            text="إغلاق",
            command=self.destroy,
            bg="#fff3f0",
            fg="#9c2e1f",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=12,
            pady=6,
        ).pack(side="right")

    def previous_month(self):
        self.month -= 1
        if self.month == 0:
            self.month = 12
            self.year -= 1
        self.build_calendar()

    def next_month(self):
        self.month += 1
        if self.month == 13:
            self.month = 1
            self.year += 1
        self.build_calendar()

    def pick_date(self, picked_date):
        self.date_var.set(picked_date.strftime(DATE_FORMAT))
        self.destroy()


class PlantCareGUI:
    def __init__(self, root):
        self.root = root
        self.selected_name = None

        self.name_var = tk.StringVar()
        self.interval_var = tk.StringVar()
        self.watered_var = tk.StringVar(value=self.today())
        self.fertilized_var = tk.StringVar(value=self.today())
        self.search_var = tk.StringVar()
        self.status_var = tk.StringVar(value="جاهز")

        self.configure_window()
        self.configure_styles()
        self.build_ui()
        self.load_data()
        self.refresh_table()

    def configure_window(self):
        self.root.title("Plant Care")
        self.root.geometry("1080x680")
        self.root.minsize(900, 560)
        self.root.configure(bg="#eef5ee")

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("App.TFrame", background="#eef5ee")
        style.configure("Card.TFrame", background="#ffffff", relief="flat")
        style.configure("Toolbar.TFrame", background="#e1eee3")

        style.configure(
            "Title.TLabel",
            background="#eef5ee",
            foreground="#17351f",
            font=("Segoe UI", 24, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background="#eef5ee",
            foreground="#52705a",
            font=("Segoe UI", 11),
        )
        style.configure(
            "Field.TLabel",
            background="#ffffff",
            foreground="#26382b",
            font=("Segoe UI", 10, "bold"),
        )
        style.configure(
            "Small.TLabel",
            background="#ffffff",
            foreground="#63766a",
            font=("Segoe UI", 9),
        )
        style.configure(
            "Status.TLabel",
            background="#e1eee3",
            foreground="#314d39",
            font=("Segoe UI", 10),
        )

        style.configure(
            "TEntry",
            fieldbackground="#f8fbf8",
            foreground="#1d2d22",
            bordercolor="#c7d9cb",
            lightcolor="#c7d9cb",
            darkcolor="#c7d9cb",
            padding=8,
        )

        style.configure(
            "TButton",
            font=("Segoe UI", 10, "bold"),
            padding=(10, 8),
            background="#f4f8f4",
            foreground="#223529",
            bordercolor="#c7d9cb",
        )
        style.map(
            "TButton",
            background=[("active", "#e2eee4"), ("pressed", "#d2e3d6")],
        )

        style.configure(
            "Primary.TButton",
            background="#287346",
            foreground="#ffffff",
            bordercolor="#287346",
        )
        style.map(
            "Primary.TButton",
            background=[("active", "#205f39"), ("pressed", "#194d2f")],
            foreground=[("active", "#ffffff")],
        )

        style.configure(
            "Danger.TButton",
            background="#fff3f0",
            foreground="#9c2e1f",
            bordercolor="#efc7bf",
        )
        style.map("Danger.TButton", background=[("active", "#ffe3de")])

        style.configure(
            "Treeview",
            background="#ffffff",
            foreground="#243629",
            fieldbackground="#ffffff",
            bordercolor="#d7e4da",
            rowheight=34,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Treeview.Heading",
            background="#dcebe0",
            foreground="#1f3d2b",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
        )
        style.map(
            "Treeview",
            background=[("selected", "#2d7d4f")],
            foreground=[("selected", "#ffffff")],
        )

    def build_ui(self):
        page = ScrollableFrame(self.root)
        page.pack(fill="both", expand=True)

        container = ttk.Frame(page.content, style="App.TFrame", padding=22)
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=0)
        container.rowconfigure(2, weight=1)

        self.build_header(container)
        self.build_toolbar(container)
        self.build_table(container)
        self.build_form(container)

    def build_header(self, parent):
        header = ttk.Frame(parent, style="App.TFrame")
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 16))

        ttk.Label(
            header,
            text="متابعة النباتات",
            style="Title.TLabel",
            anchor="e",
        ).pack(fill="x")
        ttk.Label(
            header,
            text="واجهة مرتبة لإدارة السقاية والتسميد من ملف plant.py",
            style="Subtitle.TLabel",
            anchor="e",
        ).pack(fill="x", pady=(4, 0))

    def build_toolbar(self, parent):
        toolbar = ttk.Frame(parent, style="Toolbar.TFrame", padding=12)
        toolbar.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 14))
        toolbar.columnconfigure(0, weight=1)

        search = ttk.Entry(
            toolbar,
            textvariable=self.search_var,
            justify="right",
            font=("Segoe UI", 11),
        )
        search.grid(row=0, column=0, sticky="ew", padx=(10, 0))
        search.insert(0, "")
        search.bind("<KeyRelease>", lambda _event: self.refresh_table())

        ttk.Button(
            toolbar,
            text="تحديث القائمة",
            command=self.reload_data,
        ).grid(row=0, column=1, padx=(10, 0))

        ttk.Button(
            toolbar,
            text="تنبيهات اليوم",
            style="Primary.TButton",
            command=self.show_today_alerts,
        ).grid(row=0, column=2)

        ttk.Label(
            toolbar,
            textvariable=self.status_var,
            style="Status.TLabel",
            anchor="e",
        ).grid(row=1, column=0, columnspan=3, sticky="ew", pady=(8, 0))

    def build_table(self, parent):
        table_card = ttk.Frame(parent, style="Card.TFrame", padding=12)
        table_card.grid(row=2, column=0, sticky="nsew", padx=(0, 16))
        table_card.rowconfigure(0, weight=1)
        table_card.columnconfigure(0, weight=1)

        columns = (
            "watering_status",
            "fertilizer_status",
            "interval",
            "fertilized",
            "watered",
            "name",
        )
        self.tree = ttk.Treeview(
            table_card,
            columns=columns,
            show="headings",
            selectmode="browse",
        )

        headings = {
            "name": "اسم النبات",
            "watered": "آخر سقاية",
            "fertilized": "آخر تسميد",
            "interval": "فاصل السقاية",
            "fertilizer_status": "حالة التسميد",
            "watering_status": "حالة السقاية",
        }
        widths = {
            "name": 180,
            "watered": 125,
            "fertilized": 125,
            "interval": 105,
            "fertilizer_status": 135,
            "watering_status": 135,
        }

        for column in columns:
            self.tree.heading(column, text=headings[column])
            self.tree.column(column, width=widths[column], minwidth=90, anchor="center")

        y_scroll = ttk.Scrollbar(table_card, orient="vertical", command=self.tree.yview)
        x_scroll = ttk.Scrollbar(table_card, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

        self.tree.tag_configure("needs", background="#fff1ed")
        self.tree.tag_configure("ok", background="#f2fbf4")
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.tree.bind("<MouseWheel>", self.on_tree_mousewheel)

    def build_form(self, parent):
        form_card = ttk.Frame(parent, style="Card.TFrame", padding=18)
        form_card.grid(row=2, column=1, sticky="ns")

        self.add_field(form_card, "اسم النبات", self.name_var, 0)
        self.add_field(form_card, "السقاية كل كام يوم", self.interval_var, 1)
        self.add_date_field(form_card, "آخر سقاية", self.watered_var, 2)
        self.add_date_field(form_card, "آخر تسميد", self.fertilized_var, 3)

        ttk.Label(
            form_card,
            text="صيغة التاريخ: YYYY-MM-DD",
            style="Small.TLabel",
            anchor="e",
        ).grid(row=8, column=0, sticky="ew", pady=(0, 12))

        ttk.Button(
            form_card,
            text="إضافة نبات",
            style="Primary.TButton",
            command=self.add_plant_from_form,
        ).grid(row=9, column=0, sticky="ew", pady=4)
        ttk.Button(
            form_card,
            text="تعديل المحدد",
            command=self.edit_selected_plant,
        ).grid(row=10, column=0, sticky="ew", pady=4)
        ttk.Button(
            form_card,
            text="حذف المحدد",
            style="Danger.TButton",
            command=self.delete_selected_plant,
        ).grid(row=11, column=0, sticky="ew", pady=4)

        ttk.Separator(form_card).grid(row=12, column=0, sticky="ew", pady=14)

        ttk.Button(
            form_card,
            text="تحديث السقاية لليوم",
            command=self.mark_watered_today,
        ).grid(row=13, column=0, sticky="ew", pady=4)
        ttk.Button(
            form_card,
            text="تحديث التسميد لليوم",
            command=self.mark_fertilized_today,
        ).grid(row=14, column=0, sticky="ew", pady=4)
        ttk.Button(
            form_card,
            text="مسح الحقول",
            command=self.clear_form,
        ).grid(row=15, column=0, sticky="ew", pady=(14, 4))

    def add_field(self, parent, label, variable, index):
        row = index * 2
        ttk.Label(
            parent,
            text=label,
            style="Field.TLabel",
            anchor="e",
        ).grid(row=row, column=0, sticky="ew", pady=(0, 5))
        ttk.Entry(
            parent,
            textvariable=variable,
            width=28,
            justify="right",
            font=("Segoe UI", 11),
        ).grid(row=row + 1, column=0, sticky="ew", pady=(0, 13))

    def add_date_field(self, parent, label, variable, index):
        row = index * 2
        ttk.Label(
            parent,
            text=label,
            style="Field.TLabel",
            anchor="e",
        ).grid(row=row, column=0, sticky="ew", pady=(0, 5))

        date_row = ttk.Frame(parent, style="Card.TFrame")
        date_row.grid(row=row + 1, column=0, sticky="ew", pady=(0, 13))
        date_row.columnconfigure(0, weight=1)

        ttk.Entry(
            date_row,
            textvariable=variable,
            width=20,
            justify="right",
            font=("Segoe UI", 11),
        ).grid(row=0, column=0, sticky="ew", padx=(8, 0))

        ttk.Button(
            date_row,
            text="📅",
            width=4,
            command=lambda: self.open_date_picker(variable),
        ).grid(row=0, column=1)

    def open_date_picker(self, variable):
        DatePicker(self.root, variable)

    def load_data(self):
        if plant is None:
            messagebox.showerror(
                "ملف plant.py غير موجود",
                "حط ملف plant.py في نفس فولدر main.py ثم شغل البرنامج مرة تانية.",
            )
            return

        if hasattr(plant, "load_plants"):
            plant.load_plants()

    def reload_data(self):
        self.load_data()
        self.refresh_table()
        self.status_var.set("تم تحديث القائمة")

    def get_plants(self):
        if plant is None:
            return []
        return getattr(plant, "plants", [])

    def today(self):
        return datetime.now().strftime(DATE_FORMAT)

    def days_since(self, date_text):
        date_value = datetime.strptime(date_text, DATE_FORMAT).date()
        return (datetime.now().date() - date_value).days

    def validate_date(self, date_text, field_name):
        try:
            datetime.strptime(date_text, DATE_FORMAT)
        except ValueError:
            raise ValueError(f"{field_name} لازم يكون بالشكل YYYY-MM-DD")
        return date_text

    def validate_form(self):
        name = self.name_var.get().strip()
        interval_text = self.interval_var.get().strip()
        watered = self.watered_var.get().strip()
        fertilized = self.fertilized_var.get().strip()

        if not name:
            raise ValueError("اكتب اسم النبات.")

        try:
            interval = int(interval_text)
        except ValueError:
            raise ValueError("فاصل السقاية لازم يكون رقم صحيح.")

        if interval <= 0:
            raise ValueError("فاصل السقاية لازم يكون أكبر من صفر.")

        self.validate_date(watered, "آخر سقاية")
        self.validate_date(fertilized, "آخر تسميد")
        return name, interval, watered, fertilized

    def add_plant_from_form(self):
        if plant is None:
            return

        try:
            name, interval, watered, fertilized = self.validate_form()
        except ValueError as error:
            messagebox.showerror("بيانات غير صحيحة", str(error))
            return

        if any(item.get("name") == name for item in self.get_plants()):
            messagebox.showerror("اسم مكرر", "في نبات بنفس الاسم موجود بالفعل.")
            return

        plant.add_plant(name, interval)
        if hasattr(plant, "edit_plant"):
            plant.edit_plant(name, name, interval, watered, fertilized)

        self.refresh_table()
        self.clear_form()
        self.status_var.set(f"تمت إضافة {name}")

    def edit_selected_plant(self):
        if plant is None:
            return
        if not self.selected_name:
            messagebox.showinfo("اختار نبات", "اختار نبات من الجدول الأول.")
            return

        try:
            name, interval, watered, fertilized = self.validate_form()
        except ValueError as error:
            messagebox.showerror("بيانات غير صحيحة", str(error))
            return

        duplicated = any(
            item.get("name") == name and item.get("name") != self.selected_name
            for item in self.get_plants()
        )
        if duplicated:
            messagebox.showerror("اسم مكرر", "في نبات بنفس الاسم موجود بالفعل.")
            return

        plant.edit_plant(self.selected_name, name, interval, watered, fertilized)
        self.selected_name = name
        self.refresh_table()
        self.status_var.set(f"تم تعديل {name}")

    def delete_selected_plant(self):
        if plant is None:
            return
        if not self.selected_name:
            messagebox.showinfo("اختار نبات", "اختار نبات من الجدول الأول.")
            return

        confirmed = messagebox.askyesno(
            "تأكيد الحذف",
            f"متأكد إنك عايز تحذف {self.selected_name}؟",
        )
        if not confirmed:
            return

        plant.remove_plant(self.selected_name)
        self.refresh_table()
        self.clear_form()
        self.status_var.set("تم حذف النبات")

    def mark_watered_today(self):
        if plant is None:
            return
        if not self.selected_name:
            messagebox.showinfo("اختار نبات", "اختار نبات من الجدول الأول.")
            return

        plant.update_watering(self.selected_name)
        selected = self.selected_name
        self.refresh_table()
        self.load_plant_into_form(selected)
        self.status_var.set(f"تم تحديث سقاية {selected}")

    def mark_fertilized_today(self):
        if plant is None:
            return
        if not self.selected_name:
            messagebox.showinfo("اختار نبات", "اختار نبات من الجدول الأول.")
            return

        plant.update_fertilizer(self.selected_name)
        selected = self.selected_name
        self.refresh_table()
        self.load_plant_into_form(selected)
        self.status_var.set(f"تم تحديث تسميد {selected}")

    def on_select(self, _event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        plant_name = values[-1]
        self.load_plant_into_form(plant_name)

    def on_tree_mousewheel(self, event):
        self.tree.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"

    def load_plant_into_form(self, name):
        for item in self.get_plants():
            if item.get("name") == name:
                self.selected_name = name
                self.name_var.set(item.get("name", ""))
                self.interval_var.set(str(item.get("watering_interval", "")))
                self.watered_var.set(item.get("last_watered", self.today()))
                self.fertilized_var.set(item.get("fertilized", self.today()))
                return

    def clear_form(self):
        self.selected_name = None
        self.name_var.set("")
        self.interval_var.set("")
        self.watered_var.set(self.today())
        self.fertilized_var.set(self.today())
        self.tree.selection_remove(self.tree.selection())

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        search_text = self.search_var.get().strip().lower()
        visible_count = 0

        for item in self.get_plants():
            name = item.get("name", "")
            if search_text and search_text not in name.lower():
                continue

            try:
                watering_days = self.days_since(item.get("last_watered", self.today()))
                fertilizer_days = self.days_since(item.get("fertilized", self.today()))
                interval = int(item.get("watering_interval", 1))
            except (ValueError, TypeError):
                watering_status = "تاريخ غير صحيح"
                fertilizer_status = "تاريخ غير صحيح"
                tag = "needs"
            else:
                watering_status = "يحتاج سقاية" if watering_days >= interval else "تمام"
                fertilizer_status = "يحتاج تسميد" if fertilizer_days >= 30 else "تمام"
                tag = "needs" if "يحتاج" in watering_status + fertilizer_status else "ok"

            self.tree.insert(
                "",
                "end",
                values=(
                    watering_status,
                    fertilizer_status,
                    item.get("watering_interval", ""),
                    item.get("fertilized", ""),
                    item.get("last_watered", ""),
                    name,
                ),
                tags=(tag,),
            )
            visible_count += 1

        total_count = len(self.get_plants())
        self.status_var.set(f"عدد النباتات: {total_count} | المعروض: {visible_count}")

    def show_today_alerts(self):
        alerts = []

        for item in self.get_plants():
            name = item.get("name", "")
            try:
                watering_days = self.days_since(item.get("last_watered", self.today()))
                fertilizer_days = self.days_since(item.get("fertilized", self.today()))
                interval = int(item.get("watering_interval", 1))
            except (ValueError, TypeError):
                alerts.append(f"{name}: راجع التواريخ")
                continue

            if watering_days >= interval:
                alerts.append(f"{name}: يحتاج سقاية")
            if fertilizer_days >= 30:
                alerts.append(f"{name}: يحتاج تسميد")

        if not alerts:
            messagebox.showinfo("تنبيهات اليوم", "كل النباتات تمام النهارده.")
            return

        messagebox.showwarning("تنبيهات اليوم", "\n".join(alerts))


if __name__ == "__main__":
    window = tk.Tk()
    app = PlantCareGUI(window)
    window.mainloop()
