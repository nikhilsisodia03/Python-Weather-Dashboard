# Weather Dashboard Application

A desktop weather application built with Python and Tkinter. It retrieves current weather data from the OpenWeatherMap API, stores search records in SQLite, and plots recorded temperatures with Matplotlib.

## Features

- Search for a city and retrieve current temperature, humidity, and weather conditions.
- Fetch live data from the OpenWeatherMap API.
- Store weather records locally in SQLite.
- Plot previously recorded temperatures with Matplotlib.
- Switch between dark and light interface themes.
- Clear saved weather records.
- Press Enter in the city field to search.

## Technologies

- Python
- Tkinter
- Requests
- SQLite
- Matplotlib
- OpenWeatherMap API

## Requirements

- Python 3.9 or newer
- An OpenWeatherMap API key
- Tkinter (usually included with Python; on some Linux systems it must be installed separately)

## Setup

1. Clone or download this repository.
2. Open a terminal in the project folder.
3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Create an API key in your OpenWeatherMap account.
5. Set the key as an environment variable. Do not paste API keys into source code or commit them to GitHub.

   **macOS / Linux (current terminal session):**
   ```bash
   export OPENWEATHER_API_KEY="your_api_key_here"
   ```

   **Windows PowerShell (current terminal session):**
   ```powershell
   $env:OPENWEATHER_API_KEY="your_api_key_here"
   ```

6. Run the application:

   ```bash
   python main.py
   ```

The application creates `weather.db` in the project folder the first time it runs.

## Project structure

```text
weather-dashboard/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Notes

- An internet connection is required to retrieve live weather data.
- The temperature graph displays records saved on the current computer.
- `weather.db` is intentionally excluded from Git by `.gitignore`.
- Never publish API keys, passwords, or private data in a public repository.

## Possible future improvements

- Add a five-day forecast.
- Display weather icons and wind speed.
- Add search history and city comparison.
- Add automated tests and application packaging.
