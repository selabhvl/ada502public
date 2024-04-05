# Project Peer Review

As part of the third sprint, you shall additionally review the fire-risk project of another group.
The review assignments between the groups are posted on Canvas.
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

### Source Code Management

[ ] Are all components of the fire risk system under version control?
[ ] What repository layout is used: Mono- or Poly-repo?
    [ ] for poly-repo: is there an overarching document (e.g. Readme) that describes how the repositories belong together? other means such as `git submodules`? 
    [ ] for mono-repo: is the internal repository structure well-documented?
[ ] What workflow is used in the repo? Trunk-based vs. Github-flow vs. Git-flow? Does commit-messages refer to feature/bug-tickets? Are tags or branches used to idenity features or stable versions?

### Continuous Integration and Deployment

[ ] Are there test cases for the most central functionality?
[ ] Are there CI-pipelines for each component that run the tests automatically?
[ ] Are there Dockerfiles for each component that create container images?
[ ] Do the CI-pipelines contain a step for building the Docker image and additionally pushing it to a container registry?

### Functionality 

[ ] Does the system comprise a component to automatically fetch weather data from MET?
[ ] Does the system offer a REST API for retrieving the fire risk at a given location?
[ ] Does the system comprise the fire risk model from the `frcm` project?
[ ] Is there functionality that automatically observes the fire risk at given location (i.e. fetches wather data in the background and updates the fire risk continuously)?
[ ] Perform a system test of all components together 

### Non-functional requirements

[ ] Does the system use messaging for the communication of two or more components?
[ ] Does the system store some information (at least historical wather data) persistently? What type of storage is used (file/bock storage vs. object storage vs. database: relational vs. non-relational)? Is it an appropriate way of storing this kind of information in terms of i) storage effiency ii) ease of retrieval iii) data consistency iv) disaster recovery capabilities?
[ ] Is information encrypted in-transfer and/or at-rest? How?
[ ] Is authentication and authorization implemented for specific system functionality? How?

