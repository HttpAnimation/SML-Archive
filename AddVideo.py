import re
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox, ttk

# Dark mode colors
dark_bg = "#1f1f1f"
dark_fg = "#ffffff"
dark_button_bg = "#353535"
dark_button_fg = "#ffffff"

def extract_video_id(url):
    pattern = r'(?:[?&]v=|\/embed\/|\/\d+\/|\/vi?\/|https:\/\/youtu.be\/|\/v\/|\/e\/|\/u\/\w+\/|https:\/\/www.youtube.com\/user\/\w+\/\w+\/|user\/\w+\/\w+\/|embed\/|youtu.be\/|\/v=|\/e=|\/u=|https:\/\/www.youtube.com\/v\/)([^#&?\/]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None

def get_video_title(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find("title").text
        return title
    except:
        return None

def video_already_exists(html_content, video_title):
    pattern = re.compile(r'<p>\s*{}\s*</p>'.format(re.escape(video_title)), re.IGNORECASE)
    return pattern.search(html_content) is not None

def add_video_to_html():
    video_url = url_entry.get()

    video_id = extract_video_id(video_url)
    if video_id is None:
        messagebox.showerror("Error", "Invalid YouTube video URL. Please provide a valid URL.")
        return

    video_title = get_video_title(video_url)
    if video_title is None:
        messagebox.showerror("Error", "Unable to retrieve the video title. Please check the URL or try again later.")
        return

    with open('index.html', 'r') as file:
        html_content = file.read()

    if video_already_exists(html_content, video_title):
        messagebox.showerror("Error", "The video already exists.")
        return

    video_section_start = html_content.find('<section>\n      <h2>Videos</h2>')
    video_section_end = html_content.find('</section>', video_section_start) + len('</section>')

    video_html = f'''
    <section>
      <div class="video-container">
        <iframe src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe>
      </div>
      <p>{video_title}</p>
    </section>
    '''

    updated_html_content = html_content[:video_section_end] + video_html + html_content[video_section_end:]

    with open('index.html', 'w') as file:
        file.write(updated_html_content)

    messagebox.showinfo("Success", f"Video '{video_title}' added successfully!")

    # Clear the text box
    url_entry.delete(0, tk.END)

def toggle_dark_mode():
    global dark_mode

    if dark_mode:
        dark_mode = False
        root.config(bg="white")
        title_label.config(fg="black")
        url_label.config(fg="black")
        add_button.config(bg="SystemButtonFace", fg="black")
        dark_mode_button.config(text="Dark Mode")
    else:
        dark_mode = True
        root.config(bg=dark_bg)
        title_label.config(fg=dark_fg)
        url_label.config(fg=dark_fg)
        add_button.config(bg=dark_button_bg, fg=dark_button_fg)
        dark_mode_button.config(text="Light Mode")

# Create the main window
root = tk.Tk()
root.title("Add Video to HTML")
root.resizable(False, False)

# Dark mode flag
dark_mode = False

# Set dark mode if enabled
if dark_mode:
    root.config(bg=dark_bg)

# Create and configure the URL label
url_label = tk.Label(root, text="Video URL:")
url_label.pack()

# Create and configure the URL entry field
url_entry = tk.Entry(root)
url_entry.pack()

# Create and configure the add button
add_button = ttk.Button(root, text="Add Video", command=add_video_to_html)
add_button.pack()

# Create and configure the dark mode button
dark_mode_button = ttk.Button(root, text="Dark Mode", command=toggle_dark_mode)
dark_mode_button.pack()

# Start the GUI main loop
root.mainloop()
