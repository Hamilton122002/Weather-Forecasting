import requests
import tkinter as tk
from tkinter import messagebox
import colorsys

# Set your OpenWeatherMap API Key and endpoint
API_KEY = "ENTER YOUR API KEY"
ENDPOINT = "http://api.openweathermap.org/data/2.5/weather"

# Create the main application window
app = tk.Tk()
app.title("Live Weather App")

# Function to fetch weather data
def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showerror("Error", "Please enter a city")
        return

    querystring = {"q": city, "appid": API_KEY, "units": "metric"}

    response = requests.get(ENDPOINT, params=querystring)

    data = response.json()

    if response.status_code == 200:
        weather = data["weather"][0]["main"]
        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]
        result_label.config(text=f"Weather: {weather}\nTemperature: {temperature:.1f}°C\nDescription: {description}")

        # Set background color and text color based on temperature
        normalized_temp = (temperature + 10) / 40  # Normalize temperature to a range of 0 to 1
        bg_color = interpolate_color(normalized_temp)
        text_color = "#FFFFFF" if normalized_temp > 0.5 else "#000000"
        app.configure(bg=bg_color)
        result_label.configure(bg=bg_color, fg=text_color)
    else:
        messagebox.showerror("Error", "Unable to fetch weather data")

# Function to interpolate color based on a normalized value
def interpolate_color(value):
    # Interpolate between blue and red (cold to hot)
    r, g, b = colorsys.hsv_to_rgb(0.66 * value, 1, 1)
    return f"#{int(r*255):02X}{int(g*255):02X}{int(b*255):02X}"

# Styling
app.geometry("300x250")

city_label = tk.Label(app, text="Enter City:", font=("Helvetica", 14), fg="Black")
city_label.pack(pady=10)

city_entry = tk.Entry(app, font=("Helvetica", 12))
city_entry.pack()

get_weather_button = tk.Button(app, text="Get Weather", font=("Helvetica", 12), command=get_weather, fg="Black")
get_weather_button.pack(pady=10)

result_label = tk.Label(app, text="", font=("Helvetica", 12))
result_label.pack()

# Run the application loop
app.mainloop()
