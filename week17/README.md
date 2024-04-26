# Week 17: Cloud Deployment Experiment

For the final stage of the project we will provide the oppertunity to deploy you fire firsk application 
in a Azure Kubernetes Cluster. The cluster was created as part of the lecture on _Infrastructure as Code (IaC)_
in week 17. You may want to take a look at the [Terraform Code](https://github.com/selabhvl/ada502public/tree/main/week17/tf), which describes how it is provisioned.

Below, you will find a description on how to get your applications into the cluster.

## Creating a Certificate for the Service Principal login

_Certificate-based Authentication (CBA)_ for service principals in Azure is based on X.509 certificates.
In order to authenticate you will have to create your own key pair consisting of a _public certificate_ and a _private key_.
After you have shared the certificate with us, you will be able to use it to authenticate as a service principal 
using your private key. 

The easiest option to create such a key pair is by using OpenSSL, which is available in Linux, Mac OS X, and Windows Subsystem for Linux.
When the `openssl` binary is installed, you can issue a self-signed certificate together with its associated private key, using the following command:
```shell
openssl req -newkey rsa:4096 -nodes -keyout key.pem -x509 -days 365 -out certificate.pem
```
This will create two files:

- `certificate.pem` and 
- `key.pem`

The first one you will share with us and the second one you will have to keep at a safe place.

In order to authenticate using `az` CLI later, you will also have to create a single file that contains certificate
and private key concatenated. The easiest way of doing this is under Bahs/Zsh/...:
```shell
cat key.pem certificate.pem > login_cert.pem
```

Moreover, the `kubelogin` command, which will be used to authenticate the service principal at the Kubernetes API of the provided AKS cluster,
requires the certificate and key to be present in the form of a PKCS#12 bundle (using the old SHA-1 Linux encoding).
You create it like this (no need to understand the meaning of all parameters here :wink:):

```shell
openssl pkcs12 \
	-certpbe PBE-SHA1-3DES \
	-keypbe PBE-SHA1-3DES \
	-export \
	-macalg sha1 \
	-in certificate.pem \ 
	-inkey key.pem \
	-out login_cert.pfx
```

If you are on Windows, you may investigate `keytool` and how to use it in order to achieve the equivalent.

## Authenticating to Azure and the AKS cluster

Make sure that you have:

- [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
- [Kubectl](https://kubernetes.io/docs/tasks/tools/) and 
- [Kubelogin](https://azure.github.io/kubelogin/install.html) 

installed. 

Before logging into Azure, you may want to set the `$AZURE_CONFIG_DIR` environment variable to a separate folder to 
keep your session with the provided service principal isolated from other Azure subscriptions that you may be working on.
Otherwise, the `az` tool will save its data into `$HOME/.azure/`.

```sh
export AZURE_CONFIG_DIR=/path/where/you/want/it
```

You then log into the service principal account with:
```sh
az login --service-principal \
    --username "{{service_principal_oid}}" \ # will be provided to you group by us
    --tenant "0a1d7995-b734-4d29-8b90-ba9a075bdd6d" \ # @hvl.no organization
    --password "/path/to/your/login_cert.pem" # adjust this to your machine
```

When you then call:
```sh
az account show
```
you should see something like:
```json
{
  "environmentName": "AzureCloud",
  "homeTenantId": "0a1d7995-b734-4d29-8b90-ba9a075bdd6d", 
  "id": "bcb6368c-c036-4f3a-a10e-d07635e32e01",
  "isDefault": true,
  "managedByTenants": [],
  "name": "Azure subscription 1",
  "state": "Enabled",
  "tenantId": "0a1d7995-b734-4d29-8b90-ba9a075bdd6d",
  "user": {
    "name": "YOUR_SERVICE_PRINCIPAL_OBJECT_UUID",
    "type": "servicePrincipal"
  }
}
```

Now, you should be able to log into the provided container registry with:
```sh
az acr login -n {{acr_name}}.azurecr.io
```
where 

> `acr_name=experimentacr`

Note that the value of `acr_name` has been determined after creating that particular resource in the lecture using Terraform.

This means that you can use `docker push` to upload images to the container registry. To log out, just call `docker logout`.

To retrieve the AKS login credentials, you initially have to call:
```sh
az aks get-credentials -n {{cluster_name}} -g {{resource_group}} --file /path/to/kube_config
```
where 
> `resource_group=experiment-rg`

> `cluster_name=experiment-k8s`

We are using the `--file` parameter here to download the `kube_config`-file to a given location to keep it 
isolated from potential cluster credentials that you are already working with.
Otherwise, the file would have been stord in `$HOME/.kube/`.


Thus, you should set your `$KUBECONFIG` environment variable to the path pointing to that file in order to make `kubectl`
work with the right cluster.

```sh
export KUBECONFIG=/path/to/kube_config
```

Finally, it remains to instruct `kubelogin` to use a service principal log in rather than the interactive log in:
```sh
kubelogin convert-kubeconfig -l spn
export AAD_SERVICE_PRINCIPAL_CLIENT_ID={{service_principal_appid}}
export AAD_SERVICE_PRINCIPAL_CLIENT_CERTIFICATE=/path/to/login_cert.pfx
```

## Build images and deploy Kubernetes resources

All of your custom software components that are part of the fire-risk system should be available as a Docker Image.
This means building a container image from source using a Dockerfile and then uploading it into a container registry.
You may either choose to upload to the public Docker Hub or using the provided private Azure Container Registry.
**Note:** Make sure that your images are built for the `linux/amd64` platform otherwise you might experience weird problems.

Images are built using the following command (assuming you are in the app source folder containing a `Dockerfile`).

```sh 
docker build -t {{app_name}}:{{tag_name}} --platform linux/amd64 .
```
Use a suitable name for `app_name` and provide a `tag_name` if needed, if the latter is left out `latest` will be used.

Then you tag your image with the container repository name, e.g. if using the Azure container registry:
```sh 
docker tag {{app_name}}:{{tag_name}} {{acr_name}}.azurecr.io/{{app_name}}:{{tag_name}}
```
and push it via
```sh  
docker push {{acr_name}}.azcurecr.io/{{app_name}}:{{tag_name}}
```

Afterwards, you may use `kubectl` to define as many `deployments`, `statefulsets`, `services`, `configmaps`, and `secrets`
as you like to get your app running.

Have a look into [test-app.k8s.yml](./test-app.k8s.yml) and [test-app-srv.k8s.yml](./test-app-srv.k8s.yml) for 
a minimal example of a deployment and a service.
