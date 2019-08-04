# cs50-web-2018-x-projects-1
Projects1 about Python, Flask and SQL PostgresSQL
users register on the platform with email, username and password, they can log in once they have registered, if they have not done so, send an alert message to register and / or in case of erroneously entering the email or the password will too . The password is encrypted and users can log out from any page they are working on.
 
The import of the BOOKS book database. CSV, was performed with the module import.py, which contains the delimiter of each field, to make the import correctly. If there are errors in the import for other additional characters, it must be done through another module such as import_failure.py in order to leave a historical record of the information. 
All this information goes to a SaaS and PaaS database , HEROKU PostgreSQL , Adminer.cs50.net.  
 
Once the information is loaded, the search is done by (columns) ISBN, Title and Author, ordered and presented per year in descending form, that is, presenting the latest version of the book. If it does not exist in the database or the information is wrong, it will throw a 404 Not Found error. The information submitted by a table to have a link on the ISBN code, which redirects and shows us all book information, and make our evaluation of it .
With the ISBN code we can consult the API of the book, where you will find all the information before and after making the qualification of it. If the ISBN entered for the API is wrong it returns error 404 equally.
Unprocessed SQL commands were used, no SQLAlchemy ORM was used .
Users are monitored on all pages of the platform to track who is connected.
 
The tables used are: Books database, Review revision information, and Users users.

enlace video : https://www.youtube.com/watch?v=Yruta3O5Asw&feature=youtu.be

