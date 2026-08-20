## K8s-Authentication:

To add a new user in the K8s cluster you will need 2 yaml file for RBAC (Role based Authentication)
1) role.yaml
2) binding.yaml 

File: Role.yaml

apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-reader
rules:
- apiGroups: [""]  # "" - indicates the core API group
  resources: ["pods"]
  verbs: ["get", "watch", "list"]

> kubectl config set0credentials adam --client-key=User1.key --client-certificate=User1.crt 
> kubectl config set-context User1 --cluster=CusterName_give
> kubectl config get-context

> kubectl config use-context User1 ## means you have switched context to User1







