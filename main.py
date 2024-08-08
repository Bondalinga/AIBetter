import openai
import keyboard
import pyperclip
import pyautogui
import time
import tkinter as tk

# Set your OpenAI API key
api_key = ""
openai.api_key = api_key

# Create the main application window
root = tk.Tk()
root.overrideredirect(True)  # Remove the top bar
root.geometry("400x150+1600+900")  # Adjust position for bottom-right corner
root.attributes("-topmost", True)

# Allow window dragging
def start_drag(event):
    root.x = event.x
    root.y = event.y

def do_drag(event):
    x = root.winfo_pointerx() - root.x
    y = root.winfo_pointery() - root.y
    root.geometry(f"+{x}+{y}")

root.bind("<Button-1>", start_drag)
root.bind("<B1-Motion>", do_drag)

# Create a canvas for rounded corners
canvas = tk.Canvas(root, width=400, height=150, highlightthickness=0)
canvas.pack()

# Function to create a rounded rectangle
def create_rounded_rectangle(x1, y1, x2, y2, r, **kwargs):
    points = [
        x1+r, y1,
        x1+r, y1,
        x2-r, y1,
        x2-r, y1,
        x2, y1,
        x2, y1+r,
        x2, y1+r,
        x2, y2-r,
        x2, y2-r,
        x2, y2,
        x2-r, y2,
        x2-r, y2,
        x1+r, y2,
        x1+r, y2,
        x1, y2,
        x1, y2-r,
        x1, y2-r,
        x1, y1+r,
        x1, y1+r,
        x1, y1
    ]
    return canvas.create_polygon(points, **kwargs, smooth=True)

# Create rounded rectangle background
bg = create_rounded_rectangle(0, 0, 400, 150, 20, fill="lightgray")

# Create a label to display the status
status_label = tk.Label(root, text="Waiting...", font=("Helvetica", 12), bg="lightgray")
status_label.place(relx=0.5, rely=0.3, anchor="center")

# Create a label to display instructions
instructions = tk.Label(root, text="Press F1 to Complete Text, F2 to Correct Grammar, F3 to Improve Style, F4 to Simplify Text", font=("Helvetica", 10), bg="lightgray")
instructions.place(relx=0.5, rely=0.6, anchor="center")

# Create an exit button
exit_button = tk.Button(root, text="Exit", command=root.destroy, font=("Helvetica", 10), bg="lightgray")
exit_button.place(relx=0.5, rely=0.8, anchor="center")

# Define the functions for text processing
def complete_text(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional writer that uses the same writing style you are provided but expands text. Do not reply to my text and only do your intended purpose"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.7
    )
    return response['choices'][0]['message']['content'].strip()

def correct_grammar(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional writer that corrects grammar. If the grammar is correct don't output anything. Do not reply to my text and only do your intended purpose"},
            {"role": "user", "content": "Correct the grammar of the following text:\n" + prompt}
        ],
        max_tokens=500,
        temperature=0.7
    )
    return response['choices'][0]['message']['content'].strip()

def improve_style(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional writer that improves writing style. Do not reply to my text and only do your intended purpose"},
            {"role": "user", "content": "Improve the style of the following text:\n" + prompt}
        ],
        max_tokens=500,
        temperature=0.7
    )
    return response['choices'][0]['message']['content'].strip()

def simplify_text(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional writer that simplifies text to make it easier to understand. Do not reply to my text and only do your intended purpose"},
            {"role": "user", "content": "Simplify the following text:\n" + prompt}
        ],
        max_tokens=500,
        temperature=0.7
    )
    return response['choices'][0]['message']['content'].strip()

# Clipboard handling functions
def get_clipboard_text():
    try:
        return pyperclip.paste()
    except Exception as e:
        print(f"Error getting clipboard text: {e}")
        return ""

def set_clipboard_text(text):
    try:
        pyperclip.copy(text)
    except Exception as e:
        print(f"Error setting clipboard text: {e}")

# Processing function
def process_text_with_function(func):
    status_label.config(text="Processing...")
    root.update()
    
    # Simulate Ctrl+C to copy the highlighted text
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.1)  # Short delay to ensure the clipboard is updated

    original_text = get_clipboard_text()
    if original_text:
        try:
            processed_text = func(original_text)
            set_clipboard_text(processed_text)
            pyautogui.hotkey('ctrl', 'v')
            status_label.config(text="Processed")
        except Exception as e:
            print(f"Error processing text: {e}")
            status_label.config(text="Error")
    else:
        status_label.config(text="No text copied")
    
    root.update()
    time.sleep(2)
    status_label.config(text="Waiting...")
    root.update()

# Define hotkey actions
def on_f1():
    process_text_with_function(complete_text)

def on_f2():
    process_text_with_function(correct_grammar)

def on_f3():
    process_text_with_function(improve_style)

def on_f4():
    process_text_with_function(simplify_text)

# Register hotkeys
keyboard.add_hotkey('f1', on_f1)
keyboard.add_hotkey('f2', on_f2)
keyboard.add_hotkey('f3', on_f3)
keyboard.add_hotkey('f4', on_f4)

# Start the main loop for the tkinter window
print("Script running... Press F1, F2, F3, or F4 to process highlighted text.")
root.mainloop()
print("Script terminated.")
keyboard.wait('esc')
