from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    upper_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
                    'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    lower_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                     'v', 'w', 'x', 'y', 'z',]
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+','_']

    password_upper_letters = [choice(upper_letters) for _ in range(randint(1, 2))]
    password_lower_letters = [choice(lower_letters) for _ in range(randint(3, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_upper_letters + password_lower_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    email = email_entry.get()
    password = password_entry.get()
    if  len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    elif 1 <= len(password) < 13:
        messagebox.showinfo(title="Oops", message="Please make sure password characters entered are 13")

    else:
        is_ok = messagebox.askokcancel( message=f"These are the details entered: \nUsername: {email} "
                                                              f"\nPassword: {password} \nIs it ok to save?") 
        if is_ok:
            with open("data.txt", "a") as data_file:
                data_file.write(f"{email} | {password}\n")
                password_entry.delete(0, END)

# ---------------------------- VALIDATE PASSWORD ------------------------------ #
def validate_password():
    password = password_entry.get()

    # check if password meets the criteria
    criteria_met = True
    if len(password) < 13:
        criteria_met = False
    if not any(char.isdigit() for char in password):
        criteria_met = False
    if not any(char.isupper() for char in password):
        criteria_met = False
    if not any(char.islower() for char in password):
        criteria_met = False
    if len([char for char in password if char in "!@#$%^&*()_+"]) < 1:
        criteria_met = False

    # update criteria label with tick marks
    criteria_label.config(text=f"Password Criteria: "f" \n At least: "f"\n- 13 characters {'✔' if len(password) >= 13 else ''} " f"\n- 1 upper case {'✔' if any(char.isupper() for char in password) else ''} " f"\n- 7 lower case letters {'✔' if sum(1 for char in password if char.islower()) >= 7 else ''} " f"\n- 1 special characters {'✔' if len([char for char in password if char in '!@#$%^&*()_+']) >= 1 else ''} " f"\n- 2 numbers {'✔' if sum(1 for char in password if char.isdigit()) >= 2 else ''}", 
                          font=("Arial", 12), bg="#7ed9fa", fg="#333", anchor="w", justify="left")
    
    if criteria_met:
        status_label.config(text="Strong password", fg="#008000")
    else:
        status_label.config(text="Weak password", fg="#e60000")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg="#b3e6ff")

#LABELS
# Header Label
header_label = Label(text=f"Welcome! Please enter your password according to the criteria mentioned below.\nIf you are unable to, we will generate a password for you.\nThank you!",
                      bg="#b3e6ff", fg="black", font=("Arial", 14, "bold"), pady=20, padx=20, justify="left", anchor="nw")
header_label.grid(row=0, column=0, columnspan=3) 

#Criteria Label
criteria_label = Label(text=f"Password Criteria:\nAt least: \n- 13 characters \n- 1 upper case letters \n- 7 lower case letters\n- 1 special characters\n- 2 numbers", 
                        font=("Arial", 12), bg="#7ed9fa", fg="#333", anchor="w", justify="left")
criteria_label.grid(row=1, column=0, columnspan=2, sticky="w")

#Email Label
email_label = Label(text="Username:", font=("Arial", 12), bg="#b3e6ff", fg="#333")
email_label.grid(row=4, column=0)

#Password Label
password_label = Label(text="Password:", font=("Arial", 12), bg="#b3e6ff", fg="#333")
password_label.grid(row=5, column=0)

#Status Label
status_label = Label(text="", font=("Arial", 12))
status_label.grid(row=6, column=1)

#Email Entry
email_entry = Entry(width=35)
email_entry.grid(row=4, column=1)

#Password Entry
def toggle_password_visibility():
    if password_entry["show"] == "":
        password_entry.config(show="*")
        show_password_button.config(text="Show Password")
    else:
        password_entry.config(show="")
        show_password_button.config(text="Hide Password")

password_entry = Entry(width=35, show="*")
password_entry.grid(row=5, column=1)

show_password_button = Button(text="Show Password", font=("Arial", 12), bg="#00bbff",command=toggle_password_visibility)
show_password_button.grid(row=5, column=2)

#BUTTONS
#Generate Button
generate_password_button = Button(text="Generate Password", font=("Arial", 12), bg="#00bbff", command=generate_password)
generate_password_button.grid(row=6, column=2)

#Enter Button
add_button = Button(text="Enter", font=("Arial", 12), bg="#00bbff", width=36, command=save)
add_button.grid(row=7, column=1, columnspan=2, pady=10)

#Validate button
validate_button = Button(text="Validate", font=("Arial", 12), bg="#00bbff", command=validate_password)
validate_button.grid(row=6, column=0)

window.mainloop()
