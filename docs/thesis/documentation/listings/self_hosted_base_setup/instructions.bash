# Login as default user in sudoers or root user
ssh admin@10.10.10.20

# Install podman and podman-compose
sudo pacman -Syu podman podman-compose

# Create a new user for isolating the services
sudo useradd -m ai
sudo passwd ai
sudo usermod -aG wheel ai

# Enable linger for user ai, required to run services such as rootles containers without being logged in
sudo loginctl enable-linger ai

# Edit the sysctl.conf file
sudo vim /etc/sysctl.conf

# Add the following lines, required for rootless podman to use the ports 443 and 80
echo -e "net.ipv4.ip_unprivileged_port_start=443\nnet.ipv4.ip_unprivileged_port_start=80" | sudo tee -a /etc/sysctl.conf

# Load the new config
sudo sysctl -p

# Login as user ai and create the following directory and file
mkdir -p .config.containers

# Required for rootless podman (podman manages cgroups directly instead of systemd)
echo -e "[engine]\ncgroup_manager=\"cgroupfs\"" | sudo tee .config/containers/containers.conf

# Install and check UFW
sudo pacman -Syu
sudo ufw status

# Allow all outgoing connections
sudo ufw default allow outgoing
# Deny all incoming connections per default
sudo ufw default deny incoming

# Default rules for remote access and web
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
# Ollama
sudo ufw allow 43434

# Enable UFW
sudo ufw show added
sudo ufw enable
sudo ufw status
