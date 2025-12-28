# MITM scenario in Simple TCP Client Server environment

## Simulate the MITM scenario with containers
For a simulation of a scenario in this environment without setting up any HW, you can use the following commands:
```bash
nsak scenario bulid mitm
nsak environment simulate simple_tcp_client_server mitm
```

## Example setup with real hardware

### Setup Simple TCP Client Server environment
First, follow the steps in the [README.md](../../../../environments/simple_tcp_client_server/README.md) of the Simple TCP Client Server environment to get a working client/server setup.

### Provision NSAK
