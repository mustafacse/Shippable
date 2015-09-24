"""
Author : Mohsin Mohammad
E-mail Id : mohsinmohammad110@gmail.com
"""
# included all the required modules of django and pyhton

#-----------Start Modules----------------------#
from django.shortcuts import render
import requests
import datetime
import time
import json
from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponseRedirect, HttpResponse

#----------- End Modules ----------------------#


#------- Function to convert a number into string -------#
def fun(x):
    return str(x)


#-------- end of function -------------------------------#


#----- main function to get all details regarding given repository -----  #

def getIssues(request):
    if request.POST:        # if the form is posted then this code will work
        url = request.POST.get('url_val')   #get the url inserted in textbox by the user
        str = url.split('/')                #split the url to segregate url and username and repository name

        if(str[0] != 'www.github.com' or str[1] == "" or str[2] == ""):   #url is not proper then return to the same page
        	args = {}
            	return render(request,'home.html',args)
            
        username = str[1]      #get username from splitted string 
        reponame = str[2]      #get repository name

        #print username,reponame
        
        issues = requests.get('https://api.github.com/repos/'+username+'/'+reponame)   #call the github api to find total no of open issues
        repoItem = json.loads(issues.text or issues.content)   #it's a response object so extract json data from it and store in repoItem
                                                               
        total_no_issues = repoItem.get('open_issues_count')    # extarct total no of issues

        #print total_no_issues
        
	page = 1   #variable for pagenation support in url
        pulls = 0  #variable to store no of pull requests/issues
        
        flag = False    #a flag to iterate till we don't end up with pull issues
        
        while flag != True:
            pulls_data= requests.get('https://api.github.com/repos/'+username+'/'+reponame+'/pulls?page='+fun(page))   #github api to get pull issues
            result = pulls_data.json()    #get the json data from response object of above query
            if len(result) < 30:       #we have requested for 100 info per page so if info is less than 100 that means we are done
                pulls += len(result)    #save the pull requests count and set flag to true to get out of the loop
                flag = True
            else:                        #length is 100 that means still some pull requests are there
                pulls += 30
                page += 1                #increment page count for next page
                
        total_no_issues -= pulls        #decrease pulls from total issues now it contains total no of open issues
        
        last24Hr = (datetime.datetime.now()-datetime.timedelta(hours = 24)).strftime('%Y-%m-%dT%H:%M:%SZ')  #get the date and time of last 24 hr in same format of github json data
        
        result = requests.get('https://api.github.com/repos/'+username+'/'+reponame+'/issues?state=open&per_page=100&since='+last24Hr)  #request github api to get data of last 2 hours
        last24hr_issues = result.json()    #extract data from response object which is returned by requests

        within24Hr = 0                     #variable to store no of open issues in last 24 hours
        pullsDay = 0                       #variable to store no of pull issues in last 24 hours
        
        if(len(last24hr_issues) < 100):    #if length of list is less than 100 than we dont need to iterate for further pages,we are done
            for i in range(len(last24hr_issues)):     #iterate through each entry
                if last24hr_issues[i]['created_at'] > last24Hr:   #if the created date is in the range of 24 hours increment 24 hours count
                    within24Hr += 1
                    if last24hr_issues[i].has_key('pull_request') == True:   #if it is a pull request then increment pull count 
                        pullsDay += 1
        else:                           # if data is more than  100 than we have to apply pagenation till we find info within 24 hours
            j = 1
            while len(last24hr_issues) != 0:    # doing the same as above loop
                result = requests.get('https://api.github.com/repos/'+username+'/'+reponame+'/issues?state=open&per_page=100&page='+fun(j)+'&since='+last24Hr)
                last24hr_issues = result.json()
                for i in range(len(last24hr_issues)):
                    if last24hr_issues[i]['created_at'] > last24Hr:
			within24Hr += 1
			if last24hr_issues[i].has_key('pull_request') == True:
			   pullsDay += 1
                j += 1

        sevenDaysAgo = (datetime.datetime.now()-datetime.timedelta(hours = 24*7)).strftime('%Y-%m-%dT%H:%M:%SZ')    #get the time of 7 days ago in same format as github api date time format
        result = requests.get('https://api.github.com/repos/'+username+'/'+reponame+'/issues?state=open&per_page=100&since='+sevenDaysAgo)  #github api call to find out issues within 7 days
        sevenDaysAgo_issues = result.json()
        
        within7Days = 0    #variable to store no of open issues within 7 days
        pullsWeek = 0      #variable to store no of pull request/issues within 7 days
        
        if(len(sevenDaysAgo_issues) < 100): #if length of list is less than 100 than we dont need to iterate for further pages,we are done
            for i in range(len(sevenDaysAgo_issues)):  #iterate through each entry
                if sevenDaysAgo_issues[i]['created_at'] > sevenDaysAgo:  #if the created date is in the range of 7 days increment  count
                    within7Days += 1
                    if sevenDaysAgo_issues[i].has_key('pull_request') == True:  #if it is a pull request then increment pull count 
                        pullsWeek += 1
        else:                            # if data is more than  100 than we have to apply pagenation till we find info within 7 days
            j = 1
            while len(sevenDaysAgo_issues) != 0:        # doing the same as above loop
                result = requests.get('https://api.github.com/repos/'+username+'/'+reponame+'/issues?state=open&per_page=100&page='+fun(j)+'&since='+sevenDaysAgo)
                sevenDaysAgo_issues = result.json()
                for i in range(len(sevenDaysAgo_issues)):
                    if sevenDaysAgo_issues[i]['created_at'] > sevenDaysAgo:
			within7Days += 1
			if sevenDaysAgo_issues[i].has_key('pull_request') == True:
			   pullsWeek += 1
                j += 1
        
        args = {}
        args['openissues'] = total_no_issues   #store total no of open issues
        args['24HR'] = within24Hr - pullsDay   #store total no of open issues within 24 hours
        args['sevenDaysAgo'] = within7Days - within24Hr - pullsWeek + pullsDay  #store total no of open issues within 7 days
        args['after7Days'] = total_no_issues - within7Days+pullsWeek            #store total no of issues after 7 days
	args['reponame'] = reponame           #repository name
	args['username'] = username           #username
        return render(request,'result.html',args)    #send the results to result.html
    
    else:
	args = {}
	return render(request,'home.html',args)    #if form is not post then  nothing to do wait for user to enter url and hit submit button
