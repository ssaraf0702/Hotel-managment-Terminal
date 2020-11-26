from FunctionsFile import *

adminPass = "admin"
employeePass = "employee"

password = input("\nEnter Password : ")

if password == adminPass:
    login = Admin()
    login.isTodayNew()

    print(TextColor.GREEN + TextColor.BOLD + TextColor.UNDERLINE + "ADMIN LOGGED IN !!" + TextColor.ENDC)
    while True:
        print("\n1) Check details for a date")
        print("2) Add new Item to menu")
        print("3) Modify existing menu")
        print("4) Print Menu")
        print("5) Place Order")
        print("0) Exit")
        choice = int(input("  >>  "))

        if choice == 0:
            break

        elif choice == 1:
            login.checkDateDetails()

        elif choice == 2:
            login.addToMenu()
            login.printAndUpdateFiles()

        elif choice == 3:
            login.modifyMenu()
            login.printAndUpdateFiles()

        elif choice == 4:
            login.displayMenu()

        elif choice == 5:
            login.takeOrder()

        else:
            print(TextColor.FAIL + "Invalid Choice !!" + TextColor.ENDC)

elif password == employeePass:
    print(TextColor.GREEN + TextColor.BOLD + TextColor.UNDERLINE + "EMPLOYEE LOGGED IN !!" + TextColor.ENDC)
    login = Employee()
    login.isTodayNew()

    while True:
        print("\n1) Print Menu")
        print("2) Place Order")
        print("0) Exit")
        choice = int(input("  >>  "))

        if choice == 0:
            break

        elif choice == 1:
            login.displayMenu()

        elif choice == 2:
            login.takeOrder()

        else:
            print(TextColor.FAIL + "Invalid Choice !!" + TextColor.ENDC)

else:
    print(TextColor.FAIL + TextColor.BOLD + TextColor.UNDERLINE + "    WRONG PASSWORD !" + TextColor.ENDC)
