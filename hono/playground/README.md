# Eclipse Hono Playground

```filesystem
hono
├── deploy-hono.sh
├── playground
│   ├── device-provisioning.sh
│   ├── http-publish.sh
│   ├── mqtt-publish.sh
│   └── hono.env
│   └── variables.env
└── README.md
```

## Hono Deployment

Deploy Hono to a Kubernetes cluster, based on `minikube`, using [Eclipse helm chart](https://github.com/eclipse/packages/tree/master/charts/hono).

```bash
# path: hono
minikube start --cpus 4 --memory 8g
minikube tunnel
./deploy-hono.sh
cat playground/hono.env # should be populated
```

## Device Communication

### Provision Device

This device provisioning playground will:

- Create a `Tenant`
- Create a `Device`
- Set credentials for device

```bash
# path: hono/playground
./device-provisioning.sh
```

### Send Messages

To send a message from the device previously provisioned, run:

- **HTTP messages**:
```bash
# path: hono/playground
./http-publish.sh
```

- **MQTT messages**:
```bash
# path: hono/playground
./mqtt-publish.sh
```

## Listen for incoming messages

To listen for incoming messages, you can use both `hono-cli` or `kafka-client`.

### Hono CLI

```bash
# path: hono/playground
source hono.env
source variables.env
java -jar /path/to/hono-cli-*-exec.jar app $(echo $APP_OPTIONS) consume --tenant ${TENANT}
```

### Kafka Client


```bash
/path/to/kafka/bin/kafka-console-consumer.sh --bootstrap-server 127.0.0.1:9094 --consumer.config /tmp/dt-experiments/kafka.config --whitelist 'hono.*.my-tenant' --from-beginning
```

> **Note**: You can read messages from beginning by setting `--from-beginning` flag.
