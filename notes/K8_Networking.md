# K8_Networking

Simple Networking Commands:
> ip link
> ip addr
> ip addr add 192.168.1.10/24 dev etc0 
> ip route
> ip route add 192.168.1.10/24 via 192.168.2.1
> echo 1 > /proc/sys/net/ip4/ip_forwarding

Note, By default any client host looks for /etc/hosts file for DNS resolution, if it fails then it goes to DNS server for checking.
This order can be change by making entry in file "/etc/nsswitch.conf". look for this line "hosts:   files dns".

## Network Namespaces (nets)

Commands:
>> ip netns add red
>> ip netns add blue
>> ip netns             # To list the Network namespaces
>> ip link 
>> ip nets exec red ip link    # red = namespace name
>> ip -n red ip link

create a ns link and attach it.

>> ip link add <veth-red> type <veth> peer name <veth-blue>
>> ip link set <veth-red> netns <red>

>> ip link set <veth-blue> netns <blue> 
>> ip -n <red> addr add <192.168.15.1> dev <veth-red> .  # this is just kind of connecting to namespace
>> ip -n <blue> addr add <192.168.15.2> dev <veth-blue> 

>> ip -n <red> link set <veth-red> up # activate the interface
>> ip -n <blue> link set <veth-blue> up

Now try ping:
>> ip netns exec <red> ping <192.168.15.2>

## Create Virtual Switch:  There many options like Linux Bridge or Open vSwitch, We will be using here as "Linux Bridge"

>> ip link add <v-net-0> type bridge   ## created new interface 
>> ip link    ## Display the IP links
>> ip link set dev v-net-0 up
Now you have to link the interfaces in the new Switch-Bridge.
>> ip link add <veth-red> type <veth> peer name <veth-red-br>   ## that means cable connection created
>> ip link add <veth-blue> type <veth> peer name <veth-blue-br>  ## that means cable connection created

Now link bot the namespaces in the new virtual Switch
>> ip link set <veth-red> netns <red>
>> ip link set <veth-red-br> master v-net-0
>
>> ip link set <veth-blue> netns blue
>> ip link set <veth-blue-br> master v-net-0
>
>> ip link set <veth-blue> netns <blue> 
>> ip -n <red> addr add <192.168.15.1> dev <veth-red> .  # this is just kind of connecting to namespace
>> ip -n <blue> addr add <192.168.15.2> dev <veth-blue> 
>
>> ip -n <red> link set <veth-red> up # activate the interface
>> ip -n <blue> link set <veth-blue> up
>
>> ip addr add 192.168.15.5 

If you wanted to connect another ip range of host then you need to configure the routing table for gateway of that network.

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


POD Networking:
= = = = = = = =

* Every POD should have IP Address.
* Every POD should be able to communicate with every POD in the same node.
* Every POD should be able to communicate with every other POD on other nodes without NAT.

### Create veth pair 

 -> ip link add

### Attach veth pair 

-> ip link set . . . .
-> ip link set . . . .

### Assign IP Address

ip -n <namespace> addr add ....
ip -n <namespace> route add ....

### Bring up Interface 

ip -n <namespace> link set ....

### CNI in Kubernetes: (Container Network Interface)

* Container Runtime must create network namespace.
* Identify network the container must attach to.
* Container Runtime to invoke Network Plugin (bridge) when container is Added.
* Container is invoke Network Plugin (bridge) when container is DELeted.
* JSON format of the Network Configuration.

TO see see CNI plugin please check "kubelet.service"
 --network-plugin=cni 
 --cni-bin-dir/opt/cni/bin 
 --register-node=true \\
 --v=2 

or
ps -aux | grep kublet 

### Weaveworks (CNI)

Deploy - Deploy it as a POD in the cluster
-> kubectl apply -f "https://cloud.weave.works/k8s/net?k8s-version=$(kubectl version | base64 | tr -d '\n')"

Check logs:
-> kubectl logs weave-net-5gcmd  weave -n kube-system

By default weave gives a IP range 10.32.0.1 - 10.47.255.254 = 1,048,574 IPs. 
But you can customized as per your requirement. 

### Service Networking

Cluster IP - Can be accessible from service that gets created. The IP of the service can accessible from any POD within the cluster. 

Nodeport - Can be accessible from for the particular POD of a node with port like 30080 within the cluster. 

Kube-Proxy (basically make available the IP to access from outside)
IP Tables

- - - - - - - - - - - - - - - - - - - -
IP: Port              |    Forward To:
10.99.13.178:80       |    10.144.1.2
- - - - - - - - - - - - - - - - - - - -

> kubectl get pods -o wide 
output:
Name            READY           STATUS          RESTARTS            AGE         NODE 
db              1/1             Running         0                   14h         node-1

> kubectl  get service 
Output:
Name            TYPE           CLUSTER-IP         PORT(S)            AGE         
db-service      ClusterIP      10.103.132.104     3306/TCP           12h 

> kube-api-server  --service-cluster-ip-range ipNet (default: 10.0.0.0/24)

> ps aux | grep kube-api-server 
output:
kube-apiserver --authorization-mode=Node,RBAC --service-cluster-ip-range=10.96.0.0/12 

CIDR Range - 10.244.0.0 => 10.244.255.255 

Check the IP i.e. 10.103.132.104 traffic - 
> iptables -L -t nat | grep db-service 

or check logs:

> cat /var/log/kube-proxy.log 

Some more commands:
> kubectl -n kube-system get pods 
> kubectl -n kube-system logs <kube-proxy_fpw6j>   ## kube-proxy-fpw6j find this name from early command.
Output: iptables proxy 

> kubectl -n kube-system get ds 

### DNS in Kubernetes

Test-POD = 10.244.1.5 and then Web-POD = 10.244.2.5 plus its service 10.107.37.188.
Whenever a services, Kubernetes DNS creates a record. Within the namespace you can access the service with name of the service itself.
like http://web-service. .

Hostname     | Namespace   | Type  |  Root           | IP Address 
web-service  |   apps      |  svc  | cluster.local   | 10.107.37.188

        <- cluster.local -> 
      |                     |   
     svc                   POD
      |                     |
     apps                  apps
      |                     |
web-service             10-244-2-5 (created record)

> http://web-service.apps/apps/svc.cluster.local 

If the POD in different name space then to access it from default namespace is "http://web-service.apps" (web-service is name of the service
and apps is name of the namespace). All services are group togather in to another subdomain call "svc" , Finally all the POD and services 
group togather into a root domain call "cluster.local" . So to access the service with URL - "http://web-service.apps/apps/svc.cluster.local"

### How Kubernetes Implements DNS

The following hostname given just as an example:

(CoreDNS) DNS Server - 10.96.0.10           # Kubernetes implemented DNS server - CoreDNS
and other host entry in this dns server:

web     10.244.2.5
test    10.244.1.5
db      10.244.2.15

-> cat /etc/hosts 
nameserver   10.96.0.10 

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

note, errors, health, prometheus, proxy, reload etc. all are plugins.
All record bydefault falls under cluster.local

> kubectl get configmap -n kube-system

CoreDNS provide a service call kubedns to access the DNS for other services.
> kubectl get service -n kube-system

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
NAME            TYPE              CLUSTER-IP            EXTERNAL-IP           PORT(S)
kube-dns        ClusterIP         10.96.0.10            <none>                53/UDP, 53/TCP 
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

> cat /etc/resolv.conf
output:
nameserver         10.96.0.10
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
> kubectl get svc -n kube-system    (to know the coreDNS service)
> kubectl get pods -n kube-system (check coreDNS pods)
> kubectl describe pod core-dns************ -n kube-system   (it will display the pod details, under -ARGs: conf you will see coreDNS file path)
What is the root domain\zone configured for this kubernetes cluster?
> kubectl get configmap -n kube-system
> kubectl describe configmap coredns -n kube-system
output:
...
...
kubernetes cluster.local in-addr.arpa ip6.arpa ...

...
...

### INGRESS - Retiring (Year 2025 -2026)

When you expose different services for your PODs and wanted to access, commonly it needs lots of Loadbalancer to maintain 
the traffic for all these different types of Application services. To mitigate that Ingress concepts came.
Where you will be defining all the traffic rule in a single POD defination file. 

Ingress Controller - GCP HTTP(S) Load Balancer (GCE), NGINX maintain by Kubernetes Project.

**Nginx_Ingress_Controller*

File: nginx_Ingress_deployment.yaml  (Deployment Defination file)

apiVersion: extension/v1beta1
kind: Deployment
metadata:
  name: nginx-ingress-controller
spec:
  replicas:
  selector:
    matchLabels:
      name: nginx-ingress
  template:
    metadata:
      labels:
        name: nginx-ingress
    spec:
      containers:
        - name: nginx-ingress-controller
          image: quay.io/kubernetes-ingress-controller/nginx-ingress-controller:0.21.0
      args:
        - /nginx-ingres-controller
        - --configmap=$(POD_NAMESPACE)/nginx-configuration     # Note, it is better to create separate configmap to manage easily.
      env:
        - name: POD_NAME
         valueFrom:
           fieldRef:
             fieldPath: metadata.name
        - name: POD_NAMESPACE
          valueFrom:
            fieldFrom:
              fieldPath: metadata.namespace
      ports:
        - name: http
          containerPort: 80
        - name: https 
          containerPort: 443

**NGINX_Controller_Services*

File: nginx_Ingress_Service.yaml

apiVersion: v1
kind: Service
metadata:
    name: nginx-ingress
spec:
    type: NodePort
    ports:
    - port: 80
      targetPort: 80
      protocol: TCP
      name: http

    - port: 443 
      targetPort: 80 
      protocol: TCP 
      name: https 
selector:
    name: nginx-ingress

**NGINX_Controller_Config_Map*

File: nginx_Ingress_ConfigMap.yaml

ConfigMap:
kind: ConfigMapapiversion: v1
metadata:
  name: nginx-configuration
  .. error log path
  .. keep-alive
  .. ssl-protocol

**NGINX_Controller_Authentication*

File: nginx_Ingress_Auth.yaml

apiVersion: v1
kind: ServiceAccount
metadata:
  name: nginx-ingress-serviceaccount

(then add Roles, ClusterRoles, RoleBindings etc.)

So, in a nutshell to make Ingress Ready you should have Ingress Controller Defination, Service, ConfigMap & Auth as a simplest form. 

Ingress Resources: (from Developer or Platform side if Infra is already exist)

Route the traffic - as example, if the traffic comes www.ramsukhdasji-library/book or www.ramsukhdasji-library/videos then it should
                    route to exact service of real POD POD to get the right page. 

Example:

Ingress-book.yaml :
apiVersion: extension/v1beta1      # note this apiversion may be change according to releases, check Kubernetes documentations.
kind: Ingress 
metadata: 
  name: ingress-book 
spec:
  backend:
    serviceName: book-service   # this is the real POD where main app running.
    servicePort: 80 


One more example to setup rule for 2 different urls.

. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

File: Ingress-book.yaml
**OLD File Definitation*
`
apiVersion: extension/v1beta1
kind: Ingress
metadata:
  name: ingress-book
spec:
  rules:
    - http:
        paths:
          - path: /book
            backend:
              serviceName: book-service
              servicePort: 80
          - path: /videos
            backend:
               serviceName: video-service
               servicePort: 80
`
**NEW File Definitation*

`
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-wear-watch
spec:
  rules:
    - http:
        paths:
          - path: /wear
            pathType: Prefix
            backend:
              service:
                name: book-service
                port:
                  number: 80
          - path: /videos
            pathType: Prefix
            backend:
               service:
                  name: video-service
                  port:
                   number: 80
`
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

3RD example to setup rule for 2 different urls.
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

File: Ingress-book-videos.yaml

apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-book
spec:
  rules:
    - host: book.ramsukhdasji.com
      http:
        paths:
          - path: /book
            pathType: Prefix
            backend:
              service:
                name: book-service
                port:
                  number: 80
    - host: videos.ramsukhdasji.com
      http:
        paths:
         - path: /videos
           pathType: Prefix
           backend:
               service:
                  name: video-service
                  port:
                    number: 80

. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

> kubectl create -f Ingress-book.yaml
output:
(ingress.extension/ingress-book created)
>
> kubectl get ingress

NAME            HOSTS         ADDRESS         PORTS
ingress-book    *             80              2s

> kubectl describe ingress ingress-book-videos

Note: Take care of Default backend: default-http-backend:80 (<none_>)

Now, in k8s version 1.20+ we can create an Ingress resource from the imperative way like this:-

**IMPERATIVE_Commands*
> kubectl create ingress <ingress_name> --rule="host/path=service:port"
>
> kubectl create ingress ingress-test --rule="wear.my-online-store.com/wear*=wear-service:80"    # An Example

Find more information and examples in the below reference link:-

[Ref_Link](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#-em-ingress-em-)

References:-

[Ref_Link](https://kubernetes.io/docs/concepts/services-networking/ingress)

[Ref_Link](https://kubernetes.io/docs/concepts/services-networking/ingress/#path-types)

### Some useful commands and troubleshooting steps

> kubectl get deploy                  # (display deployments in default namespace)
> kubectl get deploy -A               # (know deployment in all namespaces)
> kubectl get pods -n kube-system     # (know assets inside namespace kube-system)
> kubectl get pods -n ingress-nginx
> kubectl get pods -A                 # All PODs in all namespaces

What is the name of ingress controller deployment?
> kubectl get deploy -n ingress-nginx  
(output might be ingress-nginx-controller)

What is the name of Ingress-Class  
> kubectl get ingressclass    # Important - You have to mention the ingress class in Ingress-Resource YAML file

      NAME    CONTROLLER             PARAMETERS   AGE
      nginx   k8s.io/ingress-nginx   <none>       309d

Ingress Resource:
> kubectl get ingress -A
> kubectl describe ingress ingress-book-videos -n <namespace_example_app_plane>  (This share all details)

Page redirection:
> kubectl create ingress <ingress-pay -n> <imp_space i.e. namespace> --rule=<"/pay=pay-service:8282">
> kubectl describe ingress -n imp-space

Related to NGINX Ingress Controller :

Create ConfigMAP object
> kubectl configmap <any name, ex: my-nginx-conf> -n ingress-namespace 

Create Service Account:
> kubectl create serviceaccount ingress-serviceaccount -n ingress-controller.yaml

Create roles and roles binding for service Account
> kubectl get roles -n ingress-namespace
> kubectl get rolebindings -n ingress-namespace
>
> kubectl describe role ingress-role -n ingress-namespace
> kubectl create -f ingress-controller.yaml
> kubectl get pods -n ingress-space
> kubectl get deploy -n ingress-space
>
> kubectl expose deploy ingress-controller -n ingress-space --name ingress -h (get the help of commands)
> kubectl expose deploy ingress-controller -n ingress-space --name ingress --port=80 --target-port=80 --type NodePort 
>
> kubectl edit svc ingress -n ingress-space  (Edit existing service if available)
> kubectl create ingress ingress-book-videos -n app-space --rule="/book=book-serivce:8080" --rule="videos=video-service:8080" (define rule)
> kubectl get ingress -n app-space
> kubectl describe ingress -n app-space
>
> kubectl logs webapp-videos***************** -n app-space

### Ingress - Annotations and rewrite-target

Different ingress controllers have different options that can be used to customise the way it works.
NGINX Ingress controller has many options that can be seen here. I would like to explain one such option that we will use in our labs. 
The Rewrite target option.

Our watch app displays the video streaming webpage at http://<watch_service>:<port_>/

Our wear app displays the apparel webpage at http://<wear_service>:<port_>/

We must configure Ingress to achieve the below. When user visits the URL on the left, his/her request should be forwarded internally to the URL on the right.
Note that the /watch and /wear URL path are what we configure on the ingress controller so we can forward users to the appropriate application in the backend.
The applications don't have this URL/Path configured on them.

http://<ingress_service>:<ingress_port>/watch --> http://<watch_service>:<port_>/

http://<ingress_service>:<ingress_port>/wear --> http://<wear_service>:<port_>/

Notice watch and wear at the end of the target URLs. The target applications are not configured with /watch or /wear paths.
They are different applications built specifically for their purpose, so they don't expect /watch or /wear in the URLs.
And as such the requests would fail and throw a 404 not found error.

To fix that we want to "ReWrite" the URL when the request is passed on to the watch or wear applications. We don't want to pass in the same path that user typed in. So we specify the "rewrite-target" option. This rewrites the URL by replacing whatever is under "rules->http->paths->path" which happens to be "/pay" in this case with the value in "rewrite-target". This works just like a search and replace function.

For example: replace(path, rewrite-target)

In our case: replace("/path","/")
`
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: test-ingress
  namespace: critical-space
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
    - http:
        paths:
          - path: /pay
            pathType: Prefix
            backend:
              service:
                name: pay-service
                port:
                  number: 8282
`
In another example given here, this could also be:

`replace("/something(/|$)(.*)", "/$2")`

`
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: rewrite
  namespace: default
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
spec:
  rules:
    - host: rewrite.bar.com
      http:
        paths:
          - path: /something(/|$)(.*)
            pathType: Prefix
            backend:
              service:
                name: http-svc
                port:
                  number: 80
`

Example: Question/Answer

Q: In the webapp namespace, create an Ingress resource named web-app-ingress. Configure it to route traffic for the host app.kodekloud.local with path / (pathType: Prefix) to the existing web-app Service on port 80.
Use apiVersion: networking.k8s.io/v1 and set ingressClassName: nginx.
The Ingress Controller is already deployed - you only need to create the Ingress resource.

Now enable TLS termination on the web-app-ingress Ingress. Add the tls section to use the existing app-tls Secret for the host app.kodekloud.local.
Edit the existing Ingress resource to add a spec.tls section.

Add an annotation to the web-app-ingress Ingress to redirect all HTTP requests to HTTPS. Use the NGINX Ingress Controller annotation for SSL redirect.

Ans:
`
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-app-ingress
  namespace: webapp
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - app.kodekloud.local
      secretName: app-tls
  rules:
    - host: app.kodekloud.local
      http:
        paths:
          - path: "/"
            pathType: Prefix
            backend:
              service:
                name: web-app
                port:
                  number: 80  # the current running service showed me the port
`

### Gateway API (Because of Ingress Limitatios )

Ingress Supports Only:
    - Host matching
    - Path matching
    - Http Only

No Native Support for :
    - TCP/UDP Routing 
    - Traffic Splitting/Weighting
    - Header manipulation
    - Authentication
    - Rate Limiting
    - Redirects
    - Rewritting
    - Middleware
    - Websocket Support
    - Custom error pages 
    - Session affinity
    - Cross-Origin resource sharing 

Gateway APi having 3 modes of instance -

* Gateway Class [Infrastructure Providers]
* Gateway [Cluster Operators]
* HTTPRoute, TCPRoute, GRPCRoute [Application Developers]

>> GatewayClass <<

File -- gateway-class.yaml

apiVersion: gateway.networking.k8s.io/v1
kind: GatewayClass
metadata:
  name: example-class
spec:
  controllerName: example.com/gateway-controller

File -- gateway.yaml

apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: example-gateway
spec:
  gatewayClassName: example-class
  listeners:
    - name: http
      protocol: HTTP
      port: 80

File -- http-route.yaml

apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: example-httproute
spec:
  parentref:
    - name: Example-gateway
    hostnames:
    - "www.example.com"
    rules:
    - matches:
      - path:
          type: PathPrefix
          value: /login
      backendRef:
      - name: example-svc
        port: 8080

### Gateway API Installation - for Experiements

(This section you can just try for TESTING purpose)

To use the Gateway API, a controller is required. In this lab, we will install "NGINX Gateway Fabric" - as the controller.
Follow these steps to complete the installation:

Install the Gateway API resources
> kubectl kustomize "https://github.com/nginx/nginx-gateway-fabric/config/crd/gateway-api/standard?ref=v1.5.1" | kubectl apply -f -

Deploy the NGINX Gateway Fabric CRDs
> kubectl apply -f https://raw.githubusercontent.com/nginx/nginx-gateway-fabric/v1.6.1/deploy/crds.yaml

Deploy NGINX Gateway Fabric
> kubectl apply -f https://raw.githubusercontent.com/nginx/nginx-gateway-fabric/v1.6.1/deploy/nodeport/deploy.yaml

Verify the Deployment
> kubectl get pods -n nginx-gateway

View the nginx-gateway service
> kubectl get svc -n nginx-gateway nginx-gateway -o yaml

Update the nginx-gateway service to expose ports 30080 for HTTP and 30081 for HTTPS
kubectl patch svc nginx-gateway -n nginx-gateway --type='json' -p='[
  {"op": "replace", "path": "/spec/ports/0/nodePort", "value": 30080},
  {"op": "replace", "path": "/spec/ports/1/nodePort", "value": 30081}
]'

> kubectl get httproute -n nginx-gateway
> kubectl describe httproute frontend-route -n nginx-gateway
> kubectl get gateway nginx-gateway -n nginx-gateway

### Useful Steps to deal Gateway-API - In Details - Explanation

**1) Installing Gateway API with NGINX*

The Gateway API defines custom resources, but a controller is needed to implement them. For this demo, we’ll use the NGINX Gateway Controller, which supports all standard Gateway API resources.

To install the NGINX Gateway Controller, run the following commands:

> kubectl kustomize "https://github.com/nginx/nginx-gateway-fabric/config/crd/gateway-api/standard?ref=v1.6.2" | kubectl apply -f -
>
> kubectl kustomize "https://github.com/nginx/nginx-gateway-fabric/config/crd/gateway-api/experimental?ref=v1.6.2" | kubectl apply -f -
>
> helm install ngf oci://ghcr.io/nginx/charts/nginx-gateway-fabric --create-namespace -n nginx-gateway

What this does:

Installs the NGINX Gateway Controller, along with the Gateway API Custom Resource Definitions (CRDs) and related resources.

[NGINX Gateway Fabric Reference](https://docs.nginx.com/nginx-gateway-fabric/install/helm/)

**2) GatewayClass Definition*

A GatewayClass defines a set of Gateways that are implemented by a specific controller. Think of it as a blueprint that tells Kubernetes which controller will manage the Gateways.

-->> Purpose

* Decouples Gateway configuration from the actual implementation: This allows you to define Gateways without worrying about the underlying controller.
* Supports multiple gateway implementations in a single cluster: For example, you can have both NGINX and Istio Gateways in the same Kubernetes cluster.

Here’s an example of a GatewayClass:

`
apiVersion: gateway.networking.k8s.io/v1
kind: GatewayClass
metadata:
  name: nginx
spec:
  controllerName: nginx.org/gateway-controller
`
Explanation:

controllerName: This must match the name expected by your controller (e.g., nginx.org/gateway-controller for NGINX). 
It tells Kubernetes which controller will manage Gateways of this class.

**3) Configuring HTTP Gateway and Listener*

A Gateway is a Kubernetes resource that defines how traffic enters your cluster. It specifies the protocols, ports, and routing rules for incoming traffic.
Here’s an example of a Gateway that listens for HTTP traffic:

`
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: nginx-gateway
  namespace: default
spec:
  gatewayClassName: nginx
  listeners:
    - name: http
      protocol: HTTP
      port: 80
      allowedRoutes:
        namespaces:
          from: All
`

-->> Explanation:

* gatewayClassName: Refers to the GatewayClass (e.g., nginx) that will manage this Gateway.
* listeners: Defines how the Gateway listens for traffic.
      -> name: A unique name for this listener.
      -> protocol: Specifies that this listener will handle HTTP traffic.
      -> port: The port number on which the Gateway will listen for HTTP traffic.
      -> allowedRoutes: Specifies which namespaces can define routes for this Gateway. Here, from: All allows routes from all namespaces.

This configuration sets up a Gateway to handle HTTP traffic on port 80 and forward it to the appropriate backend services.

**4) HTTP Routing*

An HTTPRoute defines how HTTP traffic is forwarded to Kubernetes services. It works in conjunction with a Gateway to route requests based on specific rules, such as matching paths or headers.

Here’s an example of an HTTPRoute:

`
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: basic-route
  namespace: default
spec:
  parentRefs:
    - name: nginx-gateway
    rules:
    - matches:
      - path:
          type: PathPrefix
          value: /app
      backendRefs:
      - name: my-app
        port: 80
`

-->> Explanation:

* parentRefs: Links this route to a specific Gateway (e.g., nginx-gateway).
* rules: Defines how traffic is routed.
    -> matches: Specifies the conditions for matching traffic.
        --> path: Matches requests with a specific path prefix (e.g., /app).
    -> backendRefs: Specifies the backend service (e.g., my-app) and port (e.g., 80) to which the traffic should be forwarded.

This configuration routes all requests with the path prefix /app to my-app service on port 80.

[HTTP Routing Guide](https://gateway-api.sigs.k8s.io/guides/user-guides/http-routing/)

**5) HTTP Redirects and Rewrites*

Redirects and rewrites are powerful tools for modifying incoming requests before they reach the backend service.

Example: **HTTP** to **HTTPS** Redirect Redirects are used to force traffic to a different scheme (e.g., HTTP to HTTPS). Here’s an example:

    Example: **HTTP** to **HTTPS** Redirect

    `
    apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: https-redirect
  namespace: default
spec:
  parentRefs:
    - name: nginx-gateway
    rules:
    - filters:
      - type: RequestRedirect
        requestRedirect:
          scheme: https
    `
Explanation:

* filters: Defines additional processing for requests.

  -> type: RequestRedirect: Specifies that this filter will redirect requests.
  -> requestRedirect.scheme: Redirects all HTTP requests to HTTPS.

This configuration ensures that all incoming HTTP traffic is redirected to HTTPS, improving security.

[HTTP Redirects Guide](https://gateway-api.sigs.k8s.io/guides/user-guides/http-redirect-rewrite/)

>> Path Rewrite <<

Rewrites modify the request path before forwarding it to the backend.
Here’s an example:

`
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: rewrite-path
  namespace: default
spec:
  parentRefs:
    - name: nginx-gateway
    rules:
    - matches:
      - path:
          type: PathPrefix
          value: /old
      filters:
      - type: URLRewrite
        urlRewrite:
          path:
            replacePrefixMatch: /new
      backendRefs:
      - name: my-app
        port: 80
`

-->> Explanation

* matches.path: Matches requests with the path prefix /old.
* filters.type: URLRewrite: Specifies that this filter will rewrite the URL.
  -> replacePrefixMatch: /new: Replaces the /old prefix with /new.
* backendRefs: Forwards the modified request to my-app service on port 80

This configuration rewrites requests from **/old** to **/new** before sending them to the backend.

[HTTP Rewrite Guide](https://gateway-api.sigs.k8s.io/guides/user-guides/http-redirect-rewrite/)

**6) HTTP Header Modification*

You can modify HTTP headers in requests or responses to add, set, or remove specific headers.
Here’s an example:

`
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: header-mod
  namespace: default
spec:
  parentRefs:
    - name: nginx-gateway
    rules:
    - filters:
      - type: RequestHeaderModifier
        requestHeaderModifier:
          add:
            x-env: staging
      backendRefs:
      - name: my-app
        port: 80
`
-->> Explanation

* filters.type: RequestHeaderModifier: Specifies that this filter will modify request headers.
  -> add.x-env: Adds a custom header (x-env) with the value staging.
* backendRefs: Forwards the modified request to the my-app service on port 80.

This configuration is useful for adding metadata to requests, such as environment-specific headers.

[HTTP Header Guide](https://gateway-api.sigs.k8s.io/guides/user-guides/http-header-modifier/)

**7) HTTP Traffic Splitting*

Traffic splitting allows you to distribute traffic between multiple backend services. This is often used for canary deployments or A/B testing.
Here’s an example:

`
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: traffic-split
  namespace: default
spec:
  parentRefs:
    - name: nginx-gateway
    rules:
    - backendRefs:
      - name: v1-service
        port: 80
        weight: 80
      - name: v2-service
        port: 80
        weight: 20
`

Explanation:

* backendRefs: Specifies the backend services and their weights.
    -> weight: 80: Sends 80% of traffic to v1-service.
    -> weight: 20: Sends 20% of traffic to v2-service.
* This configuration splits traffic between two services, with most traffic going to v1-service.

[HTTP Traffic Splitting Guide](https://gateway-api.sigs.k8s.io/guides/user-guides/traffic-splitting/)

**8) HTTP Request Mirroring*

Request mirroring allows you to send a copy of incoming requests to a secondary service for testing or analysis, without affecting the primary service.
Here’s an example:

`
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: request-mirror
  namespace: default
spec:
  parentRefs:
    - name: nginx-gateway
    rules:
    - filters:
      - type: RequestMirror
        requestMirror:
          backendRef:
            name: mirror-service
            port: 80
      backendRefs:
      - name: my-app
        port: 80
`

-->> Explanation:

* filters.type: RequestMirror: Specifies that this filter will mirror requests.
    -> requestMirror.backendRef: Points to the secondary service "mirror-service" that will receive the mirrored requests.
* backendRefs: Forwards the original request to the primary service my-app.

[HTTP Traffic Request Guide](https://gateway-api.sigs.k8s.io/guides/user-guides/http-request-mirroring/)

**9) TLS Configuration*

TLS (Transport Layer Security) is used to encrypt traffic between clients and servers, ensuring secure communication. 
In Kubernetes, you can terminate **TLS** traffic at the Gateway level by using a certificate stored in a Kubernetes Secret. 
This means the Gateway will handle decrypting the traffic before forwarding it to backend services.

The following example demonstrates how to configure a Gateway to terminate TLS traffic:

`
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: nginx-gateway-tls
  namespace: default
spec:
  gatewayClassName: nginx
  listeners:
    - name: https
      protocol: HTTPS
      port: 443
      tls:
        mode: Terminate
        certificateRefs:
        - kind: Secret
          name: tls-secret
      allowedRoutes:
        namespaces:
          from: All
`

-->> Explanation

* protocol: Specifies that this listener will handle HTTPS traffic.
* tls.mode: Indicates that the Gateway will terminate the TLS connection (decrypt the traffic).
* certificateRefs: Points to a Kubernetes Secret (e.g., tls-secret) that contains the TLS certificate and private key.
* allowedRoutes: Configures which namespaces can define routes for this Gateway. Here, from: All allows routes from all namespaces.

This setup is commonly used for secure communication between clients and the Gateway, while backend services receive unencrypted traffic.

[TLS Configuration Guide](https://gateway-api.sigs.k8s.io/guides/user-guides/tls/)

**10) TCP, UDP, and Other Protocols*

The Gateway API supports more than just HTTP traffic. You can configure Gateways to handle protocols like TCP, UDP, and even gRPC.
This flexibility makes it suitable for a wide range of applications, such as databases, DNS servers, and microservices.

>>TCP Example<<
TCP is a connection-oriented protocol often used for applications like databases. The following example shows how to configure a Gateway for TCP traffic:

`
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: tcp-gateway
  namespace: default
spec:
  gatewayClassName: nginx
  listeners:
    - name: tcp
      protocol: TCP
      port: 3306
      allowedRoutes:
        namespaces:
          from: All
`

-->> Explanation:

* protocol: Specifies that this listener will handle TCP traffic.
* port: The port number for the listener, commonly used for MySQL databases.
* allowedRoutes: Allows routes from all namespaces to use this Gateway.

This configuration is ideal for exposing database services to external clients.

>>UDP Example<<

UDP is a connectionless protocol often used for DNS or streaming applications. Here’s an example of a Gateway configured for UDP traffic:
`
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: udp-gateway
  namespace: default
spec:
  gatewayClassName: nginx
  listeners:
    - name: udp
      protocol: UDP
      port: 53
      allowedRoutes:
        namespaces:
          from: All
`

-->> Explanation:

* protocol: Specifies that this listener will handle UDP traffic.
* port: The port number for the listener, commonly used for DNS services.
* allowedRoutes: Allows routes from all namespaces to use this Gateway.

This setup is useful for exposing DNS services or other UDP-based applications.

>>gRPC Example<<

**gRPC** is a high-performance RPC (Remote Procedure Call) framework often used in microservices.
The Gateway API supports gRPC by using HTTPRoute resources. Here’s an example:

`
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: grpc-route
  namespace: default
spec:
  parentRefs:
    - name: nginx-gateway
    rules:
    - matches:
      - method:
          service: my.grpc.Service
          method: GetData
      backendRefs:
      - name: grpc-service
        port: 50051
`

-->> Explanation:

* method.service: Specifies the gRPC service name (e.g., my.grpc.Service).
* method.method: Specifies the gRPC method to match (e.g., GetData).
* backendRefs: Points to the backend service (grpc-service) and its port 50051.

This configuration routes gRPC requests to the appropriate backend service, enabling seamless communication between microservices.

>>Last But Not the Least<<
The Gateway API enables expressive, structured routing with features like header rewrites, traffic splits, and protocol flexibility. Starting with HTTP basics lays a strong foundation before incorporating advanced protocols like TLS and TCP. This ensures a smooth, secure, and scalable ingress strategy in your Kubernetes clusters.
