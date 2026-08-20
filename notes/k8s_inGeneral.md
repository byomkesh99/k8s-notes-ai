When you install the Kubernetes in a Node indeed you install the following componants:

* API Servers : Acts as the front end of the K8s, user management devices, CLI all talk to the API.
* etcd : Distributed reliable key-value store, think of this way if you are having mutiple master nodes & worker nodes than who is gonna keep info of them to avoid conflict, its etcd.
* kubelet : Is a agent which is run on each node in the Cluster.
* Container Runtime : is the underline software i.e. used to run containers. (in our case it will be Docker, but there are many options as well)
* Controller: is the brain behind orchestration, monitors the nodes when goes down, it makes decision to bring new container in such cases.
* Scheduler : Distributing work across multiple nodes.

See Scree-shot of master-worker.jpeg

K8s - Command line utility:

kubectl - it call kube control. kubectl helps to deploy and manage the application on K8s cluster.

$ kubectl run hello-minikube    <-|  # It helps to deploy application in the cluster.
$ kubectl cluster-info          <-|  # to know about the cluster.
$ kubectl get node              <-|  # Listing all nodes in the cluster.


Configure Network interfaces for Ubuntu machine:

# /etc/net/interfaces
# configuring enp0s8 interface
auto enp0s8
iface enp0s8 inet static
    address 192.168.1.31
    netmask 255.255.255.0
    
POD:    
Kubernetes does not deploy the container directly in the worker nodes, the containers are encapsulated in a kubernetes object known as POD.
A POD is a single instance of an application, its kind a smallest object you can create in Kubernetes. 

Reference PODs -
Kubernetes Concepts - https://kubernetes.io/docs/concepts/
Pod Overview- https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/

The below yml file express the top level yml definition for creating PODs or Deployment or Replica set.

pod-definition.yml 
------------------
apiVersion:
kind:
metadata:

spec:
------------------

Kind            Version
------------------------
POD         |   v1
Service     |   v1
ReplicaSet  |   apps/v1
Deployment  |   apps/v1
-----------------------


With Values:

pod-definition.yml 
------------------
apiVersion: v1  <- v1 is a string
kind: Pod       <- Pod also is a string     # What are the kinds you wanted to use like POD, Services, Replica set etc.
metadata:
  name: App-pod       <- From here till down "type" is a Dictionary # Metadata is a data about Pods
  labels:
    app: App
    type: frontend

spec:                                       # specification is about lists of containers, remember 1 POD can hold mutiple containers
  containers:
    - name: ngnix-container
      image: ngnix
------------------

To create the POD -
Command: 
>> kubectl create -f pod-definition.yml    # to start POD
>> kubectl get pods						# Lists of running pods
>> kubectl delete --all pods 			# Delete all pods

Instruction: Create a Kubernetes Pod definition file using values below:
Name: prostgres
Labels tier -> db-tier
Container name: postgres
Image: postgres

-------------------
apiVersion: v1
kind: Pod
metadata:
  name: postgres
  labels:
    tier: db-tier
    
spec:
  containers:
    - name: postgres
      image: postgres
--------------------      

Extending property ... 

--------------------
apiVersion: v1
kind: Pod
metadata:
  name: postgres
  labels:
    tier: db-tier
spec:
  containers:
    - name: postgres
      image: postgres
      env:
        - name: POSTGRES_PASSWORD
          value: mysecretpassword
------------------      


## Kubernetes Controller Replication:
====================================

Controller Replication is the brain in the K8s cluster, it monitors and manage the PODs, if any POD become unhealthy then it creates another POD.
It manages muti-nodes too. So it actually mantain the High Availability (HA) of PODs in the K8s cluster. Even if one POD is there in the single node and
by any chance it become unhealthy then Replication Controller (RC) bring another new container in the POD.

Loadbalancing and Scaling: If application demands more container based on loads increases the RC automatically deploy new container for load balancing purpose.

Replication controller (RC) & Replica Set (TS) : Both does the same work but they are NOT the same. RC is older concept, RS is a new recomanded way to setup replication.

File: rc-definitation.yml -

apiVersion: v1
kind: ReplicationController
metadata:
  name: App-rc
  lebels:
    app: App
    type: front-end
spec:                       # This is a specification for replication controller
  template:
    metadata:
        name: postgres
        labels:
            tier: db-tier
    spec:                   # This is a specification for POD - because POD managed by RC
        containers:
            - name: postgres
              image: postgres
              env:
                - name: POSTGRES_PASSWORD
                  value: mysecretpassword
  replicas: 3

Note above, we have mentioned the number of replication which will maintain the number of PODs in the cluster.
make a note template & replicas the children of "spec:" or other way they should be in the same vertical line.

>> kubectl create -f rc-definitation.yml        # It will create PODs here which 3
>> kubectl get replicationcontroller            # RC with current state
>> kublectl get pods                            # Lists of number of PODs


### Replica Set
=================

https://kubernetes.io/docs/reference/kubectl/cheatsheet/

replicaset-definition.yml (code tested)

------------------------------

apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: App-replicaset
  labels:
    app: App
    type: front-end
spec:                       # This is a specification for replicaSet
  template:
    metadata:
      name: App-pod
      labels:
        app: App
        
    spec:                   # This is a specification of Pods
      containers:
        - name: nginx-container
          image: nginx

  replicas: 3
  
  selector: 
      matchLabels:
          app: App
		  
------------------------------
  
Note: please note above the difference between RC & RS, RS is having another item i.e. "selector"

>> kubectl create -f replicaset-definition.yml
>> kubectl get replicaset
>> kubectl describe replicaset
>> kublectl get pods
>> kubectl delete replicaset App-replicaset

What is the special about Labels and Selectors?

As we know ReplicaSet(RS) controller monitor & maintain the desired counts of containers in the PODs.
Now when there are 100 + of containers how RS going to identify the and track the containters for maintain the desire counts.
That is via lebelings and selectors. See the screen shot K8_RS_Labels_selectors it will give an idea.

Scale: If you wanted to update the number of replica then just update the number i.e. "replicas: 3" & run the following command.

>> kubectl replace -f replicaset-definition.yml
OR

Without modify in the file -
>> kubectl scale --replicas=6 -f replicaset-definition.yml
OR
>> kubectl scale --replicas=6 replicaset App-replicaset  # replicaset is "TYPE" & App-replicaset is "NAME" here

More: ReplicaSet Template as Example:
https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/


Distribution of PODs in my cluster -
>> kubectl get pods -o wide
NAME                     READY   STATUS    RESTARTS   AGE   IP           NODE        NOMINATED NODE   READINESS GATES
App-replicaset-9grlp   1/1     Running   0          12m   10.244.2.5   kubenode1   <none>           <none>
App-replicaset-9vn82   1/1     Running   0          11m   10.244.1.6   kubenode2   <none>           <none>
App-replicaset-xcwwd   1/1     Running   0          19m   10.244.1.5   kubenode2   <none>           <none>


>> kubectl get all

NAME                         READY   STATUS    RESTARTS   AGE
pod/App-replicaset-9grlp   1/1     Running   0          13m
pod/App-replicaset-9vn82   1/1     Running   0          11m
pod/App-replicaset-xcwwd   1/1     Running   0          19m


NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   23h



NAME                               DESIRED   CURRENT   READY   AGE
replicaset.apps/App-replicaset   3         3         3       19m



Display Number of Pods in a replicaset.

kubemaster:~/k8s/pods# kubectl get replicaset
NAME               DESIRED   CURRENT   READY   AGE
App-replicaset   3         3         3       17m


Deleting Single Pods to test whether desire pod in a replica set maintain or not.

kubemaster:~/k8s/replica$ kubectl get pods
NAME                     READY   STATUS    RESTARTS   AGE
App-replicaset-9grlp   1/1     Running   0          87s
App-replicaset-vwvbm   1/1     Running   0          7m51s
App-replicaset-xcwwd   1/1     Running   0          7m51s

kubemaster:~/k8s/replica$ kubectl delete pod App-replicaset-vwvbm   # App-replicaset-vwvbm is the pod name
pod "App-replicaset-vwvbm" deleted

kubemaster:~/k8s/replica$ kubectl get pods
NAME                     READY   STATUS    RESTARTS   AGE
App-replicaset-9grlp   1/1     Running   0          108s
App-replicaset-9vn82   1/1     Running   0          10s
App-replicaset-xcwwd   1/1     Running   0          8m12s


Now I tried to create new Pod mentioned in pod-definition.yml file.

kubemaster:~/k8s/pods# kubectl create -f pod-definition.yml
pod/App-pod created

kubemaster:~/k8s/pods# kubectl get pods
NAME                     READY   STATUS        RESTARTS   AGE
App-pod                0/1     Terminating   0          7s
App-replicaset-9grlp   1/1     Running       0          7m50s
App-replicaset-9vn82   1/1     Running       0          6m12s
App-replicaset-xcwwd   1/1     Running       0          14m

See, replicaset terminating the extra Pod to maintain desire count of Pods.


Another Example of Replicaset:

----------------------

apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: frontend
  labels:
    app: mywebsite
    tier: frontend
spec:
  replicas: 4
  template:
      metadata:
        name: App-pod
        labels:
          app: App
      spec:
        containers:
          - name: nginx
            image: nginx
  selector:
    matchLabels:
      app: App
------------------------


### Deployment: 
===============

*** Note: In production, always you will run Deployment definition not Replica Definition.


File: deployment-definition.yml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: App-deployment
  labels:
    app: App
    type: front-end
spec:                       
  template:
    metadata:
      name: App-pod
      labels:
        app: App
        
    spec:                   
      containers:
        - name: nginx-container
          image: nginx

  replicas: 3
  
  selector: 
      matchLabels:
          app: App
		  

>> kubectl create -f deployment-definition.yml		  


>>  kubectl get all			# It created deployment app then replica and then pods.

NAME                                   READY   STATUS    RESTARTS   AGE
pod/App-deployment-5dcf6cc75-6trxz   1/1     Running   0          14s
pod/App-deployment-5dcf6cc75-k6cw8   1/1     Running   0          14s
pod/App-deployment-5dcf6cc75-tdmk5   1/1     Running   0          14s


NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   23h


NAME                               READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/App-deployment   3/3     3            3           14s

NAME                                         DESIRED   CURRENT   READY   AGE
replicaset.apps/App-deployment-5dcf6cc75   3         3         3       14s


>> kubectl describe deployment

Name:                   App-deployment
Namespace:              default
CreationTimestamp:      Thu, 01 Aug 2019 14:45:44 -0400
Labels:                 app=App
                        type=front-end
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=App
Replicas:               3 desired | 3 updated | 3 total | 3 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=App
  Containers:
   nginx-container:
    Image:        nginx
    Port:         <none>
    Host Port:    <none>
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    NewReplicaSetAvailable
OldReplicaSets:  <none>
NewReplicaSet:   App-deployment-5dcf6cc75 (3/3 replicas created)
Events:
  Type    Reason             Age   From                   Message
  ----    ------             ----  ----                   -------
  Normal  ScalingReplicaSet  2m3s  deployment-controller  Scaled up replica set App-deployment-5dcf6cc75 to 3


Delete Deployment:
>> kubectl delete deployment natunApp-deployment


### Deployment - Update and Rollback:

Rollout command:
>> kubectl rollout status deployment/App-deployment

>> kubectl rollout history deployment/App-deployment   #  Rollout Hostory

There are 2 types of Deployment Strategy: Recreate & Rolling Update.

Recreate: Destroy older version of App and then deploy newer version of App (with PODs), its neede down time of Application.
Rolling update: Destroy 1 App/Container/Pod, upgrade the new App/Container/Pod and carry until finish all stack.

Once you do the changes in the deployment-definition.yml file then apply the changes.

>> kubectl apply -f deployment-definition.yml

Or Just to update the Image, meaning an alternative way:

>> kubectl set image deployment/App-deployment nginx=nginx:1.9.1
Or
>> kubectl set image deployment/App-deployment nginx-container=nginx:1.12-perl

>> kubectl describe deployment App-deployment         # It describes about the deplyment details Recreate/rollout


If you wanted to rollout the changes:

>> kubectl rollout undo deployment/App-deployment

To see the changes -
>> kubectl get replicasets      # make a note of 2 replicas number
>> 

Kubecontrol RUN command - to create POD simply.
>> kubectl run nginx --image=nginx


Summarize Commands:
- - - - - - - - - -
Create:
>> kubectl create -f deployment-definition.yml
>> kubectl create -f deployment-definition.yml --record         # To keep a track of change record

Get:
>> kubectl get deployments

Update:
>> kubectl apply -f deployment-definition.yml
>> kubectl set image deployment/App-deployment nginx=nginx:1.9.1

Status:
>> kubectl rollout status deployment/App-deployment
>> kubectl rollout history deployment/App-deployment

Rollback
>> kubectl rollout undo deployment/App-deployment




### Basic Networking:
=====================
See screen shot : K8_Networking-1 



### Kubernetes Services:
=========================
Basically giving services or accessibility from POD to you Node where you can access the web page of PODs in the outside world.
Your POD network is 10.244.0.1/2/3 .. and Nodes network 192.168.1.2, so you will be accessing page like http://192.168.1.2:30008

See screenshot K8_Service-1.jpg

Service Types:

1) NodePort:

Screen-shot K8_Service-1.jpg About Noteport-Service-POD.

File: service-definition.yml
----------------
apiVersion: v1
kind: Service
metadata:
  name: App-service
  
spec:
  type: NodePort    # If this type is not mentioned then its ClusterIP (Default one) 
  ports:
    - targetPort: 80  # is a port of POD where actual container will produce
      port: 80   # its a internal port of service call clusterIP port where target port mapped. 
      nodePort: 30008  # is a port where services is acciable from anaywhere, ex: http://192.168.1.2:30008
  selector:
    app: App
    type: front-end
----------------

Deployment POD [Target Port: 80 ] -> Mappeed to Service Port [port: 80] -> Mapped to NodePort [port: 30008]
Now access : http://192.168.1.2:30008    

IMP Note: look at the above "selector", it indeed helps to idenify the PODs for which we are using this services.
          We copied the "app: App & type: front-end" part from the pod-definition.yml's "labels" part.

Commands:          

>> kubectl create -f service-definition.yml
>> kubectl get services

>> curl http://192.168.1.2:30008


Till now we have learned above to access the Single POD.
But in the real world we will have multiple PODs to handle, K8 service look for "app: App" in the selector and 
loadbalance it automatically, no further configuration needed. Also PODs can be in mutiple Nodes even though "Service" span
across the cluster. Ex: if you hit http://192.168.1.2:30008 or http://192.168.1.3:30008 or http://192.168.1.4:30008 you will
get the same web page. See Screen Shot K8_Service-3.jpg.

Used Algorithm: Random, SessionAffinity: Yes

Do the practical: Make sure your Pods are running thru Deployment then run "kubectl create -f service-definition.yml"

          
2) ClusterIP: (services for back-end App & DB or more)
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Deployment POD -> Backend POD like DB [expose with cluster IP] -> RADIS POD [expose with cluster IP].

As we not accessing the app from browser (outside of my cluster), cluster IP is enough.

----------------
apiVersion: v1
kind: Service
metadata:
  name: back-end
  
spec:
  type: ClusterIP       # if you do NOT define and type then services will consider Cluster IP by-default
  ports:
    - targetPort: 80
      port: 80
      
  selector:             # "app & type" we are taking from PODs definition labels
    app: App
    type: back-end
----------------



3) LoadBalancer: 
~~~~~~~~~~~~~~~~~








One More Example:

Instruction: Let us know try to create a service-definition.yml from from scratch. You task to create a service to 
enable the frontend pods to access a backend set of PODs.
* Service Name: image-processing
* labels: app=>App
* type: ClusterIP
* Port on the service: 80
* Port exposed by image processing container: 8080

Answer:
~~~~~~~
File: deployment-definition.yml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: image-processing-deployment
  labels:
    tier: backend
spec:
  replicas: 4
  template:
    metadata:
      name: image-processing-pod
      labels:
        tier: backend
    spec:
      containers:
        - name: mycustom-image-processing
          image: someorg/mycustom-image-processing
  selector:
    matchLabels:
      tier: backend


File: service-definition.yml
---
apiVersion: v1
kind: Service
metadata:
  name: image-processing
  labels:
    app: App
spec:
  type: ClusterIP
  ports:
    - port: 80
      targetPort: 8080
  selector:
    tier: backend



### Micro-services Architecture:
===============================
kubectl create -f .   # means all will start

root@kubemaster:~/k8s/voting_App# kubectl create -f redis-deployment.yml

The Deployment "redis-deployment" is invalid: spec.template.metadata.labels: Invalid value: map[string]string{"app":"demo-voting-app", "name":"redis-pod"}: `selector` does not match template `labels`
root@kubemaster:~/k8s/voting_App#

error validating "postgress-deployment.yml": error validating data: [ValidationError(Deployment.spec.template.spec.containers[0].ports[0]): 
unknown field "containersPort" in io.k8s.api.core.v1.ContainerPort, ValidationError(Deployment.spec.template.spec.containers[0].ports[0]): missing required field "containerPort" in io.k8s.api.core.v1.ContainerPort]; if you choose to ignore these errors, turn validation off with --validate=false

pod/postgress-deployment-6689c5889f-9rkzl    0/1     ImagePullBackOff   0          4m29s


https://github.com/kubernetes/examples/blob/master/guestbook-go/README.md


Deploy a Multi-tier GuestBook application on a Kubernetes cluster following instructions given.

apiVersion: v1
kind: Service
metadata:
  name: redis
spec:
  selector:
    app: kftab-assignment
    name: backend-app
  ports:
  - protocol: TCP
    port: 6379
    targetPort: 6379


apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-deployment
  labels:
    app: kftab-assignment
    name: backend-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: kftab-assignment
      name: backend-app
  template:
    metadata:
      labels:
        app: kftab-assignment
        name: backend-app
    spec:
      containers:
      - name: redis
        image: redis
        ports:
        - containerPort: 6379



apiVersion: v1
kind: Service
metadata:
  name: app
spec:
  type: LoadBalancer
  selector:
    app: kftab-assignment
    name: frontend-app
  ports:
    - name: http
      protocol: TCP
      port: 80



apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment
  labels:
    app: kftab-assignment
    name: frontend-deployment
spec:
  replicas: 2
  
  selector:
    matchLabels:
      app: kftab-assignment
      name: frontend-app
  
  template:
    metadata:
      labels:
        app: kftab-assignment
        name: frontend-app
    spec:
      containers:
        - name: frontend
          image: gcr.io/google-samples/gb-frontend:v4
          ports:
            - name: http
              protocol: TCP
              containerPort: 80
          env:
            - name: GET_HOSTS_FROM
              value: dns


## Entrypoint and CMD in Docker & Same function in Kubernetes i.e. commands & args:

POD Definition:

apiVersion: v1
kind: Pod
metadata:
  name: ubuntu-sleeper-pod
spec:
  containers:                               
    - name: ubuntu-sleeper            #     Docker world
      image: ubuntu-sleeper           #     From Ubuntu
      command: ["sleep2.0"]           <---> ENTRYPOINT ["sleep"]
      args: ["10"]                    <---> CMD ["5"]


For Docker:
>> docker run ubuntu-sleep 10
>> docker run --name ubuntu-sleeper --entrypoint sleep2.0 ubuntu-sleeper 10

for K8s:
>> kubectl create -f pod-definitation.yaml

One Scenario: If you edit the pod yaml file of running POD then 
you may not be able to run it always. You will see there will be one
file created under /tmp/ folder , hit the kubectl replace command to re-kick it.
>> kubectl edit pod <pod name> - if fails then do the following.
>> kubectl replace --force -f /tmp/kubectl-edit-23475843.yaml



## INTERVIEW Preparation:

* Kubernetes Architechture 
* Deployment, ReplicaSet, Replication Conreoller 
* What is POD
* ClusterIP. NodePort, LoadBalancer 
* Namespaces and its use
* Multi Container PODs
* Daemonset - to know - use for monitoring, logging agent. or CNI like flannel, weave-net. So, number of node = number of replica. once node gets deleted, replica also gets deleted. Example kube-proxy running as deamon set

* Static POD, Manual Scheduling, Labels
* Taint & Tolaration - And then Affinity 
* SSL Certificates implementations
* Configmap & Secrets 
* Kubernetes Autoscaling 
* Kubernetes Authentication and Authorozation, Role base access
* Networking policies 
* Ingress Implementation & Gateway API. Replace Ingress with GatewayAPI 
* Storage 
* Logging and Monitoring
* Helm Chart
* Deploy using Kustomize 