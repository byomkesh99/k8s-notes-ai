# Troubleshooting Steps

## How to think to solve K8s failures

[RefLink - Troubleshooting Clusters](https://kubernetes.io/docs/tasks/debug/debug-cluster/)

K8s NODE Failures

        $ kubectl get nodes
        $ kubectl get pods
        $ kubectl get pods -n kube-system

CHECK CONTROL PLAINS

        $ service kube-apiserver status
        $ service kube-controller-manager status
        $ service kube-scheduler status
        $ #Check Logs Control-Plain Components
        $ kubectl logs kube-apiserver-master -n kube-system

CHECK SERVICES ON WORKER NODES

        $ service kubelet status     (Possible Error if kubelet stopped : Node node01 status is now: NodeNotReady)
        $ service kube-proxy status


CHECK SERVICE LOGS

        $ sudo journalctl -u kube-apiserver

WORKER NODES FAILURE

        $ kubectl get nodes
        $ kubectl describe node worker-1

Note: Depending on the status it set to True or False or Unknown.
  -> If the node is out of diskspace then the OutOfDisk flag will be True.
  -> The node is out of memory then MemoryPressure flag will be True.
  -> When the Disk space is low then DiskPressure flag will be True.
  -> Similarly, if the to many processess are running then PIDPressure flag will set to True.

Example:

        Type             Status  LastHeartbeatTime                 LastTransitionTime                Reason                       Message
         ----             ------  -----------------                 ------------------                ------                       -------
         MemoryPressure   False   Thu, 09 Jul 2026 12:41:31 +0200   Tue, 23 Sep 2025 16:38:53 +0200   KubeletHasSufficientMemory   kubelet has sufficient memory available
         DiskPressure     False   Thu, 09 Jul 2026 12:41:31 +0200   Tue, 23 Sep 2025 16:38:53 +0200   KubeletHasNoDiskPressure     kubelet has no disk pressure
         PIDPressure      False   Thu, 09 Jul 2026 12:41:31 +0200   Tue, 23 Sep 2025 16:38:53 +0200   KubeletHasSufficientPID      kubelet has sufficient PID available
         Ready            True    Thu, 09 Jul 2026 12:41:31 +0200   Tue, 23 Sep 2025 16:39:13 +0200   KubeletReady                 kubelet is posting ready status

When WORKER node unable to communicate to MASTER-Controlplane Node then STATUS of MemoryPressure, DiskPressure, OutOfDisk will be "Unknown"

If the WORKER Node is down then check the followings:

* login to Worker Node and check with 'top' command to know its CPU and Memory utilization.
* Check the Physical Diskspace (df -kh),
* Check the status of the "kubelet" -  "service kubelet status"
* Check the kubelet logs - "sudo journalctl -u kubelet"
* Check the kubelet Certificate and they are not expired - " openssl x509 -in /var/lib/kubelet/worker-1.crt -text " and they part of right group & correct CA.

KUBELET config files:
        $ journalctl -u kubelet
        $ /var/lib/kubelet/config.yaml
        $ /etc/kubernetes/kubelet.conf

DEBUGGING Service Issues:

        $ kubectl get pods -l app=hostname      # app=hostname is a lebel of selector . This output will gives your pods over all health
        $ kubectl get pods -o wide              # to get all PODs IP addresses
        $ kubectl get pods -l app=hostname -o=jsonpath='{.items[*].status.podIP}'          # Display only the IPs
        $ kubectl run -it --rm --restart=Never busybox --image=busybox sh                  # Using temporary busybox you can test the connectivity of other PODs
                / # for ip in 10.244.0.11  10.244.0.14 10.244.0.16; do wget -q0- $ip:9376; done 

Check Service Definition and Endpoints

        $ kubectl get svc my_host_service -o yaml
        $ kubectl get endpointslices -l kubernetes.io/service-name=my_host_service -n default   # list the all endpoints IPs

CoreDNS Troubleshoooting Steps: Part 1

        $ kubectl get pods --namespace=kube-system -l k8s-app=kubedns
        $ kubectl get endpointslices -l kubernetes.io/service-name=kube-dns --namespace=kubesystem

CoreDNS Troubleshoooting Steps: Part 2

        $ kubectl exec -it <Your_App_Pod_Name> --exec /etc/resolv.conf
        $ kubectl exec -it busybox -- nslookup kubernetes.default.svc.cluster.local            # Busybox helps to run temporarily to check the DNS resolution
        $ kubectl exec -it busybox -- nslookup my-apps-service.default.svc.cluster.local

Troubleshooting CNI and kube-proxy

* Check DaemonSet Pod Status
* Analyze CNI Pod Logs
* Make sure all the kube-proxy pods are running fine
* For kube-proxy services to check to find the issues -->>

        $ kubectl get pods -n kube-system k8s-app=kube-proxy
        $ kubectl logs kube-proxy-bcd23 -n kube-system
        $ kubectl get configmap kube-proxy -n kube-system -o yaml
        $ ipvsadm -ln                                                   # in the Node itself to see IP tables

**Things to Remember*

When the static pods (which are under /etc/kubernetes/manifests/) breaks then you CANNOT fix them by editing from "kubectl edit pod <static_Pod_Name>".
You have fix them by editing files under "/etc/kubernetes/manifests/" . Example files "kube-scheduler.yaml" or kube-controller-manager.yaml.

kube-scheduler.yaml - When there is issues in this file, the PODs will be showing as an Pending state
kube-controller-manager.yaml - When there is issues in this file, Pod shows 'CrashloopBackOff' error.
