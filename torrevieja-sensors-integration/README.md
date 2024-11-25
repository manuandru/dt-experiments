# Torrevieja Sensors Integration

This module allows to run the Torrevieja Sensors Integration project described in my Master Thesis.

## Requirements

- `docker`
- `docker compose`

## Deployment

1. Clone the repository

```bash
git clone --recurse-submodules --depth 1 https://github.com/manuandru/dt-experiments.git
```

2. Navigate to the project folder

```bash
cd dt-experiments/torrevieja-sensors-integration
```

3. Build the environment

```bash
./build-env.sh
```

4. (Optional) Adjust configuration files (i.e. `.env*` files)

- `db/.env.influxdb2-admin-password`
- `db/.env.influxdb2-token`
- `db/.env.influxdb2-username`
- `http-to-mqtt-scraper/.env`

5. Run the project

```bash
docker compose up
```
