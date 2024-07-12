# LLM Systems Project

## Preparation
### Install docker

Installing Docker on different platforms involves a few distinct steps for each operating system. Below are the general instructions for installing Docker on some of the most common platforms:

#### Docker on Linux (Debian/Ubuntu based distributions):
1. **Update the package index**:
   ```sh
   sudo apt-get update
   ```

2. **Install packages to allow apt to use a repository over HTTPS**:
   ```sh
   sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
   ```

3. **Add Docker’s official GPG key**:
   ```sh
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
   ```

4. **Add the Docker repository to APT sources**:
   ```sh
   sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
   ```

5. **Update the package index again**:
   ```sh
   sudo apt-get update
   ```

6. **Install the latest version of Docker CE (Community Edition)**:
   ```sh
   sudo apt-get install docker-ce
   ```

#### Docker on Linux (Fedora, CentOS, RHEL):
1. **Install required packages**:
   ```sh
   sudo yum install -y yum-utils
   ```

2. **Add the Docker repository**:
   ```sh
   sudo yum-config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo
   ```

3. **Install Docker CE**:
   ```sh
   sudo yum install docker-ce docker-ce-cli containerd.io
   ```

#### Docker on macOS:
1. **Download Docker Desktop for Mac** from the [official Docker website](https://www.docker.com/products/docker-desktop).
2. **Install the downloaded package** by following the installation wizard.

#### Docker on Windows:
1. **Download Docker Desktop for Windows** from the [official Docker website](https://www.docker.com/products/docker-desktop).
2. **Run the installer** and follow the installation wizard.
3. **Enable Docker in your system settings** if necessary.

#### General Tips:
- **Post-Installation Steps**: After installation, you may need to add your user to the `docker` group to avoid using `sudo` for every Docker command (`sudo usermod -aG docker $USER`) and then log out and back in.
- **Check Version**: To confirm that Docker has been installed, you can check the Docker version with `docker --version` or `docker version`.
- **Start Docker Service**: On Linux, you might need to start the Docker service with `sudo systemctl start docker` and enable it to start on boot with `sudo systemctl enable docker`.

Please replace any placeholder URLs with the actual download URLs provided by Docker on their official website. Always refer to the [official Docker documentation](https://docs.docker.com/get-docker/) for the most accurate and up-to-date installation instructions.


### Build docker and run
```
cd llmsys_s24_hw1
docker build -t llmsys_s24_hw1 .
docker run -it -v {/path/to/your/project} --name=centos7-CUDA --gpus all {docker_name} /bin/bash
```

### Docker exec
```
docker exec -it centos7-CUDA /bin/bash
```

