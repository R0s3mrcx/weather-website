# Weather Online

<p align="center">
A web application to get real-time weather updates for cities around the world.
</p>

![weather-web](https://github.com/user-attachments/assets/abf3458c-4ec8-44eb-94e2-db82843133b2)

# Features

* Responsive design optimized for mobile and desktop.
* Utilizes APIs to fetch real-time weather data.
* Provides weather details including temperature, humidity, and wind speed.
* Developed using the [Reflex](https://reflex.dev) *framework* with pure Python.

# Local Execution

1. Create a Python virtual environment:
```
python -m venv .venv
```

2. Activate the virtual environment:

Windows:
```
.venv\Scripts\activate
```
MacOS/Linux:
```
source .venv/bin/activate
```

3. Install the required dependencies:
```
python -m pip install -r requirements.txt
```

4. Set up the environment variable for API usage in the .env file:
```
API_KEY=<YOUR_API_KEY>
```

You need to obtain an API key from:

- [OpenWeatherMap](https://openweathermap.org/api)

5. Initialize Reflex:
```
reflex init
```

6. Run the application using Reflex:
```
reflex run
```

> [!NOTE]
> Access http://localhost:3000/ to view the web application.
