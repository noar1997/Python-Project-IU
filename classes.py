from datetime import datetime
import json
import sys
from rich.console import Console
from rich.table import Table
from rich.text import Text
import pyfiglet
 #This function was created outside of the classes so it could be re used. It equals the frequency to a specific value so it can be passed on the system and check if said user is following the frequency
def can_complete_habit(habit, last_date, today):
    frequency = habit["frequency"].lower()
    if frequency == "daily":
        return (today.date() > last_date.date())
    elif frequency == "weekly":
        return (today - last_date).days >= 7
    elif frequency == "monthly":
        return (today.month != last_date.month or today.year != last_date.year)
    else:
        return False
    
# Logic to check if the habit has been broken based on their frequency
def streak_broken(last_date, today, frequency):
    days_difference = (today - last_date).days
    if frequency.lower() == "daily":
        return days_difference > 1
    elif frequency.lower() == "weekly":
        return days_difference > 7
    elif frequency.lower() == "monthly":
        return days_difference > 31
    return False

 #File is opened and the possible error of file missing is handled
def load_credentials():
    try:
        with open("habit_data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
 #To save the file
def save_credentials(data):
    with open("habit_data.json", "w") as file:
        json.dump(data, file, indent=4)




 #The class login mainly contains a way for the user to enter it's own credentials, and the system checks against the json file to see if said username and password exists, it mainly works with if and else.'
class Login:
    def __init__ (self, username=None, password=None):
        if username is not None and password is not None:
            self.username = username.lower()
            self.password = password
        else:
            self.username = input("Please enter your username: ").lower()
            self.password = input("Please enter your password: ")



    def check (self):
        credentials = load_credentials()
        if self.username in credentials:
            if self.password == credentials[self.username]["password"]:
                proceed = input("Welcome to the app! Would you like to proceed to the dashboard? Y/N: ")
                if proceed.upper() == "Y":
                    import dashboard
                    dashboard.start_dashboard(self.username)
                
                    
                else:
                    print("Exiting")
                    return False


            else:
                print("Wrong password.")
                return False

        else:
                option = input(f"Your credentials are not in the system, {self.username}, Would you like to add a new username? Y/N: ")

                if option.upper() == "Y":
                    credentials[self.username] = {"password": self.password, "habits":[]}
                    save_credentials(credentials)
                    print(f"The username, {self.username}, has been added. ")



                elif option.upper() == "N":
                    print("Bye!")
                    exit()

                else:
                    print("Invalid option. Exiting. ")
                    exit()


 #The class Habits contains mainly menus and key functions for the use of the program itself.

class Habits:
    def dashboard(self):
        console = Console()
        print(pyfiglet.figlet_format("Habit   Tracker!"))
        table = Table(title="")
        table.add_column("Option", justify="center", style="cyan", no_wrap=True)
        table.add_column("Action", style="magenta")
        table.add_row("1", "View habits")
        table.add_row("2", "Add a new habit")
        table.add_row("3", "Mark habit as completed")
        table.add_row("4", "Analytics")
        table.add_row("5", "User")

        table.add_row("6", "Log out")
        console.print(table)
        try:
            decision = int(input("Enter an option : "))
            return decision
        except ValueError:
            print("Invalid input. Please enter a number.")
            return None
     #Table is created so user can decide if to create own habit, or use from a list of pre defined ones.
    def dashboard2(self):
        console = Console()
        table = Table(title="")
        table.add_column("Option", justify="center", style="cyan", no_wrap=True)
        table.add_column("Action", style="magenta")
        table.add_row("1", "Use pre-existing habits")
        table.add_row("2", "Create your own habit")
        table.add_row("3", "Log out")
        console.print(table)

        try:
            decision2 = int(input("Enter an option : "))
            return decision2
        except ValueError:
            print("Invalid input. Please enter a number.")
            return None
     #Dashboard showing options of pre defined habits, the variable is passed as a int to avoid errors when user enters the numerical option
    def dashboard3(self):
        console = Console()
        table = Table(title="")
        table.add_column("Option", justify="center", style="cyan", no_wrap=True)
        table.add_column("Action", style="magenta")
        table.add_row("1", "Studying: Daily")
        table.add_row("2", "Excercising: Daily")
        table.add_row("3", "Doing laundry: Weekly")
        table.add_row("4", "Reviewing finances: Monthly")
        table.add_row("5", "Log out")
        console.print(table)
        try:
            decision3 = int(input("Enter an option : "))
            return decision3
        except ValueError:
            print("Invalid input. Please enter a number.")
            return None

     #This function allows the user to pull pre defined habits given by the system, streak and progress are set to 0
    def add_predefined_habit(self, username, habit_name, frequency):
        habit = {
            "habit": habit_name,
            "frequency": frequency,
            "start_date": datetime.today().strftime("%Y-%m-%d"),
            "completion_log": [],
            "streak": 0,
            "progress": 0,
            "longest_streak": 0
            }

        data = load_credentials()
        if username in data:
            data[username]["habits"].append(habit)
            save_credentials(data)
            print(f"Predefined habit, {habit_name}, has been added succesfully!")
        else:
            print("User not found")


     #This function was created to retreive information from the .json file and be displayed in a visualy friendly way
    def print_habits(self, username):
        data = load_credentials()
        user_data = data[username]
        habits_list = user_data["habits"]
        console = Console()
        if not habits_list:
            print("You have no habits yet.")
            return

        table = Table(title="Current habits")
        table.add_column("Habit", style="cyan", no_wrap=True)
        table.add_column("Frequency", style="magenta")

        for habit in habits_list:
            table.add_row(habit['habit'], habit['frequency'])

        console.print(table)


     #User can create it's own habit, entering the name, frequency, and by default it will take the day's date and streak and progress is by default 0
    def create_own_habit(self, username, habit_name, frequency):
        habit = {
            "habit": habit_name,
            "frequency": frequency,
            "start_date": datetime.today().strftime("%Y-%m-%d"),
            "completion_log": [],
            "streak": 0,
            "progress": 0,
            "longest_streak": 0
            }
        data = load_credentials()
        if username in data:
            data[username]["habits"].append(habit)
            save_credentials(data)
            print(f"A new habit, {habit_name}, has been added succesfully!")
        else:
            print("User not found")


    def habit_completed(self, username):
        data = load_credentials()
        user_data = data.get(username)
        habits = user_data.get("habits", [])

        if not habits:
            print("You have no habits to complete.")
            return

        print("Which habit have you completed today?")
        for h, habit in enumerate(habits, 1):
            print(f"{h}. {habit['habit']} ({habit['frequency']})")
         # So user can see a list of the habits and mark them based on the frequency
        try:
            choice = int(input("Enter the number of the habit: ")) -1
            if choice < 0 or choice >= len(habits):
                print("Invalid choice")
                return
        except ValueError:
            print("Please enter a number")
            return


        habit = habits[choice]
        today = datetime.today()
        today_str = today.strftime("%Y-%m-%d")

        if today_str in habit["completion_log"]:
            print(f"Habit '{habit['habit']}' was already completed today.")
            return


        if habit["completion_log"]:
            last_date_str = habit["completion_log"][-1]
            last_date = datetime.strptime(last_date_str, "%Y-%m-%d")
            days_passed = (today - last_date).days
        else:
            last_date = None
            days_passed = None
        #Way to check if habit can be completed
        if days_passed is None or can_complete_habit(habit, last_date, today):
            if last_date and streak_broken(last_date, today, habit["frequency"]):
                habit["streak"] = 0
            habit["completion_log"].append(today_str)
            habit["streak"] = habit.get("streak", 0) + 1
            habit["progress"] = habit.get("progress", 0) + 1
            if habit["streak"] > habit.get("longest_streak", 0):
                habit["longest_streak"] = habit["streak"]
            save_credentials(data)
            print("Habit has been completed.")
        else:
            print("Habit can not be completed due to it's frequency.")
            print(f"It was completed {days_passed} days ago, which exceeded it's frequency.")




 #This class mainly focuses on retreiving data from the file pertinent to the "habit", and when it was completed. It also shows if there is a streak and how many days, vs the progress of said habit. The completion log column gives the date of when it was completed.
class Analytics:
    def habit_details(self, username):
        data = load_credentials()
        user_data = data.get(username)
        habits = user_data.get("habits", [])
        console = Console()

        if not habits:
            print("You have no habits.")
            return
        table = Table(title="Habit Details")
         # To create styled table
        table.add_column("Habit", style="cyan", no_wrap=True)
        table.add_column("Frequency", style="green")
        table.add_column("Streak", justify="center", style="yellow")
        table.add_column("Status", justify="center", style="red")
        table.add_column("Progress", justify="center", style="blue")
        table.add_column("Completion Log", style="white")
        table.add_column("Longest Streak", justify="center", style="bright_red")

        today = datetime.today()
        streak_reset = False

        for habit in habits:
             # Getting last completion date
            if habit["completion_log"]:
                last_completion_str = habit["completion_log"][-1]
                last_date = datetime.strptime(last_completion_str, "%Y-%m-%d")
                #Checking if streak was broken to update "streak" column
                if streak_broken(last_date, today, habit["frequency"]):
                    habit["streak"] = 0
                    display_streak = "0"
                    status = "Broken"
                    streak_reset = True
                else:
                    display_streak = str(habit["streak"])
                    status = "Active"
            else:
                display_streak = "0"
                status = "Inactive"
            #I implemented this line so if more than 5 dates are completed, the screen doesn't get overloaded
            if len(habit["completion_log"]) > 5:
                recent_dates = [date[5:] for date in habit["completion_log"][-5:]]
                habit_log = ", ".join(recent_dates) + ", ..."
            else:
                habit_log = ", ".join([date[5:] for date in habit["completion_log"]])
            table.add_row(
                habit["habit"],
                habit["frequency"],
                display_streak,
                status,
                str(habit["progress"]),
                habit_log,
                str(habit.get("longest_streak", 0))
                
            )

        console.print(table)
        if streak_reset:
            save_credentials(data)

 #The class summary will work with the option "User", to display information on the streak and how the user has worked with the habits.
class Summary:
    def user_summ(self, username):
        data = load_credentials()
        user_data = data.get(username, {})
        habits = user_data.get("habits", [])
        console = Console()


        if not habits:
            print("No habits to analyze.")
            return
        
        longest_streak = 0
        longest_habit = None 
        completed_today = 0
        today = datetime.today().strftime("%Y-%m-%d")
        recent_completions = []
        inactive_habits = []
        
        #Finding longest streak and the habits that were completed "today"
        for habit in habits:
            if habit.get("longest_streak", 0) > longest_streak:
                longest_streak = habit["longest_streak"]
                longest_habit = habit["habit"]
        #Determining number of habits completed today
            if today in set(habit["completion_log"]):
                completed_today += 1
        console.print(f"\n[bold underline]User Summary for {username.title()}[/bold underline]\n", justify = "center", style="blue")
        #Last habit completed
        if habit["completion_log"]:
            last = habit["completion_log"][-1]
            recent_completions.append((habit["habit"], last))
        else:
            inactive_habits.append(habit["habit"])
        console.print(f"\n[bold underline]User Summary for {username.title()}[/bold underline]\n", justify="center", style="blue")

        if longest_habit:
            message = Text(f" Longest streak: '{longest_habit}' with {longest_streak} day{'s' if longest_streak != 1 else ''}.", style="bold")
            console.print(message, style ="red")
            console.rule()
        else:
            print("No data fund.")
        
        # Total habits created 
        console.print(f"\n Total habits created: {len(habits)}", style="green")
        console.rule()
        # Habits completed today
        console.print(f" Habits completed today: {completed_today}", style="cyan")
        console.rule()

        if inactive_habits:
            console.print(" Habits with no completions:", style="bright_red")
            for habit_name in inactive_habits:
                console.print(f" - {habit_name}", style="red")
            console.rule()

        if recent_completions:
            last_habit = max(recent_completions, key=lambda x: x[1])
            console.print(f" Last habit completed: '{last_habit[0]}' on {last_habit[1]}", style="white")
            console.rule()