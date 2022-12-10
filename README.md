# Birdnest

This is a pre-assignment for a trainee application to the company Reaktor.

Full description of the assigment can be found here:
[Birdnest](https://assignments.reaktor.com/birdnest/)

## Short description

The service should request for live drone location information and if an aerospace violation is detected, query for the drone owner information and publish it on website. Only data regarding owners of offending drones should be queried and published. The web page should update its contents regularly without user interaction.

The user interface is not important and the page should only show the list of the owners of the offending drones.

## Technology

* The application is implemented in Python, using the Flask framework.
* The application will be published on [Fly.io](fly.io) platform.
* There will be a scheduled method, which polls the drone detector in given
  intervals regardless if the front end has been used or not

### Persistent data storage

The application doesn't use any persistent storage. All information is lost during the application shut down.

## Downloading and starting

You should have Python 3 already installed in your system. we assume Linux or similar operating system is in use.

Clone the project from GitHub:

```
$ git clone https://github.com/jatufin/birdnest
```

Go to the project folder and build the Flask environment:
```
$ python3 -m venv venv
$ . venv/bin/activate
(venv) $ pip install Flask
(venv) $ pip install wheel
(venv) $ pip install Flask-APScheduler
(venv) $ pip install requests
```

Start the application:

```
$ flask run
```

The front end of the application can be opened in your browser: [localhost:5000](http://localhost:5000/)

## Configuration

Python variables containing configuration information can be found in the `config.py` file.

No environmental variables are used.

## Testing

Unit tests can be found in the `tests` directory. They can be executed from the project root directory with following command:
```
$ python3 -m unittest
```
## Future suggestions

Store bird nests in a list inside the Drones object. This way multiple nests with different size No Fly Zones could be surveyed.
