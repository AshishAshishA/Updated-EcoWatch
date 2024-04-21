How To Run in local env

Steps:
1. Create a virtual env using command 
        python -m venv <env_name> (for windows)

2. Install Dependencies using
        pip install -r requirements.txt

3. Change some variables in Settings and in views
        for ease just comment and uncomment certain lines
               Settings                                          blogs/views
        comment        uncomment                            comment        uncomment
          28             27                                   266             272
          31             32                                   273         
          34             36
          118
          119

3. Make Migrations and migrate
        python manage.py makemigrations
        python manage.py migrate

5. Create Superuser to access admin panel(optional)
        python manage.py createsuperuser
        then provide the necessary details like name and password

6. Run The Server
        python manage.py runserver

7. Go to admin panel and create SocialAccountSites
        Or you can use mine temporarily by uncommenting line 117 in settings.py


Just Git commands for me
…or create a new repository on the command line
echo "# Updated-EcoWatch" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/AshishAshishA/Updated-EcoWatch.git
git push -u origin main

…or push an existing repository from the command line
git remote add origin https://github.com/AshishAshishA/Updated-EcoWatch.git
git branch -M main
git push -u origin main