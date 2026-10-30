import os
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib.pyplot as plt
import requests

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "weather.db")


def initialize_database():
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS weather (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                temperature REAL NOT NULL,
                humidity REAL NOT NULL,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


def fetch_weather():
    city = city_entry.get().strip()

    if not city:
        messagebox.showerror("Missing city", "Please enter a city name.")
        return

    if not API_KEY:
        messagebox.showerror(
            "API key missing",
            "Set the OPENWEATHER_API_KEY environment variable before running the app."
        )
        return

    try:
        response = requests.get(
            BASE_URL,
            params={"q": city, "appid": API_KEY, "units": "metric"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"].title()
        city_name = data.get("name", city)

        with sqlite3.connect(DB_PATH) as connection:
            connection.execute(
                "INSERT INTO weather (city, temperature, humidity) VALUES (?, ?, ?)",
                (city_name, temperature, humidity)
            )

        result_label.config(
            text=f"{city_name}\n{description}\nTemperature: {temperature} °C\nHumidity: {humidity}%",
            fg="white" if dark_mode["enabled"] else "black"
        )

    except requests.exceptions.HTTPError:
        messagebox.showerror("Weather service error", "City not found or API request rejected.")
    except requests.exceptions.RequestException as error:
        messagebox.showerror("Network error", f"Could not retrieve weather data:\n{error}")
    except (KeyError, IndexError, ValueError):
        messagebox.showerror("Data error", "The weather service returned an unexpected response.")


def show_graph():
    try:
        with sqlite3.connect(DB_PATH) as connection:
            rows = connection.execute(
                "SELECT city, temperature, recorded_at FROM weather ORDER BY id"
            ).fetchall()

        if not rows:
            messagebox.showinfo("No data", "Fetch weather data before viewing the graph.")
            return

        labels = [f"{row[0]} ({row[2]})" for row in rows]
        temperatures = [row[1] for row in rows]

        plt.figure(figsize=(10, 5))
        plt.plot(labels, temperatures, marker="o")
        plt.title("Recorded Temperatures")
        plt.xlabel("City and recording time")
        plt.ylabel("Temperature (°C)")
        plt.xticks(rotation=35, ha="right")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    except sqlite3.Error as error:
        messagebox.showerror("Database error", str(error))


def reset_data():
    if not messagebox.askyesno("Confirm reset", "Delete all saved weather records?"):
        return

    try:
        with sqlite3.connect(DB_PATH) as connection:
            connection.execute("DELETE FROM weather")
        messagebox.showinfo("Reset complete", "All saved weather records were deleted.")
    except sqlite3.Error as error:
        messagebox.showerror("Database error", str(error))


def toggle_mode():
    dark_mode["enabled"] = not dark_mode["enabled"]
    if dark_mode["enabled"]:
        root.configure(bg="#1e1e1e")
        title.configure(bg="#1e1e1e", fg="white")
        frame.configure(bg="#2b2b2b")
        city_label.configure(bg="#2b2b2b", fg="white")
        result_label.configure(bg="#3c3f41", fg="white")
    else:
        root.configure(bg="#f4f6f7")
        title.configure(bg="#f4f6f7", fg="black")
        frame.configure(bg="white")
        city_label.configure(bg="white", fg="black")
        result_label.configure(bg="white", fg="black")


initialize_database()

dark_mode = {"enabled": True}
root = tk.Tk()
root.title("Weather Dashboard")
root.geometry("500x600")
root.configure(bg="#1e1e1e")

style = ttk.Style()
style.theme_use("default")
style.configure("TButton", font=("Arial", 11), padding=6)
style.configure("TEntry", padding=5)

title = tk.Label(
    root, text="Weather Dashboard",
    font=("Arial", 20, "bold"), bg="#1e1e1e", fg="white"
)
title.pack(pady=15)

frame = tk.Frame(root, bg="#2b2b2b", bd=2, relief="ridge")
frame.pack(pady=10, padx=20, fill="x")

city_label = tk.Label(frame, text="Enter city:", bg="#2b2b2b", fg="white")
city_label.pack(pady=5)

city_entry = ttk.Entry(frame, width=30)
city_entry.pack(pady=5)
city_entry.bind("<Return>", lambda event: fetch_weather())

ttk.Button(frame, text="Get Weather", command=fetch_weather).pack(pady=8)
ttk.Button(root, text="Reset Data", command=reset_data).pack(pady=5)

result_label = tk.Label(
    root, text="Weather information will appear here",
    font=("Arial", 13), bg="#3c3f41", fg="white",
    width=34, height=6, wraplength=380
)
result_label.pack(pady=15)

ttk.Button(root, text="Show Temperature Graph", command=show_graph).pack(pady=5)
ttk.Button(root, text="Toggle Dark / Light Mode", command=toggle_mode).pack(pady=5)

root.mainloop()
