## Docker Setup

1. Build Image

    `docker build -t djwanguo:0.1 .`

2. Run in development mode

    `docker run -d --name djwanguo -e DJANGO_DEBUG=1 -p 8000:8000 -v $(pwd):/app djwanguo:0.1 python manage.py runserver 0.0.0.0:8000`

3. Create Superuser (NOTICE: EXECUTE THIS ONLY WHEN FIRST SETUP)

    `docker exec -it djwanguo python manage.py createsuperuser`


## Docker-compose Setup

1. Generate DJANGO_SECRET_KEY

    ```bash
    >>> import secrets
    >>> secrets.token_urlsafe(66)
    'w5vB35EEzYk37UBx4yxe0nVT_F2isnaMjxRuKUFDXdtdEnj2BXm0gPgx1hCE45BtpDSMDs26PhjIJjXPxQ-kjT2w'
    >>>
    ```

2. Create or edit .env file

    ```
    DJANGO_SECRET_KEY=w5vB35EEzYk37UBx4yxe0nVT_F2isnaMjxRuKUFDXdtdEnj2BXm0gPgx1hCE45BtpDSMDs26PhjIJjXPxQ-kjT2w
    DJANGO_ADMIN_TITLE=<Use-your-own-site-TITLE>
    ```

3. Start services

    `docker compose up -d`

4. Create Superuser (NOTICE: EXECUTE THIS ONLY WHEN FIRST SETUP)

    `docker compose exec app python manage.py createsuperuser`
