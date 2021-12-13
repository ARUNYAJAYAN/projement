# projement

This is a simple REST Web Api for projectmangement. Implemented using Django-DRF.

Features:


Admin/ management can creat project(POST).


admin/ management can create, update, list and retrive project, companies, developers. Also they can see the logs (history), dawnload excle files of project descriptions.


developers can update project information and add additional developement hours


Token based authentication and role based authorization(Admin or employer and developer)


Fully functional Django-Admin panel.


UserStory:
User can register based on role and can login.

Steps for Installation and Running:


Clone the repo using git clone <reponame> 2.cd <reponame>
  
  
Grab a virtual environment and activate it
  
  
virtualenv <ur-env-name>
  
  
source <ur-env-name>/bin/activate
  
  
Install dependencies
  
  
pip install -r requirements.txt
  
  
To run the project:
  
  
python manage.py makemigrations
  
  
python manage.py migrate
  
  
python manage.py runserver
  
  
python manage.py createsuperuser
  
  
After creating users via API/Admin dashboard and super user Admin should enter the admin portal and should add users to their corresponding developer model. This is done based on an assumption. Can be made better by adding this step at the registration flow itself.
  
  
Endpoints and response:
Use postman for executing API's(Swagger Integration is in the future scope) API docs: https://www.getpostman.com/collections/7488dd0655c7a4911211
