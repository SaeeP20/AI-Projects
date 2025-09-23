import readline from "readline";

const API_KEY = "e3d057b74049af97b57e2c9e2c0b37ea"

const emojiMap = {
    Clear: "☀️",
    Clouds: "☁️",
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

        if (data.cod != 200) {
            console.log("Error: ", data.message);
            return;
        }

        let condition = data.weather[0].main;
        let temp = data.main.temp;

        let emoji = emojiMap[condition || "🤷"];
        let tempEmoji = temp > 30 ? "🔥" : temp > 20 ? "😎" : temp < 10 ? "🥶" : "🙂";

        console.log(`${emoji} ${tempEmoji} ${temp}°C in ${data.name}`);
    } catch (err) {
        console.error("Error fetching weather: ", err);
    }
}

const rl = readline.createInterface({
  input: process.stdin,   // where to read input from
  output: process.stdout, // where to print questions/output
});

rl.question("Enter a city: ", (location) => {
  getWeather(location);
  rl.close();
});