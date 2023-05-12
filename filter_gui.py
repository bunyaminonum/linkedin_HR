import tkinter as tk
from tkinter import ttk
from pymongo import MongoClient
from connect_database import MDB
import tkinter.messagebox as messagebox


import tkinter as tk
from pymongo import MongoClient
import tkinter as tk
from tkinter import ttk
from pymongo import MongoClient
from connect_database import MDB



class MongoDBFilter:
    def __init__(self):
        self.db = MDB()
        self.collection = self.db.collection
        self.filters = {}
        self.fields = []

    def add_filter(self, field_name, filter_value):
        if field_name == "num_followers":
            try:
                min_value, max_value = filter_value.split("-")
                min_value = int(min_value.strip())
                max_value = int(max_value.strip())
                self.filters[field_name] = {'$gte': min_value, '$lte': max_value}
            except (ValueError, AttributeError):
                # Geçerli bir aralık belirtilmediyse veya hatalı bir değer girildiyse hata mesajı gösterilebilir veya isteğe bağlı olarak başka bir işlem yapılabilir.
                print("Geçersiz num_followers aralığı. Geçerli bir aralık belirtin (örn. 500-1000).")
        else:
            self.filters[field_name] = {'$regex': filter_value, '$options': 'i'}

    def add_field(self, field_name):
        self.fields.append(field_name)

    def get_data(self):
        if not self.filters:
            return self.collection.find({}, self.fields)
        else:
            return self.collection.find(self.filters, self.fields)


class FilterGUI:
    def __init__(self, root):
        self.root = root
        self.filters = []
        self.filter_entries = {}

        self.root.title("MongoDB Filter")
        self.root.geometry("800x400")

        self.label_field = tk.Label(self.root, text="Field Name:")
        self.label_field.pack()

        self.field_name = tk.StringVar()
        self.field_name_entry = tk.Entry(self.root, textvariable=self.field_name)
        self.field_name_entry.pack()

        self.label_field_value = tk.Label(self.root, text="Field Value:")
        self.label_field_value.pack()

        self.field_value_entry = tk.Entry(self.root)
        self.field_value_entry.pack()

        self.fields = ["name", "education", "experience", "works_at", "location", "num_followers", "profile_url"]

        self.checkbox_frame = tk.Frame(self.root)
        self.checkbox_frame.pack()

        for field in self.fields:
            var = tk.IntVar()
            checkbox = tk.Checkbutton(self.checkbox_frame, text=field, variable=var)
            checkbox.pack(side="left", padx=5, pady=5)
            self.filter_entries[field] = (checkbox, var)

        self.add_filter_button = tk.Button(self.root, text="Add Filter", command=self.add_filter)
        self.add_filter_button.pack(side="top", padx=5, pady=5)

        self.filter_frame = tk.Frame(self.root)
        self.filter_frame.pack()

        self.filter_button = tk.Button(self.root, text="Filter", command=self.filter_data)
        self.filter_button.pack(side="top", padx=5, pady=5)

        self.all_data_button = tk.Button(self.root, text="All Data", command=self.get_all_data)
        self.all_data_button.pack()

        self.results_frame = tk.Frame(self.root)
        self.results_frame.pack(fill="both", expand=True)

        self.results_table = ttk.Treeview(self.results_frame, columns=["ID"] + self.fields, show="headings")
        self.results_table.heading("ID", text="ID")
        for field in self.fields:
            self.results_table.heading(field, text=field.capitalize())

        self.results_table.column("ID", width=50)
        for field in self.fields:
            self.results_table.column(field, width=100)

        self.scrollbar_y = ttk.Scrollbar(self.results_frame, orient="vertical", command=self.results_table.yview)
        self.results_table.configure(yscrollcommand=self.scrollbar_y.set)
        self.scrollbar_y.pack(side="right", fill="y")

        self.results_table.pack(side="left", fill="both",expand=True)
        self.results_table.bind("<ButtonRelease-1>", self.copy_selected_row)

    def get_all_data(self):
        filter_obj = MongoDBFilter()
        results = filter_obj.get_data()
        self.display_results(results)

    def copy_selected_row(self, event):
        selected_item = self.results_table.focus()
        values = self.results_table.item(selected_item, "values")
        row_text = "\t".join(str(value) for value in values)
        self.root.clipboard_clear()
        self.root.clipboard_append(row_text)

        # Tam satırı kopyalamak için tüm hücreleri seçin
        self.results_table.selection_set(selected_item)
        self.results_table.focus(selected_item)

    def add_filter(self):
        field_name = self.field_name.get()
        field_value = self.field_value_entry.get()
        if field_name and field_value:
            self.filters.append((field_name, field_value))
            # Görsel arayüzde filtreyi göstermek için yeni bir etiket ve düğme oluşturulur
            filter_label = tk.Label(self.filter_frame,
                                    text=f"Filter {len(self.filters)}: {field_name} = {field_value}")
            filter_label.pack(side="left", padx=5, pady=5)

            remove_button = tk.Button(self.filter_frame, text="Remove",
                                      command=lambda name=field_name: self.remove_filter(name))
            remove_button.pack(side="left", padx=5, pady=5)

            # Filtreyi temizlemek için giriş alanlarını sıfırla
            self.field_name.set("")
            self.field_value_entry.delete(0, "end")

    def remove_filter(self, field_name):
        for i, (name, _) in enumerate(self.filters):
            if name == field_name:
                self.filters.pop(i)
                break

        self.display_filters()

    def display_filters(self):
        for child in self.filter_frame.winfo_children():
            child.destroy()

        for i, (field_name, field_value) in enumerate(self.filters, start=1):
            filter_label = tk.Label(self.filter_frame, text=f"Filter {i}: {field_name} = {field_value}")
            filter_label.pack(side="left", padx=5, pady=5)

            remove_button = tk.Button(self.filter_frame, text="Remove",
                                      command=lambda name=field_name: self.remove_filter(name))
            remove_button.pack(side="left", padx=5, pady=5)

    def filter_data(self):
        if self.filters:
            filter_obj = MongoDBFilter()

            for field_name, field_value in self.filters:
                filter_obj.add_filter(field_name, field_value)

            for field, (_, var) in self.filter_entries.items():
                if var.get() == 1:
                    filter_obj.add_field(field)

            results = filter_obj.get_data()
            self.display_results(results)
        else:
            messagebox.showinfo("Uyarı", "En az bir filtre ekleyin.")

    def display_results(self, results):
        for child in self.results_table.get_children():
            self.results_table.delete(child)

        for i, result in enumerate(results, start=1):
            data = [i] + [result.get(field, "") for field in self.fields]
            self.results_table.insert("", "end", values=data)

root = tk.Tk()
gui = FilterGUI(root)
root.mainloop()