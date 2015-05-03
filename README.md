# Tourini, a Social Network Website
## CS6083 Database Systems Final Project
### Description
  This project is to establish a database system backend a web-based server. In this project people that like to travel a lot can sign up at the site, can post photos and diary entries about their travel, and can connect with and get advice from other travelers. In this first part of the project, we designed a relational database that can serve as a relational backend for this new website. Registered users on the site are identified by a unique user name, and they can optionally upload a short profile with information about themselves. Users can upload photos that they have taken on their trips, where each photo has a unique ID and is labeled with the time when, and place where, it was taken, and maybe a short caption. As a social networking site, users also need mechanisms to interact with each other. Each user can organize their friends into circles.All location information is stored in longitude and latitude coordinates.

### Tools
  We use Flask, which is a microframework for Python based on Werkzeug, Jinja 2 and good intentions, for our website. About the back-end, we use MySQL to manage our database by Flask-SQLAlchemy extension. 
