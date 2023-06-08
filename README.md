# grpc-mafia
A Mafia game client-server app built on gRPC

# Install and run

Clone this repository to your machine.
To run, `cd` to the root directory of the repository and execute this command:

    ./run.sh

Or paste the script into the shell directly:

    docker-compose build
    docker-compose down
    docker-compose up -d
    python3 client/client_player.py -u John_Doe localhost:50051

(Note: you might have to use `python` instead of `python3`)

This will run a server and 4 client apps: 3 bots, and 1 player. The player client app will open the user GUI,
while the bot apps will run inside Docker containers in the background.