# bank-app

Design and implementation of an independent bank website.

## Want to use this project?
Uses the default Django development server.

  1. Build the images and run the containers. Spin up the containers:
  
        ```
        $ docker-compose up -d --build
        ```
  2. Create superuser:
        ```
        $ docker-compose exec web python manage.py createsuperuser
        ```
  3. Unit Tests:
        ```
        $ docker-compose exec web python manage.py test
        ```
     
Test it out at http://localhost:8000. \
The "backend" folder is mounted into the container and your code changes apply automatically.

##### If you want to use Swagger to document the API:
http://localhost:8000/api/swagger

##### Tools to run the application::
* [docker] - https://www.docker.com/get-started