import pandas as pd
import matplotlib.pyplot as plt
import pickle
import os
from datetime import datetime 

def add_expense(df):

   # Description Validation
    while True:

        description = input("\nEnter expense description: ").strip()

        if description == "":

            print("Description cannot be empty!")

        else:

            break

# Amount Validation
    while True:

            try:

                amount = float(input("Enter amount: "))

                if amount <= 0:

                    print("Amount must be greater than 0!")

                    continue

                break

            except ValueError:

                print("Invalid amount! Please enter numbers only.")

       # AI Prediction
    description_vector = vectorizer.transform([description])

    predicted_category = model.predict(description_vector)[0]

    confidence = model.predict_proba(description_vector).max()

    print(f"\nPredicted Category: {predicted_category}")

    print(f"Confidence: {confidence:.2f}")

    if confidence < 0.50:

        print("\nWarning: AI is not very confident about this prediction.")

        # User Confirmation
        confirm = input("Use this category? (yes/no): ")

        if confirm.lower() == "yes":

            category = predicted_category

        else:

            while True:

                category = input("Enter correct category: ").strip().title()

                if category == "":

                    print("Category cannot be empty!")

                else:

                    break

        category = category.strip().title()

        # Duplicate Check
        duplicate = (
            (df["description"] == description) &
            (df["amount"] == amount) &
            (df["category"] == category)
        ).any()

        if duplicate:

            print("\nThis expense already exists!")

            return df

        # Use Date time 

        curent_date = datetime.now().strftime("%d-%m-%y")

        # Create Expense
        new_data = {
            "date" : curent_date,
            "description": description,
            "amount": amount,
            "category": category
        }

        # Add Expense
        df = pd.concat(
            [df, pd.DataFrame([new_data])],
            ignore_index=True
        )

        # Save Data
        df.to_csv("expenses.csv", index=False)

        print("\nExpense Added Successfully!")
                
    return df

def view_expense(df):

    if len(df) == 0:

        print("\nNo expenses found!")

        return

    print("\n===== Expense Data =====")

    print(df)

    return df

def update_expense(df):

        if df.empty:

            print("\nNo expenses found!")

            return

        print(df)
        try:
            index = int(input("\nEnter row index to update: "))
            if index not in df.index:
                print("Invalid Index!")
                return

        except ValueError:
                print("Please Enter Number Only!")
                return

        new_description = input("New Description: ").strip()

        if new_description == "":
            print("Description cannot be empty!")
            return

        df.at[index, "description"] = new_description

        try:

            amount = float(input("Enter amount: "))

            if amount <= 0:

                print("Amount must be greater than 0!")

                return

        except ValueError:

            print("Invalid amount! Please enter numbers only.")

        df.at[index, "amount"] = amount

        new_category = input("New Category: ").strip().title()

        if new_category == "":
            print("Category cannot be empty!")
            return

        df.at[index, "category"] = new_category

        df.to_csv("expenses.csv", index=False)

        print("\nExpense Updated Successfully!")

        return df

def delete_expense(df):
    
        print(df)

        try:
            index = int(input("\nEnter row index to delete: "))
            if index not in df.index:
                print("Invalid Index!")
                return

        except ValueError:
                print("Please Enter Number Only!")
                return

        df = df.drop(index).reset_index(drop=True)

        df.to_csv("expenses.csv", index=False)

        print("\nExpense Deleted Successfully!")

        return df

def analytics_expense(df):


        if df.empty:

            print("No expenses found.")

            return

        total = df["amount"].sum()
        

        # Adding Date column

        today = datetime.now().strftime("%d-%m-%y")

        current_month = datetime.now().strftime("%m-%y")

        month_expense = df[df["date"].str[3:] == current_month]["amount"].sum()

        today_expense = df[df["date"] == today]["amount"].sum()

        print("\nToday's Expense:", today_expense)

        print("\n   This Month Expense:", month_expense)

        print("\nTotal Expense:", total)


        category_total = df.groupby("category")["amount"].sum()

        print("\n===== Category Wise Expense =====")

        print(category_total)

        
        #Highest Category Expense

        if len(category_total) > 0:

            highest_category = category_total.idxmax()

            highest_amount = category_total.max()

            percentage = (highest_amount / total) * 100

            print("\nHighest Spending Category:", highest_category)

            print(f"{highest_category} accounts for {percentage:.2f}% of your total spending.")

            if percentage > 50:

                print(f"\nWarning: More than half of your spending is on {highest_category}.")

            else:

                print("\nYour spending is fairly balanced.")

            print("Amount:", highest_amount)
        
        else:
            print("\nNo category data found.")


        # Graph
        if len(df) == 0:
            print("No expenses found.")
            return
        
        category_total.plot(kind="bar")

        plt.title("Expense By Category")

        plt.xlabel("Category")

        plt.ylabel("Amount")

        plt.show()

        return df

def exit_expense(df):

        print("\nExiting App...")

        return df

# Load ML model
model = pickle.load(open("model.pkl", "rb"))

# Load vectorizer
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

if not os.path.exists("expenses.csv"):
    pd.DataFrame(
        columns=["date","description","amount","category"]
    ).to_csv("expenses.csv", index=False)

# Main loop
while True:

    print("\n===== AI Expense Tracker =====")

    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Update Expense")
    print("4. Delete Expense")
    print("5. Show Analytics")
    print("6. Exit")

    choice = input("\nEnter your choice: ")

    # Load latest data
    df = pd.read_csv("expenses.csv")

    # ADD EXPENSE

    if choice == "1":

        df = add_expense(df)

    # VIEW EXPENSES
    elif choice == "2":
        
        view_expense(df)

    # UPDATE EXPENSE
    elif choice == "3":

        update_expense(df)

    # DELETE EXPENSE
    elif choice == "4":

        delete_expense(df)

    # ANALYTICS
    elif choice == "5":

        analytics_expense(df)

    # EXIT
    elif choice == "6":

        exit_expense(df)
        break

    else:

        print("\nInvalid Choice!")