####################
# VIRTUALENV SETUP #
####################

Step 1: Make sure python3 and pip3 exist in the ubuntu VM
which python3
which pip3

Step 2: Use pip3 to install virtualenv, then check it's installed
sudo pip3 install virtualenv
pip3 freeze | grep virtualenv

Step 3: Make a directory and then use virtualenv on it
mkdir ~/scraper_site
cd ~
virtualenv scraper_site

Step 4: Run the source command on the virtualenv directory's "activate"
source ~/scraper_site/bin/activate

After all this is done, you should see the directory's name prefixed in parentheses:
(scraper_site) osboxes@osboxes:~/scrape/RegistrarAnalyzer$

In addition, you only need to run python or pip (not python3 or pip3) because this virtual environment is essentially
its own container.

To get the requirements needed for the project, execute the following command when you are in the RegistrarAnalyzer
root directory:
sudo pip install -r requirements.txt

To get out of the virtual environment, type the "deactivate" command with no parameters.

####################
# START DJANGO     #
####################

Go to the RegistrarAnalyzer project directory and go into the se_site directory. In here is a file called manage.py
that will be needed to run the server. Make sure you are in the virtual environment first!

python manage.py runserver

After running this command, you should get a prompt like "Starting development server at http://127.0.0.1:8000/"

######################
# PYTHON WEB SCRAPER #
######################

The web scraping scripts can be found in the python_scripts/ directory. Please use the scrapeterms.py script to get
JSON data. Running this script for all 34 semesters for one course may take a little more than 3 minutes, and around
100 MB of RAM. The scraper requires dryscrape and BeautifulSoup to be installed.

Functions are documented in the Numpy documentation style, and plotly is the library that will be used to make the
graphs (python framework, not the js version).

######################
#     DB schema      #
######################

uses se_site/db.sqlite3

Courses(id, course_name, instructor, semester, time_start, time_end, enroll_now, room, honors, meeting_days,
credit_vaule, enroll_max)