# KUBERBETES_SECURITY

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
> openssl req -new -key admin.key -subj "/CN=kube-admin/OU=system:masters" -out admin.csr  #
(This system:masters group included to identify users as under Admin group with admin privillege)
> openssl x509 -req -in admin.csr -CA ca.crt -CAkey ca.key -out admin.crt

**CERTIFICATE_API*

Use-Case: Suppose there is new team member joined and you wanted to give user access to K8s Cluster. In this case this Certificate Api method works.

**REMEMBER*
Controller Manager - All the certificate related activity managed by Kubernetes Controller Manager (cat /etc/kubernetes/manifests/kube-controller-manager.yaml)

        spec:
          containers:
          - command:
            - kube-controller-manager
            - --cluster-signing-cert-file=/etc/kubernetes/pki/ca.crt   # this crt and below key is responsible to sign new user certificates
            - --cluster-signing-key-file=/etc/kubernetes/pki/ca.key


1) User created his/her "my_user.csr" file encode (base_64) it and via K8s my_user.yaml file send it for "Admin" to sign it.
2) Now Admin will see the new user certificate sign request by hitting command below command

> kubectl get csr
> kubectl certificate approve my_user
(this "approve" command will enable to approve newly requested CSR certificate to sign)
> kubectl get csr my_user -o yaml
(This command will show the certificate in a encoded format. User need to decode it and use the real certificate for cluster access)
> echo "LSfkjhfwkdhuddjdkjhddjkjdiiqoqo8290478rodqw89ey21ejqwohqe ... ... .." | base64 --decode  # Decode the certificate
(IMPORTANT Part - User i.e. my_user will need the CRT file to access the K8s Cluster)

Example Usecase:

A new member akshay joined our team. He requires access to our cluster. The Certificate Signing Request is at the /root location.

controlplane ~ ➜  ls
akshay.csr  akshay.key

> cat akshay.csr | base64 -w 0  # csr in one line
LS0tLS1CRUdJTiBDRVJUSUZJQ0FURSBSRVFVRVNULS0tLS0KTUlJQ1ZqQ0NBVDRDQVFBd0VURVBN
QTBHQTFVRUF3d0dZV3R6YUdGNU1JSUJJakFOQmdrcWhraUc5dzBCQVFFRgpBQU9DQVE4QU1JSUJD

`
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: akshay
spec:
  request: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURSBSRVFVRVNULS0tLS0KTUlJQ1ZqQ0NBVDRDQVFBd0VURVBNQTBHQTFVRUF3d0dZV3R6YUdGNU1JSUJJakFOQmdrcWhraUc5dzBCQVFFRgpBQU9DQVE4QU1JSUJDZ0tDQVFFQXBUNVhwdVQxUGIwTlNoZXhaU3EyT2JEVUtXOUN6b2NvbStyZlY1bC80bUlxClA1aktiYTNFWHV2QU5lSjNnRlZ0WlFRQjB5SnI3bERJaW54Zk1UaEtnZ2tDTkJTWXYwT1U3cVpZYklZS0ZqSFUKa2wrblJUdkpHL0E0NkpwMlFLNnB4ZWRTQVNsQ0NuRlM3L3FqT0JNRG1mK2prNlBVNk4vdFJhWXB1UGlMd0JWeQozeEFENEVBZllkb0NsbkNqWnRVOUxucThSUkJEdDBBRC9oN2pPOVFrcUVIRzFYYUl4K2dnSyt2K0E5UEU1MzJ5CmgxWWNZSEF1enVBNUtkbnlTcDhqZE1pOUZaUDNaQ3lVZzRVRE4xdk1WYVBLK0dvZkE1Z0hBQzNQMEdZNC9iS1YKNWsybjF6S1JVcktGNTVaQTVOTkk4YkZzTkJncWQvK0NseVc3YVJKK0NRSURBUUFCb0FBd0RRWUpLb1pJaHZjTgpBUUVMQlFBRGdnRUJBQnpwb1VuNFo0NlRuQmttaUhwYk9DNDUyMGlzdHlQdFVSSVFETDZTcTRwdHpYMzg0WlBUCmp0RmFQaFNTUTJleWdwc1BiRTlGTkVZZmlacnRLNlhJdHNtWG1vWkFzN0hiWVFqdUgzcDQ4UWlCbnhBaG5kTisKajJjRUtCRW92NFRRdzFMd0Z1bDN5Y2I3TGc1ckxwdUdGVEJvK3FyN0dCWHRRYVhLTmRVNFVLV2lHaTNNMVV3ZApQVlhVeDhGdjhHWVNGT2lmemFvTXVqNWRSNlMrV0RMbnlaZnFZRFJlVzNyQXlIRFcyTEtndVl6M2U4VjhiYm1vCjFTYzZKcDdyK1dsRWNrUjZaQWV4azRFelBwWW9jeTlWcHZMM1UydkRkeThOS09JWGlkb2hHc3J5cTFjQWZ5MGkKTlJyeTVXRlJydCtFRGsyZU1TMkplYmsyRWVqZllwdXRZbkE9Ci0tLS0tRU5EIENFUlRJRklDQVRFIFJFUVVFU1QtLS0tLQo=
  signerName: kubernetes.io/kube-apiserver-client
  usages:
    - client auth
`
> kubectl apply -f akshay.yaml
> kubectl certificate approve akshay

You are not aware of a request coming in. What groups is this CSR requesting access to? Check the details about the request. Preferably in YAML.
> kubectl get csr <new_agent_smith> -o yaml
OR as example for user akshay
> kubectl get csr akshay -o yaml
> echo "LSfkjhfwkdhuddjdkjhddjkjdiiqoqo8290478rodqw89ey21ejqwohqe ... ... .." | base64 --decode  # Decode the certificate if user is role is correct
(IMPORTANT Part - User i.e. my_user will need the CRT file to access the K8s Cluster)

groups:
  - system:masters
  - system:authenticated

> kubectl certificate deny agent-smith  # to deny certificate if user is not correct role
> kubectl delete csr agent-smith   # Delete CSR request

## KubeConfig

To connect Kubernetes Cluster, Server API URL mentioned in ~/HOME/.kube/config file.
It has a 3 section, 1) Cluster 2) Context 3) Users

Under the file ~/HOME/.kube/config you will get the existing cluster connection information. (Check the Screenshot)
Suppose you have cluster in Google or Azure or AWS then you need add the context in this "~/HOME/.kube/config" file

> kubectl config view 
(Will display all the cluster-context-user information)

**INFORMTANT: Without the API SERVER connection URL knowing, you won't be able to configure ArgoCD

Example: My Personal Cluster URL

        cluster:
           certificate-authority-data: DATA+OMITTED
           server: https://127.0.0.1:12345

**Authentication:*

* You can not create user account or listing user account using kubectl but can create service account for application to use.

>> kubectl create serviceaccount sa1
>> kubectl get service account

kube-apiserver - can be configure to authenticate using following method

* Static Password File
OR
* Static Token File
OR
* Certificates
OR
* Identity Services - like LDAP etc.


Lets see how Static Password File use for authentication as an example.

you have file user-details.csv contains details as follows.
password123,user1,uid001

And in the kube-apiserver service file append the following line:
File: /etc/kubernetes/manifests/kube-apiserver.yaml, under container command section
--basic-auth-file=user-details.csv

## Article on Setting up Basic Authentication

Setup basic authentication on Kubernetes (Deprecated in 1.19)
Note: This is not recommended in a production environment. 
This is only for learning purposes. 
Also note that this approach is deprecated in Kubernetes version 1.19 and is no longer available 
in later releases

Follow the below instructions to configure basic authentication in a kubeadm setup.

Create a file with user details locally at /tmp/users/user-details.csv

## User File Contents

password123,user1,uid0001
password123,user2,uid0002
password123,user3,uid0003
password123,user4,uid0004
password123,user5,uid0005

Edit the kube-apiserver static pod configured by kubeadm to pass in the user details. The file is located at /etc/kubernetes/manifests/kube-apiserver.yaml


apiVersion: v1
kind: Pod
metadata:
  name: kube-apiserver
  namespace: kube-system
spec:
  containers:
  - command:
    - kube-apiserver
      <content_hidden>
    image: k8s.gcr.io/kube-apiserver-amd64:v1.11.3
    name: kube-apiserver
    volumeMounts:
    - mountPath: /tmp/users
      name: usr-details
      readOnly: true
  volumes:
  - hostPath:
      path: /tmp/users
      type: DirectoryOrCreate
    name: usr-details


Modify the kube-apiserver startup options to include the basic-auth file

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  name: kube-apiserver
  namespace: kube-system
spec:
  containers:
  - command:
    - kube-apiserver
    - --authorization-mode=Node,RBAC
      <content_hidden>
    - --basic-auth-file=/tmp/users/user-details.csv
Create the necessary roles and role bindings for these users:

---
kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  namespace: default
  name: pod-reader
rules:
- apiGroups: [""] # "" indicates the core API group
  resources: ["pods"]
  verbs: ["get", "watch", "list"]

---

## This role binding allows "jane" to read pods in the "default" namespace.

kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: read-pods
  namespace: default
subjects:
- kind: User
  name: user1 # Name is case sensitive
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role #this must be Role or ClusterRole
  name: pod-reader # this must match the name of the Role or ClusterRole you wish to bind to
  apiGroup: rbac.authorization.k8s.io
Once created, you may authenticate into the kube-api server using the users credentials

curl -v -k https://localhost:6443/api/v1/pods -u "user1:password123"

^^ the above method nor recommanded as they the credentials are in plain text menthod.
   but good to know the concepts.

Recommanded way to use certificates for authentication.

## TLS for Kubernetes

[Certificates checklist from Mumshad Manambet](https://github.com/mmumshad/kubernetes-the-hard-way/tree/master/tools)

## View and Check Kubernetes certificate

open file - /etc/kubernetes/manifests/kube-apiserver.yaml and check the certificates.

Example of Client using certificate using curl.
>> curl https://my-kube-playground:6443/api/v1/pods \
    --key admin.key
    --cert admin.crt
    --cacert ca.crt
Display:
{
  "kind": "PodList",
  "apiVersion": "v1",
  "metadata": {
    "selfLink": "api/v1/pods",
  },
  "items": []
}


So everytime, if we need to access our PODS using these CRTs, we need to specify these certificate details.
To minimize this efforts KubeConfig file feature came, we need to specify all the CRTs details in KubeConfig file and
reference it in query statement.

File: KubeConfig
    --server my-kube-playground:6443
    --key admin.key
    --cert admin.crt 
    --cacert ca.crt 

>> kubectl get pods --kubeconfig config

## Cluster <-> Contexts <->  Users = To access the cluster from users using key & crts create a context to avoid using CRTs and Key again and again.

File: KubeConfig.yaml

`
apiVersion: v1
kind: Config
current-context: dev@users@domain.com
clusters:
  -name: my-kube-playarea
    cluster:
      certificate-authority: /etc/kubernetes/pki/ca.crt  
      server: https://my-kube-playground:6443  # Instead of certificate-authority you can use certificate-authority-data: <encode_format for crt content>
contexts:
   -name: my-kube-admin@my-kube-playarea
    context:
      cluster: my-kube-playground
      user: my-kube-admin
      namespace: life-science
users:
  -name: my-kube-admin
   user:
      client-certificate: /etc/kubernetes/pki/admin.crt
      client-key: /etc/kubernetes/pki/admin.key
`

**EXAMPLE_OF_ANOTHER_KUBE_CONFIG_FILE*

`
apiVersion: v1
kind: Config

clusters:
- name: production
  cluster:
    certificate-authority: /etc/kubernetes/pki/ca.crt
    server: https://controlplane:6443

- name: development
  cluster:
    certificate-authority: /etc/kubernetes/pki/ca.crt
    server: https://controlplane:6443

- name: kubernetes-on-aws
  cluster:
    certificate-authority: /etc/kubernetes/pki/ca.crt
    server: https://controlplane:6443

- name: test-cluster-1
  cluster:
    certificate-authority: /etc/kubernetes/pki/ca.crt
    server: https://controlplane:6443

contexts:
- name: test-user@development
  context:
    cluster: development
    user: test-user

- name: aws-user@kubernetes-on-aws
  context:
    cluster: kubernetes-on-aws
    user: aws-user

- name: test-user@production
  context:
    cluster: production
    user: test-user

- name: research
  context:
    cluster: test-cluster-1
    user: dev-user

users:
- name: test-user
  user:
    client-certificate: /etc/kubernetes/pki/users/test-user/test-user.crt
    client-key: /etc/kubernetes/pki/users/test-user/test-user.key
- name: dev-user
  user:
    client-certificate: /etc/kubernetes/pki/users/dev-user/developer-user.crt
    client-key: /etc/kubernetes/pki/users/dev-user/dev-user.key
- name: aws-user
  user:
    client-certificate: /etc/kubernetes/pki/users/aws-user/aws-user.crt
    client-key: /etc/kubernetes/pki/users/aws-user/aws-user.key

current-context: test-user@development
preferences: {}
`

I would like to use the dev-user to access test-cluster-1. Set the current context to the right one so I can do that.
> kubectl config use-context research --kubeconfig /root/my-kube-config

We can follow the same process to add Dev, SIT, UAT and Prod cluster access credentials.

>> kubectl config view     <- to view kube config
OR
>> kubectl config view --kubeconfig=my-custom-config



== == == == == == == == == == == == == == = == == == == == == ==

## API Groups

API Version check:
$ curl https://kube-master:6443/version
{
  "major": "1"
  "minor": "13"
  .
  .
  .
  .
}

Similarly PODs -
$ curl https://kube-master:6443/api/v1/pods

API mainy grouped in to 2 major part

/api - core group
/apis - names group

                /core
                /api
<--------------- /v1 ------------>
|                 |              |
name spaces     PODs            rc 
events          endpoints       nodes
bindings        PV              PVC
configmaps      secrets         services 


                                  named
                                  /apis

/apis     /extensions     /networking.k8s.io      /storages.k8s.io        /authentication.k8s.io       /certificates.k8s.io 

/v1                       /v1                                                                           /v1
  /statefulsets             > /networkingpolicies                                                          > certificatesigningrequests
  /replicasets
  /deployments
          > list
          > get
          > create
          > delete
          > update
          > watch

Ref: [kubernetes-api](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.19/#pod-v1-core)

Note: you might not have access to kube-api directly from client without admin keys and crts but if you install kubectl-proxy
you can access the Kube-api details. Note, kubectl-proxy & kube-proxy is NOT same.

$ kubectl proxy
[Starting to server on 127.0.0.1:8001]

$ curl http://localhost:8001 -k

== == == == == == == == == == == == == == = == == == == == == ==

## AUTHORIZATION

Meaning - once some get the access k8s cluster, what are things they can do.
So it is coming in picture when we want they users/groups can access our cluster, view them but they should not be able to delete any things.
The common authorizations parts are - NODE | ABAC | RBAC | Webhook | Always Allow | Always Deny.

Most of the time Role Based Access Control (RBAC) going to use, but some time NODE and Webhook also require.
Note, in the API configuration yaml file you have to specify the authorization mode, by default "Always Allow" mean all allow.

in Kube-API (/etc/kubernetes/manifests/kube-apiserver.yaml) Conf File:  --authorization-mode=Node,RBAC,Webhook ## (Add it) IMPORTANT Part

By-default: --authorization-mode=AlwaysAllow  (You need to modify as per your need)

RBAC Access Control: [for Developer]

* Can view PODs
* Can create PODs
* can Delete PODs
* Can create configmaps

Ref: Third Party tool - [Open_Policy_Agent](https://www.openpolicyagent.org/) - To manage RBAC(Role Base Access Control) users. It also call "Webhook"

File: developer-role.yaml

`
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: developer
rules:
    - apiGroups: [""]
      resources: ["pods"]
      verbs: ["list", "get", "update", "delete"]
      resourcesNames: ["blue-pod", "orange-pod"]          # optional to provide access to particular group for specific PODs
    - apiGroups: [""]
      resources: ["ConfigMap"]
      verbs: ["create"]
`

>> kubectl create -f developer-role.yaml

The you need to link the users ro the role.

File: devuser-developer-binding.yaml

`
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: devuser-developer-binding
subjects:
    - kind: User
      name: dev-user
      apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: developer
  apiGroup: rbac.authorization.k8s.io
`
>> kubectl create -f devuser-developer-binding.yaml

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

**AS_Example_Some_Questions_Answers*

Q: Inspect the environment and identify the authorization modes configured on the cluster. Check the kube-apiserver settings

File: /etc/kubernetes/manifests/kube-apiserver.yaml

- --authorization-mode=Node,RBAC

Q: How many roles exist in the default namespace?
> kubectl get roles
No resources found in default namespace. i.e. Zero roles for now

Q: How many roles exist in all namespaces together?
> kubectl get roles -A 
NAMESPACE     NAME                                             CREATED AT
blue          developer                                        2026-06-16T10:57:03Z
kube-public   kubeadm:bootstrap-signer-clusterinfo             2026-06-16T10:45:15Z

Q: What are the resources the kube-proxy role in the kube-system namespace is given access to?
> kubectl describe role kube-proxy -n kube-system

PolicyRule:
  Resources   Non-Resource URLs  Resource Names  Verbs
  configmaps  []                 [kube-proxy]    [get]

Q: What actions can the kube-proxy role perform on configmaps?
Get

Q: Which account is the kube-proxy role assigned to?
> kubectl get rolebindings -n kube-system
NAME                                                ROLE                                                  AGE
kube-proxy                                          Role/kube-proxy                                       31m
> kubectl describe rolebinding kube-proxy -n kube-system

Name:         kube-proxy
Role:
  Kind:  Role
  Name:  kube-proxy
Subjects:
  Kind   Name                                             Namespace
  Group  system:bootstrappers:kubeadm:default-node-token                # Here is the Group assigned for the role kube-proxy

Q: Create the necessary roles and role bindings required for the dev-user to create, list and delete pods in the default namespace. Use the given spec:

Role: developer
Role Resources: pods
Role Actions: list
Role Actions: create
Role Actions: delete
RoleBinding: dev-user-binding
RoleBinding: Bound to dev-user

> kubectl create role developer --verb=list,create,delete --resource=pods
PolicyRule:
  Resources  Non-Resource URLs  Resource Names  Verbs
  pods       []                 []              [list create delete]
> kubectl create rolebinding dev-user-binding --role=developer --user=dev-user

Q: A set of new roles and role-bindings are created in the blue namespace for the dev-user. However, the dev-user is unable to get details of the dark-blue-app pod in the blue namespace. Investigate and fix the issue

> kubectl describe roles developer -n blue
> kubectl edit role developer -n blue
(Corrected the Resource Name)

> kubectl --as dev-user get pod dark-blue-app -n blue
NAME            READY   STATUS    RESTARTS   AGE
dark-blue-app   1/1     Running   0          20m

Q: Add a new rule in the existing role developer to grant the dev-user permissions to create deployments in the blue namespace. Remember to add api group "apps".
> kubectl edit role developer -n blue
`
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  creationTimestamp: "2026-06-16T12:54:05Z"
  name: developer
  namespace: blue
  resourceVersion: "2955"
  uid: 7c133ac4-ae28-49a1-b7cc-2b9b99f204c7
rules:
    - apiGroups:
      - ""
      resourceNames:
      - dark-blue-app
      resources:
      - pods
      verbs:
      - get
      - watch
      - create
      - delete
    - apiGroups:    # This Part has been added
      - apps
      resources:
      - deployments
      verbs:
      - get
      - watch
      - create
      - delete
`
> kubectl describe roles developer -n blue
Name:         developer
PolicyRule:
  Resources         Non-Resource URLs  Resource Names   Verbs
  pods              []                 [dark-blue-app]  [get watch create delete]
  deployments.apps  []                 []               [get watch create delete]     # New DEPLOYMENT
> kubectl --as dev-user create deployment nginx --image=nginx -n blue  # Test now by creating new DEPLOYMENT


= = = = = = = = = = = = = = = = = = = = = = = = = =

## Cluster Roles

To List a Namespaced and Non-namespaced Resources
> kubectl api-resources --namespaces=true
> kubectl api-resources --namespaces=false

Cluster Admin - Can view, create, delete Nodes
Storage Admin - Can view, create, delete PV's

Cluster role and cluster role binding - check MM video or K8s documents.

File: cluster-admin-role.yaml
`
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: cluster-administrator
rules:
    - apiGroups: [""] # "" indicates the core API group
      resources: ["nodes"]
      verbs: ["get", "delete", "list", "create"]
`
> kubectl create -f cluster-admin-role.yaml

File: cluster-admin-role-binding.yaml
`
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: cluster-admin-role-binding
subjects:
    - kind: User
      name: cluster-admin # Name is case sensitive. # This cluster role binding allows User to read secrets in any namespace.
      apiGroup: rbac.authorization.k8s.io
roleRef:
    kind: ClusterRole
    name: cluster-administrator
    apiGroup: rbac.authorization.k8s.io
`
> kubectl create -f cluster-admin-role-binding.yaml

**NOTE* - Cluster role and role-binding not just a scope within the cluster, it also can be use to manage user's all the Namespaces too.

Ref Weblink: [auth-RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/)

-> when you create cluster roles, K8s PODs are falling under same cluster roles.

Cluster scoped are below:
Node, PV, clusterrole, cluster rolebindings, certificatessigningrequests, namespaces.

Checking clusterroles:
>> kubectl get clusterroles
>> kubectl get clusterrole --no-headers=false | wc -l      <- get counts
>> kubectl get clusterrolebindingd --no-header | wc -l
>> kubectl describe clusterrolebindingd cluster-admin

**Example*

Q-1: A new user michelle joined the team. She will be focusing on the nodes in the cluster. Create the required ClusterRoles and ClusterRoleBindings so she gets access to the nodes.

> kubectl create clusterrole michelle-role --verb=get,list,watch --resource=nodes
> kubectl create clusterrolebinding cluster-role-binding-michelle --clusterrole=michelle-role --user=michelle

To Verify
> kubectl describe clusterrole michelle-role
> kubectl describe clusterrolebinding cluster-role-binding-michelle

Q-2: michelle's responsibilities are growing and now she will be responsible for storage as well. Create the required "ClusterRoles" and "ClusterRoleBindings" to allow her access to Storage. Get the API groups and resource names from command "kubectl api-resources" . Use the following spec -- --

ClusterRole: storage-admin
Resource: persistentvolumes
Resource: storageclasses
ClusterRoleBinding: michelle-storage-admin
ClusterRoleBinding Subject: michelle
ClusterRoleBinding Role: storage-admin

**IMPERATIVE_Way*
> kubectl create clusterrole storage-admin --resource=persistentvolumes,storageclasses --verb=list,create,get,watch
> kubectl create clusterrolebinding michelle-storage-admin --clusterrole=storage-admin --user=michelle
>
> kubectl get nodes --as michelle           # Verify if the user michelle having access to node

Note Find the HELP from below commands. It has a sample command as an example as well.
> kubectl create clusterrole --help | less
> kubectl create clusterrolebinding --help | less

**DECLARATIVE_Way*
File: Cluster-role-Storage.yaml
`
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: storage-admin
rules:
    - apiGroups:
      - ""
      resources:
      - persistentvolumes
      verbs:
      - list
      - create
      - get
      - watch
    - apiGroups:
      - storage.k8s.io
      resources:
      - storageclasses
      verbs:
      - list
      - create
      - get
      - watch
`
File - Cluster-roleBinding-storage.yaml
`
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: michelle-storage-admin
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: storage-admin
subjects:
    - apiGroup: rbac.authorization.k8s.io
      kind: User
      name: michelle
`

= = = = = = = = = = = = = = = = = = = = = = = = = =

## Service Account

As we know there are mainly 2 types of accounts works in K8s.

  1) User Account
  2) Service Account - for application

Note: When you create a service account, it mounts in the POD like a projected volume in the Pod. 
      And the directory path is /var/run/secrets/kubernetes.io/serviceaccount/ . Default service account comes with lots of limitations.

**IMPERATIVE*
>> kubectl create serviceaccount deboard_sa         # debord_sa is new custom service account
>> kubectl get serviceaccount                       # to view
>> kubectl describe serviceaccount deboard_sa
&
>> kubectl get sa -A | grep default                # view all the defult service account

**DECLARATIVE*

File: service-definitation.yaml
`
apiVersion: v1
kind: ServiceAccount
metadata:
  name: deboard_sa
  namespace: default
#automountServiceAccountToken: false # Optional - if you wanted hide the serviceaccount Token
`

File: POD-Definitation.yaml
`
apiVersion: v1
kind: Pod
metadata:
  name: my-monitoring-dashboard
spec:
  containers:
    - name: my-monitoring-dashboard
      image: my-monitoring-dashboard
  serviceAccount: deboard_sa          # Here the ServiceAccount name added to bind the account with Application Pod
  ###automountServiceAccountToken: false # Use it as per your need
`

When a service account gets created then a Token also created automatically. 
This token will be using by outsider application to authenticate to K8s.

>> kubectl describe secret deboard_sa-token-kbbdm       <- shows the secret token details.
>> kubectl exec -it my-monitoring-dashboard ls /var/run/secrets/kubernetes.io/serviceaccount         <- Token path

bydefault service account mount the token - if you need to stop it then edit the pod defination by adding following lines.

spec:
  containers:
     - name: my-k8s-deboard
       image: my-k8s-deboard
  automountServiceAccountToken: false       <- This line to add

**CREATE_TOKENs*
--> Manually create a long-lived API token for a ServiceAccount
[ServiceAccount-Official-Docs](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/)  
(manually-create-a-long-lived-api-token-for-a-serviceaccount)

> kubectl create token deboard_sa     # By-default generated token active for 1 hour then de-activated
> kubectl create token deboard_sa --duration 2h   # validaty extension
> jq -R 'sokit(".") | select(length > 0) | .[0],.[1] | @base64d | fromjson' <<< euhy653jslkjfg3g84kwlkjnr32rwnfenlfnfowe4  # DECODE the Token & see details

= = = = = = = = = = = = = = = = = = = = = = = = = =

## Securing Image Repository

If you do not mention any repo path bydefault images pulls from Docker. When we mention image: nginx, it actually add the pth as below.

docker.io/library/nginx.

If google then

gcr.io/kubernetes-e2e-test-image/dnsutils.

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

File: nginx-pod.yaml

apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
spec:
  containers:
    - name: nginx
      image: private-registry.io/apps/internal-app
  imagePullSecrets:
      - name: regcreden          <- check above the registry name

Ref [Image_Pull_Secret](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/)

### Docker Security

Example as command:
CHOWN, DAC, KILL, SETFCAP, SETPCAP, SETGID, SETUID
NET_BIND, NET_RAW, MAC_ADMIN, BROADCAST, NET_ADMIN, SYS_ADMIN
SYS_CHROOT, AUDIT_WRITE, many more etc.

Provide the extra permission/reduce permission to the user in docker container
>> docker run --cap-add MAC_ADMIN ubuntu
>> docker run --cap-drop KILL ubuntu
>> docker run --privileged ubuntu

Note: If the same permission apply from the K8s PODs level then all the container inside the POD will get apply the same permission.

### Security Context

The below one for POD level -
File: ubuntu.yaml

apiVersion: v1
kind: Pod
metadata:
  name: web-pod
spec:
  securityContext:
    runAsUser: 1000

  containers:
    - name: ubuntu
      image: ubuntu
      command: ["sleep", "3600"]


The Below one for container level:
File: ubuntu.yaml

apiVersion: v1
kind: Pod
metadata:
  name: web-pod
spec:
  containers:
    - name: ubuntu
      image: ubuntu
      command: ["sleep", "3600"]
      securityContext:
         runAsUser: 1000
         capabilities:
           add: ["MAC_ADMIN", "SYS_TIME", "NET_ADMIN"]

File: multi-pod.yaml -- here 2 images running with 2 different user ID. One uid as 1001 and another 1002
`
apiVersion: v1
kind: Pod
metadata:
  name: multi-pod
spec:
  securityContext:
    runAsUser: 1001
  containers:
    -  image: ubuntu
       name: web
       command: ["sleep", "5000"]
       securityContext:
         runAsUser: 1002

    -  image: ubuntu
       name: sidecar
       command: ["sleep", "5000"]
`
>> kubectl exec ubuntu-sleeper -- whoami

= = = = = = = = = = = = = = = = = = = = = = = = = =

### Network Policy (Incoming: Ingress, & Expernal: Egress)

[Official Documentation Page](https://kubernetes.io/docs/tasks/administer-cluster/declare-network-policy/#limit-access-to-the-nginx-service)

NOTE: It SUPPORTs 1) kube-router 2) Clico 3) Romana

It DOES NOT supports as of date July 2026 - Flannel

The network policy to define network traffic Ingress or Egress to each App tier which running in the PODs.
Ingress - Incoming traffic
Egress - Outgoing traffic 

A) Web App (running under a POD)  B) API App (running under other POD)  C) DB App (running under another POD).
To make us understand if you consider traffic condition of "B", any traffic coming from A to B is Ingress in respective to B and out going traffic from
"B" to "C" is Egress respective of "B". Bydefault there is no restriction in the Kubernetes cluster. You have define the network policy.

Lets say if you wanted to restrict the network traffice for DB (C), here is the defination as an example:

file - networkpolicy.yaml

apiVersion: network.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-policy 
spec: 
    podSelector:
      matchLabels:
          role: db     # The rule is for DB Pod, meaning Ingress/Incoming network traffic for DB Pod. And its from API-Pod. Check the below "podSelector"
    policyType:        # note, unless you define policy type all traffic allowded with in the K8s cluster
      - Ingress
      # - Egress
    ingress:
      - from:
         - podSelector:
             matchLabels:
               name: api-pod  # This the label mentioned in API-POD also, meaning from "api-pod" traffic allowed for DB Pod
        ports:
         - protocol: TCP
           port: 3306


What if you have multiple env like prod & stage and having api-pod matchLabels, then you can separate from name spaces.
Check below -

file - networkpolicy.yaml

apiVersion: network.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-policy
  namespace: prod 
spec: 
    podSelector:
      matchLabels:
          role: db 
    policyType:        <- note, unless you define policy type all traffic allowded with in the K8s cluster
      - Ingress
      - Egress
    ingress:
      - from:
         - podSelector:
             matchLabels:
               name: api-pod
            namespaceSelector:          # <- if you wanted to restric traffic from namespace level then commen out podSelector blocks
                matchLabels:
                  kubernetes.io/metadata.name: prod
         - ipBlock:                   # if wanted allow ingress from outside network, example backup
           cidr: 192.168.6.10/32
        ports:
         - protocol: TCP
           port: 3306

    egress: 
      - to:
         - ipBlock:
              cidr: 192.168.6.10/32
        ports:
          - protocol: TCP
            port: 80

NOTE: By-default all namespace PODs allow to access with same matchLabels. Example, if you have "test-API" lables in in Dev and Prod env then PODs 
can be accessible from each env even though they are in separate namespace. To restic that you need you specify the namespace name in the Network Policy.
All THESE RESTRICTION policy works WITHIN the cluster.

Lets say you have another DB backup server in another network Ex: 192.168.6.10/32 network. Then you have to specify - ipBlock: as Ingress to allow traffic
from Backup DB server and then also specify Egress - ipBlock: for outgoing traffic from DB server to Backup DB server.

Commands:
>> kubectl get networkpolicies
>> kubectl describe netpol payroll       # payrole is policy name

Note: As of now this "Network Policy" supports by 1) Kube-router 2) Calico 3) Romana. But "Flannel" does not support Network Policy.

Another Example:

Create a network policy to allow egress traffic from the Internal application only to the payroll-service and db-service.
Use the spec given below. You might want to enable ingress traffic to the pod to test your rules in the UI.

Also, ensure that you allow egress traffic to DNS ports TCP and UDP (port 53) to enable DNS resolution from the internal pod.

. Policy Name: internal-policy
. Policy Type: Egress
. Egress Allow: payroll
. Payroll Port: 8080
. Egress Allow: mysql
. MySQL Port: 3306

File: internal-policy.yaml (here only EGRESS policy configured as an example)
`
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: internal-policy
  namespace: default
spec:
  podSelector:
    matchLabels:
      name: internal
  policyTypes:
    - Egress
  egress:
    - to:
      - podSelector:
          matchLabels:
            name: payroll
      ports:
        - protocol: TCP
          port: 8080
    - to:
      - podSelector:
          matchLabels:
            name: mysql
      ports:
        - protocol: TCP
          port: 3306
`

> kubectl get networkpolicies
NAME              POD-SELECTOR    AGE
internal-policy   name=internal   9m20s
payroll-policy    name=payroll    34m

**Scenario Based Question on Network Policy*

If I have 500 Pods running in the Prod cluster and I have 10 different DB and I wanted to allow only 200 Apps to allow the direct DB access. Then, will not my Network Policy will be very BIG?

ANS:
No, a well-designed NetworkPolicy does not become huge. The trick is to use labels strategically, not to list every Pod individually.

* 500 Pods
* 200 applications need database access

Is a BAD Design

In this case we have to use "Common Labels" 

Lebels should look like this way (In the DB YAML POD) -

        labels:
          access-db: "true"

As example for 2 application's labels looks like this when  a Deployment gets database access gets:

APP1:

      template:
        metadata:
          labels:
            app: payment
            access-db: "true"   # <- Make a note this label - This is common label in Pod and DB as well

App2:

      template:
        metadata:
          labels:
            app: order
            access-db: "true"   # <- Make a note this label - This is common label in Pod and DB as well


Database NetworkPolicy
Your database Pods might have label:

    labels:
      app: postgres

NetworkPolicy:

        apiVersion: networking.k8s.io/v1
        kind: NetworkPolicy

        spec:
          podSelector:
            matchLabels:
              app: postgres

          ingress:
          - from:
            - podSelector:
                matchLabels:
                  access-db: "true"       # <- Make a note this label - This is common label in Pod and DB as well

**How it Flows*

        Payment Pod
        access-db=true
                │
                │ Allowed
                ▼
             PostgreSQL
        
        Order Pod
        access-db=true
                │
                │ Allowed
                ▼
             PostgreSQL
        
        Inventory Pod
        access-db=true
                │
                │ Allowed
                ▼
             PostgreSQL
        
        Frontend Pod
        access-db=false
                │
                │ ❌ Denied
                ▼
             PostgreSQL


**This Is Why Labels Matter So Much*

When you first learn Kubernetes, labels seem like just metadata.
In production, they're much more than that. They drive:

* Deployments
* Services
* NetworkPolicies
* PodDisruptionBudgets
* ServiceMonitors (Prometheus)
* Admission policies
* GitOps automation

A well-designed labeling strategy is one of the foundations of a scalable Kubernetes platform.

### Kubectx and Kubens - Command Line Utilities

**THEY are External TOOL installed*

>> kubectx <context_name>
>> kubectx -c                 # Display current context
>> kubectx kind-cka-cluster3 

>> kubens  # Display all the namespace
>> kubens <new_namespace>
>> kubens kube-system  # Switching to kube-system namespace

### Custom Resource Definition (CRD)
