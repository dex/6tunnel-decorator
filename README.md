# 6tunnel-decorator
A Kubenetes operator that enables IPv6 port-forwarding based with 6tunnel

## Prerequisite
 - Install [metacontroller](https://metacontroller.app/) firstly.
 - run `create_configmap.sh` to load script into `ConfigMap`.
 - run `kubectl apply -f ipv6-node-port.yaml` to install the operator.

## Usage
Add the annotation to your `service` which is supposed to have node port set for IPv4. 
Given `NodePort` is 8080, and then add the following to `annotations`
```
  "ipv6-node-port": "8080"
```
