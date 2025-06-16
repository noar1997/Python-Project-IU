from classes import Habits

from classes import Summary

from classes import Analytics
#Function to prevent the code exiting from every meny
def pause():
    input("\nHit enter to return to main menu.")


 #This function mainly contains code to make the menus work + contains pre defined habits

def start_dashboard(username):
    menu = Habits()
    analytics = Analytics()
    summary = Summary()
    
    
    while True:
        decision = menu.dashboard()
        if decision == 1:
            decision = menu.print_habits(username)
            pause()
        

        elif decision == 2:
            decision2 = menu.dashboard2()
    
            if decision2 == 1:
                decision3 = menu.dashboard3()

                if decision3 == 1:
                    menu.add_predefined_habit(username, "reading", "daily")
                    pause()

                elif decision3 == 2:
                    menu.add_predefined_habit(username, "Excercising", "daily")
                    pause()
                elif decision3 == 3:
                    menu.add_predefined_habit(username, "Doing Laundry", "Weekly")
                    pause()
                elif decision3 == 4:
                    menu.add_predefined_habit(username, "Reviewing Finances", "Monthly")
                    pause()

                elif decision3 == 5:
                    print("Logging out...")
                    exit()

                else:
                    print("Wrong option!")
                    exit()
                    pause()

            elif decision2 == 2:
                habit_name = input("Enter the name of your new habit: ")
                frequency = input("Enter the frequency of your habit: ")
                menu.create_own_habit(username, habit_name, frequency)
                pause()
            elif decision2 == 3:
                print("Logging out...")
                exit()

            else:
                print("Invalid input")
                exit()
                pause()

        elif decision == 3:
            decision = menu.habit_completed(username)
            pause()
        elif decision == 4:
            decision = analytics.habit_details(username)
            pause()

        elif decision == 5:
            summary.user_summ(username)
            pause()

        elif decision == 6:
            print("Logging out!")
            exit()


        else:
            print("Invalid input")
            exit()