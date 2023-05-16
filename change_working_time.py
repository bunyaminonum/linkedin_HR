from connect_database import MDB
import re

class WorkingTimeUpdater:
    def __init__(self):
        self.db = MDB()
        self.users_collection = self.db.collection

    def convert_working_time(self, working_time):
        years = 0
        months = 0

        if "yrs" in working_time:
            years_str = working_time.split(" yrs")[0].strip()
            if years_str:
                years = int(years_str)
        elif "yr" in working_time:
            years_str = working_time.split(" yr")[0].strip()
            if years_str:
                years = int(years_str)

        if "mos" in working_time:
            months_str = working_time.split(" mos")[0].split(" ")[-1].strip()
            if months_str:
                months = int(months_str)
        elif "mo" in working_time:
            months_str = working_time.split(" mo")[0].split(" ")[-1].strip()
            if months_str:
                months = int(months_str)

        return (years, months)

    def update_user_experience(self, user):
        experiences = user["experience"]
        for experience in experiences:
            if "working_time" in experience:
                if isinstance(experience["working_time"], tuple):
                    # Daha önce dönüştürülmüş bir değer var, geçerli değeri kullan
                    continue

                if "yrs" in experience['working_time'] or "yr" in experience['working_time'] or "mo" in experience['working_time'] or "mos" in experience['working_time']:
                    experience["working_time"] = self.convert_working_time(experience["working_time"])

    def update_user_total_working_time(self, user):
        total_years = 0
        total_months = 0

        for experience in user["experience"]:
            if "working_time" in experience:
                experience_years, experience_months = experience["working_time"]
                total_years += experience_years
                total_months += experience_months

        # Ayları yıla çevir
        total_years += total_months // 12
        total_months = total_months % 12

        # Toplam deneyimi total_working_time alanına ata
        user["total_working_time"] = (total_years, total_months)

    def run(self):
        # Tüm kullanıcıları alın
        users = self.users_collection.find()

        # Her kullanıcı için tüm deneyim alanlarını güncelle
        for user in users:
            self.update_user_experience(user)
            self.update_user_total_working_time(user)

            # Güncellenmiş belgeyi kaydedin
            self.users_collection.replace_one({"_id": user["_id"]}, user)

