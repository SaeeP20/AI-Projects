import readline from "readline"; //imports function to read user input

const API_KEY = "e3d057b74049af97b57e2c9e2c0b37ea"

const emojiMap = { //maps the weather to emojis
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
        const data = await res.json(); //response handling

        if (data.cod != 200) { //only successful if .cod returns 200 otherwise error
            console.log("Error: ", data.message);
            return;
        }

        let condition = data.weather[0].main; //extracts main weather condition
        let temp = data.main.temp;

        let emoji = emojiMap[condition || "🤷"];
        let tempEmoji = temp > 30 ? "🔥" : temp > 20 ? "😎" : temp < 10 ? "🥶" : "🙂";

        console.log(`${emoji} ${tempEmoji} ${temp}°C in ${data.name}`); //prints the message
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