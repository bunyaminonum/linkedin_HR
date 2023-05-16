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
        self.new_record_window = None
        self.root.title("MongoDB Filter")
        self.root.geometry("800x400")
        self.db = MDB()

        style = ttk.Style()
        style.theme_use('clam')  # Modern görünüm için 'clam' temasını kullanabilirsiniz

        self.label_field = ttk.Label(self.root, text="Field Name:")
        self.label_field.pack()

        self.field_name = tk.StringVar()
        self.field_name_entry = ttk.Entry(self.root, textvariable=self.field_name)
        self.field_name_entry.pack()

        self.label_field_value = ttk.Label(self.root, text="Field Value:")
        self.label_field_value.pack()

        self.field_value_entry = ttk.Entry(self.root)
        self.field_value_entry.pack()

        # Diğer widgetlerin ttk versiyonlarını da kullanabilirsiniz
        self.fields = ["name", "education", "experience", "works_at", "location", "num_followers", "profile_url", 'skills', 'about']

        self.checkbox_frame = ttk.Frame(self.root)
        self.checkbox_frame.pack()

        for field in self.fields:
            var = tk.IntVar()
            checkbox = ttk.Checkbutton(self.checkbox_frame, text=field, variable=var)
            checkbox.pack(side="left", padx=5, pady=5)
            self.filter_entries[field] = (checkbox, var)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side="top", padx=10, pady=10)

        self.add_filter_button = tk.Button(self.button_frame, text="Add Filter", command=self.add_filter)
        self.add_filter_button.pack(side="left", padx=5, pady=5)

        self.filter_frame = tk.Frame(self.root)
        self.filter_frame.pack()

        self.filter_button = tk.Button(self.button_frame, text="Filter", command=self.filter_data)
        self.filter_button.pack(side="left", padx=5, pady=5)

        self.all_data_button = tk.Button(self.button_frame, text="All Data", command=self.get_all_data)
        self.all_data_button.pack(side="left", padx=5, pady=5)

        # add new record
        self.new_record_button = tk.Button(self.button_frame, text="New Record", command=self.open_new_record_window)
        self.new_record_button.pack(side="left", padx=5, pady=5)

        # delete record
        self.delete_button = tk.Button(self.button_frame, text="Delete Record", command=self.delete_record)
        self.delete_button.pack(side="left", padx=5, pady=5)

        # update record
        self.update_record_button = tk.Button(self.button_frame, text="Update Record", command=self.update_record)
        self.update_record_button.pack(side="left", padx=5, pady=5)

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

    #add new record
    def open_new_record_window(self):
        self.new_record_window = tk.Toplevel(self.root)
        self.new_record_window.title("New Record")
        self.new_record_window.geometry("600x500")
        self.new_record_window.geometry("+{}+{}".format(int(self.new_record_window.winfo_screenwidth() / 2 - 200),
                                                        int(self.new_record_window.winfo_screenheight() / 2 - 175)))
        self.new_record_window.configure(padx=50, pady=50)
        label_name = tk.Label(self.new_record_window, text="Name:")
        label_name.pack()
        entry_name = tk.Entry(self.new_record_window)
        entry_name.pack()

        label_education = tk.Label(self.new_record_window, text="Education:")
        label_education.pack()
        entry_education = tk.Entry(self.new_record_window)
        entry_education.pack()

        label_experience = tk.Label(self.new_record_window, text="Experience:")
        label_experience.pack()
        entry_experience = tk.Entry(self.new_record_window)
        entry_experience.pack()

        label_works_at = tk.Label(self.new_record_window, text="Works At:")
        label_works_at.pack()
        entry_works_at = tk.Entry(self.new_record_window)
        entry_works_at.pack()

        label_location = tk.Label(self.new_record_window, text="Location:")
        label_location.pack()
        entry_location = tk.Entry(self.new_record_window)
        entry_location.pack()

        label_num_followers = tk.Label(self.new_record_window, text="Num Followers:")
        label_num_followers.pack()
        entry_num_followers = tk.Entry(self.new_record_window)
        entry_num_followers.pack()

        label_profile_url = tk.Label(self.new_record_window, text="Profile URL:")
        label_profile_url.pack()
        entry_profile_url = tk.Entry(self.new_record_window)
        entry_profile_url.pack()

        label_about = tk.Label(self.new_record_window, text="About:")
        label_about.pack()
        entry_about = tk.Entry(self.new_record_window)
        entry_about.pack()

        label_skills = tk.Label(self.new_record_window, text="Skills:")
        label_skills.pack()
        entry_skills = tk.Entry(self.new_record_window)
        entry_skills.pack()

        save_button = tk.Button(self.new_record_window, text="Save",
                                command=lambda: self.save_record(entry_name.get(), entry_education.get(),
                                                                 entry_experience.get(), entry_works_at.get(),
                                                                 entry_location.get(), entry_num_followers.get(),
                                                                 entry_profile_url.get(), entry_about.get(),
                                                                 entry_skills.get()))
        save_button.pack()

    #delete record
    def delete_record(self):
        selected_item = self.results_table.focus()
        if selected_item:
            profile_url = self.results_table.item(selected_item)["values"][self.fields.index("profile_url")]


            # Confirm dialog
            confirmation = messagebox.askquestion("Confirmation", "Are you sure you want to delete this record?")
            if confirmation == "yes":

                # Delete the record
                self.db.collection.delete_one({"profile_url": profile_url})


                messagebox.showinfo("Success", "Record deleted successfully.")
                self.get_all_data()  # Refresh the results table
            else:
                messagebox.showinfo("Cancelled", "Deletion cancelled.")
        else:
            messagebox.showinfo("Warning", "No record selected.")

    #update record
    def update_record(self):
        selected_item = self.results_table.focus()
        if not selected_item:
            messagebox.showinfo("Uyarı", "Güncellenecek bir kayıt seçilmedi.")
            return

        values = self.results_table.item(selected_item, "values")
        if len(values) <= 1:
            messagebox.showinfo("Uyarı", "Güncellenecek bir kayıt seçilmedi.")
            return

        # Seçilen kaydın verilerini al
        record_id = values[0]
        record_values = values[1:]

        # Eski verileri içerecek olan pencereyi aç
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Record")
        update_window.geometry("400x300")
        update_window.geometry(
            "+{}+{}".format(int(update_window.winfo_screenwidth() / 2 - 200),
                            int(update_window.winfo_screenheight() / 2 - 150)))
        update_window.configure(padx=50, pady=50)

        # Kayıt alanlarını düzenlemek için etiketler ve giriş kutuları oluştur
        entry_values = []
        for i, field_name in enumerate(self.fields, start=1):
            label = tk.Label(update_window, text=field_name.capitalize() + ":")
            label.pack()
            entry = tk.Entry(update_window)
            entry.pack()
            entry.insert(0, record_values[i - 1])
            entry_values.append(entry)

        # Güncelleme işlemini gerçekleştiren metodu tanımla
        def perform_update():
            db = MDB()
            # Güncellenecek verileri al
            updated_values = [entry.get() for entry in entry_values]

            # Güncellenecek kaydın profil URL'sini al
            profile_url = record_values[-1]

            # Veritabanında kaydı güncelle
            result = db.collection.update_one({"profile_url": profile_url},
                                              {"$set": dict(zip(self.fields, updated_values))})

            if result.modified_count > 0:
                messagebox.showinfo("Başarılı", "Kayıt güncellendi.")
                update_window.destroy()
                self.get_all_data()
            else:
                messagebox.showinfo("Uyarı", "Kayıt güncellenirken bir hata oluştu.")

        # Enter tuşuna basıldığında güncelleme işlemini yap
        update_window.bind("<Return>", lambda event: perform_update())

        # Güncelleme işlemini gerçekleştirecek olan düğmeyi oluştur
        update_button = tk.Button(update_window, text="Güncelle", command=perform_update)
        update_button.pack()

    def save_record(self, name, education, experience, works_at, location, num_followers, profile_url, about, skills):
        collection = self.db.collection

        new_record = {
            "name": name,
            "education": education,
            "experience": experience,
            "works_at": works_at,
            "location": location,
            "num_followers": num_followers,
            "profile_url": profile_url,
            "about": about,
            "skills": skills
        }

        collection.insert_one(new_record)

        messagebox.showinfo("Success", "New record saved successfully.")

        self.new_record_window.destroy()

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