# Flask-Microblog
Flask App deployed on the Heroku

In this project I implemented some features like:
  - Supporting multiple lanuages with Flask-Babel;
  - Integration with the Gravar service that provides Avatars to the user's profile;
  - Password recovery via emails;
  - Live language translation using Microsoft translation service and AJAX;
  - Full text search with the Elasticsearch service;
  - API to work with users;


API:
- api/users/ - get all users
- api/users/<id> - get user with <id>
- api/users/<id>/followers - get followers of the user with <id>
- api/users/<id>/followed - get those to whom the user with <id> is subscribed
- (POST) api/users username=<username> password=<password> email=<email> - create new user
- (PUT) api/users/<id> "about_me=..." - editing user
