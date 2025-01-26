run "docker-compose up --build" to build the app

acceder al contenedor de fastapi/postgres: docker exec -it <CONTAINER ID> /bin/bash

Una vez dentro de postgres: 
    - psql -U postgres
    -  psql -U postgres -d PacientsApi
    - select * from users;
    - select * from pacients;
