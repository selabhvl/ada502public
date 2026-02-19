# Deployment Workshop

The main objective of this week's workshop is the deployment of your current FireGuard service.
First of all, you need to decide on what cloud computing model you want to use for this.

- Infrastructure as a Service (IaaS)
- Platform as a Service (PaaS)
- Function as a Service (FaaS) / Serverless

IaaS will give you the highest degree of freedom but it also the most complex and requires most manual effort.
A "serverless"-type of deployment will make your life very easy in the beginning because you do not have to worry about:
infrastructure, operating systems, security etc;
However, you are limited in terms of of customizations (and may face some additional costs in the end).
PaaS, especially _containers_ represents a reasonable middle ground between Iaas and SaaS.
With Nrec, you have access to an IaaS (and as a consequence setting up PaaS/FaaS yourself) for free.
If you want to use some hosted PaaS or SaaS services, you will have to find them yourself (and probably also pay for them for yourself).

Simply, hop to the section that represents your chosen strategy. If you are undecided, start with reading the IaaS section.

## IaaS 

Infrastructure as a service is the most foundational of all the cloud service offerings. 
It allows you to build other cloud service types yourself. 
IaaS refers to basic virtual computing resources, i.e.

- virtual CPUs and memory with a virtual network interface card (NIC) called **virtual machine**
- virtual networks with firewall rules, represented by **virtual networks** and **security groups**
- virtual hard drives (--> will be covered in week 10)

If you have followed along with the [previous workshop](../workshop_week_06/objectives.md), you will already 
be runnng your own virtual machine, which is accessible via virtual network and accessible via specified 
network security group rules. 
Thus, it is a straightforward approach to use this machine for hosting web services such as fire guard.


### Package FireGuard

First of all, you will need to package your FireGuard application. 
The common way of packaging in Python is by creating a so-called [_wheel_](https://packaging.python.org/en/latest/overview/#python-binary-distributions) (file ending: `.whl`). 
The advantage being  that this format can handle pre-compiled binaries and version dependencies.
Using `uv`, building a wheel is very easy:

```bash
uv build
```

creates the wheel file the `dist/` subdirectory. 
 
In the spirit of continuous integration you do not want to run this manually every time on your local machine
every time you want to create a new version/release of your software product.
Instead, it should be run on you CI-server as part of a pipeline.
Hence, extend your GH Actions workflow definition with another step that creates the Python package.

In order to somehow _publish_ this package, you will have to find a place to store the resulting package.
There are several options:
- You can simply use GitHub to store the file for you as part of a [release](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository). To automatically create releases from GH Action runs, have have a look at [Softpropos great GH release action](https://github.com/softprops/action-gh-release)
- You could also publish your package on the official Python packaging index [PyPI](https://pypi.org/). In this way it will become available also for others to directly install via `pip install`. If you want to learn more you can follow [this guid](https://packaging.python.org/en/latest/tutorials/packaging-projects/).

### Run services remotely

Once, the package is created on accessible somewhere, we are ready to run it on the VM.
Log into your machine using SSH and prepare a folder for the execution (it is advisable to create a fresh Python virtual environment):

```bash
mkdir app
cd app
python3 -m venv .venv
source .venv/bin/activate
```

Next, you install your app's package into the environment.
To get the package into the machine you coudl either
- download it from PyPI (if you have uploaded there in the first step)
- download it from the GitHub release
- manually copy the `.whl` file onto the machine using `scp`.

You install the package with:
```bash
pip install {package}
```


Once that is done, you can run the application with your application's [entry point](https://docs.astral.sh/uv/concepts/projects/config/#entry-points). 
The name of the entry point and what it does is specified in `pyrproject.toml`. You may want to take a look how [I did it in the `ttf-indicator` project](https://github.com/webminz/ttf-indicator/blob/main/pyproject.toml#L17).



> [!CAUTION]
> **Problems with wrong Python versions?!**
> 
> You may experience problem when trying to install a wheel package using the Python version inside the VM, e.g.:
> ```
> ERROR: Package 'frcm' requires a different Python: 3.12.3 not in '>=3.13'
> ```
> This due to the fact that Ubuntu comes with a [specific pre-installed Python version](https://documentation.ubuntu.com/ubuntu-for-developers/reference/availability/python/), which is handled by the operating system.
> If you want to install a specific (more recent) Python version, you will have to install it yourself.
> Basically, there are two options:
> 1. Compile and install from source
> 2. Use [`uv`](https://docs.astral.sh/uv/concepts/python-versions/) to manage and install the right Python version
>
> The second option is definetely the easier option: You simply install uv on the VM and take it from there.
> The first option is the more laborious one, in return you will get the full experience about administering 
> software packaes in Linux. If you are in for ride, you can do it as follows:
> 
> First, you will have to make sure to have some system libraries installed, which are needed for compression and encryption
> ```
> sudo apt install openssl libbz2-dev libssl-dev liblzma-dev
> ```
> Next, you will have to download the Python sources from [the official website](https://www.python.org/downloads/source/) as "Gzipped source tarball" using curl.
> ```bash
> curl https://www.python.org/ftp/{version}/Python-{version}.tgz -O
> ```
> Unpack the archive and switch directories:
> ```bash
> tar xzf Python-{version}.tgz && cd Python-{version}/
> ```
> Finally, you will invoke the c-compiler via make to build Python from it's source code. The resulting file will by default installed `/usr/local/`.
> ```bash
> ./configure
> sudo make install
> ```
> Finally, there should be a `python3.{version}` on your `$PATH` that you can use to create virtual environment.

### Security and best practices

Before, we can start talking how we can automate deploying the most recent version after each successful build, we first have to talk a bit about
security and some best practices:


In general, you should apply the "_principle of least privilege_".
This means dedicating a non-root account for running FireGuard ant grant that account only the permissions it needs.


```bash
sudo adduser fireguard
sudo mkdir -p /home/fireguard/.ssh
sudo chown -R fireguard:fireguard /home/fireguard/.ssh
```

Now, generate a new SSH key pair for automation (`ssh-keygen -t ed25519 -f deploy_key`) and place that public key under `/home/fireguard/.ssh/authorized_keys` on the VM by using `scp`.


### Turn you CI-pipeline into CD-pipeline

Finally, you have to add a pipeline step that connects with SSH to your VM and runs a deployment script. 
Focus on repeatability: have the pipeline copy the latest artifact, install dependencies, update configuration, and restart the FireGuard service in a single script. 
For this, you should write a Bash script `deploy.sh` in the `/home/fireguard/` folder, which does the above.
Eventually, you add a final step to the pipeline that calls the `deploy.sh` script.
For this, you will have to store the SSH private key as a [secret and access it in the GH Action](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets):


Example GH Actions snippet:
```yaml
steps:
	# ... steps before
	- name: Set up deploy key
		run: |
			mkdir -p ~/.ssh
			echo "$DEPLOY_KEY" > ~/.ssh/deploy_key
			chmod 600 ~/.ssh/deploy_key
        env:
			DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
	- name: Run deployment
		run: ssh fireguard@{IP} /home/fireguard/deploy.sh
		
``` 


## PaaS 

You might as well use your virtual machine (IaaS) to run a platform (such as Docker) and use it to deploy your services (PaaS).
Docker is just a presentative of container technology (you may also use podman if you prefer).
It is installed under Ubuntu with 

```bash
sudo apt install docker.io
```

You can check the installation by running:
```bash
sudo docker system info
```

### Build and share a docker image

Write a Dockerfile that installs only the runtime dependencies needed by FireGuard, copies the package from the GH Actions artifact or wheel, and exposes the service port. Prefer a multi-stage build so the final image only contains the light-weight runtime image (e.g., python:slim), and label the image with the Git SHA by passing build args from your pipeline. After building, push the image to a registry you control (Docker Hub, GitHub Container Registry, etc.) by authenticating in the workflow and tagging the image with both the branch name and a release version.

Template Dockerfile:
```Dockerfile
FROM python:3.13-slim
RUN useradd --create-home fireguard
USER fireguard
WORKDIR /home/fireguard
COPY /dist .
RUN pip install {package}
EXPOSE 8000
CMD ["entry-point"]
``` 
.

### Run the container on the VM

On the VM, install Docker if necessary, pull the tagged image from the registry, and start it with a docker run command that maps the port, mounts the configuration directory, and injects secrets via environment variables or files. Use docker-compose or a simple systemd unit to keep the container running and restart it on failure. Always pull the hash you just pushed so the VM runs the exact image that your pipeline produced.

### Docker best practices


- Run your container as a non-root user, set appropriate resource limits (`--memory`, `--cpus`), and bind only the necessary ports.


## FaaS

To use "serverless" / Function as a Service (FaaS) compute you generally need to rely on some proprietary commercial
service offering. The big three being:

- AWS Lambda
- Azure Functions
- Google Gloud Functions

There could potentially also be some "backend as a service" solutions such as Firebase or Supabase. However,
those often are limited to running JavaScript/TypeScript, since we are using Python, you will have to find
something else...

You are free to explore these if you like but this is completely optionally and you may have to handle possible costs yourself.

