# Install instructions

#### VIRTUALENV SETUP 

Step 1: Make sure python3 and pip3 exist in the ubuntu VM
which python3
which pip3

Step 2: Use pip3 to install virtualenv, then check it's installed
sudo pip3 install virtualenv
pip3 freeze | grep virtualenv

Step 3: Make a directory and then use virtualenv on it

```
mkdir ~/scraper_site
cd ~
virtualenv scraper_site
```

Step 4: Run the source command on the virtualenv directory's "activate"

```
source ~/se_siteenv/bin/activate
```

After all this is done, you should see the directory's name prefixed in parentheses:
(scraper_site) osboxes@osboxes:~/scrape/RegistrarAnalyzer$

In addition, you only need to run python or pip (not python3 or pip3) because this virtual environment is essentially
its own container.

To get the requirements needed for the project, execute the following command when you are in the RegistrarAnalyzer
root directory:

```
pip install -r requirements.txt
```

To get out of the virtual environment, type the "deactivate" command with no parameters.

#### START DJANGO

Go to the RegistrarAnalyzer project directory and go into the se_site directory. In here is a file called manage.py
that will be needed to run the server. Make sure you are in the virtual environment first!

```
python manage.py runserver --settings=se_site.settings.dev
```

After running this command, you should get a prompt like "Starting development server at http://127.0.0.1:8000/"

To run manage.py on the production server, use settings.prd instead of settings.dev

#### PYTHON WEB SCRAPER 

The web scraping scripts can be found in the python_scripts/ directory. Please use the scrapeterms.py script to get
JSON data. Running this script for all 34 semesters for one course may take a little more than 3 minutes, and around
100 MB of RAM. The scraper requires dryscrape and BeautifulSoup to be installed.

Functions are documented in the Numpy documentation style, and plotly is the library that will be used to make the
graphs (python framework, not the js version).

#### DB schema

uses sql database located at se_site/db.sqlite3

Courses(id, course_name, instructor, semester, time_start, time_end, enroll_now, room, honors, meeting_days,
credit_vaule, enroll_max)

#### Server Config

ssh setup, basic firewall setup, fail2ban
https://www.digitalocean.com/community/tutorials/how-to-protect-an-nginx-server-with-fail2ban-on-ubuntu-14-04

configure domain name: https://www.digitalocean.com/community/tutorials/how-to-set-up-a-host-name-with-digitalocean

configure web server and related packages:
https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04

To restart and debug server:
```
sudo service gunicorn restart
sudo service nginx restart
sudo service gunicorn status
```

https://medium.com/@ayarshabeer/django-best-practice-settings-file-for-multiple-environments-6d71c6966ee2#.q6vzay9f9
for instructions on how to setup settings module, will just use three, base, dev, and prd

secret key in settings.py removed, moved to file secrets.py, excluded from version control to conceal the
SECRET_KEY constant for development just override in settings.py

# Website samples

The website will generate two different plots shown below

### Stacked Bar Chart
![stacked_bar_chart](/picture1.png?raw=true "stacked_bar_chart image")


### Pie Chart 
![pie_chart](/picture2.png?raw=true "pie_chart image")
