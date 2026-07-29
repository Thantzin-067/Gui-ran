import tkinter as tk

root = tk.Tk()
root.title(" YOUR FILES HAVE BEEN ENCRYPTED! ")
root.geometry("650x450")
root.configure(bg="#3a0000")

# Header
label_header = tk.Label(
    root, 
    text=" ATTENTION! YOUR FILES ARE LOCKED ", 
    font=("Arial", 16, "bold"), 
    fg="#ff3333", 
    bg="#3a0000"
)
label_header.pack(pady=15)

msg = (
    "All your personal files, documents, and databases have been encrypted\n"
    "using RSA-2048 & AES-256 Military Encryption.\n\n"
    "To get your files back, you must send 0.5 Bitcoin to:\n"
    "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh\n\n"
    "Contact SOC / IT Admin if you have Enterprise Disaster Recovery!"
)

label_msg = tk.Label(
    root, 
    text=msg, 
    font=("Arial", 10), 
    fg="#ffffff", 
    bg="#3a0000",
    justify="center"
)
label_msg.pack(pady=10)

box_frame = tk.Frame(root, bg="#1a0000", bd=2, relief="solid")
box_frame.pack(pady=10, ipadx=15, ipady=8)

label_status = tk.Label(
    box_frame, 
    text="STATUS: WAITING FOR RANSOM PAYMENT", 
    font=("Courier", 11, "bold"), 
    fg="#ffcc00", 
    bg="#1a0000"
)
label_status.pack()

btn_close = tk.Button(
    root, 
    text="Close Warning Screen", 
    command=root.destroy, 
    bg="#555555", 
    fg="white", 
    font=("Arial", 9, "bold")
)
btn_close.pack(pady=15)

root.mainloop()