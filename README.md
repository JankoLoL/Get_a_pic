## README for the get_a_pic_app

### Description:

This application is built using the Django REST Framework and allows users to upload images in PNG or JPG format.

### Features:

1. **Image Upload**: Users can upload images via an HTTP request.
2. **Image Listing**: Users can list all their uploaded images.
3. **Account Tiers**:
    - **Basic**: After uploading an image, users receive:
        - A link to a thumbnail that's 200px in height.
    - **Premium**: Users receive:
        - A link to a thumbnail that's 200px in height.
        - A link to a thumbnail that's 400px in height.
        - A link to the originally uploaded image.
    - **Enterprise**: Users receive:
        - A link to a thumbnail that's 200px in height.
        - A link to a thumbnail that's 400px in height.
        - A link to the originally uploaded image.
        - Ability to fetch an expiring link to the image (the link expires after a given number of seconds, which the
          user can specify between 300 and 30000 seconds).
4. **Admin Tier Customization**: Admins can create arbitrary tiers with configurable features like:
    - Arbitrary thumbnail sizes.
    - Presence of the link to the originally uploaded file.
    - Ability to generate expiring links.
5. **Admin UI**: Managed via `django-admin`.
6. **User Interface**: There's no custom user UI, just the browsable API from Django Rest Framework.
7. **Admin Customizations**: Administrators have the ability to define new thumbnail sizes and create new account plans.
Flexibility and Adjustments:
While the application provides administrators with the flexibility to define new thumbnail sizes and create new account
plans beyond the default ones, it's important to note:

***Code Adjustments***: Introducing new plans or thumbnail sizes that differ from the default specifications
might necessitate changes or optimizations in the application's code to ensure optimal performance and functionality.
Always test thoroughly when introducing changes to the application's settings or behaviors.


### Considerations:

- **Tests**: Ensure tests are written and passing.
- **Validation**: Proper validation of image types and sizes.
- **Performance**: Designed with scalability in mind. Anticipate heavy traffic and large numbers of image uploads.

---

## Endpoints and Their Functions:

1. **Main Page**:
    - Local URL: `http://localhost:8000/`
    - Docker URL: `http://0.0.0.0:8000/`
    - Description: This serves as the landing page of the application.

2. **API Routes**:

   **User Profiles**:
    - Local URL: `http://localhost:8000/api/userprofile/`
    - Docker URL: `http://0.0.0.0:8000/api/userprofile/`
    - Description: List user profile details.

   **Images**:
    - Local URL: `http://localhost:8000/api/images/`
    - Docker URL: `http://0.0.0.0:8000/api/images/`
    - Description: Endpoints to upload, list, retrieve, update, and delete images.

   **Plans**:
    - Local URL: `http://localhost:8000/api/plans/`
    - Docker URL: `http://0.0.0.0:8000/api/plans/`
    - Description: Endpoint for creating new account plans. Available only to administrator.

   **Thumbnail Sizes**:
    - Local URL: `http://localhost:8000/api/thumbnail-sizes/`
    - Docker URL: `http://0.0.0.0:8000/api/thumbnail-sizes/`
    - Description: Endpoint for defining and adding thumbnail sizes. Available only to administrator.

   **Expiring Links**:
    - Local URL: `http://localhost:8000/api/expiring-link/`
    - Docker URL: `http://0.0.0.0:8000/api/expiring-link/`
    - Description: Endpoints to generate and manage expiring links for images. Only for Enterprise user and admin.

3. **Login Page**:
    - Local URL: `http://localhost:8000/login/`
    - Docker URL: `http://0.0.0.0:8000/login/`
    - Description: The login page for users to authenticate themselves.

4. **Retrieve Expiring Link**:
    - Local URL: `http://localhost:8000/expiring-link/`
    - Docker URL: `http://0.0.0.0:8000/expiring-link/`
    - Description: Endpoint to create an expiring link using a given token.

---

### Setting Up:

To set up and run the application locally, follow the steps below:

### Prerequisites:

1. Ensure you have Docker installed on your machine. If not, you can download and install Docker
   from [Docker's official website](https://www.docker.com/get-started).
2. Ensure `docker-compose` is available. It typically comes bundled with Docker installations.

### Steps:

1. **Clone the Repository**:
   ```
   git clone [your-repository-link]
   cd [repository-name]
   ```

   Replace `[your-repository-link]` with the link to your Git repository and `[repository-name]` with the name of your
   cloned directory.

2. **Build the Docker Image**:
   ```
   docker-compose build
   ```

3. **Run the Application**:
   ```
   docker-compose up
   ```

   This command will start the application along with any associated services (like databases). Once the command
   completes and the terminal shows that all services are started, you can access the application through your browser.

4. **Initialize the Database** (Only needed the first time):
   In another terminal window/tab:
   ```
   docker-compose run web python manage.py migrate
   ```

   This will apply Django migrations and initialize your database schema.

5. **Create Superuser** (For accessing the admin panel):
   ```
   docker-compose run web python manage.py createsuperuser
   ```

   Follow the prompts to set up an admin username, email, and password.

6. **Accessing the Application**:

   Browsable API. Open a web browser and navigate to:
    - Local URL: `http://localhost:8000/`
    - Docker URL: `http://0.0.0.0:8000/`

   #### Admin Panel. Navigate to:

    - Local URL: `http://localhost:8000/admin/`
    - Docker URL: `http://0.0.0.0:8000/admin/`

and use the superuser credentials you created

7. **Shutting Down**:
   When you're done, you can shut down the application and all its services with:
   ```
   docker-compose down
   ```

8. **Running Tests**:
   To ensure the application is working as expected, run the tests using:
   ```
   docker-compose run web python manage.py test get_a_pic_app.tests
   ```

### Note:

Remember to replace placeholders like `[your-repository-link]` with actual values pertinent to your project setup.

## Local Settings Configuration (local_settings.py)

In this project, we use a `local_settings.py` file to manage local configuration settings. This file is typically not
included in the version control system (e.g., Git) and is used to store sensitive or environment-specific configuration.

### Why Use `local_settings.py`?

The `local_settings.py` file allows you to:

- Store sensitive information like secret keys, API tokens, and database passwords securely.
- Customize settings for local development, such as debugging options or development database configurations.

### Usage:

1. **Creating the `local_settings.py` File**:

   To get started with `local_settings.py`, you can create the file in the same directory as your main `settings.py`.
   Here's a simple example:

   ```python
   # local_settings.py

   # Secret Key
   SECRET_KEY = 'your-secret-key-here'

   # Database Configuration (For Development)
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your-database-name',
           'USER': 'your-database-user',
           'PASSWORD': 'your-database-password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   


### Author: Adam Chrzanowski
