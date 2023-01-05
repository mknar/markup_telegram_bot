After cloning this repository go to the root directory

For windows, you need to make a file sharing for the project folder. Example:
  add C:\Users\path_to_my_folder to Docker Filesharing. Go to docker dashboard -> settings ->Resources -> FileSharing. Add required folder and hit Apply & Restart.

In project root run command:
  docker-compose up
  
After the successful launch of the containers, the admin panel will be available at:
  http://localhost:8000/admin

Administrator access:
  Username: bot_admin
  Password: bot_password
 
Telegram bot link:
  https://t.me/simple_markup_bot

Docker hub image link:
  https://hub.docker.com/r/mknar/django-app
