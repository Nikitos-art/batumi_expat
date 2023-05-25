Batumi Cafes Project

Description: This is a small project that will be checking data from Google to see if there are any new cafes in town.

Tech Details:

Cafes Batumi uses Beautiful Soup, lxml, Selenium and 3rd party libraries to check with Google if there are any new cafes in Batumi. So the first part of the project is a cafes scraper/parser and add the data to my local DB. First I will do an initial scrape for cafes. Then I will implement a checker/automation code to check for new opened cafes. 1.1) MongoDB is used for storage and Docker container for local deployment.

Flask is used for back-end. It will read the data from the cafes DB and will serve that data to the front using the appropriate routing and links. And serve these to front end templates.

Flask servers static files and so far there are the following pages: 1.0) Main page will have: 1.0.a) Some flight info from Batumi. 1.0.b) 1.0.c) 1.0.d) 1.0.e)

1.1) Cafes
1.2) Apartments for rent
1.3) Barber shops
1.4) Gyms
1.5) For kids & moms
