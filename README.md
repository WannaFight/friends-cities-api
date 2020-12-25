# friends-cities-api
Small API to get user's friends cities from VK. \
This repo is based on https://github.com/WannaFight/vk-friends-cities.

</br>

## Usage
| Endpoint                                           | Description             |
|----------------------------------------------------|-------------------------|
|https://cognomen.herokuapp.com/                     |Base URL                 |
|https://cognomen.herokuapp.com/cities?user=TARGET_ID&lang=LANG|Returns JSON with results, send arg "lang=en" to display output in English, default = Russian|


</br>

```bash
~$ curl https://cognomen.herokuapp.com 
>>> {"code":200,"content":[{"message":"Welcome to my API"}]}

~$ curl https://cognomen.herokuapp.com/cities?user=id1 
>>> {"code":204,"content":[{"message":"User https://vk.com/id1 has no friends."}]}

~$ curl https://cognomen.herokuapp.com/cities?user=cyeecespedes&lang=en
>>> {"code":200,"content":[{"current_city":"St. Petersburg","home_city":"Not specified","user":"https://vk.com/id31752625"},...]}
```

LANG is [code](https://cloud.google.com/translate/docs/languages) for language supported by Google Translate

## requirements.txt
|                     |                                               |
|---------------------|-----------------------------------------------|
|Flask==1.1.2         |API                                            |
|googletrans==4.0.0rc1|Translate names of cities to specifies language|
|vk==2.0.2            |VK API                                         |
|gunicorn==20.0.4     |Server to run on heroku                        |

</br>
 


