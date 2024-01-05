# Week 2 - Installation of Software Development Environment

In this course, we will be chiefly be using 

- the distributed version control system (VCS) [git](https://git-scm.com/) to share code and to collaborate on coding, 
- the [Python](https://www.python.org/) programming language, and
- the container virtualization software [Docker](https://www.docker.com/).

Moreover, we highly recommend installing tools for working with the above:

- An integrated development environment (e.g. [JetBrains PyCharm](https://www.jetbrains.com/pycharm/)) or editor (e.g. [Visual Studio Code](https://code.visualstudio.com/), [NeoVim](https://neovim.io/)) that 
has matching capabilities (syntax highlighting, language server, debugger etc.)
- A graphical git client, such as e.g. [GitHub for Desktop](https://desktop.github.com/), [SourceTree](https://www.sourcetreeapp.com/), or [LazyGit](https://github.com/jesseduffield/lazygit) 
- An SQL workbench, e.g. [DBeaver](https://dbeaver.io/)
- An HTTP workbench, e.g. [Postman](https://www.postman.com/) or [httpie](https://httpie.io/cli).

We also expect you to have a [GitHub](https://github.com/) account!

## Git

### Windows 

You can download the Installer from the official [git page](https://git-scm.com/download/win).
After the download has finished, simply launch the installer and follow along through the wizard (Simply leave the default settings in each window).
Additionally, we recommend installing the [Windows Terminal](https://apps.microsoft.com/detail/9N0DX20HK701?hl=nb-no&gl=no) if you not already have it installed.

### Mac OS X

The easiest way to install git is by installing the _XCode command line tools_.
If you not already have it already, you can trigger the installation by opening a terminal window and type in 
```bash
git
```
This will trigger an assistant asking you if you want to install it. Confirm with `y` and wait.


### Linux

Most distributions will have git already installed. 
You can check whether it is available by typing the respective command below.
If it is not there, consult the documentation of the package manager for your Linux distribution on how to install it.


### Installation Check

Finally, you may open a terminal window and type 
```bash
git --version
```
to check whether git is installed correctly and what version you have (=> it should at least be greater then `2.0`)


## Python 

You will have to install both the Python interpreter itself, as well as the Python package manager [Poetry](https://python-poetry.org/)

### Windows

Open a terminal window (e.g. the Windows Terminal recommended above) and type in 
```bash
python
```
this will either take you directly into the Python interpreter (meaning that it is already installed; you can leave by typin `quit()`) 
or it will prompt you if you want to install it from the Windows app store (simplly confirm with yes).

Next, we will install `poetry` using their installation script.
For this, open up `PowerShell` (either directly or selecting it in Windows Terminal) and past in the following
```PowerShell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```
This will invoke a terminal based installation wizard that will guide you through.

### Mac OS X

For installing Python, we recommended using [Homebrew](https://brew.sh/):

Thus, if you not already have it, install it by pasting the follwing snippet into a terminal and install it:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

When the installation is complete, you can run 
```bash
brew install python
```
in order to install Python. 

Afterwards, you can check your Python version with 
```bash
python3 -V
```

Next, in order to install `poetry` run the following snippet:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Linux

Depending on your distribution, Python 3 might already be installed. 
We recommend consulting you distributions package manager's documentation to see how to get Python for your distribution.

Below, we provide some instructions that are specific for Debian-based Linux distributions such as Ubuntu:
You may notice that on these systems `python3` is already available.
However, the setup tools and the `pip` package manager, which are required for installing new Python packages, are missing.
You can install the missing dependencies by running:
```bash
sudo apt-get update
sudo apt-get install python3-pip
```

Afterwards, make sure that all Python packages and dependencies are up to date by running:
```bash
python3 -m pip install --upgrade pip setuptools wheel
```

Finally, we can install `poetry` using the installer:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

## Docker

For the Docker installation, we refer to the official documentation:

- [Windws](https://docs.docker.com/desktop/install/windows-install/)
- [Max OS X](https://docs.docker.com/desktop/install/mac-install/)
- [Linux](https://docs.docker.com/desktop/install/linux-install/)