from connect_database import MDB
import re

class WorkingTimeUpdater:
    def __init__(self):
        self.db = MDB()
        self.users_collection = self.db.collection

    def convert_working_time(self, working_time):
        """
        Converts the working time from string format to a tuple of years and months.

        Args:
            working_time (str): The working time string in the format "x yrs y mos".

        Returns:
            tuple: A tuple containing the years and months extracted from the working time string.
        """
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
        """
        Updates the working time in each experience of a user by converting it to a tuple of years and months.

        Args:
            user (dict): The user dictionary containing the "experience" field to be updated.
        """
        experiences = user["experience"]
        for experience in experiences:
            if "working_time" in experience:
                if isinstance(experience["working_time"], tuple):
                    # There is already a converted value, use the current value
                    continue

                if "yrs" in experience['working_time'] or "yr" in experience['working_time'] or "mo" in experience[
                    'working_time'] or "mos" in experience['working_time']:
                    experience["working_time"] = self.convert_working_time(experience["working_time"])

    def update_user_total_working_time(self, user):
        """
        Updates the total working time of a user based on the sum of individual experiences.

        Args:
            user (dict): The user dictionary containing the "experience" field.
        """
        total_years = 0
        total_months = 0

        for experience in user["experience"]:
            if "working_time" in experience:
                experience_years, experience_months = experience["working_time"]
                total_years += experience_years
                total_months += experience_months

        # Convert months to years
        total_years += total_months // 12
        total_months = total_months % 12

        # Assign the total experience to the total_working_time field
        user["total_working_time"] = (total_years, total_months)

    def run(self):
        """
        Runs the process of updating experience and total working time for all users.
        """
        # Get all users
        users = self.users_collection.find()

        # Update all experience fields for each user
        for user in users:
            self.update_user_experience(user)
            self.update_user_total_working_time(user)

            # Save the updated document
            self.users_collection.replace_one({"_id": user["_id"]}, user)

