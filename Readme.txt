# Programming Assignment: Web

Platform: Flask 0.12.2
          Python 2.7.12 (default, Nov 19 2016, 06:48:10) 
          [GCC 5.4.0 20160609]

Database used: mysql  Ver 14.14 Distrib 5.7.18

Author : M Durga Keerthi

Before running code, 
**create database with the follwing tables  
   1.user with fields userid int(11) not null auto_increment, username char(20) not null, password char(20) not null, pic_count int(11) not null,del_count int(11) not null, primary key(userid)
   2.picnames with fields picturename char(250) not null, uploader char(20) not null
   3.comments with fields commentedpic char(250) not null, commentedtext char(250) not null, commenteduser char(20) not null
   
-------------
Run the app $ python main.py  
-------------

All the uploaded files will be saved to uploads folder in the same directory as main.py
All css files are in static/css directory
All html files are in templates folder

-----------Design-----------------
Anyone can register with this app. If the username already exists, person trying to sign in should type corresponding password else new account with the requested username will be created.
The user can upload pictures under 'upload image' link
The user can see all the pictures he/she uploaded under 'Your pictures' and then select one of them to delete.
The user can see all the uploaded pictures by all the users under 'All Uploaded pictures'. Details like who uploaded the picture, comments made by various users on picture can be seen.
The user can sign out using 'logout' link
----------------------------------

Thank You

