import json
from tabulate import tabulate
from datetime import date


# Text-Colours class
class TextColor:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\u001b[32m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    MAGENTA = '\033[95m'
    CYAN = "\033[96m"


# Employee class
class Employee:
    def isTodayNew(self):

        today = date.today()
        dateFormat = today.strftime("%d-%m-%Y")
        search = "./data/d-" + dateFormat + '.json'

        try:
            openFile = open(search, "r+")
        except:
            openFile = open(search, "w+")
            emptyJson = {
                "totalOrders": 0,
                "totalBilling": 0,
                "totalCostPrice": 0,
                "totalProfit": 0,
                "tax": 0,
                "orders": []
            }
            openFile.write(json.dumps(emptyJson))

    def takeOrder(self):
        Employee.displayMenu(self)

        # opening menu file
        openFile = open("Menu.json", "r+")
        menuData = json.loads(openFile.read())

        # opening todays details file
        today = date.today()
        dateFormat = today.strftime("%d-%m-%Y")
        search = "./data/d-" + dateFormat + '.json'
        openFile = open(search, "r+")
        todaysDetails = json.loads(openFile.read())

        todaysDetails['totalOrders'] += 1

        orderTotalMrp = 0
        orderTotalCp = 0
        totalQuantity = 0
        cart = []

        phoneNum = input(TextColor.BLUE + "\n    Enter phone number of customer : " + TextColor.ENDC)

        print(TextColor.FAIL + "    To End order enter item Id = 0" + TextColor.ENDC)

        while True:
            orderItemId = int(input(TextColor.BLUE + "\n    Item id        : " + TextColor.ENDC))
            if orderItemId == 0:
                break

            if orderItemId <= 1000 or orderItemId > 1000 + len(menuData['itemsList']):
                print(TextColor.FAIL + "        Invalid Item Id." + TextColor.ENDC)
                continue

            itemIndex = orderItemId - 1000 - 1

            if not menuData['itemsList'][itemIndex]['isAvailable']:
                print(TextColor.FAIL + "        Item unavailable." + TextColor.ENDC)
                continue

            quantity = int(input(TextColor.BLUE + "    Enter Quantity : " + TextColor.ENDC))

            mrp = menuData['itemsList'][itemIndex]['item_mrp'] * quantity
            orderTotalMrp += mrp
            orderTotalCp += menuData['itemsList'][itemIndex]['item_cp'] * quantity
            totalQuantity += quantity

            cart.append([orderItemId, quantity, mrp])

        tax = orderTotalMrp * 0.05

        todaysDetails['totalCostPrice'] += orderTotalCp
        todaysDetails['totalProfit'] = todaysDetails['totalProfit'] + orderTotalMrp - orderTotalCp
        todaysDetails['tax'] += tax
        todaysDetails['totalBilling'] += orderTotalMrp + tax

        currOrderJson = {
            "phoneNumber": phoneNum,
            "noOfItems": totalQuantity,
            "orderBillBefTax": orderTotalMrp,
            "orderBill": orderTotalMrp + tax,
            "itemDetails": cart
        }

        todaysDetails['orders'].append(currOrderJson)
        openFile = open(search, "w+")
        openFile.write(json.dumps(todaysDetails))
        print()
        Employee.generateBill(self, currOrderJson)

    def generateBill(self, currOrderDetails):
        openFile = open("Menu.json", "r+")
        menuData = json.loads(openFile.read())

        print("-------------------------------------------------------------------------")
        results = [(menuData['itemsList'][item[0] - 1001]['itemName'], item[1], item[2]) for item in
                   currOrderDetails['itemDetails']]
        print(TextColor.YELLOW + tabulate(results, headers=["Name", "Quantity", "Bill"],
                                          tablefmt="simple") + TextColor.ENDC)
        print("--------------------------------------------------------------------------")
        print(TextColor.YELLOW + "    Total    = " + str(currOrderDetails['orderBillBefTax']))
        print("    Tax (5%) = " + str(currOrderDetails['orderBill'] - currOrderDetails['orderBillBefTax']))
        print("    Bill     = " + str(currOrderDetails['orderBill']) + TextColor.ENDC)

    def displayMenu(self):
        openFile = open("Menu.json", "r+")
        jsonData = json.loads(openFile.read())

        results = [(item['itemId'], item['itemName'], item['item_mrp'], item['itemDesc']) for item in
                   jsonData['itemsList'] if item['isAvailable']]
        print("\n" + TextColor.CYAN + tabulate(results, headers=["Id", "Name", "Mrp", "Description"], tablefmt="pretty",
                                        colalign="left") + TextColor.ENDC + "\n")

    def makeHtmlFile(self):
        openFile = open("Menu.json", "r+")
        jsonData = json.loads(openFile.read())

        strCss = "<!DOCTYPE html>\n<html>\n<head>\n<style>\nbody{ \n background-color: lightGray; \n } \n table { \n font-family: Arial, Helvetica, sans-serif; \n border-collapse: collapse; \n width: 600px; \n  } \n td,th { \n border: 3px solid DodgerBlue; \n padding: 9px;} \n tr:nth-child(even){background-color: #f2f2f2;} \n tr:hover {background-color: hsla(9, 100%, 64%, 0.5);} \n th { \n padding-top: 12px; \n padding-bottom: 12px; \n text-align: left; \n background-color: #4CAF50; \n color: white;} \n </style> \n </head> \n <body>\n"
        results = [(item['itemId'], item['itemName'], item['item_mrp'], item['itemDesc']) for item in
                   jsonData['itemsList'] if item['isAvailable']]

        openFile = open("./templates/table.html", "w+")
        strTable = tabulate(results, headers=["Id", "Name", "Mrp", "Description"], tablefmt="html")
        strEnd = "\n</body></html>"
        openFile.write(strCss + strTable + strEnd)


# Admin Class
class Admin(Employee):
    def checkDateDetails(self):
        toContinue = "1"
        while toContinue != "0":
            checkDate = input(TextColor.BLUE + "    Enter the desired date (format : dd-mm-YYYY) : " + TextColor.ENDC)
            search = "./data/d-" + checkDate + '.json'

            try:
                openFile = open(search, "r+")
                dataJson = json.loads(openFile.read())
                print(TextColor.MAGENTA + "    Date : " + checkDate + " details")
                print("        Total Orders     : " + str(dataJson['totalOrders']))
                print("        Total Cost price : " + str(dataJson['totalCostPrice']))
                print("        Total Profit     : " + str(dataJson['totalProfit']))
                print("        Total Tax        : " + str(dataJson['tax']))
                print("        Total Billing    : " + str(dataJson['totalBilling']))
                print(TextColor.ENDC)

                if len(dataJson['orders']) > 0:
                    choice = input(
                        TextColor.BLUE + "        Do you wish to see all the orders of " + checkDate + "? (any , 0 ) : " + TextColor.ENDC)

                    if choice != '0':
                        i = 1
                        for order in dataJson['orders']:
                            print("\n\n---------------")
                            print(TextColor.YELLOW + "Order Id : " + str(i))
                            print("Phone number : " + order['phoneNumber'] + TextColor.ENDC)
                            Employee.generateBill(self, order)
                            i += 1

                print("*************************************************************************")


            except:
                print(TextColor.FAIL + "        File for date " + checkDate + " not available !" + TextColor.ENDC)

            toContinue = input(TextColor.BLUE + "\n    Check another date? (any key, 0) : " + TextColor.ENDC)

    def printAndUpdateFiles(self):
        print("\nUpdated Menu : ")
        Admin.displayMenu(self)
        Admin.makeHtmlFile(self)

    def addToMenu(self):
        print("Menu : ")
        Admin.displayMenu(self)
        openFile = open("Menu.json", "r+")
        jsonData = json.loads(openFile.read())

        itemId = jsonData['noOfItems'] + 1000 + 1
        name = input(TextColor.BLUE + "    Enter name of dish : ")
        cp = int(input("    Enter cost price   : "))
        mrp = int(input("    Enter MRP         : "))
        profit = mrp - cp
        description = input("    Enter description  : " + TextColor.ENDC)

        myJson = {
            "itemId": itemId,
            "itemName": name,
            "item_cp": cp,
            "item_mrp": mrp,
            "item_profit": profit,
            "itemDesc": description,
            "isAvailable": True
        }

        jsonData['noOfItems'] += 1
        jsonData['itemsList'].append(myJson)

        openFile = open("Menu.json", "w+")
        openFile.write(json.dumps(jsonData))

        # print(myJson["itemId"])

    def modifyMenu(self):
        print("Existing Menu : ")
        Admin.displayMenu(self)

        openFile = open("Menu.json", "r+")
        jsonData = json.loads(openFile.read())

        itemId = int(input(TextColor.BLUE + "    Enter Id of item to modify : " + TextColor.ENDC))
        itemIndex = itemId - 1000 - 1

        try:
            if itemIndex < 0:
                itemId = itemIndex / 0

            jsonData['itemsList'][itemIndex]
            # print(jsonData['itemsList'][itemIndex]['itemName'])

            toContinue = '1'

            while toContinue != '0':
                choice = int(input(TextColor.BLUE +
                                   "\n    Enter the field you want to modify\n        1)Name\n        2)Cost prize and Selling Price\n        3)Description\n        4)Availablity\n          >>  "))
                print(TextColor.ENDC)
                if choice == 1:
                    jsonData = Admin.modifyName(self, jsonData, itemIndex)

                elif choice == 2:
                    jsonData = Admin.modifyPrice(self, jsonData, itemIndex)

                elif choice == 3:
                    jsonData = Admin.modifyDescription(self, jsonData, itemIndex)

                elif choice == 4:
                    jsonData = Admin.modifyAvailiblity(self, jsonData, itemIndex)

                else:
                    print(TextColor.FAIL + "    Invalid choice, please try again." + TextColor.ENDC)

                toContinue = input(
                    TextColor.BLUE + "\n    Update another field or gop to previous menu ? (any, 0) : " + TextColor.ENDC)

            openFile = open("Menu.json", "w+")
            openFile.write(json.dumps(jsonData))

        except:
            print(TextColor.FAIL + "    Item id dosent exist, please try again !!" + TextColor.ENDC)
            Admin.modifyMenu(self)

    def modifyName(self, jsonData, index):
        jsonData['itemsList'][index]['itemName'] = input(TextColor.GREEN + "            Enter new name : ")
        print("            Name updated" + TextColor.ENDC)
        return jsonData

    def modifyPrice(self, jsonData, index):
        jsonData['itemsList'][index]['item_cp'] = int(input(TextColor.GREEN + "            Enter new cost price : "))
        jsonData['itemsList'][index]['item_mrp'] = int(input("            Enter new Selling price : "))
        jsonData['itemsList'][index]['item_profit'] = jsonData['itemsList'][index]['item_mrp'] - \
                                                      jsonData['itemsList'][index]['item_cp']
        print("            Cost and Selling price updated" + TextColor.ENDC)
        return jsonData

    def modifyDescription(self, jsonData, index):
        jsonData['itemsList'][index]['itemDesc'] = input(TextColor.GREEN + "            Enter new description : ")
        print("            Description updated" + TextColor.ENDC)
        return jsonData

    def modifyAvailiblity(self, jsonData, index):
        if jsonData['itemsList'][index]['isAvailable']:
            jsonData['itemsList'][index]['isAvailable'] = False
            print("            " + TextColor.FAIL + jsonData['itemsList'][index][
                'itemName'] + " is now unavailable." + TextColor.ENDC)
        else:
            jsonData['itemsList'][index]['isAvailable'] = True
            print("            " + TextColor.GREEN + jsonData['itemsList'][index][
                'itemName'] + " is now available." + TextColor.ENDC)
        return jsonData

    def displayMenu(self):
        openFile = open("Menu.json", "r+")
        jsonData = json.loads(openFile.read())

        results = [(item['itemId'], item['itemName'], item['item_cp'], item['item_mrp'], item['item_profit'],
                    item['isAvailable'], item['itemDesc']) for item in jsonData['itemsList']]
        print("\n" + TextColor.CYAN + tabulate(results, headers=["Id", "Name", "Cost price", "Selling Price", "Profit",
                                                                 "Availablity",
                                                                 "Description"], tablefmt="pretty",
                                               colalign="left") + "\n" + TextColor.ENDC)
