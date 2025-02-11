

## install the Kwasm operator

Clone:

- repo: https://github.com/KWasm/kwasm-operator
- path: charts/kwasm-operator
- revision: kwasm-operator-chart-0.2.3

```yaml
kwasmOperator:
  installerImage: ghcr.io/spinkube/containerd-shim-spin/node-installer:v0.18.0
```

add the following to the `clusterrole.yaml` template:

```yaml
  - verbs:
      - '*'
    apiGroups:
      - coordination.k8s.io
    resources:
      - leases
```

## Annotate the nodes

```
kubectl annotate node --all kwasm.sh/kwasm-node=true
node/lke341670-542353-17c15b8e0000 annotated
node/lke341670-542353-199be2370000 annotated
node/lke341670-542353-22a0971d0000 annotated
```

Or use the `annotate-nodes-policy` and change the pool-id. Add the `yaml` to the `team-admin-argocd` repo.

## install CRDs

Add to the `team-admin-argocd` repo:

```
kubectl apply -f https://github.com/spinkube/spin-operator/releases/download/v0.4.0/spin-operator.crds.yaml
```

## Create `RuntimeClass`

Add to the `team-admin-argocd` repo: https://github.com/spinkube/spin-operator/releases/download/v0.4.0/spin-operator.runtime-class.yaml

## Create `SpinAppExecutor`

Add to the `team-team-spinkube` repo: https://github.com/spinkube/spin-operator/releases/download/v0.4.0/spin-operator.shim-executor.yaml


## Install spin operator

Clone:

- repo: https://github.com/spinframework/spin-operator
- revision: v0.4.0

```yaml
version: "0.4.0"
```

## Create a spin app

add the following files to the `team-spinkube-argocd` repo: https://github.com/spinkube/spin-operator/releases/download/v0.4.0/spin-operator.shim-executor.yaml


## Expose the service

Expose the service and add a URL path `/hello`

## Login to the private registry

```
spin registry login -u 'xx' -p xxx harbor.labs.try-apl.net
```

## TO-DO

- network policies (now netpols for team have been disabled)