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

Also, using a command line editor such as `nano`, or `vim`/`vi` (important: you [exit vi](https://thenewstack.io/how-do-you-exit-vim-a-newbie-question-turned-tech-meme/) by writing `:q`)

## Connecting to Nrec

At the end of today, each group should have it's own virtual machine in the project `hvl-ada502-spring2026`,
hence, the following steps shall be undertaken **per group**, i.e. only one in your group has to do the following:

Read and follow the [documentation guide](https://docs.nrec.no/create-linux-machine.html) to learn how to create 
a virtual machine in Nrec and connect to it via SSH.
Use the following parameters when creating the instance:
- `Instance Name` -> use a name reflecting your group number, e.g. "fireguard-group-01".
- `Boot Source` -> select yould favourite Linux images, if you have no prior experience with Linux, choose `GOLD Ubuntu 24.04 LTS`.
- `Flavor/Size` -> select `c1.large`.
- `Network` -> select `dual stack`.
- `Security Groups` -> Keep the `default` network security group in the first place (you can add more later).
- `Key Pair` -> create a key pair on your local machine with `ssh-keygen` and then upload the _public key_ with "Import Key Pair".
- keep the remaining options as is and click on "Launch Instance".

You may also want to read more on [SSH](https://docs.nrec.no/ssh.html) and [Network Security Groups](https://docs.nrec.no/security-groups.html).

**Bonus** Once you made it into the machine, you may want [to add additional users for your group members](https://documentation.ubuntu.com/server/how-to/security/user-management/#listing-adding-and-deleting-local-users)
and then disabling [login for the root account](https://documentation.ubuntu.com/server/how-to/security/user-management/#disabling-the-root-account-password).
Make sure that you add your public SSH certificates for the newly created users by adding the public keys in 
the `~/.ssh/authorized_keys` file (where `~` refers to the home directory of the user, ususally `/home/<username>`.
The home directory of the `root` user is `/root`).

## Serving static content 

The Nrec virtual machine can be used a server to host whatever network service you might think of.
At the current stage, you probably do not have a running FireGuard system yet.
Thus, one way to at least show "_something_" could be to host some static content, e.g a documentation landing page,
which documents your system. This documentation could then grow throughout the project.

The easiest way to get started with some documentation is by using [_mkdocs_](https://www.mkdocs.org/).
Follow [their getting started guide](https://www.mkdocs.org/getting-started/) to learn how to install it 
and serve your first documentation.
Are you able to serve this static documentation from you VM so that other can browse it too?
- Perhaps, you will have to update your network security rules? Do you know what ports to open?
- Also, you may have to understand the difference between [0.0.0.0](https://en.wikipedia.org/wiki/0.0.0.0) and [127.0.0.1](https://en.wikipedia.org/wiki/Localhost)
and run the `mkdocs serve --help` command once.

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

**Bonus**: There are basically no limits how advanced you want to design your CI-pipelines. The bare minumum should be one _regression test_ step.
Possible things you may want to try out:
- using an existing [GitHub Action](https://github.com/marketplace/actions/publish-test-results) to publish test results 
- using [pytest](https://docs.pytest.org/) to run your unit and integration tests in a more convenient way (possibly adding it as a ["dev dependency"](https://docs.astral.sh/uv/concepts/projects/dependencies/#development-dependencies)).
- adding [test coverage](https://pytest-cov.readthedocs.io/) to your CI-pipeline,
- adding a static analysis step to your CI-pipeline, e.g. a [linter](https://docs.astral.sh/ruff/),
- adding some ![](https://img.shields.io/badge/build-passing-brightgreen)  eyecandy to your `README.md` with [shields](https://shields.io/).
