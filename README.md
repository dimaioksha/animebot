# Introduction

Hurray! This is the next step of working with encoder&decoder and convolutional layers. At this topic i am going to create a functional telegram bot, which will be able to work with user~s photos and find the most similar to them from database.

If you have not seen the previous part of my project, you should follow this [link](https://github.com/DmitryIo/animefaces) to get know about how all this works.

Ready? Go!

# Concepts

Bots are very popular today and their popilarity increases fastly. The most popular platform for implementation bots is Telegram. And that is exactly why i have chosed it.

Telegram provides useful API for their bots. And the library for working with it is [`pyTelegramBotAPI`](https://github.com/eternnoir/pyTelegramBotAPI). It is an intuitive thing, and i like it very much.

# Implementation

**1 Step**

Here we go! The first step of creating any telegram bot is to make an introduction. This is an example of how it works:

![](./img/introduction.PNG)

It takes from users data his name and send response by command `/start`, `Привет`, `Hello` and etc.

**2 Step**

Ok. Now the bot is able to answer first command. The next goal is to make an interactive bars for communicating with user. 

I have decided to make 3 bars: 'Random number', 'How are you?' and the third one is a secret at that moment. We will talk about the third later!

![](./img/2.PNG)

If you push on `Как дела?` the bot will answer you with two inline buttons!

![](./img/3.PNG)

You can chose your answer and then the bot will send you another one message. It is done because of `callback_querry_handler` which detects any callbacks in the system. When you send to bot everything, the callback of your movement is processed by bot and then he decides what to do next. 

`This is a fun functioality of my bot. He can send you random number if you want`

![](./img/4.PNG)

**3 Step**
BIG DEAL!

Ok, it is enough for funny features and now i am going to make something useful. The first thing i am going to talk about is [MongoDB](https://www.mongodb.com/). This is one of the most powerful cloud databases for small projects. Mongo provides programmers wide spectre of functions and things which are very helpful for project implementation. I am going to use FreeMongoCloud to create database of users. Working with MongoDB API is described in this [file](mongodb.py).

![](./img/5.PNG)

Great! Now i can save data of users and then make some operations with their data. There are some fields like `name`, `surname`, `id` and etc.
