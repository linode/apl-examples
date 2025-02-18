
## install Kserve CRDs

The Kserve CRDs can not be installed using ArgoCD (because the CRD is to large). Therefor we need to add the chart manually:

- Select view: Team
- Select team: admin
- open the shell
- run the following cmd:

helm install -n team-admin kserve-crd oci://ghcr.io/kserve/charts/kserve-crd --version v0.14.1

## Install Kserve-resources

Add the Kserve resources chart to the catalog:

URL: https://github.com/kserve
Path: /charts/kserve-resources
Revision: v0.14.1
icon: https://avatars.githubusercontent.com/u/83512434?s=200&v=4

Install the Kserve resources by creating a workload in the `kserve` namespace using the team-admin. 

- Namespace: `kserve`
- Select `create Namespace`
- Use the default values



## Install the NVIDIA GPU Operator

```
Add the Following Helm chart to the catalog:

URL: https://github.com/NVIDIA/gpu-operator
Path: /deployments/gpu-operator
Revision: v24.9.2

Install the Install the NVIDI GPU Operator by creating a workload in the `team-admin`. 

Set the version in the `Chart.yaml to `v24.9.2`
```


or:

```bash
helm repo add nvidia https://helm.ngc.nvidia.com/nvidia
helm repo update
helm install --wait --generate-name -n gpu-operator --create-namespace nvidia/gpu-operator --version=v24.9.1
```

## Add the open-webui Helm chart to the catalog

URL: https://github.com/open-webui
Path: /helm-charts
Revision: open-webui-5.10.1

## Huggingface

Create an account.

Request access to https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct

Wait until you are granted access.

Create a Token:

- go to: https://huggingface.co/settings/tokens
- use Token type = Write

<!-- <p><img src="https://github.com/linode/apl-example-apps/blob/main/img/hf-token.png/?raw=true" width="100%" align="center"></p> -->

## Create `InferenceService`

### Create a new Team (or use an existing Team)

### Create a sealed secret with the token:

- name: hf-secret
- Key: HF_TOKEN
- Value: huggingface-token

### Create network policies

Create an `egress` network policy:

- name: huggingface
- FQDN: huggingface.co
- Port: 443

Create an `ingress` network policy:

- name: inference-service
- Selector label name: `app`
- Selector label value: `huggingface-llama3-predictor-00001`
- mode: allow all

### Create `InferenceService`
Add the following manifest to the Team's GitOps repository called: `team-<team-name>-argocd`:

```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: huggingface-llama3
spec:
  predictor:
    model:
      modelFormat:
        name: huggingface
      args:
        - --model_name=llama3
        - --model_id=meta-llama/meta-llama-3-8b-instruct
      env:
        - name: HF_TOKEN
          valueFrom:
            secretKeyRef:
              name: hf-secret
              key: HF_TOKEN
              optional: false
      resources:
        limits:
          cpu: "6"
          memory: 24Gi
          nvidia.com/gpu: "1"
        requests:
          cpu: "6"
          memory: 24Gi
          nvidia.com/gpu: "1"
```

### Expose the service (optional)

## Install open-webui

- select the team where the open-webui is going to be installed (use the same team as where the InferenceService is created)

### Install the open-webui Helm chart

- create a workload and use the following values:

```yaml
ollama:
  enabled: false
pipelines:
  enabled: false
replicaCount: 1
openaiBaseApiUrl: https://huggingface-llama3-predictor-team-<team-name>.<cluster-domain>>/openai/v1

WEBUI_AUTH
```

### Create network policy

Create an `ingress` network policy:

- name: inference-service
- Selector label name: `app.kubernetes.io/component`
- Selector label value: `open-webui`
- mode: allow all

### Expose the open-webui service


