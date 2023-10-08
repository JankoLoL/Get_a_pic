## README.md for the get_a_pic_app

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
     - Ability to fetch an expiring link to the image (the link expires after a given number of seconds, which the user can specify between 300 and 30000 seconds).
4. **Admin Tier Customization**: Admins can create arbitrary tiers with configurable features like:
   - Arbitrary thumbnail sizes.
   - Presence of the link to the originally uploaded file.
   - Ability to generate expiring links.
5. **Admin UI**: Managed via `django-admin`.
6. **User Interface**: There's no custom user UI, just the browsable API from Django Rest Framework.

### Considerations:
- **Tests**: Ensure tests are written and passing.
- **Validation**: Proper validation of image types and sizes.
- **Performance**: Designed with scalability in mind. Anticipate heavy traffic and large numbers of image uploads.

Certainly! Below is an expanded section of the README that describes the functionality associated with each endpoint in your `urls.py`.

---

## Endpoints and Their Functions:

1. **Main Page**:
   - URL: `http://localhost:8000/`
   - Description: This serves as the landing page of the application.

2. **API Routes**:

   **User Profiles**:
   - URL: `http://localhost:8000/api/userprofile/`
   - Description: Endpoints for creating, retrieving, updating, and deleting user profiles.

   **Images**:
   - URL: `http://localhost:8000/api/images/`
   - Description: Endpoints to upload, list, retrieve, update, and delete images.

   **Plans**:
   - URL: `http://localhost:8000/api/plans/`
   - Description: Endpoints for creating, retrieving, updating, and deleting account plans (Basic, Premium, Enterprise, etc.).

   **Thumbnail Sizes**:
   - URL: `http://localhost:8000/api/thumbnail-sizes/`
   - Description: Endpoints for defining, retrieving, updating, and deleting thumbnail sizes.

   **Expiring Links**:
   - URL: `http://localhost:8000/api/expiring-link/`
   - Description: Endpoints to generate and manage expiring links for images.

3. **Login Page**:
   - URL: `http://localhost:8000/login/`
   - Description: The login page for users to authenticate themselves.

4. **Retrieve Expiring Link**:
   - URL: `http://localhost:8000/expiring-link/<str:token>/`
   - Description: Endpoint to retrieve the actual image or content associated with an expiring link using a given token.

---

By adding this section to your README, users and developers will have a clear understanding of each available endpoint and its functionality.
This will facilitate easier usage and debugging of the application.

### Setting Up:


To set up and run the application locally, follow the steps below:

### Prerequisites:
1. Ensure you have Docker installed on your machine. If not, you can download and install Docker from [Docker's official website](https://www.docker.com/get-started).
2. Ensure `docker-compose` is available. It typically comes bundled with Docker installations.

### Steps:

1. **Clone the Repository**: 
   ```
   git clone [your-repository-link]
   cd [repository-name]
   ```

   Replace `[your-repository-link]` with the link to your Git repository and `[repository-name]` with the name of your cloned directory.

2. **Build the Docker Image**:
   ```
   docker-compose build
   ```

3. **Run the Application**:
   ```
   docker-compose up
   ```

   This command will start the application along with any associated services (like databases). Once the command completes and the terminal shows that all services are started, you can access the application through your browser.

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
   - Browsable API: Open a web browser and navigate to `http://localhost:8000/`
   - Admin Panel: Navigate to `http://localhost:8000/admin/` and use the superuser credentials you created.

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

In this project, we use a `local_settings.py` file to manage local configuration settings. This file is typically not included in the version control system (e.g., Git) and is used to store sensitive or environment-specific configuration.

### Why Use `local_settings.py`?

The `local_settings.py` file allows you to:

- Store sensitive information like secret keys, API tokens, and database passwords securely.
- Customize settings for local development, such as debugging options or development database configurations.

### Usage:

1. **Creating the `local_settings.py` File**:

   To get started with `local_settings.py`, you can create the file in the same directory as your main `settings.py`. Here's a simple example:

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

   # Debug Mode (Enable for local development)
   DEBUG = True

### Author: Adam Chrzanowski
