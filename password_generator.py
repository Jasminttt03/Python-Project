import tkinter as tk
from tkinter import messagebox
import random
import string

# ---------- 1.  Helper: evaluate password strength ----------
def evaluate_strength(pwd: str) -> tuple[str, str]:
    """
    Return a (label, color) describing how strong the password is.
    Very simple scoring:
        +1 if length >= 8
        +1 if length >= 12
        +1 for each character class present (upper, lower, digit, special)
    Score -> strength:
        0-5 : Weak      (red)
        6-8 : Medium    (yellow)
        9-12: Strong    (green)
    """
    if not pwd:
        return "", "black"
    
    # Count character-class presence
    has_upper   = any(c.isupper() for c in pwd)
    has_lower   = any(c.islower() for c in pwd)
    has_digit   = any(c.isdigit() for c in pwd)
    has_special = any(c in string.punctuation for c in pwd)

    score = 0
    length = len(pwd)
    if length >= 8:
        score += 1
    if length >= 12:
        score += 1
    score += has_upper + has_lower + has_digit + has_special

    match score:
        case 0 | 1 | 2:
            return "Weak", "red"
        case 3 | 4:
            return "Medium", "yellow"
        case 5 | 6:
            return "Strong", "green"
        
   # ---------- 2.  Generate password ----------
def generate_password():
    """Generate a secure password based on user preferences, then show strength."""
    try:
        length = int(length_entry.get())
        if length < 4:
            messagebox.showerror("Error", "Password length must be at least 4")
            return
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number for length.")
        return
    
    #Read check-box states (True/False)
    use_upper = var_upper.get()
    use_lower = var_lower.get()
    use_digits = var_digits.get()
    use_special = var_special.get()

    # If user deselected everything, abort
    if not (use_upper or use_lower or use_digits or use_special):
        messagebox.showerror("Error", "Please select at least one character type.")
        return
    
    # Build the character pool string & & guarantee at least one of each chosen type
    char_pool = ""
    password_chars = []

    if use_upper:
        char_pool += string.ascii_uppercase
        password_chars.append(random.choice(string.ascii_uppercase))
    if use_lower:
        char_pool += string.ascii_lowercase
        password_chars.append(random.choice(string.ascii_lowercase))
    if use_digits:
        char_pool += string.digits
        password_chars.append(random.choice(string.digits))
    if use_special:
        char_pool += string.punctuation
        password_chars.append(random.choice(string.punctuation))

    # Fill remaining slots, shuffle for unpredictability
    remaining = length - len(password_chars)
    password_chars += random.choices(char_pool, k=remaining)
    random.shuffle(password_chars)

    password = "".join(password_chars)

    # Show password
    output_entry.delete(0, tk.END)
    output_entry.insert(0, password)

    # Evaluate & display strength
    strength, color = evaluate_strength(password)
    strength_label.config(text=f"Strength: {strength}", fg = color)

# ---------- 3.  Copy to clipboard ----------
def copy_to_clipboard():
    """Copy the generated password to the clipboard."""
    pwd = output_entry.get()
    if pwd:
        root.clipboard_clear()
        root.clipboard_append(pwd)
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    else:
        messagebox.showwarning("Empty", "No password to copy")

# ---------- 4.  GUI layout ----------
root = tk.Tk()
root.title("Secure Password Generator")
root.geometry("420x380")
root.resizable(False, False)

#Password length
tk.Label(root, text="Password Length:").pack(pady=(12,0))
length_entry = tk.Entry(root)
length_entry.pack()

#Check-boxes for options
var_upper = tk.BooleanVar(value=True)
var_lower = tk.BooleanVar(value=True)
var_digits = tk.BooleanVar(value=True)
var_special = tk.BooleanVar(value=False)

tk.Checkbutton(root, text="Include Uppercase Letters", variable=var_upper).pack(anchor="w", padx=22)
tk.Checkbutton(root, text="Include Lowercase Letters", variable=var_lower).pack(anchor="w", padx=22)
tk.Checkbutton(root, text="Include Numbers", variable=var_digits).pack(anchor="w", padx=22)
tk.Checkbutton(root, text="Include Special Characters", variable=var_special).pack(anchor="w", padx=22)

# Generate button
tk.Button(root, text="Generate Password", command=generate_password, bg="lightblue").pack(pady=12)

# Output field
tk.Label(root, text="Generated Password:").pack()
output_entry = tk.Entry(root, width=46, font=("Consolas", 10))
output_entry.pack()

#Strength display
strength_label = tk.Label(root, text="Strength:", font=("Arial", 10, "bold"))
strength_label.pack(pady=4)

# Copy button
tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard, bg="lightgreen").pack(pady=6)

root.mainloop()
