# Reliability and Code Quality

## Friday Lab tasks: Individual/Group work 08-10, Follow-up & Discussions 10-12

## Task 1 (Static Analysis)
- Install [SonarLint](https://plugins.jetbrains.com/plugin/7973-sonarlint) in your PyCharm IDE 
- Run SonarLint on your python project (e.g., dynamic-frcm)
- Select 10 quality issues identified by SonarLint
- Investigate how to fix these issues (Determine if the issue is also a false positive)

## Task 2 (Dynamic Analysis - DAST)
- Clone the vulnerable web application: https://github.com/tosdanoye/vul-webapp-dict-search
- Build and run the web app docker image
  ```
  docker build -t vulnapp .
  docker run -p 8080:8080 vulnapp
  
  ```
- Load the web app at: `http://localhost:8080`
- Manually perform the vulnerability tests specified on the Canvas page
- Discuss what the vulnerabilities mean and their implications

## Task 3 (Dynamic Analysis - DAST)
- Download, install, and configure [OWASP ZAP](https://www.zaproxy.org/download/)
- Start ZAP 
- In the Quick Start page, select 'Automated Scan' and point your URL to http://localhost:8080
- Select 'use traditional spider' and press 'Attack'
- When the analysis is finished, click 'Alerts' and browse through the found issues.
- Discuss the listed vulnerabilities and their implications 

## Task 4 (Installing SonarQube)
- Install [SonarQube](https://docs.sonarsource.com/sonarqube/latest/try-out-sonarqube/) server by running the docker image 

  ```
  docker run -d --name sonarqube -e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true -p 9000:9000 sonarqube:latest
  ```
- Check that you can login to SonarQube at ```http://localhost:9000``` (username=admin, password=admin)
- We'll revisit SonarQube in the discussion part on Friday.