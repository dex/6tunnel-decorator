#/bin/sh
kubectl -n metacontroller create configmap ipv6-node-port --from-file=sync.py