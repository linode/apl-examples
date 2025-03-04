# Example app in Python using RabbitMQ

This app provides a minimal example of a chat app, sending messages to all clients that are currently connected.

It consists of a simple static webpage with minimal scripts to send messages through the application server to a
connected RabbitMQ cluster. Due to the exchange type "fanout", all messages will be relayed to all connected clients.

Note this is a minimal example which does not consider persistence, reconnection / error handling, cleaning up etc.

# Why using RabbitMQ?

The application server accepts the websocket connections, and would generally be able to exchange messages between them.
However, typically multiple application server instances exist, and usually not all clients are connected to the same
instance. The RabbitMQ cluster takes care of exchanging the messages between those.

# Running the example

## Platform preparation

The platform admin needs to activate `RabbitMQ` in the Platform Apps.
Also Harbor is required with configured object storage.

## Building the app

The app does not include a Dockerfile, but an image can be generated with Buildpacks.

1. In the app platform, select `Build`, then `Create Build`.
2. Provide an image name, e.g. `rmq-example-app`.
3. Select as Mode `Buildpacks`.
4. Set the Repo URL to `https://github.com/linode/apl-example-app.git`.
5. Set the path to `rabbitmq-python-example`.
6. Confirm with `Submit`.
7. Copy out the image repository for creating the workload in the following step.

## Creating the workloads

### Creating the RabbitMQ cluster

1. Go to `Workloads`, then `Create Workload`.
2. Select `RabbitMQ-Cluster`.
3. Set a name, e.g. `example`.
4. Click `Submit`.

### Creating the application server deployment

1. Go to `Workloads`, then `Create Workload`.
2. Select `K8s-Deployment`. 
3. Set a name, e.g. `rmq-example-app`.
4. In the chart values, update the `image` and `env` section. Adjust `image.repository` with the value from the build.
   Also, update the `name` references in the `secretKeyRef` entries.
   The format of the secret name is `rabbitmq-<name>-cluster-default-user`, where `<name>` is to be replaced with the
   cluster name you chose above. It should look like this:

```yaml
image:
  repository: <your-image-repo>
  pullPolicy: IfNotPresent
  tag: latest
env:
  - name: NOTIFIER_RABBITMQ_HOST
    valueFrom:
      secretKeyRef:
        name: example-rabbitmq-cluster-default-user
        key: host
  - name: NOTIFIER_RABBITMQ_USER
    valueFrom:
      secretKeyRef:
        name: example-rabbitmq-cluster-default-user
        key: username
  - name: NOTIFIER_RABBITMQ_PASSWORD
    valueFrom:
      secretKeyRef:
        name: example-rabbitmq-cluster-default-user
        key: password
```

## Create a networking policy

1. Go to `Network Policies`, select `Create Netpol`.
2. Provide any name for the policy, e.g. `rabbitmq-example`.
3. Rule type is `ingress`. Set the selector name `otomi.io/app` and value `example-rabbitmq-cluster`, where applicable
   replacing `example` with the name you chose for the RabbitMQ instance.
4. Set mode to `AllowOnly`.
5. Set the namespace to `team-<team-name>`, according to the team deploying the application, e.g. `team-demo`.
6. Optionally limit the in-cluster exposure to the app, i.e. set the selector label name to `otomi.io/app` and the
   selector label value to the name of your app workload, e.g. `rmq-example-app`.

## Exposing the service

1. As soon as the workload is deployed, go to `Services` and `Create Service`.
2. Select the name of your workload from the list, e.g. `rmq-example-app`.
3. Under Exposure, select `External`
4. Confirm with `Submit`.

As soon as the service is configured, the app should be available using the link URL in the application platform
console.
