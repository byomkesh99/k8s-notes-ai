# Why JSONPath Useful?

JSONPath allows you to extract exactly the information you need from Kubernetes resources without manually reading large YAML or JSON outputs.

In real production, when you have 500 Pods, 200 Deployments, and 100 Nodes, you don't want to read the entire YAML output.

In a big infrastructure if you wanted to see only the following item then you will need JSON

* Pod IP
* Node Name
* Container Image
* Restart Count

The following command will give a big line of yaml output where you need to find your item to work on

        $ kubectl get pods -o yaml

Instead if I give the following command then I will have selective output which I wanted to know

        $ kubectl get pods -o jsonpath='{.items[*].metadata.name}'

Output:
        $ kubectl get pods -o jsonpath='{.items[*].metadata.name}'
          bar-app
          foo-app

I general the following command will give full JSON output

        $ kubectl get nodes -o json
        $ kubectl get pods -o json


More commands to get more info

        $ kubectl get pods -o jsonpath='{.items[0].spec.containers[0].image}'
          Output: registry.k8s.io/e2e-test-images/agnhost:2.39

        $ kubectl get pods -o jsonpath='{.items[*].status.nodeInfo.architecture}'       # For Architechture
        $ kubectl get pods -o jsonpath='{.items[*].status.capacity.cpu}'                # For CPUs
        $ kubectl get pods -o jsonpath='{.items[*].metadata.name}{"\n"}{.items[*].status.capacity.cpu}'  # \n for newline, & for \t for Tab

Example 2: Get Pod IP Addresses

        $ kubectl get pods -o jsonpath='{.items[*].status.podIP}'

        Output:
        10.244.2.7
        10.244.2.8
        10.244.2.9

Example 3: Which Node is Running My Pod?

        $ kubectl get pods -o jsonpath='{.items[*].spec.nodeName}'

        Output:
        worker-node1
        worker-node2

Example 4: Which Image is Running?

        $ kubectl get pods -o jsonpath='{.items[*].spec.containers[*].image}'

        Output:
        nginx:1.26
        redis:7

Example 5: External IP of a Service

        $ kubectl get svc my-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}'

        Output:
        35.86.11.112

Example 6: Get Secret Value

        $ kubectl get secret db-secret -o jsonpath='{.data.username}'


## Not to memorize the command but to know the Pattern

        .metadata.name
        .spec.containers
        .status.podIP
        .spec.nodeName
        .status.phase

### These are most useful day to day commands

        # Pod Names
        $ kubectl get pods -o jsonpath='{.items[*].metadata.name}'

        # Pod IPs
        $ kubectl get pods -o jsonpath='{.items[*].status.podIP}'

        # Node Names
        $ kubectl get pods -o jsonpath='{.items[*].spec.nodeName}'

        # Container Images
        $ kubectl get pods -o jsonpath='{.items[*].spec.containers[*].image}'

        # Ready Replicas
        $ kubectl get deployment myapp -o jsonpath='{.status.readyReplicas}'