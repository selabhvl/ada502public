# Workshop 3: Service Orchestration 

The goal of (voluntary) workshop is to try out Kubernetes.

There are two ways to do this:

- set up Kubernetes yourself
- join my existing cluster


## Set-up yourself 

You can spin up your own Kubernetes cluster on your group's Nrec machine.
Kubernetes is open-source software, hence you can simple download the binaries
of the individual Kubernetes components and configure everything with `kubeadm`.
However, this is a bit more cumbersome.

The easiest way to set-up Kubernetes on your own Hardware, if you are using Canonical's `snap`,
is to use [microk8s](https://canonical.com/microk8s/docs/getting-started#1-overview)


You install it with:
```bash
sudo snap install microk8s --classic --channel=1.35
```

In order to access microk8s withou super user privileges, add you user to the `microk8s` group.
```bash
sudo usermod -a -G microk8s $USER # add user to the group in order to run the binary
```

You will have to refres your session (e.g. by re-connecting the SSH session) before the changes become active.
Afterwards, you can access the cluster with
```bash
microk8s kubectl
```

or by downlading the config file so that you can use `kubectl` directly (note that `kubectl` also has to be installed first).
```bash
mkdir -p ~/.kube
chmod 0600 ~/.kube
microk8s config > ~/.kube/config
```

Now, you are ready to go the set up whatever resources you like in your private cluster:

You may also consider:

- supplying storage (in order to set up stateful applications like databases) using `rook-ceph`
- configuring `cert-manager` together with an `ingress`-controller
- setting up `prometheus` for obeservability


## Joining my cluster 

I have already done the above, so you don't have to.
You may join the cluster with your virtual machine or ask for user access by providing a certificate.

### Join the cluster 

If you want to contribute to the cluster with the computing power of your virtual machine,
your are more than welcome to do so by running:

```bash
microk8s join 158.39.75.244:25000/$TOKEN
```

The value for `TOKEN`, you will get from me, if you want to try this out, please contact me via E-mail
so we can arrange a session to peer the nodes :wink:

> [!IMPORTANT]
> In order to make the clusters talk with each other, firewall excemptions must be put in place.
> According to the [microk8s documentation](https://canonical.com/microk8s/docs/services-and-ports)
> the nodes are talking to each other using port `25000`. Thus, make sure that access to this
> port is allowed from IP `158.39.75.244`. (maybe also port `16443` needs to be open but we will see...)


### Access to the cluster 

To authenticate with a cluster, the `kubectl` command is using a TLS certificate
stored in a so called "_kube config_", the latter is basically a YAML file 
containing the sensitive certificate data. 
You can specify what _kube config_ to use by setting the `KUBECONFIG` environment variable,
otherwise it will look for the default at `~/.kube/config`.

In order to obtain the certificate proceed as follows:

1. Generate a private key
```bash
openssl genrsa -out username.key 4096 # change the file name if you like
```

2. Generate a _certificate signing request (CSR)_:
```bash
openssl req -new -key username.key -out username.csr -subj "/CN=username"
```

Important is that you chose a distinct name for the value of `CN` (common name).

Download the `.csr` file and transfer it to me.

In particular, in order to get access to my cluster you **must provide** the following:

- The `.csr` file containing the signing request using the correct username in the `CN`-field.
- The name of your group, a.k.a. the name for your personal `namespace` in Kubernetes.
- The IP from the virtual machine to access the cluster from (I would like to avoid having the Kubernetes API on the public internet and 
create individual firewall rules for that.)

In return, I will provide you with
- The `ca.crt` ([_certificate authority_](https://en.wikipedia.org/wiki/Certificate_authority)) used to connect to the cluster 
- The signed certificate (`.crt` file) used to authenticate yourself with the cluster 
- The confirmed `namespace` name


I will then sign the request and provide you with a `.crt` file plus the `ca.crt` file.
Upload these files to your virtual machine, and then create the `~/.kube/config` as follows:

```bash
cat > ~/.kube/config <<EOF
apiVersion: v1
kind: Config
clusters:
- name: microk8s-patrick
  cluster:
    certificate-authority-data: $(base64 -w 0 ./ca.crt)
    server: https://158.39.75.244:16443
contexts:
- name: patricks-nrec-cluster
  context:
    cluster: microk8s-patrick
    user: $USERNAME
    namespace: $NAMESPACE
current-context: test-nrec
users:
- name: $USERNAME
  user:
    client-certificate-data: $(base64 -w 0 ./username.crt)
    client-key-data: $(base64 -w 0 ./username.key)
EOF
```
Before running this comman, make sure that:

- You are inside your Nrec VM
- Your current directory contains `username.crt`, `username.key` and `ca.crt` (otherwise you maye have to rename/move files around)
- You have set the `USERNAME` env variable with a value that is consistent with the `CN`-field in the signing request (`export USERNAME=username`)
- You hvae set the `NAMESPACE` env variable with your group's name (`export NAMESPACE=groupNN`)


Finally, you can test the connection using 
```bash
kubectl get nodes
```


### Work inside the cluster 

Every group that asks for user access, will get their own namespace.
In that namespace you can freely create all the resources you like.
If you want to expose some services to the outside, you may define an ingress rule,
which will use the already confiured ingress controller with TLS termination:


```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: groupNN-ingress # adjust
  namespace: groupNN # adjust
spec:
   rules:
   - host: groupNN.ada502-fireguard.live # adjust
     http:
       paths:
       - path: /
         pathType: Prefix
         backend:
           service:
             name: your-service # adjust
             port:
               number: 80 # adjust
```

Also make sure that all your resources are created in your group's namespace `groupNN`!


If you need stateful services (like databases), you will have to create _persistent volume claim (PVC)_ like so:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: your-volume-name
  namespace: groupNN
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: ceph-rbd
  resources:
    requests:
      storage: 5Gi # please be considerate here, should be enough

```

> [!TIP]
> During the live demo on Zoom, I did not manage make the data in the PostgreSQL container persistent.
> This was due to using the wrong path! If I would have read the [container documentation](https://hub.docker.com/_/postgres#pgdata)
> correctly, I would have avoided the problem. It clearly states: "Important Note: (for PostgreSQL 17 and below) Mount the data volume at /var/lib/postgresql/data and not at /var/lib/postgresql because mounts at the latter path WILL NOT PERSIST "
> Thus, make sure to ALWAYS read the documentation of the container image properly to familiarize yourself **where** the mount points inside the container are!
