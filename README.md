# Shippable
Open Issue Count for a given repository

Given Problem : 
#################
Create a repository on GitHub and write a program in any programming language that will do the following: 

Input : User can input a link to any public GitHub repository

Output :

Your UI should display a table with the following information -

- Total number of open issues

- Number of open issues that were opened in the last 24 hours

- Number of open issues that were opened more than 24 hours ago but less than 7 days ago

- Number of open issues that were opened more than 7 days ago 

###############

My Approach :
(1) As the problem stated that we have to count open issues for three different conditions. Now first I have calculated the no of issues for a given repository by using suitable github api call. This value is a combination of total open issues and pull requests/issues but we are interested in open issues.

(2) To solve above problem I have calculated total no of pull requests by calling pulls in github api till I have not reach the end of last pull reqquests page. Subtracted pulls from total issues and here I have my total no of open issues.

(3) In next step I have calculated the time of last 24hour and store in a string with the same format as github json data have. Then called github api using since to get all info of issues which were created within 24 hours. I have checked whether information date is greater or not if greater than increment the 24 hours count and check for pull request if it is pull also then increment pull counts.At the end of this loop if I subtract pull count from 24 hours count. I will get open issues within 24 hrs. (First goal is covered)

(4) Next goal is calculate the total no of open issues occured in last 7 days but after 24 hours of current time. I have stored date time of last 7th day from the current system time. Again use the github api with since call to get data within 7 days.I have checked all information of last 7 days and if the created date satisfy the time range increment within7days count and also check for pull request if it is then increment the pull request count.

(5) We have calculated till 7 days now rest of all data definitely fall in last category. So no need to iterate further.

(6) At last I have stored total open issues.
    open issues opened within 24 hours : (total open issues in 24 hours - total pull request in 24 hours)
    open issues opened more than 24 hours ago but less than 7 days ago : total no of open issues in 7 days - (total no of        issues within 24 hours) + total pull request within 24 days - total no of pull request within 7 days
    open issues opened more than 7 days ago : total no of issues  - total no of open issues in 7 days + no of pull request in     a week.

(7) Print the above data on a html page. (Done!!!!!)
 
 Note : For main code got to git folder and  check views.py. 
         
Link of heroku deployment : https://open-issue-count.herokuapp.com
