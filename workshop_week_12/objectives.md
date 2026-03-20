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
microk8s join $IP:$PORT/$TOKEN
```

The IP, PORT, and TOKEN values will be provided by me during the workshop session on 2026-03-20.

Probably, some network security group rules have to be configured


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

Download the `.csr` file and transfer it to me,
I will then sign the request and provide you with a `.crt` file plus the `ca.crt` file.
Upload these files to your virtual machine, and then create the `~/.kube/config` as follows:

```bash
cat > ~/.kube/config <<EOF
apiVersion: v1
kind: Config
clusters:
- name: microk8s
  cluster:
    certificate-authority-data: $(base64 -w 0 ./ca.crt)
    server: https://158.39.75.244:16443
contexts:
- name: test-nrec
  context:
    cluster: microk8s
    user: username
    namespace: $NAMESPACE
current-context: test-nrec
users:
- name: username
  user:
    client-certificate-data: $(base64 -w 0 ./username.crt)
    client-key-data: $(base64 -w 0 ./username.key)
EOF
```
I will provide you with the value for the `NAMESPACE`,
you have to make sure that the certificate, and key files are present
as well as the value for the username if consistent with what you chose in the `CN`
when creating the CSR.

Finally, you can thest the connection using 
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
