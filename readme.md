🧠 Quora Clone - Django Web Application

    This project is a simple Quora-inspired Q&A platform built using Django. Users can sign up, log in, post questions, answer questions, like answers, and log out.

    🚀 Features
        1. 🔐 User authentication (Login, Signup, Logout)

        2. ❓ Post questions

        3. 📄 View all questions

        4. ✍️ Answer questions

        5. 👍 Like answers

    🛠️ Tech Stack
        1. Backend: Django (Python)

        2. Database: MySQL

        3. Frontend: Django Templates (HTML, CSS, Bootstrap)

    🏁 Getting Started
        1. Clone the Repository

            command -- git clone https://github.com/yourusername/quora-clone-django.git
                       cd quora-clone-django

        2. Create a Virtual Environment

            command -- python -m venv env
                       source env/bin/activate   # On Windows: env\Scripts\activate

        3. Install Dependencies

            command -- pip install -r requirements.txt

        4. Apply Migrations

            command -- python manage.py makemigrations
                       python manage.py migrate
        
        5. Run the Server

            command -- python manage.py runserver

        Now visit http://127.0.0.1:8000 in your browser!


        🧪 Functionality Overview

            Feature	                         Description
            User Signup/Login	       Users can register and log into their accounts.
            Post Questions	           Authenticated users can ask questions.
            View Questions	           Authenticated users can browse posted questions.
            Answer Questions	       Authenticated users can answer any question.
            Like Answers	           Authenticated Users can like answers or question posted by others.
            Logout	                   Users can log out securely.
