import speedtest
import tkinter as tk
from tkinter import messagebox
import csv
import os
import time

# =========================================================
# Network Performance & Traffic Analysis Tool
# This tool measures Download, Upload, and Ping speeds.
# It analyzes the results based on Traffic Analysis concepts (Topic 3).
# It automatically saves the results to a CSV file.
# =========================================================

def run_speed_test():
    # Disable the button while testing
    btn_start.config(state=tk.DISABLED, text="Testing... Please Wait")
    root.update()

    try:
        # 1. Connect to the best server (Ookla)
        st = speedtest.Speedtest()
        st.get_best_server()
        server_info = st.results.server
        
        # 2. Measure speeds
        download_speed = st.download() / 1_000_000  # Convert to Megabits
        upload_speed = st.upload() / 1_000_000      # Convert to Megabits
        ping = st.results.ping
        
        # 3. Display results in the GUI
        lbl_server.config(text=f"Server: {server_info['sponsor']} ({server_info['country']})")
        lbl_download.config(text=f"Download Speed: {download_speed:.2f} Mbps")
        lbl_upload.config(text=f"Upload Speed: {upload_speed:.2f} Mbps")
        lbl_ping.config(text=f"Ping (Latency): {ping:.2f} ms")
        
        # 4. Analyze results (Traffic Analysis) - Linked to Lecture Topic 3
        analysis = analyze_results(download_speed, upload_speed, ping)
        lbl_analysis.config(text=analysis)
        
        # 5. Save results to CSV (Creates the file if it doesn't exist)
        save_to_csv(download_speed, upload_speed, ping, server_info)
        
        messagebox.showinfo("Success", "Test completed successfully! Results saved to speed_test_results.csv")
        
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during the test: {e}")
    
    finally:
        # Re-enable the button
        btn_start.config(state=tk.NORMAL, text="Start Test")

def analyze_results(download, upload, ping):
    report = ""
    if download > 50:
        report += "✔️ Download speed is Excellent.\n"
    elif download > 10:
        report += "⚠️ Download speed is Moderate (Possible Congestion).\n"
    else:
        report += "✖️ Download speed is Poor (Bottleneck detected).\n"

    if ping < 50:
        report += "✔️ Latency is Low (Stable connection).\n"
    else:
        report += "⚠️ Latency is High (High latency detected).\n"
    
    return report

def save_to_csv(download, upload, ping, server):
    filename = "speed_test_results.csv"
    
    # Check if the file exists (If not, it will be created)
    file_exists = os.path.isfile(filename)
    
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # If the file is new, write the header row
        if not file_exists:
            writer.writerow(["Time", "Server", "Country", "Download (Mbps)", "Upload (Mbps)", "Ping (ms)"])
        
        # Write the data row
        writer.writerow([
            time.strftime("%Y-%m-%d %H:%M:%S"), 
            server['sponsor'], 
            server['country'], 
            f"{download:.2f}", 
            f"{upload:.2f}", 
            f"{ping:.2f}"
        ])

# ---------------------------------------------------------
# Build the Graphical User Interface (GUI)
# ---------------------------------------------------------
root = tk.Tk()
root.title("Network Performance & Traffic Analysis Tool")
root.geometry("500x450")
root.configure(bg="#f0f0f0")

# Title
lbl_title = tk.Label(root, text="Network Performance & Traffic Analysis Tool", font=("Arial", 14, "bold"), bg="#f0f0f0")
lbl_title.pack(pady=10)

# Start Button
btn_start = tk.Button(root, text="Start Test", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=run_speed_test)
btn_start.pack(pady=10)

# Server Info
lbl_server = tk.Label(root, text="Server: Waiting to start...", bg="#f0f0f0", font=("Arial", 10))
lbl_server.pack(pady=5)
# Results
lbl_download = tk.Label(root, text="Download Speed: --", bg="#f0f0f0", font=("Arial", 12))
lbl_download.pack(pady=5)

lbl_upload = tk.Label(root, text="Upload Speed: --", bg="#f0f0f0", font=("Arial", 12))
lbl_upload.pack(pady=5)

lbl_ping = tk.Label(root, text="Ping (Latency): --", bg="#f0f0f0", font=("Arial", 12))
lbl_ping.pack(pady=5)

# Analysis (Traffic Analysis)
lbl_analysis = tk.Label(root, text="", bg="#f0f0f0", font=("Arial", 10), fg="blue", justify="left")
lbl_analysis.pack(pady=15)

# Note (for the Doctor)
lbl_note = tk.Label(root, text="Note: The file 'speed_test_results.csv' will be created automatically in the same directory.", bg="#f0f0f0", font=("Arial", 8), fg="gray")
lbl_note.pack(pady=5)

root.mainloop()