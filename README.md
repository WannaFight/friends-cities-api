# friends-cities-api
Small API to get user's friends cities from VK. \
This repo is based on https://github.com/WannaFight/vk-friends-cities.

## Usage
|                                |                                        |
|-----------------------------------------------|-------------------------|
|https://cognomen.herokuapp.com                 |Base URL                 |
|https://cognomen.herokuapp.com/                |Base URL                 |
|https://cognomen.herokuapp.com/cities/TARGET_ID|Returns JSON with results, send Header "lang: en" to display output in English|

```bash
~$ curl https://cognomen.herokuapp.com 
>>> {"code":200,"content":[{"message":"Welcome to my API"}]}

~$ curl https://cognomen.herokuapp.com/cities/id1 
>>> {"code":204,"content":[{"message":"User https://vk.com/id1 has no friends."}]}

~$ curl https://cognomen.herokuapp.com/cities/
```