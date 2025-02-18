

## install the Kwasm operator

Add the Kwasn Helm chart to the Catalog:

- repo: https://github.com/KWasm/kwasm-operator
- path: charts/kwasm-operator
- revision: kwasm-operator-chart-0.2.3

Go to the charts repo and add the following to the `clusterrole.yaml` template in the kwasm-operator chart:

```yaml
  - verbs:
      - '*'
    apiGroups:
      - coordination.k8s.io
    resources:
      - leases
```

Create a workload in the `team-admin`

- Name: kwasm-operator
- Namespace: kwasm-operator
- Select `Create namespace`
- Values:

```yaml
kwasmOperator:
  installerImage: ghcr.io/spinkube/containerd-shim-spin/node-installer:v0.18.0
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

Add the Spin Operator Helm chart to the Catalog:

- repo: https://github.com/spinframework/spin-operator
- revision: v0.4.0

Create a workload in the `team-admin`

- Name: spin-operator
- Namespace: spin-operator
- Select `Create namespace`
- Values:

```yaml
version: "0.4.0"
```

## Create a spin app

Add the following files to the `team-spinkube-argocd` repo: https://github.com/spinkube/spin-operator/releases/download/v0.4.0/spin-operator.shim-executor.yaml


## Expose the service

## Login to the private registry

```
spin registry login -u 'xx' -p xxx harbor.labs.try-apl.net
```

## TO-DO

- network policies (now netpols for team have been disabled)
- solve `clusterpolicy` issue to annotate nodes:

```
one or more objects failed to apply, reason: error when patching "/dev/shm/2763883015": admission webhook "validate-policy.kyverno.svc" denied the request: path: spec.rules[0].mutate.targets.: auth check fails, additional privileges are required for the service account 'system:serviceaccount:kyverno:kyverno-background-controller': cannot update/v1/Node in namespace
```

- test `URL Path` in service for the mapping to `/hello` and `/go-hello`