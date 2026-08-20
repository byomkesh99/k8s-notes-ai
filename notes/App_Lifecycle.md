# App_Lifecycle Management

Deployment Strategy - 
        Recreate - before deployment it shutsdown the current pod (which means application will be down for that period) and the upgrade the new PODs
        Rolling update - shutdown the old version and update newer version Pods one by one, thats the way application will not gets down completely.

Rolling update is the default deployment Strategy. 

Update the new image in deployment-definitation.yml file and run "kubectl apply -f deployment-definition.yml" 

Samething can be done from "kubectl set image deployment/myapp-deployment nginx-container=nginx:1.9.1"  1.9.1 is the newer version 

Rollback : --- 

Rollback the deployment > kubectl rollout undo deployment/myapp-deployment 

Rollback Test with command:

> kubectl get replicasets 

[Check this command before the rollback start and the check this after the rollback]

**Summarize Commands:*

Create          > kubectl create -f deployment-definitation.yml
Get             > kubectl get depployments

Update          > kubectl apply -f deployment-definition.yml
                > kubectl set image deployment/myapp-deployment nginx-container=nginx:1.9.1

Status          > kubectl rollout status deployment/myapp-deployment
                > kubectl rollout history deployment/myapp-deployment
Rollback        > kubectl rollout undo deployment/myapp-deployment

=v=v=v=v=v=v=v=v=v=v=v=v=v=vv==v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=v=

*** Config Maps:

To set environment variable -

apiVersion: v1 
kind: Pod
metadata:
  name: simple-webapp-color
spec:
  containers:
    - name: simple-web-app-color 
      image: simple-webapp-color
      ports:
        - containerPort: 80
      envFrom:
        - configMapRef:
            name: app-color

    
ConfigMap --
  APP_COLOR: blue
  APP_MODE: prod 


Imperative:

      > kubectl create configmap 
                <config-name> --from-literal=<key>=<value>

      > kubectl create configmap app-config --from-literal=APP_COLOR=blue --from-literal=APP_MOD=prod 

      > kubectl create configmap  <config-name> --from-file=<path-to-file>

      > kubectl crete configmap app-config --from-file=app_config.properties 

Declarative:

*File-Config-map.yaml:*

apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
   APP_COLOR: blue
   APP_MODE: prod

> kubectl create -f config-map.yaml

Create Config Maps 

 app config --
  APP_COLOR: blue 
  APP_MODE: prod

 mysql-config -- 
  poer: 3306
  max_allowed_packet: 128M

 redis-config --
  port: 6379
  rdb-compression: yes 

## To view configMaps

> kubectl get configmaps
> kubectl describe configmaps   (in more details)

## Sum up - to apply configmap and how it looks

File:~ pod-definition.yaml
apiVersion: v1
kind: Pod
metadata:
  name: simple-webapp-color
spec:
  containers:
    - name: simple-web-app-color 
        image: simple-webapp-color
        ports:
          - containerPort: 8080

        envFrom:
          - configMapRef:
              name: app-config 

File:~ configmap.yaml 
apiVersion: v1 
kind: ConfigMap 
metadata:
  name: app-config 
data:
  APP_COLOR: blue 
  APP_MODE: prod

So this configuration makes the web portal color as BLUE background -- :):):)

### Why is envFrom a List? 

Because Kubernetes allows:
`
envFrom:
    - configMapRef:
        name: app-config

    - configMapRef:
        name: logging-config

    - secretRef:
        name: db-secret

    - secretRef:
        name: api-secret
`
Example: Multiple ConfigMaps
**ConfigMap_1*
`
data:
  APP_NAME: payment-service
  APP_PORT: "8080"
`
**ConfigMap_2*
`
data:
  LOG_LEVEL: DEBUG
  TIMEZONE: UTC
`
**POD_definitation*
`
containers:
    - name: app
        image: nginx
      envFrom:
        - configMapRef:
            name: app-config        # Just name of ConfigMap allow to bring the key-values in this Container

        - configMapRef:
            name: logging-config    # Just name of ConfigMap allow to bring the key-values in this Container 
`

### ConfigMap + Secret

(This is very common in production.)

**ConfigMap*
<YAML_File>
data:
  DB_HOST: mysql
  DB_PORT: "3306"

**Secret*
<YAML_File>
stringData:
  DB_USER: admin
  DB_PASSWORD: secret123

**POD*
<YAML_File>
containers:
    - name: app
      image: nginx
      envFrom:
        - configMapRef:
            name: db-config
        - secretRef:
            name: db-secret

**Result_In-Bash_Terminal*
DB_HOST=mysql
DB_PORT=3306
DB_USER=admin
DB_PASSWORD=secret123