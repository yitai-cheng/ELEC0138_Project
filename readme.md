# ELEC0138 Security and Privacy Group Project.
This project simulates potential attacks on a company's web application and database system, and provides corresponding mitigation strategy to prevent the attacks.

Concretely, this project simulates phishing attack, SQL injection attack, and brute force attack in python code.

To mitigate phishing attack, we develop a machine learning model to detect phishing emails. Then

To mitigate SQL injection attack, we use Django framework to build a web application. We use Django's built-in protection mechanism to prevent SQL injection attack.

To mitigate brute force attack, we use a multi-factor authentication system to make the login process safer.

In our design, admins of the company's web application could manipulate the database through the web application to change information about other staffs.
In case that the attacker has somehow login as the admin, to prevent the attacker to see the other credentials of the staffs, we use a one-way encryption algorithm to encrypt the password of the staffs in the database.

We provide a backup system to backup the database to Google Drive. The backup system is implemented by Celery and Redis.
Furthermore, we provide https to encrypt the communication between the client and the server to prevent credentials leakage during data transmission.

We develop three versions of the web application.
1. The first version is the original version of the web application. It suffers from all potential attacks mentioned before. To run it: python origin/manage.py runserver
2. The second version is the fake website for phishing attack. To run it: python phishing/manage.py runserver
3. The third version is the secure version of the web application. It mitigates all potential attacks mentioned before and add additional mitigation strategy including database backup. To run it: python secure/manage.py runserver

To run https instead of http: python manage.py runsslserver --cert your_dir/ELEC0138_Project/ssl/server.crt --key your_dir/ELEC0138_Project/ssl/server.key
