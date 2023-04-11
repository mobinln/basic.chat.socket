# Basic Chat SocketIO Server

This is a basic chat socketio server built with Python. It uses the Flask and Flask-SocketIO libraries to provide a simple chat server that allows multiple users to chat with each other in real-time in rooms.

## Installation

To run the server, you'll need to have Python 3 installed on your machine. You can install the required Python packages by running the following command in the terminal:

```sh
pip install -r requirements.txt
```

This will install the Flask and Flask-SocketIO libraries, as well as any other required dependencies.

## Usage

To start the server, run the following command in the terminal:

```sh
flask run
```

This will start the server and listen for incoming socketio connections. Once the server is running, you can connect to it using a socketio client such as a web browser.

## Contributing

If you'd like to contribute to this project, please fork the repository and make your changes in a separate branch. When you're ready to submit your changes, create a pull request and describe your changes in detail. We welcome contributions from anyone who wants to help make this project better!

here is a list of features you can contribute to this project:

- add redis connection and cache active_users, rooms or messages
- add database to save users, rooms and messages
- add authentication
- add logging for server
- add a homepage and documentation
- and many more features...
