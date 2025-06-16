# Python-Project-IU
Final phase for OOP project

Habit Tracker application built in Python. 

USer can create it's own habit, or select from a pre defined set of habits.

App can track daily - weekly - monthly habits, calculate completion, and show streaks. 

Features:
    Login authentication
    Create your own habits
    Mark habit as completed
    Track habit streaks
    Analytics module with data breakdown
    View a user summary

Installation:
    Clone the following repository:
        git clone https://github.com/noar1997/Python-Project-IU
        cd Python-Project-IU

Use:
    Run: python main.py

Unit Testig:
    Using the unittest module and including mocking to isolate logic.

    The components tested were the following:
        can_complete_habit(), streak_broken(), create_own_habit(), add_predefined_habit().
    
    To run the tests: python test_habtis.py


Index:
    Python-Project-IU/
        classes.py              Core Logic containing classes
        habit_data.json         User and habits storage
        main.py                 Main program running the app   
        test_habits.py          Unit testing
        README.md               Description of the project