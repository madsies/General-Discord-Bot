# General-Discord-Bot

## Key Tech

- Uses MySQL database to handle persistent data storage
- Uses two RESTful APIs to grab data to share to users.
- Heavy use of discord.Embed and discord.ui.View for a cleaner user experience
- Key hidden data is stored privately, away from github in .env file

## Commands

### Fun

#### Poke
- Pokes a user, with toggles for random, and if it should be silent or not

#### Dog
- Uses the public [dog api](https://dog.ceo/dog-api/) to pull pictures of dogs
- Can specify the breed of dog with the dog subcommand (or random)

### Greetings

#### OnMemberJoin
- Creates an embed with a welcome message and basic information when a user joins the server

#### Hello
- Basic hello command, greets the user when ran.

### Leaderboard

#### Leaderboard
- Uses discord views to have a more interactive experience.
- Uses data stored in MySQL database to show a leaderboard of stats in the server.
- 10 Users/Page, Traversable with discord view buttons

### Predictions

#### Prediction [WIP]
- Allows a user to start a "Prediction" where they have a question and possible answers
- Users are allowed to "Bet" on the prediction with discord views.
- When the timer has ended, the prediction creator will be prompted to choose the correct answer
- The users who get the correct prediction will be awarded the bet pool accordingly.

### Server Stats
 
#### Server info
- Sends the user a discord embed containing key stats about the server, namely
    - Member Count
    - Creation Date
    - Number of Channels

#### On_Message handler
- Tracks when users send messages and increments a count in the MySQL database, for use in the leaderboard.
- In future will be used for granting money for the predictions and other games.


### Weather

#### Weather Current
- Grabs the current weather from the [open weather api](https://openweathermap.org/)
- Displayed in a discord embed with important current data
- Image embeds are also taken from the api according to the current weather


#### Weather Hourly
- Grabs the (3) Hourly forecast for the specified location
- Returns 8 timestamps (the next 24hrs)
- Displays vital information in embed fields