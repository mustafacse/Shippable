from django.shortcuts import render
import requests
import datetime
import time
import json
from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponseRedirect, HttpResponse

def fun(x):
    return str(x)

def getIssues(request):
    if request.POST:
        url = request.POST.get('url_val')
        str = url.split('/')

        if(str[0] != 'www.github.com' or str[1] == "" or str[2] == ""):
        	args = {}
            	return render(request,'home.html',args)
        username = str[1]
        reponame = str[2]
        #print username,reponame
        issues = requests.get('https://api.github.com/repos/'+username+'/'+reponame)
        #issues = json.loads('https://api.github.com/repos/'+username+'/'+reponame)
        repoItem = json.loads(issues.text or issues.content)
	print repoItem
        #print "Django repository created: " + repoItem['created_at']
        total_no_issues = repoItem.get('open_issues_count')
        #print total_no_issues
        
        #print issues.json()
	page = 1
        pulls = 0
        flag = False
        while flag != True:
            pulls_data= requests.get('https://api.github.com/repos/'+username+'/'+reponame+'/pulls?page='+fun(page)+'&state=open&pre_page=100')
            result = pulls_data.json()
            if len(result) < 100:
                pulls += len(result)
                flag = True
            else:
                pulls += 100
                page += 1
        total_no_issues -= pulls
        last24Hr = (datetime.datetime.now()-datetime.timedelta(hours = 24)).strftime('%Y-%m-%dT%H:%M:%SZ')
        
        result = requests.get('https://api.github.com/repos/'+username+'/'+reponame+'/issues?state=open&per_page=100&since='+last24Hr)
        last24hr_issues = result.json()

        within24Hr = 0
        pullsDay = 0
        if(len(last24hr_issues) < 100):
            for i in range(len(last24hr_issues)):
                if last24hr_issues[i]['created_at'] > last24Hr:
                    within24Hr += 1
                    if last24hr_issues[i].has_key('pull_request') == True:
                        pullsDay += 1
        else:
            j = 1
            while len(last24hr_issues) != 0:
                result = requests.get('https://api.github.com/repos/'+username+'/'+reponame+'/issues?state=open&per_page=100&page='+fun(j)+'&since='+last24Hr)
                last24hr_issues = result.json()
                for i in range(len(last24hr_issues)):
                    if last24hr_issues[i]['created_at'] > last24Hr:
			within24Hr += 1
			if last24hr_issues[i].has_key('pull_request') == True:
			    pullsDay += 1
                j += 1

        sevenDaysAgo = (datetime.datetime.now()-datetime.timedelta(hours = 24*7)).strftime('%Y-%m-%dT%H:%M:%SZ')
        result = requests.get('https://api.github.com/repos/'+username+'/'+reponame+'/issues?state=open&per_page=100&since='+sevenDaysAgo)
        sevenDaysAgo_issues = result.json()
        within7Days = 0
        pullsWeek = 0
        if(len(sevenDaysAgo_issues) < 100):
            for i in range(len(sevenDaysAgo_issues)):
                if sevenDaysAgo_issues[i]['created_at'] > sevenDaysAgo:
                    within7Days += 1
                    if sevenDaysAgo_issues[i].has_key('pull_request') == True:
                        pullsWeek += 1
        else:
            j = 1
            while len(sevenDaysAgo_issues) != 0:
                result = requests.get('https://api.github.com/repos/'+username+'/'+reponame+'/issues?state=open&per_page=100&page='+fun(j)+'&since='+sevenDaysAgo)
                sevenDaysAgo_issues = result.json()
                for i in range(len(sevenDaysAgo_issues)):
                    if sevenDaysAgo_issues[i]['created_at'] > sevenDaysAgo:
			within7Days += 1
			if sevenDaysAgo_issues[i].has_key('pull_request') == True:
			    pullsWeek += 1
                j += 1
        
        args = {}
        args['openissues'] = total_no_issues
        args['24HR'] = within24Hr - pullsDay
        args['sevenDaysAgo'] = within7Days - within24Hr - pullsWeek + pullsDay
        args['after7Days'] = total_no_issues - within7Days+pullsWeek
	args['reponame'] = reponame
	args['username'] = username
        return render(request,'result.html',args)
    
    else:
	args = {}
	return render(request,'home.html',args)    
