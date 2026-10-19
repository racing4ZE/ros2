# 4ZE Racing Driverless ROS 2

ROS 2 development environment for the 4ZE Racing Formula Student Electric Driverless project.

The environment uses **ROS 2 Jazzy inside Docker**. ROS 2 is not installed directly on Windows or the WSL host.

---

## Architecture

```text
Windows 11
    │
    ▼
WSL 2
    │
    ▼
Ubuntu 22.04
    │
    ▼
Docker Desktop
    │
    ▼
Docker Container
    │
    ▼
Ubuntu 24.04
    │
    ▼
ROS 2 Jazzy
```

---

## Repository Structure

```text
ros2/
│
├── .devcontainer/
│   └── devcontainer.json
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── mockup_ws/
│   └── src/
│       └── 4ze_vehicle_description/
│
├── driverless_ws/
│   └── src/
│
├── scripts/
│   ├── setup.sh
│   └── verify_environment.sh
│
├── .gitignore
└── README.md
```

### Workspaces

#### `mockup_ws`

Temporary vehicle mockup based on the previous vehicle specifications.

Used for:

- Environment verification
- ROS 2 visualization
- RViz testing
- Gazebo/simulation development where applicable

#### `driverless_ws`

Main workspace for the new vehicle Driverless development.

This workspace is intentionally separate from the mockup.

---

# Prerequisites

Install the following on the host machine:

- Windows 11
- WSL 2
- Ubuntu 22.04 inside WSL
- Docker Desktop
- Docker Desktop WSL 2 integration
- Visual Studio Code
- Dev Containers extension

ROS 2 does **not** need to be installed directly on Windows or on the Ubuntu WSL host.

---

# 1. WSL Setup

Verify WSL:
```bash
wsl --version
```

Verify the installed distributions:
```bash
wsl -l -v
```

Ubuntu should be running under WSL 2.

Inside Ubuntu, verify Docker:
```bash
docker version
```

Docker commands should work through Docker Desktop's WSL 2 integration.

---

# 2. Clone the Repository

Inside WSL:
```bash
git clone <REPOSITORY_URL>
```

Enter the repository:
```bash
cd ros2
```

---

# 3. Load the Docker Image

The ROS 2 Docker image is distributed separately through a GitHub Release.

Download:
```text
4ze-ros2-jazzy-v1.0.0.tar
```

Load the image:
```bash
docker load -i 4ze-ros2-jazzy-v1.0.0.tar
```

Verify:
```bash
docker images
```

The following image should be available:
```text
4ze-ros2    jazzy-v1.0.0
```

The Docker image `.tar` is **not stored in the Git repository**.

---

# 4. Start the Container

From the repository root:
```bash
docker compose -f docker/docker-compose.yml up -d
```

Check the container:
```bash
docker ps
```

The container should be running as:
```text
4ze_ros2
```

To enter the container manually:
```bash
docker exec -it 4ze_ros2 bash
```

The default working directory is:
```text
/driverless_ws
```

---

# 5. VS Code Dev Container

Open the repository folder in Visual Studio Code.

Use:
```text
Ctrl + Shift + P
```

Select:
```text
Dev Containers: Reopen in Container
```

VS Code will attach to the `4ze_ros2` container.

Verify the workspace:
```bash
pwd
```

Expected:
```text
/driverless_ws
```

---

# 6. Verify ROS 2

Inside the container:
```bash
echo $ROS_DISTRO
```

Expected:
```text
jazzy
```

Check ROS 2:
```bash
ros2 --version
```

Check Colcon:
```bash
colcon --version
```

---

# 7. Verify the Development Environment

Run:
```bash
/scripts/verify_environment.sh
```

The verification script checks:

- ROS 2 Jazzy
- ROS 2 CLI
- Colcon
- Driverless workspace
- Mockup workspace
- Vehicle description package
- Gazebo

A successful environment ends with:
```text
======================================
ENVIRONMENT CHECK PASSED
======================================
```

---

# 8. Setup Script

The setup script can be run with:
```bash
/scripts/setup.sh
```

It checks the ROS 2 installation, verifies both workspaces and builds the mockup workspace.

---

# 9. Build the Mockup

Enter the mockup workspace:
```bash
cd /mockup_ws
```

Build:
```bash
colcon build
```

Source the workspace:
```bash
source install/setup.bash
```

---

# 10. Launch the Mockup

Run:
```bash
ros2 launch 4ze_vehicle_description display.launch.py
```

RViz should open and display the vehicle mockup.

This serves as the primary end-to-end environment acceptance test.

---

# 11. Driverless Development

The actual Driverless development workspace is:
```text
/driverless_ws
```

Source directory:
```text
/driverless_ws/src
```

New Driverless ROS 2 packages should be created inside:
```bash
cd /driverless_ws/src
```

The mockup workspace should not be used for new vehicle Driverless packages.

---

# 12. Development Workflow
```text
Windows 11
    │
    ▼
WSL Ubuntu
    │
    ▼
Docker Desktop
    │
    ▼
4ZE ROS 2 Container
    │
    ├── /mockup_ws
    │      └── Temporary vehicle mockup
    │
    └── /driverless_ws
           └── Actual Driverless development
```

---

# 13. Docker Image Versioning

Docker images are versioned rather than using an unversioned `latest` tag.

Current image:
```text
4ze-ros2:jazzy-v1.0.0
```

When the development environment changes, create a new version.

Example:
```text
4ze-ros2:jazzy-v1.1.0
```

The corresponding Docker image archive should be distributed through a GitHub Release.

---

# 14. Creating a New Docker Image Release

After modifying the Docker environment, build the new image:
```bash
docker build -t 4ze-ros2:jazzy-v1.1.0 ./docker
```

Save the image:
```bash
docker save -o 4ze-ros2-jazzy-v1.1.0.tar 4ze-ros2:jazzy-v1.1.0
```

Upload the `.tar` file as a GitHub Release asset.

Do **not** commit the `.tar` file to Git.

---

# 15. Useful Docker Commands

### Start the container
```bash
docker compose -f docker/docker-compose.yml up -d
```

### Stop the container
```bash
docker compose -f docker/docker-compose.yml down
```

### Enter the container
```bash
docker exec -it 4ze_ros2 bash
```

### View running containers
```bash
docker ps
```

### View container logs
```bash
docker logs 4ze_ros2
```

---

# 16. Useful ROS 2 Commands

### Build the Driverless workspace
```bash
cd /driverless_ws
colcon build
source install/setup.bash
```

### Build the mockup workspace
```bash
cd /mockup_ws
colcon build
source install/setup.bash
```

### Launch the mockup
```bash
cd /mockup_ws
source install/setup.bash
ros2 launch 4ze_vehicle_description display.launch.py
```

### Verify the environment
```bash
/scripts/verify_environment.sh
```

---

# 17. Git Workflow

The Git repository contains:

- ROS 2 source code
- Docker configuration
- Dev Container configuration
- Setup scripts
- Verification scripts
- Documentation

Build artifacts and Docker image archives are not committed.

Do not commit:
```text
build/
install/
log/
*.tar
```

Check the repository before committing:
```bash
git status
```

Commit changes:
```bash
git add .
git commit -m "Description of change"
git push
```

---

# 18. Environment Acceptance Test

A new development machine is considered ready when the following are working:
```text
[✓] Windows 11
[✓] WSL 2
[✓] Ubuntu 22.04
[✓] Docker Desktop
[✓] Docker WSL integration
[✓] 4ZE ROS 2 Docker image
[✓] Docker Compose
[✓] VS Code Dev Container
[✓] ROS 2 Jazzy
[✓] Colcon
[✓] /driverless_ws
[✓] /mockup_ws
[✓] 4ze_vehicle_description
[✓] RViz
[✓] Gazebo
[✓] Environment verification script
```

The final practical test is:
```bash
cd /mockup_ws
source install/setup.bash
ros2 launch 4ze_vehicle_description display.launch.py
```

If the vehicle appears correctly in RViz, the ROS 2 development environment is ready for Driverless development.

---

# Current Environment Version
```text
ROS 2:          Jazzy
Container OS:   Ubuntu 24.04
Host OS:        Windows 11
WSL:            Ubuntu 22.04
Docker Image:   4ze-ros2:jazzy-v1.0.0
```

---

# Maintainer

**4ZE Racing Driverless**
