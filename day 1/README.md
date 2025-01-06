## DAY 1: WARM UPS

This quick project test your understanding of the folliowing technologies

- Python
- AWS S3 Setup
- API fetching and processing
- Work environment setup

In this project, Openweather API was utilized and this was fetched using python. The result was then parsed into json format before being stored inside an S3 bucket.

## STEP INVOLVED

### 1. Create openweather account

Proceed to openweather website and create an account. After this, create an API key which will be used in fetching the weather information across different regions.

### 2. Setup your work environment within VSCode

Create a new directory and open it via VSCode. Create .env file inside this folder and proceed to the next step.
Inside the .env file add the following

```
WEATHER_API_KEY=put the values here
AWS_BUCKET_NAME=put a unique bucket name here (if you are seeing error while creating the bucket, you might need to change the name here. No underscore. You can use camelCase pattern)

```

### 3. Set up AWS within your terminal

AWS needs to be configured within your terinal as the python code will be run within it while creating and moving file to your s3 bucket. To do this:

- login to your AWS console (IAM login)
- Navigate to IAM >> Users, create a new user and attach the addministrator and s3 administrator as policy.
- Save the new user and open the new user details
- create access key (don't forget to Ddownload the SECRET key and ID ) and note the SECRET key and ID.
- open the terminal in vscode and use the gitbash window.
- Run the code `aws configure`
- put the Access Key ID and press enter
- Put the secret access key also and press enter
- you can leave the region and the rest as default by continue pressing enter.
- that should setup your aws identity

### 3. Setup python environment

[Download]("https://www.python.org/downloads/") python from the website and install (for window users). Linux users can follow the steps highlighted on the official website depending on their flavor of linux. Don't forget to setup the environmental variables also. Obviously, you need python to allow you run .py scripts

### 4. folder structure.

create the following folders and files

```
weather-dashboard/
├── src/
│   ├── init.py
│   └── weather_dashboard.py
├── .env
├── .gitignore
└── requirements.txt

```

inside the .gitignore you'll want to prevent git from moving specific files to your repo either because of security or due to file size (not in this case though).

So, inside .gitignore, type:

```
.env
.git

```

Inside the requirement.txt, type the following python packages and their version. We will need to install them in the next step

```
boto3==1.26.137
python-dotenv==1.0.0
requests==2.28.2

```

- boto3 allows python to speak to your aws s3 bucket
- python-dotenv let you be able to store and retrieve data inside secured .env
- requests allows you to fetch data via API

That should be all for folder structuring

let's get our hands dirty now

### 5. Installing the package needed

Remember what we put in the requirement.txt? Now lets install the three packages

`python install -r requirement.txt`

This will install the three packages and make them accessible to use

### 6. Let write the script to fetch and store the weather info

The next step is to actually do what we are here for. The code literally have the following scope.

- Import packages
- fetch and parse info from api as json
- create s3 bucket
- push the json files to the bucket
- call the main function

Literally all of these are function (for Javascript people).
The end product of the code will look like this [Here]("https://github.com/KodenOps/devops_challenge/blob/main/day%201/src/weather_script.py")

Now, let's test what we've cooked so far by navigating to the `src forlder`
Then run this command `python weather_dashboard.py`

### 7. Final check and housekeeping

The terminal should show you that

- bucket has been created
- some weather info are displayed on the terminal

This means you did not burn the house. You are a great chef. Now go to your AWS console and check the S3 page. You should see the files.json inside the bucket.

Now empty the bucket and delete the bucket to prevent unwanted billing on top small project
