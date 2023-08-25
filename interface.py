import tkinter as tk
from tkinter import ttk
import getDcSpec
from decouple import config

username = config('USERNAME1')
password = config('PASSWORD')

def on_button_click():
    provider = input_var1.get()
    consumer = input_var2.get()
    
    # Call the create_contract function from contract_logic module
    contract_info = getDcSpec.get_data_contract_specification(username, password, provider, consumer)
    
    result_label.config(text=contract_info)
    
    # Clear input fields after clicking the button
    input_var1.set("")  # Clear provider input field
    input_var2.set("")  # Clear consumer input field

app = tk.Tk()
app.title("Collibra Data Contract creation")

# Set the default window size (width x height)
app.geometry("400x250")
top_padding = 35    

# Create styles for labels and buttons
style = ttk.Style()
style.configure("TLabel", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12))

# Create and position the first input field
label1 = ttk.Label(app, text="Insert the name of the Provider DP:")
label1.pack(pady=(top_padding, 10))
input_var1 = tk.StringVar()
input1 = ttk.Entry(app, textvariable=input_var1)
input1.pack(pady=5)

# Create and position the second input field
label2 = ttk.Label(app, text="Insert the name of the Consumer DP:")
label2.pack(pady=10)
input_var2 = tk.StringVar()
input2 = ttk.Entry(app, textvariable=input_var2)
input2.pack(pady=5)

# Create and position the button
button = ttk.Button(app, text="Establish Contract", command=on_button_click, style="TButton")
button.pack(pady=15)

# Create a label to display the selected options
result_label = ttk.Label(app, text="", style="TLabel")
result_label.pack()

app.mainloop()
input_var1 = None
input_var2 = None