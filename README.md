# gs-gmf-gdal-workload-identity
This is a space for sharing info with external GDAL contribs


## Requirements

### Tools

```
# move to tmp dir
cd /tmp/
# installing azure cli
sudo apt remove azure-cli -y && sudo apt autoremove -y
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# If this does not work, you can try installing the deb package directly
# Here is an example for Jammy but you can find the right one for your distribution here https://packages.microsoft.com/ubuntu/
wget https://azurecliprod.blob.core.windows.net/archive/20220421.27/ubuntu-jammy/azure-cli_2.36.0-1~jammy_all.deb
sudo dpkg -i azure-cli_2.36.0-1~jammy_all.deb

# install azure plugin for k8s api auth
cd /tmp/
wget https://github.com/Azure/kubelogin/releases/download/v0.0.26/kubelogin-linux-amd64.zip
unzip -j kubelogin-linux-amd64.zip bin/linux_amd64/kubelogin
## move the bin in your path
mv kubelogin ~/.local/bin/kubelogin

# installing kubectl (for interacting with kuberentes api)
cd /tmp/
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
## move the bin in your path
mv kubectl ~/.local/bin/kubectl

# installing k9s  (for interacting with kuberentes api, like kubectl but with style)
## download the binary based on your architecture
wget https://github.com/derailed/k9s/releases/download/v0.25.18/k9s_Linux_x86_64.tar.gz
tar -xvzf k9s_Linux_x86_64.tar.gz
chmod u+x k9s
## move the bin in your path
mv k9s ~/.local/bin/k9s
```
### Access

```
az login
az account list
az account set --subscription <...>
az aks get-credentials --resource-group gs-gdal-tests --name gs-gdal-tests --file ~/.kube/gs_gdal_cluster
```


### Usefule tools

copy files into pod
```
kubectl cp --help               
Copy files and directories to and from containers.

#from local to remote
kubectl cp /tmp/foo <some-pod>:/tmp/bar -c <specific-container>

```

login into pod
```
kubectl exec mypod -it -- bash
```

image for debuging
```
https://github.com/camptocamp/docker-azure-debug-helper
```


## Azure Cluster Hands-on

## Kubernetes 

### Accessing cluster 

```
export KUBECONFIG=~/.kube/gs_gdal_cluster
```


### Creating mypod

```
# pod-test.yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: mypod
    azure.workload.identity/use: "true"
  name: mypod
  namespace: default
spec:
  containers:
  - args:
    - bash
    image: python:latest
    name: mypod
    tty: true
  serviceAccountName: workload-identity-sa

```

### Storage

url = https://gsgdaltests.blob.core.windows.net/
storage_name = test
