# GreyFinder

YouTube Preview:
[![Watch the video](https://img.youtube.com/vi/nWTzfKL8vcE/maxresdefault.jpg)](https://youtu.be/nWTzfKL8vcE)


**GreyFinder** is a Flask app that allows a user to upload a CSV file containing image links (e.g. [https://pastebin.com/BmA8B0tY](https://pastebin.com/BmA8B0tY)). After the CSV is uploaded, the images from within the file are presented to the user in a grid, along with an option to filter by size and optionally show greyscale versions of the images. The images are loaded as the bottom of the page scrolls into view.

A new user is created when a user that is not already present in the database attempts to log in. Each user is presented with only the images they have downloaded. Downloads are performed in an asynchronous task.

A clean and minimal interface allows for easy styling. The intended deployment is for locally hosted full-screen kiosk-type user interfaces.

## Installation

Make sure Python3 and pip3 are installed on your system: [https://realpython.com/installing-python/](https://realpython.com/installing-python/)

Download and unarchive this zip, or git clone this repository, to a folder on your filesystem

Open a Terminal window and enter the following after navigating to the project folder:
```
pip3 install virtualenv

python3 -m venv venv

source venv/bin/activate

flask db upgrade
```


## Usage

Open a Terminal window and enter the following after navigating to the project folder:
```
source venv/bin/activate

flask run
```
Open http://localhost:5000 in your favorite browser

Enter any user name and any password

Click the Choose File button and select a CSV file containing a list of image URLs

Click the Upload button

A background task is now downloading your images, and they should pop up momentarily


## API

While the server is running, you can issue a POST command to /api/tokens with a registered user:pass to retrieve an auth token:
```
curl --user jarek:test -X POST http://localhost:5000/api/tokens

{"token":"3lwfv+TQ3rmE0y9SzBmRAVrutVm80bCM"}
```
Using this token, you can then make API calls as the authenticated user by passing the token inside the header as Authorization: Bearer TOKEN, for example to /api/all_pictures
```
curl -H "Authorization:Bearer 3lwfv+TQ3rmE0y9SzBmRAVrutVm80bCM" http://localhost:5000/api/all_pictures
[{"url":"images/1_picsum.photos_id_12_300_200.jpg"},{"url":"images/1_picsum.photos_id_434_300_200.jpg"},{"url":"images/1_picsum.photos_id_966_300_200.jpg"},{"url":"images/1_picsum.photos_id_637_300_200.jpg"}]
```
You can retrieve a single image from the user's account, indexed by their upload index using /api/picture/{int}
```
curl -H "Authorization:Bearer 3lwfv+TQ3rmE0y9SzBmRAVrutVm80bCM" http://localhost:5000/api/picture/1
[{"url":"images/1_picsum.photos_id_434_300_200.jpg"}]
```
You can retrieve the greyscale version of that image by appending ?greyscale to the call
```
curl -H "Authorization:Bearer 3lwfv+TQ3rmE0y9SzBmRAVrutVm80bCM" http://localhost:5000/api/picture/1?greyscale
[{"url":"images/1_picsum.photos_id_434_300_200-greyscale.jpg"}]
```