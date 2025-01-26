run "docker-compose up --build" to build the app

acceder al contenedor de fastapi/postgres: docker exec -it <CONTAINER ID> /bin/bash

Una vez dentro de postgres: 
    -  psql -U postgres -d PatientsApi;
    - select * from users;
    - select * from patients;
