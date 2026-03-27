# Project Peer Review

As part of the third sprint, you shall additionally review the fire-risk project of another group.
The review assignments between the groups [are posted on Canvas](https://hvl.instructure.com/courses/25065/assignments/76727).
Your task is to retrieve to latest stable code snapshot from your assigned group 
(either by cloning it locallay and/or forking their repository) and try following 
their `README` description on how to make the system running.
The primary goal is to make the other's group solution running.
However, if you run into _technical problems_ make sure to not spent more than **2 hours** (in total) on
trying to "fix" their solution!
Also, keep in mind that several points in the review check list may be answered without running the code.

We would like to invite you to help your fellow student progress and help them to improve their solution.
Write your review in the way that you yourself would have liked to receive this type of feedback!
To help you a bit with the question "what to look at", we have created a small _checklist_ below.
Try to answer each point in 1-3 sentences. 
But feel free to add additional aspects and topics that you would like to give feedback on for your peers!

## Review Checklist

### General Architecture

- [ ] What is the general architecture of the application? Monolith vs. Microservices vs. something in-betwen? What are the central _components_
of the application? What are their roles? How do they interact and communicate?
- [ ] Are all the components developed by the group itself under version control? Are they in the same repository or spread across multiple repositories (if so: is there documentation where to find everything)?
- [ ] What workflow is used in the repo/project? Trunk-based vs. Github-flow vs. Git-flow? Do commit-messages refer to features/bug-tickets? Are tags or branches used to idenity features or stable versions?
- [ ] Is there a backlog or statement stating what features are working what is currently missing?

### Continuous Integration and Deployment

- [ ] Are there test cases for the most central functionality? What type of tests are run (unit tests, integration tests, end-to-end tests)? Are there any additional static analysis checks?
- [ ] Are there CI-pipelines for each component or the whole application that run the automatically? When do they run (on push, on pull request, on schedule)?
- [ ] Are there Dockerfiles for each component or the whole application that create container images to package the application? If the group is using some form of SaaS/PaaS (like supabase/firebase): how does the deployment process work?
- [ ] Is the appliation reachable on the web? IP address? Is there TLS a.k.a. https

### Functionality 

- [ ] Does the system comprise a component to automatically fetch weather data from MET?
- [ ] Does the system offer a REST API for retrieving the fire risk at a given location?
- [ ] Does the system comprise all call to the fire risk model `frcm`?
- [ ] Is there functionality that automatically observes the fire risk at given location (i.e. fetches wather data in the background and updates the fire risk continuously)?
- [ ] Perform a system test of all components together: Does it work? What is missing?

### Non-functional requirements

- [ ] Does the system use messaging for the communication of two or more components?
- [ ] Does the system store some information (at least historical wather data) persistently? What type of storage is used (file/bock storage vs. object storage vs. database: relational vs. non-relational)? 
- [ ] Is information encrypted in-transfer and/or at-rest? How?
- [ ] Is authentication and authorization implemented for specific system functionality? How?

