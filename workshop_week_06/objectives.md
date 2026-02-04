# Infrastructure Worksop on 2026-02-06

The goals of this workshop are as follows:

- You should be able to connect to your group's Nrec machine and publish some static content from there
- You should be able to create the necessary source code repository(ies) on GitHub, which you will need for the FireGuard project
- You should be able to set-up a first CI-pipeline in one of your repositories 

## Prerequisites

In order to particpate in this workshop you need to bring you laptop and make sure you have:

- [git installed](https://git-scm.com/install/windows)
- [uv installed](https://docs.astral.sh/uv/getting-started/installation/)
- a user on [GitHub](https://github.com/)
- an activated user on [Nrec](https://nrec.no/)
- also it is recommended to have some IDE installed (e.g. Visual Studio Code, PyCharm, ...).

Also, be warned: This workshop (and cloud computing in general) will often require you to (at least partially) work
on the command line, often you work with Linux systems. If you have only ever used Windows and have not touched 
the command line (e.g. PowerShell) much, it is advisable to learn [some basics](https://www.terminaltutor.com/)
such as moving around in the file system, moving files around, and so on. If you know what the following commands do, you are good:
`cd`, `pwd`, `ls`, `mv`, `cp`, `rm`, `mkdir`, `touch`.

## Connecting to Nrec

Each group already has it's own virtual machine in the project `hv-ada502-spring2026`.
Log into the dashboard and see if you can identify your group's `instance`.

Now, follow the [documentation guide](https://docs.nrec.no/create-linux-machine.html#id4) from "Allowing SSH and ICMP access" 
(since the machines are already created) 
to learn how you can connect to the virtual machine from your own computer using SSH. 
You may want to read more on [SSH](https://docs.nrec.no/ssh.html) and [Network Security Groups](https://docs.nrec.no/security-groups.html)
while doing this.

**Bonus** Once you made it into the machine, you may want [to add additional users for your group members](https://documentation.ubuntu.com/server/how-to/security/user-management/#listing-adding-and-deleting-local-users)
and then disabling [login for the root account](https://documentation.ubuntu.com/server/how-to/security/user-management/#disabling-the-root-account-password).
Make sure that you add your public SSH certificates for the newly created users.


## Serving static content 

The Nrec virtual machine can be used a server to host whatever network service you might think of.
At the current stage, you probably do not have a running FireGuard system yet.
Thus, one way to at least show "_something_" could be to host some static content, e.g a documentation landing page,
which documents your system. This documentation could then grow throughout the project.

The easiest way to get started with some documentation is by using _mkdocs.
Follow [their getting started guide](https://www.mkdocs.org/getting-started/) to learn how to install it 
and serve your first documentation.
Are you able to serve this static documentation from you VM so that other can browse it too?
Perhaps, you will have to update your network security rules.

## Source code repositories

For your FireGuard project, you will at least on git repository (it is up to you whether you want 
to have everything in one single repository, a so called _monorepo_, or whether you have repositories for
each component that makes up the FireGuard system).

For this course we recommend to host your repositories as _public repositories_ on GitHub. 
When creating these, make sure that you add all group member's as collaborators.

## A first CI-pipeline 

You should also set up your first CI-pipeleine, we recommend using GitHub Actions, which is 
already integrated with your GitHub repository and is free as long as you do not plan to 
run a lot of compute-intensive jobs. 

Start by reading through the [Quickstart](https://docs.github.com/en/actions/get-started/quickstart) and 
the [Understand GitHub Actions](https://docs.github.com/en/actions/get-started/understand-github-actions).
Afterwards, try to adjust their example workflow file such that it instead runs some unit tests on 
one of your Python projects using the uv build tool.
You may also want to check out what the [uv creators are saying about using uv in GitHub Actions](https://docs.astral.sh/uv/guides/integration/github/).
