# Helm

Helm is like a package manager that helps to install, upgrade, rollback, and uninstall K8s objects.
We do not need to micro-manage each K8s object for us.

## Helm Architecture

                Helm CLI
                    |
                    |
          -------------------
          |                 |
     Kubernetes API Server
                    |
             Kubernetes Cluster

Currently Helm 3 is running most of the K8s platform. Earlier it was Helm 2
Differences between them - Helm 3 differs from Helm 2 primarily through the removal of Tiller, namespace-scoped releases, and secrets-based storage. Tiller removed for security reasons because with Tiller user will get more powerfull resource access to the Cluster.

Commands:
        $ helm install <workpress>
        $ helm upgrade <wordpress>
        $ helm rollback <wordpress> 
        $ helm uninstall <wordpress> ## It should be your release name 
        $ helm --help 
        $ helm pull 
        $ helm list 

Sub commands & sub-sub commands 

        $ helm repo --help 

          Available Commands:
             add         add a chart repository
             index       generate an index file given a directory containing packaged charts
             list        list chart repositories
             remove      remove one or more chart repositories
             update      update information of available charts locally from chart repositories

        $ helm repo update --help

[Artifact-HUB](https://artifacthub.io/) -    # Check & Know this site for helm chart 

In the above site you will find all packages. Its like docker Hub.
Also can be search from command line. Example:

        $ helm search wordpress  OR 
        $ helm search hub wordpress 

To search in specific repository you need to mention the repo name with repo urls .
Example :

        $ helm repo add bitnami https://charts.bitnami.com/bitnami 
        $ helm install my-rease bitnami/wordpress 

The chart deploy it as a release, to check the release run the following command

        $ helm list 
        $ helm uninstall my-release 

- [Helm hub:](https://hub.helm.sh/)
- [Helm charts GitHub Project:](https://github.com/helm/charts)
- [Installing Helm:](https://helm.sh/docs/intro/install/)
- [Helm v3 release notes:](https://helm.sh/blog/helm-3-released/)

Example:

        $ helm create webappl-1    # <- this will create the folllowing files

        folder structure =
        -> webapp-1 
              -> templates
                   - configmap.yaml 
                   - deployment.yaml 
                   - service.yaml 
              -> chart.yaml
              -> and values.yaml   # this file is very useful for us and templates.

After values.yml gets updated you can run the folllowing commands

        $ helm upgrade mywebapp mywebapp-release webapp-1/ --values webapp-1/values.yaml 

## From - KodeKloud ---

[KodeKloud Ref Video](http://www.youtube.com/watch?v=kJscDZfHXrQ)

### Helm Chart

A Basic Example of using Helm: Check the templating part

File: deployment.yaml

    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: Hello-India-deployment
      labels:
        app: Hello-India
    spec:
      replicas: {{ .Values.replicaCount }}    # Mark this Point
      selector:
        matchLabels:
          app: Hello-India
      template:
        metadata:
          labels:
            app: Hello-India
        spec:
          containers:
          - name: Hello-India
            image: {{ .Values.image.repository }}   # Mark this Point
            ports:
            - containerPort: 80

File: service.yaml

     apiVersion: v1
     kind: Service
     metadata:
       name: Hello-India-Service
     spec:
       type: NodePort
       ports:
         - port: 80
           targetPort: 80
           protocol: TCP
           name: http
       selector:
         app: Hello-India

File: Values.yaml

     replicaCount: 2
     image:
       repository: helloIndia:1.1

File: Chart.yaml

     apiVersion: v2
     appVersion: "1.10.1"
     name: hello India
     description: a exmaple App
     
     type: application

Along with all yaml file like, deployment.yaml, service.yaml you can use file like values.yaml for 
templating the other yaml codes plus "Chart.yaml" would be for Helm chart to run .

Which actually to run the Application via Helm chart 

Example Code (Chart.yaml):

        apiVersion: v2                    # This comes in Helm-3 to differentiate between Helm 2 or 3
        appVersion: 5.8.1                 # Application version i.e. wordpress
        version: 12.1.27                  # Chart version
        name: wordpress                   # Name of the chart (you name it according to App)
        description: Web publishing platform
        type: application                 # There are 2 type - application and Library
        dependencies:
          -  condition: mariadb.enable
             name: mariadb
             repository: https://charts.bitnami.com/bitnami
             version: 9.x.x 
             <code hidden>
        keywords:
          - application 
          - blog
          - wordpress
        maintainers:
          - email: container@bitnami.com 
            name: Bitnami
       home: https://github.com/bitnami/charts/tree/master/bitnami/wordpress
       icon: https://bitnami.com/assets/stacks/wordpress/img/wordpress-stack-220x234.png


## Helm Chart Structure

       > (Folder) Hello-India-chart 
           > templates       # Template directory
           > values.yaml     # Configurable values (file)
           > Chart.yaml      # Chart information (file)
           > LICENSE         # Chart License (file)
           > README.md       # Readme file
           > chart           # Dependency Chart directory
 
Another Example:

      myapp-chart/
      
          Chart.yaml
          values.yaml
      
          templates/
      
              deployment.yaml
              service.yaml
              ingress.yaml
              configmap.yaml
              secret.yaml

## $ helm --help

Common Actions for Helm:

          - helm search       # search for charts
          - helm pull         # download a chart to your local directory to view
          - helm install      # upload the chart to your Kubernetes cluster
          - helm list 

(PLEASE CHECK ALL THE EXAMPLE COMMAND BELOW)

     Usage : 
       helm [command]
     
     Available Commands:
       completion        # generate autocompletion scripts for the specified shell
       create            # create a new chart with the given name
       dependency        # manage a chart's dependencies
       env               # helm client environment information
       get               # download extended information of a named release
       help              # Help about any command
       history           # fetch release history

[artifacthub](https://artifacthub.io/) - for most popular website for helm chart application package 

        $ helm search wordpress ... ... ...  # it requires to specify where to search hub or repo 
                                             # hub means artifacthub and repo mean in a specific repo 
        $ helm search hub wordpress 

## Deploying Wordpress

        $ helm repo add bitnami https://charts.bitnami.com/bitnami   # "bitnami" has been added to your repositories
        $ helm install [release-name] [chart-name]
        $ helm install my-release bitnami/wordpress 

## Helm Release 

(Once you deploy with helm, it deploy as release and  you will see it in the following list command)

        $ helm list
        $ helm uninstall my-release  (to remove the package)

## Helm Repo

        $ helm repo
        $ helm repo list
        $ helm repo update

## Customizing Chart Parameter

A File: values.yaml - just for an example to understand

        image:
          registry: docker.io 
          repository: bitnami/wordpress
          tag: 5.8.2-debien-10-r0 
        ## @param wordpressUsername WordPress wordpressUsername
        ##
        wordpressUsername: user
        #
        ## @param wordpressPassword WordPress wordpressPassword 
        # Defaults to a random 10-character alphanumeric string if not set 
        ##
        wordpressPassword: ""
        ## @param existingSecret
        ##
        existingSecret: "" 
        ## @param wordpressEmail wordpress User Email 
        wordpressEmail: user@example.com 
        #
        ## @param wordpressBlog 
        #
        wordpressBlogName: User's Blog! 

Here is the custom command to edit the exiting parameters 

        $ helm install --set wordpressBlogName="Helm Learning" my-release bitnami/wordpress     # wordpressBlogName is there in values.yaml
        $ helm install --set wordpressEmail="abc@wordpress.com" my-release bitnami/wordpress
        OR
        $ helm install --set wordpressBlogName="Helm Tutorials" my-release bitnami/wordpress --set wordpressEmail="antoine@example.com"
        $
        OR
        $ cat custom-values.yaml
        
        wordpressBlogName: Helm Learning
        wordpressEmail: abc@wordpress.com

        $ helm install --values custom-values.yaml my-release bitnami/wordpress
        OR
        $ helm pull bitnami/wordpress         # it will download the package in a archive format in your local machine
        $ helm pull --untar bitnami/wordpress # Now untar your bitnami package
        $ ls wordpress    # go to desire folder/file and then EDIT it and then install it
        $
        $ helm install my-release ./wordpress
      

## Lifecycle Management with Helm

        $ helm install nginx-release bitnami/nginx --version 7.1.0
        $ helm upgrade nginx-release bitnami.nginx --version 18.3.6   # 18.3.6 is Chart Version
        $ helm upgrade nginx-release bitnami/nginx 
        $ helm list   (list of release) 
        $ helm history nginx-release      # (lists of releases and revision)
        $ helm rollback nginx-release 1   # Rollback to release 1 (Well, It does not release back to 1 instead Helm creates release 3)

Note: each rollback Helm add a new revision number. Here is output

      controlplane ~ ➜  helm list
      NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
      dazzling-web    default         6               2026-07-28 17:47:56.896892407 +0000 UTC deployed        nginx-18.3.6    1.27.4 
      
      controlplane ~ ➜  helm history dazzling-web
      REVISION        UPDATED                         STATUS          CHART           APP VERSION     DESCRIPTION     
      1               Tue Jul 28 17:23:59 2026        superseded      nginx-12.0.4    1.22.0          Install complete
      2               Tue Jul 28 17:24:02 2026        superseded      nginx-12.0.5    1.22.0          Upgrade complete
      3               Tue Jul 28 17:24:05 2026        superseded      nginx-12.0.4    1.22.0          Upgrade complete
      4               Tue Jul 28 17:34:03 2026        superseded      nginx-19.0.0    1.27.4          Upgrade complete
      5               Tue Jul 28 17:36:13 2026        superseded      nginx-12.0.4    1.22.0          Rollback to 3   
      6               Tue Jul 28 17:47:56 2026        deployed        nginx-18.3.6    1.27.4          Upgrade complete
      
      controlplane ~ ➜  helm rollback dazzling-web 3
      Rollback was a success! Happy Helming!
      
      controlplane ~ ➜  helm list
      NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
      dazzling-web    default         7               2026-07-28 17:52:10.023479268 +0000 UTC deployed        nginx-12.0.4    1.22.0
      
      controlplane ~ ➜  helm history dazzling-web
      REVISION        UPDATED                         STATUS          CHART           APP VERSION     DESCRIPTION     
      1               Tue Jul 28 17:23:59 2026        superseded      nginx-12.0.4    1.22.0          Install complete
      2               Tue Jul 28 17:24:02 2026        superseded      nginx-12.0.5    1.22.0          Upgrade complete
      3               Tue Jul 28 17:24:05 2026        superseded      nginx-12.0.4    1.22.0          Upgrade complete
      4               Tue Jul 28 17:34:03 2026        superseded      nginx-19.0.0    1.27.4          Upgrade complete
      5               Tue Jul 28 17:36:13 2026        superseded      nginx-12.0.4    1.22.0          Rollback to 3   
      6               Tue Jul 28 17:47:56 2026        superseded      nginx-18.3.6    1.27.4          Upgrade complete
      7               Tue Jul 28 17:52:10 2026        deployed        nginx-12.0.4    1.22.0          Rollback to 3

**Workflow diagram*

      helm create myapp
              │
              ▼
      Edit values.yaml
              │
              ▼
      Edit templates/
              │
              ▼
      helm lint
              │
              ▼
      helm template
              │
              ▼
      helm install
              │
              ▼
      helm upgrade
              │
              ▼
      helm rollback
              │
              ▼
      helm uninstall

## Some IMPORTANT Commands to remember

        $ helm repo add bitnami https://charts.bitnami.com/bitnami
        $ helm install my-release oci://REGISTRY_NAME/REPOSITORY_NAME/wordpress    

        $ helm search hub wordpress   # All wordpress version in Artifact hub website 
        $ helm search repo wordpress  # to find word press App version 
        $ helm repo list              # How many helm chart repositories are there in the controlplane node now?

        $ helm uninstall my-wordpress or apache or my-browse or my-release  # These are release name while you are going to uninstall
        $ helm repo remove hashicorp                                        # Remove particular repository 

### We can run mutiple Application Instance with different name of release in the same system

Example:

        $ helm install my-first-instance bitnami/wordpress --version 26.0.0
        $ helm install my-second-instance bitnami/wordpress --version 26.0.0 

Another Example with NGINX:

        $ helm install nginx-dev bitnami/nginx

        $ helm install nginx-stage bitnami/nginx

        $ helm install nginx-prod bitnami/nginx

Three Releases, Same Chart, Different configurations.

        helm list

OUTPUT:

        NAME           STATUS
        nginx-dev      deployed
        nginx-stage    deployed
        nginx-prod     deployed

## Helm vs Kustomize

      | Feature                | Helm                             | Kustomize                      |
      | ---------------------- | -------------------------------- | ------------------------------ |
      | Uses templates         | ✅ Yes                            | ❌ No                          |
      | Uses overlays          | Limited                          | ✅ Yes                          |
      | Package manager        | ✅ Yes                            | ❌ No                          |
      | Downloads applications | ✅ Yes                            | ❌ No                          |
      | Versioned releases     | ✅ Yes                            | ❌ No                          |
      | Rollback support       | ✅ Yes                            | ❌ No                          |
      | Built into `kubectl`   | ❌ No                             | ✅ Yes                         |
      | Best for               | Installing reusable applications | Customizing your own manifests |

## Another Example - Using HELM install Nginx and access it from Laptop via Ingress Controller

Create a Kind Configuration

File: kind-config-port-mapping.yaml

     kind: Cluster
     apiVersion: kind.x-k8s.io/v1alpha4
     
     nodes:
     - role: control-plane
       extraPortMappings:
       - containerPort: 80      # Inside the Docker Container expose to port 80
         hostPort: 80           # means Forward my Laptop's localhost:80 to Container Port 80
         protocol: TCP
     
       - containerPort: 443
         hostPort: 443
         protocol: TCP

Note: Little Explanation: 
- containerPort: 80 means Inside the Docker Container expose to port 80. Also remember, inside container, Ingress Controller listening on port 80

hostPort: 80 - means Forward my Laptop's localhost:80 to Container Port 80
Similarly port 443 also functions.

These port mappings are the key to making Ingress reachable from your Laptop.

Create the Cluster

     $ kind create cluster --config kind-config.yaml
     $ kubectl get nodes

Expected Status

     NAME                 STATUS   ROLES           AGE     VERSION
     kind-control-plane   Ready    control-plane   3h27m   v1.34.0

Install the NGINX Ingress Controller

     $ kubectl apply -f \
     https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

     (the official ingress-nginx manifest because it's designed specifically for kind clusters.)

     Wait for the controller:

     $ kubectl wait \
       --namespace ingress-nginx \
       --for=condition=ready pod \
       --selector=app.kubernetes.io/component=controller \
       --timeout=180s

     Verify:
     $ kubectl get pods -n ingress-nginx

     Output:
     ingress-nginx-controller

Install Helm (If its not there)

     $ brew install helm        # For MAC user
     $ helm version

Add the Bitnami Repository

     $ helm repo add bitnami https://charts.bitnami.com/bitnami

     $ helm repo update

Install NGINX usig Helm

     $ helm install my-nginx bitnami/nginx --set service.type=ClusterIP
       (Install it with a ClusterIP service because the Ingress Controller will expose it.)

     Verify:
     $ kubectl get pods
     $ kubectl get svc

     Output:
     NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
     kubernetes   ClusterIP   10.96.0.1       <none>        443/TCP          3h33m
     my-nginx     ClusterIP   10.96.126.173   <none>        80/TCP,443/TCP   3h29m

     $ kubectl get ingressclass
     Output:
     NAME    CONTROLLER             PARAMETERS   AGE
     nginx   k8s.io/ingress-nginx   <none>       3h34m

Create Ingress Resource or People simply say "Ingress"

File: ingress_resource.yaml

     apiVersion: networking.k8s.io/v1
     kind: Ingress
     metadata:
       name: my-nginx
     spec:
       ingressClassName: nginx
     
       rules:
       - host: my-nginx.local
         http:
           paths:
           - path: /
             pathType: Prefix
             backend:
               service:
                 name: my-nginx
                 port:
                   number: 80

Apply to create resource:

     $ kubectl apply -f ingress.yaml

For Local DNS resolution Update /etc/hosts file in your Laptop

     $ sudo vi /etc/hosts
     
     Add the line
     127.0.0.1 my-nginx.local

Verify your ingress resource

     $ kubectl get ingress

     Output:
     NAME       CLASS   HOSTS
     my-nginx   nginx   my-nginx.local

Test from you local Laptop

     $ curl http://my-nginx.local

     Or From Browser
     http://my-nginx.local

You should see the NGINX welcome page.

The complete request flow

     Browser
        │
        ▼
     my-nginx.local
        │
        ▼
     Mac /etc/hosts
        │
        ▼
     Port 80
        │
        ▼
     Ingress Controller
        │
        ▼
     Ingress Rule
        │
        ▼
     ClusterIP Service
        │
        ▼
     NGINX Pod


NOTE: If I wanted to deploy Grafana, ArgoCD then same Ingress-Controller going to work because I do not need to expose port to
80 0r 91 or 82. This is where Ingress shines. One port i.e. 80 is enough. The reason is that Ingress routes by Host or Path, not by different ports.

Host-Based Routing

     Browser

     http://nginx.local
              |
              ▼
     NGINX
     
     http://grafana.local
              |
              ▼
     Grafana
     
     http://argocd.local
              |
              ▼
     ArgoCD

Everything comes through: Port 80 . The Ingress Controller looks at the Host header and decides where to send the request.

Another option is PATH-Based Routing

     localhost/nginx
     
     localhost/grafana
     
     localhost/argocd

Again only 80 going to use.

In case your Laptop already listening in 80 port by another application like Apache, Tomcat Server then
you can configure like this

     <YAML>
     extraPortMappings:
     
     - containerPort: 80
       hostPort: 8080

Now you localhost:8080 going to map to Container:80.

If you wanted to RUN Developer and Production Cluster where both can not use 80 then 

Development:

     <YAML>
     hostPort: 8080

Production:

     <YAML>
     hostPort: 8090