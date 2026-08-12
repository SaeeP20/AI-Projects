

const API_KEY = "e3d057b74049af97b57e2c9e2c0b37ea";

const emojiMap = {
  Clear: "./sun_svgrepo.com.gif",
  Clouds: "./Frame_1.gif",
  Rain: "🌧️",
  Thunderstorm: "⛈️",
  Snow: "❄️",
  Mist: "🌫️",
  Drizzle: "💧",
};

async function getWeather(city) {
  const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${API_KEY}&units=metric`;

  try {
    const res = await fetch(url);
    const data = await res.json();

    if (data.cod !== 200) {
      document.getElementById("result").innerText = "❌ " + data.message;
      return;
    }

    const condition = data.weather[0].main;
    const temp = data.main.temp;

    const emoji = emojiMap[condition] || "🤷";
    const tempEmoji =
      temp > 30 ? "🔥" : temp > 20 ? "😎" : temp < 10 ? "🥶" : "🙂";

    const weatherDisplay =
      condition === "Clear"
        ? `<img src="${emoji}" alt="Sunny" class="sun-icon" />`
        : condition === "Clouds"
          ? `<img src="${emoji}" alt="Cloudy" class="clouds-icon" />`
          : emoji;

    document.getElementById("result").innerHTML =
      `${weatherDisplay} ${tempEmoji} ${temp}°C in ${data.name}`;
  } catch (err) {
    document.getElementById("result").innerText = "⚠️ Error fetching weather";
    console.error(err);
  }
}

document.getElementById("getWeather").addEventListener("click", () => {
  const city = document.getElementById("city").value;
  if (city) {
    getWeather(city);
  } else {
    document.getElementById("result").innerText = "⚠️ Please enter a city!";
  }
});
