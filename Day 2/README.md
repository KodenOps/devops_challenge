# DAY 2: GETTING A LIVE UPDATE ON NBA GAMES VIA MAIL/SMS

This is a basic cloud project where the game schedule for NBA games are continually fetched through API and the result are being sent directly to your preferred Email.

In this project we will be making use of the following AWS services:

- AWS SNS: This is the brain behind sending the mail/sms. It processes data and route it through one of its numerous integrated systems to send result to users.
- AWS Lambda: this is a serverless function by AWS. It allows you to run lines of code without having to create a dedicated servers like EC2 to run it. Our code will be written in Python for this challenge
- AWS EventBridge: This is like the machine that drives the running of the lambda code at interval. It runs the cron job that triggers the Lambda code to be executed based on the condition specified by the administrator
- Sportdata API: This is the intermediary between the user and the server on which the NBA games information is stored. It fetches our data for us
