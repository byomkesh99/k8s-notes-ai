# K8s Commands

## MAC Shot-cuts

        Move the insertion point to the beginning of the line -- Control-A
        Move the insertion point to the end of the line -- Control-E

IP Forwarding on MAC

        Check status: sysctl net.inet.ip.forwarding
        Enable IP Forwarding: sudo sysctl -w net.inet.ip.forwarding=1
        Disable IP Forwarding: sudo sysctl -w net.inet.ip.forwarding=0

API-Resources

> kubectl api-resources  # To know all the command shot-cuts. The commands list out all the shotcuts.

(Example Below)
> kubectl get po    # Pods
> kubctl get ns     # Namespaces
> kubectl get cp    # Configmap

## All Commands Related to POD

> kubectl get deployments
> kubectl get pod
> kubectl get pod --watch  # to watch POD status
>
> kubectl get pods --watch # If you wanted to avoid running command again & again to see status
> kubectl get replicase>
> kubectl logs [pod name]
> kubectl logs nginx-depl-777888776-bvhdjjk>
>
> kubectl create deployment mongo-meraNaam --image=mongo
> kubectl describe pod <pod_name>
> kubectl exec -it mongo-depl-777888776-bvhdjjk -- bin/bash   # mongo-depl-777888776-bvhdjjk is pod name and it gives interactive shell of running mongo DB
>
> kubectl get all --all-namespaces

$ kubectl delete deployment mongo-depl

$ kubectl apply -f <configFile.yml>

$ kubectl replace --force -f nginx.yml [after edit the yml file it just delete the old pod & create new one] 

[Shift+Option]
How to know the version of any APP service, like, POD, Service(svc), replicaSet (rs) etc
$ kubectl explain service

$ kubectl get pod --show-lebels

$ kubectl get endpoint # or kubectl get ep   #(This will display the pod of services with listening ports)

$ k get ds -A # gives objects of daemonset from all the name spaces otherwise we have to specify the namespace
$ kubectl get ds -n kube-system

## Example of Imperative Commands

create deploy nginx-demo --image=nginx -n ns-demo

> kubectl get deploy -n ns-demo
> kubectl get po -n ns-demo -o wide
> kubectl exec -it nginx-demo-cccbdc67f-l2jf7 -n ns-demo -- sh
> kubectl scale --replicas=3 deploy/nginx-demo -n ns-demo
> kubectl expose deploy/nginx-demo --name=svc-demo --port 80 -n ns-demo

## Essential Commands

> kubectl version
> kubectl cluster-info
> kubectl config
> kubectl get nodes
> kubectl get pods
> kubectl get services
> kubectl get namespaces or ns
> kubectl create ns/pod/deployment/service/configmap
> kubectl describe pod <pod_name>
> kubectl logs <pod_name>
> kubectl exec -it <pod_name> -- /bin/bash
> kubectl create -f <fine_name>.yaml
> kubectl apply -f <fine_name>.yaml
> kubectl delete -f <fine_name>.yaml
> kubectl expose pod <pod_name> --type=NodePort --port=80
> kubectl scale deployment <deployment_name> --replicas=3
> kubectl rollout status deployment/<eployment_name>
> kubectl rollout undo deployment/<eployment_name>
> kubectl config view
> kubectl config use-context <context_name>
> kubectl exec webapp -- cat /log/app.log    # read file inside running container

## Kubernetes CKA Exam Practice exercise

URL: [https://github.com/alijahnas/CKA-practice-exercises]

> kubectl run nginx --image=nginx
> kubectl describe pod newpods-x9fjq  # From running pod identify Image that used. It also shows which node its running i.e. master or worker
> kubectl get pod -o wide  # Also gives a details of which node this pod is running
> kubectl run redis --image=redis987 --dry-run=client -o yaml > redis.yaml    # Dry run redis POD with generating its yaml file togather
> kubectl create -f redis.yaml    # And then this will create and run actual POD in the system
> kubectl edit pod redis      # If you wanted to edit the Redis pod from redis987 -> redis

### EDIT POD and Run Again

> kubectl edit pod <POD_NAME>
(Run the above command. This will open the pod specification in an editor (vi editor). Then edit the required properties. When you try to save it, you will be denied. This is because you are attempting to edit a field on the pod that is not editable.)
> kubectl delete pod webapp
(You can then delete the existing pod by running the command)
> kubectl create -f /tmp/kubectl-edit-ccvrq.yaml
(Then create a new pod with your changes using the temporary file)

**2ND OPTION*
> kubectl get pod webapp -o yaml > my-new-pod.yaml
> vi my-new-pod.yaml
(make the changes to the exported file using an editor (vi editor). Save the changes)
> kubectl delete pod webapp
(Then delete the existing pod)
> kubectl create -f my-new-pod.yaml
(Then create a new pod with the edited file)

**EDIT-DEPLOYMENT*
> kubectl edit deployment my-deployment
(With Deployments you can easily edit any field/property of the POD template. Since the pod template is a child of the deployment specification,  with every change the deployment will automatically delete and create a new pod with the new changes. So if you are asked to edit a property of a POD part of a deployment you may do that simply by running the command)

### Deployment - for time saving commands specially in Exam

**CREATE DEPLOYMENT*

Create an NGINX Pod
> kubectl run nginx --image=nginx
> kubectl run custom-nginx --image=nginx --port=8080  # As example

Generate POD Manifest YAML file (-o yaml). Don't create it(--dry-run)
> kubectl run nginx --image=nginx --dry-run=client -o yaml

Create a deployment
> kubectl create deployment --image=nginx nginx
> kubectl create deployment webapp --image=kodekloud/webapp-color --replicas=3

Generate Deployment YAML file (-o yaml). Don't create it(--dry-run)
> kubectl create deployment --image=nginx nginx --dry-run=client -o yaml

Generate Deployment YAML file (-o yaml). Don’t create it(–dry-run) and save it to a file.
> kubectl create deployment --image=nginx nginx --dry-run=client -o yaml > nginx-deployment.yaml

Make necessary changes to the file (for example, adding more replicas) and then create the deployment.
> kubectl create -f nginx-deployment.yaml

In k8s version 1.19+, we can specify the --replicas option to create a deployment with 4 replicas.
> kubectl create deployment --image=nginx nginx --replicas=4 --dry-run=client -o yaml > nginx-deployment.yaml 

**AND SERVICES*

Create a Service named redis-service of type ClusterIP to expose pod redis on port 6379
> kubectl expose pod redis --port=6379 --name redis-service
> kubectl expose pod redis --port=6379 --name redis-service --dry-run=client -o yaml
(This will automatically use the pod's labels as selectors) OR
> kubectl create service clusterip redis --tcp=6379:6379 --dry-run=client -o yaml 
(This will not use the pods labels as selectors, instead it will assume selectors as app=redis. You cannot pass in selectors as an option. So it does not work very well if your pod has a different label set. So generate the file and modify the selectors before creating the service)

Create a Service named nginx of type NodePort to expose pod nginx's port 80 on port 30080 on the nodes:
> kubectl expose pod nginx --type=NodePort --port=80 --name=nginx-service --dry-run=client -o yaml

(This will automatically use the pod's labels as selectors, but you cannot specify the node port. You have to generate a definition file and then add the node port in manually before creating the service with the pod.)

> kubectl create service nodeport nginx --tcp=80:80 --node-port=30080 --dry-run=client -o yaml

(This will not use the pods labels as selectors)

Both the above commands have their own challenges. While one of it cannot accept a selector the other cannot accept a node port. 
I would recommend going with the kubectl expose command. If you need to specify a node port, generate a definition file using the same command and manually input the nodeport before creating the service.

### Handy commands to know the K8s Services

How to see all the services
> kubectl get svc

What is the type of the default kubernetes service?
> kubectl describe svc describe svc kubernetes  # kubernetes - is a service name. See the details of service

Service Endpoint
> kubectl describe svc describe svc kubernetes | grep endpoint   
Endpoint is necessary to identify if service has been mapped to POD. If endpoint is zero the its not mapped, check the services selector and pods lebels. Both should be same.

### Namespace commands quick reference

> kubectl get ns  # Get the list of all namespaces
> kubectl get pods  # this will list the pods under default namespace
> kubectl get pods --namespace=kubesystem
> kubectl create -f pod-definitaion.yml --namespace=dev-ns
> kubectl create deployment redis-deploy --image=redis --replicas=2 --namespace=dev-ns  # As example
> kubectl get pods -n dev
> kubectl config set-context --current --namespace=<your_namespace>    # Switch to different namespace

to permanent move the pods in particular namespace

apiVersion: v1
kind: Pod
metadata:
  name: myapp_pod
  namespace: dev-ns
  labels:
    app: myapp
    type: front-end-app
spec:
  containers:
    - name: nginx-containers
      image: nginx

> kubectl create namespace dev  # To create new namespace
> kubectl config set-context $(kubectl config current-context) --namespace=dev      # If you wanted to switch to particular namespace but to utilize others NS you need to use --namespace

### Limit you resources under one Namespace

File: compute-quota.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
    name: compute-quota
    namespace: dev
spec:
    hard:
        pods: "10"
        requests.cpu: "4"
        requests.memory: 5Gi
        limits.cpu: "10"
        limits.memory: 10Gi

> kubectl create -f compute-quota.yaml

### Imperative Commands in the K8s World

**CREATE*
> kubectl run --image=nginx nginx
> kubectl create deployment --image=nginx nginx
> kubectl expose deployment nginx --port 80

**EDIT/UPDATE*
> kubectl edit deployment nginx
> kubectl scale deployment nginx --replica=5
> kubectl set image deployment nginx nginx=nginx:1.18
> kubectl replace -f nginx.yaml

**DELETE*
> kubectl delete -f nginx.yaml

**IMPERATIVE OBJECT CONFIGURATION FILES*
> kubectl create -f nginx.yaml
> kubectl edit pod myapp-pod  # Remember the change will make here will NOT reflect in the nginx.yml file. Only make sure you do not bother about the file in this situation

Lets say you have modified the nginx.yaml file and updated the nginx image from 1:11 to 1.18. And after then to reflect the change, you should hit the following.
This will DELETE your old running container and run the new one
> kubectl replace --force -f nginx.yaml

### Declarative Commands in the K8s World

`
apiVersion: v1
kind: Pod
metadata:
  name: myapppod
  labels:
    app: myapp
    type: front-end-app
spec:
  containers:
    - name: nginx-containers
      image: nginx
`
Lets say you have the object configuration file, now with the following command just run the container.

**CREATE OBJECTS*
> kubectl apply -f nginx.yaml
> kubectl apply -f /path/to/config/*.yaml  # it will run all the container

**UPDATE OBJECTS*
> kubectl apply -f nginx.yaml  # After made change in your nginx.yaml file, just hit the same command

> kubectl api-resources
> kubectl explain pods
> kubectl explain pods.spec
> kubectl explain pods --recursive

### Helping Commands on Scheduling

Any pod to run in the system must need a Node, without the Node the POD will show "Pending" state. By default Kubernetes automatically assign the node.
Here were are practicing Manual Scheduling.

POD difination file: nginx.yaml

`
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  nodeName: node01    # you can use any node name as per your need like node2/3/4 or controlplane
  containers:
    - image: nginx
      name: nginx

`

> kubectl create -f nginx.yaml
> kubectl replace --force -f nginx.yaml   # If you wanted to re-run your POD after some modification on nginx.yaml file. Exmaple Node name changed

### Labels & Selector - helping commands

Replicaset-definition.yaml
`
apiVersion: app/v1
kind: ReplicaSet
metadata:
  name: simple-webapp
  labels:
    app: App1
    function: Front-end
  annotations:
    buildversion: 1.34
spec:
  replicas: 4
  template:
    metadata:
      labels:
        app: App1
        function: Front-end
    spec:
      containers:
        -name: simple-webapp
         image: simple-webapp-img
  selector:
    matchLabels:
      app: App1

`
We have deployed a number of PODs. They are labelled with "tier", "env" and "bu". How many PODs exist in the dev environment "(env)"?
> kubectl get pods --selector app=App1
> kubectl get pods --selector env=dev
How many objects are in the prod environment including PODs, ReplicaSets and any other objects?
> kubectl get all --selector env=prod --no-headers | wc -l
Identify all the PODs which is part of the prod environment, the finance BU and of frontend tier?
> kubectl get all --selector env=prod,bu=finance,tier=frontend --no-headers

### Taint & Toleration - useful commands

Taint - applies on Node and Toleration - applies on PODs

**Taint*
There are 3 taint-effect 1) NoSchedule 2) PreferNoSchedule 3) NoExecute

> kubectl taint nodes node-name key=value:taint-effect
> kubectl taint node node05 app=myapp:NoSchedule  # as example
> kubectl taint node node01 spray=mortein:NoSchedule  # Another example

Remove the Taints from Controlplane or any nodes
> kubectl describe node controlplane | grep -i taints
Output -->>  Taints:             node-role.kubernetes.io/control-plane:NoSchedule
> kubectl taint node controlplane node-role.kubernetes.io/control-plane:NoSchedule-   # Add the "-" at the end

**Toleration*

how pod-definition.yaml looks like
`
apiVersion: v1
kind: Pod
metadata:
  name: mosquito-pod
spec:
  containers:
    -name: nginx-container
     image: nginx:1.34
  tolerations:
    - key: spray
      value: mortein
      effect: NoSchedule
      operator: Equal
`

### Node Selector - quick ref commands

This feature aim to put the application POD in a higher resourced machine/node

> kubectl label nodes <node_name> <label_key>=<label_value>
> kubectl label node node01 size=Large  # Marking a particular node with lebel Large
> kubectl label node node01 color=blue  # Another example



`
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
spec:
  containers:
    - name: ml-app-processing
      image: ml-app-processing
  nodeSelector:
    size: Large

`
**CONDITION*
A condition which limits the NodeSelector :- if you have a requirement where you wanted to make a condition i.e. place the POD either Large OR Midium Node.
Or NOT Small Node then NodeSelector not going to serve the purpose. For that we need Node Affinity

### Node Affinity - Quick Ref commands

`
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
spec:
  containers:
    - name: ml-app-processing
      image: ml-app-processing
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: size
            operator: In
            values:
                - Large
                - Medium

OR (to understand condition just adding last few code line)
`

- matchExpressions:
  - key: size
    operator: NotIn
    values:
    - Small
`
**TESTED CODE BELOW*
`
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: red
  name: red
spec:
  replicas: 2
  selector:
    matchLabels:
      app: red
  strategy: {}
  template:
    metadata:
      labels:
        app: red
    spec:
      containers:
      - image: nginx
        name: nginx
        resources: {}
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: node-role.kubernetes.io/control-plane
                operator: Exists
`
Check the code above, as condition you can add "In" operator for Node values "Larger" or "Medium". Or if you wanted put POD only in "small" Node with "NotIn" operator.

How to find Labels exist on node node01?
> kubectl describe node node01 | less  # find the labels and check
> kubectl get pod -o wide  # This will display in which node what PODs are running

### Resource allocation - restrict the limits

Please check the ResourceRequiremement document for it. There is no special command for it. Just edit your POD YML and adjust the resource
Then delete the POD and recreate it.

`
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
    - name: nginx-containers
      image: nginx
      ports:
        - containerPort: 8080
      resources:
        requests:
          memory: "4Gi"
          cpu: 2
        limits:       # This is the limit i.e. this POD can utilize maximum 8 Gi memory and upto 6 CPU's
          memory: "8Gi"
          cpu: 6
`
> kubectl replace --force -f /tmp/kubectl--edit-3399948575636.yaml

### DaemonSets and its commands

Its basically a POD or PODs which will be running on all the worker nodes to share data like Monitoring Solutions, Log Viewers etc. Ex: Kube-Proxy

`
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: Monitoring-Daemon
  labels:
    app: monitoring-agent
spec:
  replicas: 4
  template:
      metadata:
        name: monitoring-agent
        labels:
          app: monitoring-agent
      spec:
        containers:
          - name: monitoring-agent
            image: monitoring-agent
  selector:
    matchLabels:
      app: monitoring-agent
`

> kubectl create -f daemon-set-definination.yaml
> kubectl get daemonset
> kubectl get daemonsets -A  # Get the all DaemonSet
> kubectl describe daemon moitoring-Daemon

Deploy a DaemonSet for FluentD Logging with specification 1) Name: elasticsearch 2) Namespace: kube-system 3) Image: registry.k8s.io/fluentd-elasticsearch:1.20

File: my_daemonset.yaml
`
apiVersion: apps/v1
kind: DaemonSet
metadata:
  labels:
    app: elastics
  name: elastics
  namespace: kube-system
spec:
  selector:
    matchLabels:
      app: elastics
  template:
    metadata:
      labels:
        app: elastics
    spec:
      containers:
      - image: registry.k8s.io/fluentd-elasticsearch:1.20
        name: fluentd-elasticsearch
        resources: {}
`
Tips: Create Deployment first with command line dry command, and then edit the file, replace Kind with DaemonSet, remove replicas, strategy, status .
and then create DaemonSet with kubectl command.
> kubectl create deployment elastics --image=registry.k8s.io/fluentd-elasticsearch:1.20 -n kube-system --dry-run=client -o yaml > my_daemonset.yaml # Just as Example

### Static POD

Kubelet having capability to read POD defination file from the following path/directory. If you do any changes related to upgrade
in the pod defination file, it will automatically take effect with the help of kubelet. Note that kubelet only works on POD level.
It will not take care any other definitation like replicaset, deployment etc. 
If you delete the file from the "manifests" directory, the pod will be destroyed. This kind of POD calls Static PODs.

/etc/kubernetes/manifests

The path mentioned in the "kubelet.service" file.
--pod-manifest-path=/etc/kubernetes/manifests \\
or
--config=kubeconfig.yaml 

and then kubeconfig.yaml file path define line below staticPodPath: /etc/kubernetes/manifest by default.
But actual config file: /var/lib/kubelet/config.yaml, looks for line "staticPodPath" will get the path of staticPod that means you can customize your "staticPodPath" path.

Example: create a static pod like busy-box(sleep 1000) and put in the /etc/kubernetes/manifests to run it automatically.

> kubectl run static-busybox --image=busybox --restart=Never --dryrun=client -o yaml --command -- sleep 1000 > static-busybox.yaml
place the file static-busybox.yaml in "/etc/kubernetes/manifests" directory. The POD will automatically run.

to know daemon of static POD use -
> docker ps   # There are other commands also.
> kubectl get pod --watch  # to watch POD status

### Priorities Classes

It basically to priritize the Critical and non-critical jobs in the system. It is namespace independent.
The ranges are from negative number to positive number i.e. 2,000,000,000 to 1,000,000,000 -> to -> -2,147,483,648

> kubectl get priorityclass

NAME                      VALUE        GLOBAL-DEFAULT   AGE   PREEMPTIONPOLICY
system-cluster-critical   2000000000   false            18m   PreemptLowerPriority
system-node-critical      2000001000   false            18m   PreemptLowerPriority


File: Priority-class.yaml
`
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000000000
description: "Priority class for the mission critical pods"
preemptionPolicy: PreemptLowerPriority
`

File: pod-definition.yaml
`
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  labels:
    app: nginx
spec:
  containers:
    - name: nginx-containers
      image: nginx
      ports:
        - containerPort: 8080
  priorityClassName: high-priority   # Instance from Priority-class.yaml
`

> kubectl get pods -o custom-columns="NAME:.metadata.name,PRIORITY:.spec.priorityClassName"  # compare the priority classes of pods

### Multiple Scheduler - Custom Scheduler

(Please refer K8s-Scheduler documentation page)

> kubectl get events -o wide  # To know all the custom scheduler
> kubectl logs my-custom-scheduler -n kube-system
> kubectl get sa my-custom-scheduler -n kube-system   # To identify sa=service_account used for this scheduler

### Admission Controllers - Quick Commands

> kube-apiserver -h | grep enable-admission-plugins   # View Enabled Admission Controller

( You will see the list enabled functions )

> kubectl exec kube-apiserver-controlplane -n kube-system -- kube-apiserver -h | grep enable-admission-plugin

### Metrics Server

> kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
(Install the Metrics Server first and then the following "TOP" command will work)
> kubectl top pods -A
NAMESPACE      NAME                                   CPU(cores)   MEMORY(bytes)
default        ryno                                   13m          30Mi
default        tiger                                  1m           16Mi
default        rabbit                                 98m          250Mi
kube-flannel   kube-flannel-ds-hbvdb                  7m           12Mi
kube-flannel   kube-flannel-ds-jrkxw                  6m           12Mi

### Logs - Kubernetes

> kubectl logs -f <POD_NAME> <CONTAINER_NAME>
> kubectl logs -f event-simulator-pod event-simulator

> kubectl logs -f webapp-1   # It works
> kubectl logs -f webapp-1-myPod simple-App-Container   # Also works, it also give logs specific to container level

### Rollout and Versioning

When you first create a deployment it triggers a rollout along with Revision. With time when you upgrade your application the Revision number also increase.
It helps to keep track of rivisions. Rolling Update is the "default deployment" strategy.

> kubectl create -f deployment-definition.yaml    # To create deployment
> kubectl get deployment  # to view the deployment
> kubectl apply -f deployment-definition.yaml    # Update the deployment
> kubectl set image deployment myapp-deployment nginx=nginx:1.8.9   # Update the deployment BUT preferred method via definnition File
> kubectl get replicasets  # Try before and after rollback to see the difference
> kubectl rollout status deployment/myapp-deployment  # Know the rollout status
> kubectl rollout history deployment/myapp-deployment  # show the revisions
> kubectl rollout undo deployment/myapp-deployment     # Rollback changes

Little more explanation about SET Container Image of Deployment
> kubectl set image deployment <Deployment_Name> <Container_Name>=nginx:1.8.9
> kubectl set image deployment frontend simple-webapp=nginxapp/webapp-color:v2

OUTPUT - Notice the changes of deployment - by keep watching it

controlplane ~ ✖ k get replicasets       # Before Image SET to nginxapp/webapp-color:v2
NAME                  DESIRED   CURRENT   READY   AGE
frontend-59dfbc6688   4         4         4       8m44s

After Image Set nginxapp/webapp-color:v2

controlplane ~ ➜  k get replicasets    # after few min
NAME                  DESIRED   CURRENT   READY   AGE
frontend-59dfbc6688   3         3         3       19m
frontend-799cddccfc   2         2         2       6s

controlplane ~ ➜  k get replicasets    # after few min
NAME                  DESIRED   CURRENT   READY   AGE
frontend-59dfbc6688   1         1         1       19m
frontend-799cddccfc   4         4         4       24s

controlplane ~ ➜  k get replicasets    # Finally Update Done :)
NAME                  DESIRED   CURRENT   READY   AGE
frontend-59dfbc6688   0         0         0       20m
frontend-799cddccfc   4         4         4       52s

### Commands and Arguments in K8s

In Dockerfile we mention like as below
`
From: Ubuntu
Entrypoint ["sleep"]
CMD ["5"]
`

The same thing has been express in K8s in following ways

File: POD-definitation.yaml
`
apiVersion: v1
kind: Pod
metadata:
  name: centos-sleeper-pod
spec:
  containers:
    - name: centos-sleeper
      image: centos
      command: [sleep]
      args: ["10"]
`
> kubectl create -f POD-definitation.yaml

### Environment Variable in K8s - ConfigMaps

> docker run -e APP_TEXT=green simple-webapp   # How we declare ENV in Docker

File: POD-definitation.yaml
`
apiVersion: v1
kind: Pod
metadata:
  name: centos-sleeper-pod
spec:
  containers:
    - name: centos-sleeper
      image: centos
      command: [sleep]
      args: ["10"]
      env:                Here we directly defining ENV variable but we can do it via "ConfigMAPs" too
      - name: APP_COLOR
        value: green
`

### To VIEW ConfigMaps

> kubectl get configmaps
> kubectl describe configmaps   (in more details)

**Imperative-Commands*

> kubectl create configmap <config_name> --from-literal=<key_s>=<value_s>
> kubectl create configmap app-config --from-literal=APP_COLOR=blue --from-literal=APP_MOD=prod
> kubectl create configmap myapp-config-map --from-literal=APP_COLOR=lightgreen --from-literal=APP_POINTER=sharp  # Just Example
> kubectl create configmap  <config_name> --from-file=<path_to_file>
> kubectl crete configmap app-config --from-file=app_config.properties 

**Declarative-Way*

File: config-map.yaml:
`
apiVersion: v1
kind: ConfigMap
metadata:
  name: APP-config
data:
   APP_COLOR: green
   APP_MODE: stage
`
> kubectl create -f config-map.yaml 

Then apply ConfigMaps to POD -- File:~ pod-definition.yaml
`
apiVersion: v1
kind: Pod
metadata:
  name: simple-webapp-color
spec:
  containers:
    - name: web-app-color
      image: webapp-color
      ports:
        - containerPort: 8080
      envFrom:
        - configMapRef:
            name: APP-config
`
> kubectl create -f pod-definition.yaml

### CREATING SECRETs and ITS Usefulness

(This is Specially for Database)

**Secrets*
DB_Host: mysql
DB_User: root
DB_Password: passwd

**Imperative*
> kubectl create secret generic <secret_Name> --from-literal=<key_name>=<values_n>
> kubectl create secret generic myapp-secret --from-literal=DB_Host=mysql --from-literal=DB_User=root --from-literal=DB_Password=passwd
> kubectl create secret generic db-secret --from-literal=DB_Host=sql01 --from-literal=DB_User=root --from-literal=DB_Password=passw0rd@123  # Another example
(When too many secrets will be there, it will be difficult yo manage)

> kubectl create secret generic <secret_Name> --from-file=<path_to_file>      # provide the key-value from File
> kubectl create secret generic my_app-secret --from-file=app_secret.properties

**Declarative*
> kubectl create -f secret_fileName.yaml

**TO_VIEW_SECRETS*
>> kubectl get secret
>> kubectl describe secrets

### Multi_Container PODs

** Co-located Containers
** Regular Init Containers    (Example: DB POD must run early then main application POD for thst this Init Container helps)
** Sidecar Containers

File: pod-definition.yaml
`
apiVersion
kind: Pod
metadata:
  name: complex-webapp
  labels:
    name: complex-webapp
spec:
  containers:
    -name: web-appl
     image: web-appl
     ports:
      - containerPort: 8080
  initContainers:               # We can see the multi-container implementation
    - name: db-checker
      image: busybox
      command: 'wait-for-db-to-start.sh'
    - name: api-checker
      image: busybox
      command: 'wait-for-another-api.sh'
`

### Autoscaler - Horizontal POD AS (HPA)

Before increase the POD horizontally, monitor the load i.e. CPU and memory utilization for POD and then plan for scaling.

>> kubectl top pod my-app-pod
>> kubectl scale deployment my-app --replicas=3

HPA - plays role to monitor your POD resource consumption/load and increase or decrease POD based on CPU utilization.

Example:

File: deployment-definitation.yaml
`
apiVersion: app/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      app: my-app
    spec:
      containers:
        - name: my-app
          image: nginx
          resources:      # resource field
            requests:
              cpu: "250m"
            limits:
            cpu: "500m"
`
**Imperative_HPA*
> kubectl autoscale deployment my-app --cpu-percent=50 --min=1 --max=10
(After creating this autoscale instance, it will increase/decrease cpu's according to load )
> kubectl delete hpa my-app
> kubectl get hpa (your hpa info)
> kubectl get hpa --watch
NAME               REFERENCE                     TARGETS              MINPODS   MAXPODS   REPLICAS   AGE
nginx-deployment   Deployment/nginx-deployment   cpu: <unknown_>/80%   1         3         7          14m

" cpu: <unknown_>/80% " - Means resource field missing in the nginx-deployment

**Declarative_HPA*
`
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 1
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 50
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
`

### Vertical Pod Autoscaling - VPA

(VPA - does not have Kubernetes built-in; hence we need to explicitly deploy it)
> kubectl apply -f https://github.co/kubernetes/autoscaler/ ... ... ... (Find the correct Path)
> kubectl get pod -n kube-system | grep vpa

File: app-vpa.yaml
`
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: my-app-vpa
spec:
  targetRef:
    apiVersion: app/v1
    kind: Deployment
    name: my-app
  updatePolicy:
    updateMode: "Auto"      # Check different from Internet
  resourcePolicy:
    containerPolicies:
      - containerName: "my-app"
        minAllowed:
          cpu: "250m"
        maxAllowed:
          cpu: "2"
        controlledResources: ["cpu"]
`

> kubectl describe vpa my-app-vpa
> kubectl get pods -l app=flask-app
> kubectl describe vpa flask-app

### Explore - Skooner - Monitoring tool

### Security - Certificates - Handy Commands

**OPEN_SSL_COMMANDS*

(The below commands to make your local CA - CERTIFICATE-AUTHORITY)
> openssl genrsa -out ca.key 2048                                     # Creating Key
> openssl req -new -key ca.key -subj "/CN=KUBERNETES-CA" out ca.csr   # Creating CSR=Certficate Signing Request
> openssl x509 -req -in ca.csr -signkey ca.key -out ca.crt            # Sign Certificate. You are going to SIGN all CSR with this command

(The below one particularly for users)
> openssl genrsa -out my_user.key 2048
> openssl req -new -key my_user.key -subj "/CN=user_real_name" -out my_user.csr    # csr = Certificate Signing Request
> openssl x509 -req -in my_user.csr -CA ca.crt -CAkey ca.key -out my_user.crt

Another Example: Lets say you are creating Admin Certificates

> openssl genrsa -out admin.key 2048
> openssl req -new -key admin.key -subj "/CN=kube-admin" -out admin.csr    # csr = Certificate Signing Request
> openssl x509 -req -in admin.csr -CA ca.crt -CAkey ca.key -out admin.crt

**CERTIFICATE_API*

Use-Case: Suppose there is new team team member joied and you eanted to give user access to K8s Cluster. In this case this Certificate Api method works.

1) User created his/her "my_user.csr" file encode (base_64) it and via K8s my_user.yaml file send it for "Admin" to sign it.
2) Now Admin will see the new user certificate sign request by hitting command below command

> kubectl get csr
> kubectl certificate approve my_user
(this "approve" command will enable to approve newly requested CSR certificate to sign)
> kubectl get csr my_user -o yaml
(This command will show the certificate in a encoded format. User need to decode it and use the real certificate for cluster access)
> echo "LSfkjhfwkdhuddjdkjhddjkjdiiqoqo8290478rodqw89ey21ejqwohqe ... ... .." | base64 --decode  # Decode the certificate

> kubectl certificate approve user_smit
You are not aware of a request coming in. What groups is this CSR requesting access to? Check the details about the request. Preferably in YAML.
> kubectl get csr <new_agent_smith> -o yaml

groups:
  - system:masters
  - system:authenticated

> kubectl certificate deny agent-smith  # to deny certificate
> kubectl delete csr agent-smith   # Delete CSR request

**View and Check Kubernetes certificate*
open file - /etc/kubernetes/manifests/kube-apiserver.yaml and check the certificates.
> kubectl get pods --kubeconfig config
I would like to use the dev-user to access test-cluster-1. Set the current context to the right one so I can do that.
> kubectl config use-context research --kubeconfig /root/my-kube-config     # my-kube-config is a Conf File - Check the security Documentation

We can follow the same process to add Dev, SIT, UAT and Prod cluster access credentials.
>> kubectl config view     <- to view kube config
OR
>> kubectl config view --kubeconfig=my-custom-config

### AUTHORIZATION - Role & Rolebindings - Namespace Level

To view the roles:
>> kubectl get roles
>> kubectl get rolebindings     # to view role bindings

To more abour role and &
>> kubectl describe role developer
>> kubectl describe rolebinding devuser-developer-binding

How user will check what access user is having?

>> kubectl auth can-i create deployments
(yes)
&
>> kubectl auth can-i delete nodes
(no)
Admin can try link this to check access of users.

>> kubectl auth can-i create deployments --as dev-user
&
>> kubectl auth can-i delete nodes --as dev-user

(ANSWER will come with yes/no)

**IMPERATIVE*
> kubectl create role developer --verb=list,create,delete --resource=pods
PolicyRule:
  Resources  Non-Resource URLs  Resource Names  Verbs
  pods       []                 []              [list create delete]
> kubectl create rolebinding dev-user-binding --role=developer --user=dev-user


### Cluster Level Roles - Rolebindings

**IMPORTANT*
To List a Namespaced and Non-namespaced Resources - USE IT A HELP GUIDE - ON RESOURCE SIDE
> kubectl api-resources --namespaces=true
> kubectl api-resources --namespaces=false

Cluster Admin - Can view, create, delete Nodes
Storage Admin - Can view, create, delete PV's

>> kubectl get clusterroles
>> kubectl get clusterrole --no-headers=false | wc -l      <- get counts
>> kubectl get clusterrolebindingd --no-header | wc -l
>> kubectl describe clusterrolebindingd cluster-admin

**IMPERATIVE_Way*
                **Cluster Admin*
Example:
> kubectl create clusterrole michelle-role --verb=get,list,watch --resource=nodes
> kubectl create clusterrolebinding cluster-role-binding-michelle --clusterrole=michelle-role --user=michelle

To Verify
> kubectl describe clusterrole michelle-role
> kubectl describe clusterrolebinding cluster-role-binding-michelle

**IMPERATIVE_Way*
                **Storage Admin*
> kubectl create clusterrole storage-admin --resource=persistentvolumes,storageclasses --verb=list,create,get,watch
> kubectl create clusterrolebinding michelle-storage-admin --clusterrole=storage-admin --user=michelle

Note Find the HELP from below commands. It has a sample command as an example as well.
> kubectl create clusterrole --help | less
> kubectl create clusterrolebinding --help | less

### Service Accounts - Handy Commands

As we know there are mainly 2 types of accounts works in K8s.

  1) User Account
  2) Service Account - for application

**IMPERATIVE*
>> kubectl create serviceaccount deboard_sa         <- debord_sa is service account name
>> kubectl get serviceaccount                         <- to view
>> kubectl describe serviceaccount deboard_sa
&
>> kubectl get sa -A | grep default                <-- view all the defult service account

**TOKENs*
> kubectl create token deboard_sa     # By-default generated token active for 1 hour then de-activated
> kubectl create token deboard_sa --duration 2h   # validaty extension
> jq -R 'sokit(".") | select(length > 0) | .[0],.[1] | @base64d | fromjson' <<< euhy653jslkjfg3g84kwlkjnr32rwnfenlfnfowe4  # DECODE the Token & see details

### Image Security - Handy commands

Private - Repository:

>> docker login pravete-registry.io
>> docker run private-registry.io/apps/internal-app
>> docker run myprivateregistry.com:5000/nginx:alpinenginx:alpine   # Just another example

If you need to pass the cred for auto auth and pull images
>> kubectl create secret docker-registry regcreden  \
        --docker-server=private-registry.io        \
        --docker-username=registry-user             \
        --docker-password= registry-password         \
        --docker-email=registry-user@email.com        \

Note: regcreden = is just a name of the secret that you are creating. Later you are going to mention it in POD definition file while pulling the image

Another Example:
>> kubectl create secret docker-registry my_priv_credential --docker-server=myprivateregistry.com:9000 --docker-username=dok_user --docker-password=dok_password --docker-email=dok_user@myprivateregistry.com

### Network Policy (Incoming: Ingress, & Expernal: Egress)

>> kubectl get networkpolicies
>> kubectl describe netpol payroll       # payrole is policy name

### Kubectx and Kubens - Command Line Utilities

**THEY are External TOOL Installed*
[Link_To_Install_For_MAC](https://formulae.brew.sh/formula/kubectx)

>> kubectx <context_name>
>> kubectx -c                 # Display current context
>> kubectx kind-cka-cluster3
>
>> kubens  # Display all the namespace
>> kubens <new_namespace>
>> kubens kube-system  # Switching to kube-system namespace

### Storage - Persistent Volume Claims - Quick Commands

Docker Volume mount commands as reference

> docker run -v data_volume:/var/lib/mysql mysql    # Your_Host_Machine:Container_Machine
> docker run -v data_volume_2:/var/lib/mysql mysql
> docker run -v /data/mysql:/var/lib/mysql mysql
> docker run --mount,type=bind,source=/data/mysql,target=/var/lib/mysql mysql

**Volume Mount_In_K8s_World*

You need to create Persistant Volume first and the claim the storage space as Persistent Volume Claim

File: pv-definitio_2.yaml

`
apiVersion: v1
kind: PersistentVolume
Metadata:
    name: pv-vol 
spec:
    accessModes:
      - ReadWriteOnce
    capacity:
        storage: 5Gi
    hostPath:
      path: /var/data     # From local Host Machine
`

>> kubectl create -f pvc-definitation_2.yaml

File: pvc-definitation.yaml (PV Claim)

`
apiVersion: v1
kind: PersistantVolumeClaim
metadata:
  name: moaclaim
spec:
  accessModes:
    - ReadWriteOnce 
  resources:
    requests:
      storage: 500Mi
`
>> kubectl get pv
>> kubectl describe pv <PV_Name>
>> kubectl create -f pvc-definitation.yaml
>> kubectl get persistentvolumeclaim   # pvc are same
>> kubectl get pvc
>> kubectl delete persistentvolumeclaim myclaim    # to delete PVC, note PVC will not get deleted if Container is running with that PVC
>> kubectl get pv pv-log

### Storage Class - GCP/Azure/AWS

Useful Commands:

> kubectl get storage
> kubectl describe pvc <my_local-pvc>

### Networking - CoreDNS

**Handy_NETWORKING_Commands*

> ip link
> ip addr add 192.168.1.10/24 dev eth0
> ip route add 192.168.1.0/24 via 192.168.2.1
> netstat -plnt
> ip addr
> ip route
> arp
> route
> cat /proc/sys/net/ipv4/ip_forward

This CoreDNS can be run as POD and it uses configuration File - /etc/coredns/Corefile

:53 {
  errors
  health
  Kubernetes cluster.local in-addr.arpa ip6.arpa {
    pods insecure
    upstream
    fallthrough in-addr.arpa ip6.arpa
  }
  prometheus : 9153
  proxy . /etc/resolv.conf
  cache 30
  reload
}

note:  errors, health, prometheus, proxy, reload etc. all are plugins. All record bydefault falls under cluster.local

> kubectl get configmap -n kube-system

CoreDNS provide a service call kubedns to access the DNS for other services.

> kubectl get service -n kube-system

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
NAME            TYPE              CLUSTER-IP            EXTERNAL-IP           PORT(S)
kube-dns        ClusterIP         10.96.0.40            <none_>                53/UDP, 53/TCP 
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

> cat /etc/resolv.conf
output:
nameserver         10.96.0.40
search  default.svc.cluster.local  svc.cluster.local  cluster.local

DNS configuration on PODs are done by Kubernetes automatically when the PODs are created. Kubelet is resposible for that.
> cat /var/lib/kubelet/config.yaml
... ...
clusterDNS:
    - 10.96.0.10
clusterDomain: cluster.local 

CoreDNS record entry: 
10-244-1-5    10.244.1.5
10-244-2-5    10.244.2.5
web-service   10.107.37.188 


Test it -> host web-service
output:
web-service.default.svc.cluster.local has a address 10.97.206.196 

Some useful commands:
> kubectl get svc -n kube-system                              (to know the coreDNS service)
> kubectl get pods -n kube-system                             (check coreDNS pods)
> kubectl describe pod core-dns************ -n kube-system    (it will display the pod details, under -ARGs: conf you will see coreDNS file path)
What is the root domain\zone configured for this kubernetes cluster?
> kubectl get configmap -n kube-system                        (to see currently running CoreDNS Pods)
> kubectl describe configmap coredns -n kube-system
