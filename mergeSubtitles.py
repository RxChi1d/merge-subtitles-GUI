import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import opencc
import os
import subprocess

# Conversion function
def convert_simplified_to_traditional(input_file, output_path):
    converter = opencc.OpenCC('s2tw')
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    traditional_content = converter.convert(content)
    temp_path = os.path.join(os.path.dirname(output_path), 'temp.srt')
    with open(temp_path, 'w', encoding='utf-8') as f:
        f.write(traditional_content)
    return temp_path

# Merge function
def merge_subtitles():
    log_text.delete(1.0, tk.END)  # Clear log block
    mkv_path = mkv_entry.get()
    srt_path = srt_entry.get()
    output_path = output_entry.get()

    temp_srt_path = os.path.join(os.path.dirname(output_path), 'temp.srt')
    
    # Check if temp.srt exists
    if os.path.exists(temp_srt_path):
        if not messagebox.askyesno("File Exists", f"'temp.srt' already exists in {os.path.dirname(output_path)}. Do you want to replace it?"):
            log_text.insert(tk.END, "File 'temp.srt' already exists. Process terminated.\n")
            return
        else:
            os.remove(temp_srt_path)
            log_text.insert(tk.END, "Existing 'temp.srt' removed.\n")
    
    # Check if output file exists
    if os.path.exists(output_path):
        if not messagebox.askyesno("File Exists", f"'{os.path.basename(output_path)}' already exists. Do you want to replace it?"):
            log_text.insert(tk.END, f"File '{os.path.basename(output_path)}' already exists. Process terminated.\n")
            return
        else:
            os.remove(output_path)
            log_text.insert(tk.END, f"Existing file '{os.path.basename(output_path)}' removed.\n")

    log_text.insert(tk.END, "Converting subtitles...\n")
    temp_srt_path = convert_simplified_to_traditional(srt_path, output_path)

    log_text.insert(tk.END, "Starting merge with ffmpeg...\n")

    lang_map = {
        'English': ('eng', 'English'),
        'zh-TW': ('cht', 'zh-TW')
    }
    lang, subtitle_title = lang_map[language_combobox.get()]

    command = [
        "ffmpeg", 
        "-i", mkv_path, 
        "-i", temp_srt_path, 
        "-c:v", "copy", 
        "-c:a", "copy", 
        "-c:s", "srt", 
        "-map", "0", 
        "-map", "1",
        "-metadata:s:s:0", f"language={lang}",
        "-metadata:s:s:0", f"title={subtitle_title}",
        "-disposition:s:s:0", "default",
        output_path
    ]
    try:
        subprocess.run(command, check=True)
        log_text.insert(tk.END, "Merge successful!\n")

        # Pop up a window asking whether to delete temp.srt
        if messagebox.askyesno("Remove temp.srt", "Do you want to remove temp.srt?"):
            os.remove(temp_srt_path)
            log_text.insert(tk.END, "temp.srt removed successfully.\n")
        else:
            log_text.insert(tk.END, "temp.srt retained.\n")
    except subprocess.CalledProcessError as e:
        log_text.insert(tk.END, f"Error occurred during merging: {e}\n")

root = tk.Tk()
root.title("Merge Subtitles")

# mkv選擇
mkv_label = tk.Label(root, text="MKV 檔案位置:")
mkv_label.pack(pady=10)
mkv_entry = tk.Entry(root, width=50)
mkv_entry.pack(pady=5)
mkv_button = tk.Button(root, text="選擇 MKV 檔案", command=lambda: mkv_entry.insert(0, filedialog.askopenfilename()))
mkv_button.pack(pady=5)

# srt選擇
srt_label = tk.Label(root, text="SRT 檔案位置:")
srt_label.pack(pady=10)
srt_entry = tk.Entry(root, width=50)
srt_entry.pack(pady=5)
srt_button = tk.Button(root, text="選擇 SRT 檔案", command=lambda: srt_entry.insert(0, filedialog.askopenfilename()))
srt_button.pack(pady=5)

# 輸出選擇
output_label = tk.Label(root, text="合併後的 MKV 檔案位置:")
output_label.pack(pady=10)
output_entry = tk.Entry(root, width=50)
output_entry.pack(pady=5)
output_button = tk.Button(root, text="選擇輸出位置", command=lambda: output_entry.insert(0, filedialog.asksaveasfilename()))
output_button.pack(pady=5)

# 語言選單
language_label = tk.Label(root, text="字幕語言:")
language_label.pack(pady=10)
language_combobox = ttk.Combobox(root, values=["English", "zh-TW"], state="readonly")
language_combobox.set("English")
language_combobox.pack(pady=5)

# 進程 block
log_label = tk.Label(root, text="運行的過程:")
log_label.pack(pady=10)
log_text = tk.Text(root, height=10, width=60)
log_text.pack(pady=10)

# 合併按鈕
merge_button = tk.Button(root, text="開始合併", command=merge_subtitles)
merge_button.pack(pady=20)

root.mainloop()
