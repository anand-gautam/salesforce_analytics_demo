# salesforce_analytics_demo

A tiny demo of using Selenium with Python to automate the basic test for SalesForce Analytics (Einstein Analytics). The tests include: login, navigate to the demo dashboard using selenium clicks; and then after launching the dashboard, checks if the deisred dashboard items have been loaded.

To run these tests, you have to register for a trail on SalesForce website (about 14 days perhaps the duration).
When you get your url after registration, navigate to the Analytics page, and directly use that url in the ea_tests_one.py file in the URL variable.
For login credentials, paste them in the secrets.py file in the obvious variables present there.

Since this is just a demo that I developed as a fun time to check the scope of Selenium with it, the code is not in the framework but rather just organized into one file, with credentials loaded ino another file.
