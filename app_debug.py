from front import app

app = app.app
server = app.server


# Run flask app
if __name__ == "__main__": app.run_server(debug=True, port=8050)
