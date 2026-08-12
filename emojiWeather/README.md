# 🌦️ Simple Weather App

A clean and lightweight weather application that fetches real-time weather data using the **OpenWeatherMap API**.

Enter any city name to instantly view the temperature, weather condition, and expressive emoji/icon indicators.

## ✨ Features

* 🔍 Search weather by city name
* 🌡️ Real-time temperature in °C
* 🌤️ Dynamic weather icons (sun, clouds, rain, etc.)
* 😎 Temperature-based emojis (🔥 hot, 🥶 cold, 🙂 mild)
* 🎨 Modern UI with gradient background and smooth styling

## 📁 Project Structure

```text
├── index.html
├── weather.js
├── style.css
├── sun_svgrepo.com.gif
└── Frame_1.gif
```

## 🚀 How It Works

The app fetches weather data from the OpenWeatherMap API:

```javascript
const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${API_KEY}&units=metric`;
```

It maps weather conditions to icons/emojis:

```javascript
const emoji = emojiMap[condition] || "🤷";
```

The weather information is then displayed on the page:

```javascript
document.getElementById("result").innerHTML =
  `${weatherDisplay} ${tempEmoji} ${temp}°C in ${data.name}`;
```

## 🛠️ Setup Instructions

1. Clone the repository.
2. Add your **OpenWeatherMap API key** inside `weather.js`.
3. Open `index.html` in your browser.
4. Enter a city name.
5. Click **Get Weather**.

## 🔑 API Key

Replace the placeholder API key in `weather.js`:

```javascript
const API_KEY = "YOUR_API_KEY_HERE";
```

> **Security note:** If this project is publicly available on GitHub, avoid committing a real API key directly to the repository. Consider using environment variables or another secure method for storing API credentials.

## 📸 Preview

*Add a screenshot or GIF of your UI here.*

For example:

```markdown
![Weather App Preview](Frame_1.gif)
```
