# Docker and Kubernetes Workshop - Student Prerequisites

Complete this setup **before the workshop**. During the Kubernetes labs, we
will use **kind (Kubernetes IN Docker)** to run a local Kubernetes cluster.

> **Important:** Do not enable the Kubernetes feature in Docker Desktop for
> this workshop. Docker Desktop provides the container runtime, while kind
> creates and manages the Kubernetes cluster.

## 1. Laptop requirements

| Requirement | Minimum | Recommended |
| --- | --- | --- |
| Operating system | Windows 10/11, macOS, or a modern 64-bit Linux distribution | Latest supported OS updates |
| Memory | 8 GB RAM | 16 GB RAM |
| Free disk space | 10 GB | 20 GB |
| CPU | 2 cores with virtualization | 4 or more cores |
| Internet | Required for installation and image downloads | Stable broadband connection |

You must also have:

- administrator access to install software;
- hardware virtualization enabled in BIOS/UEFI;
- a laptop charger;
- access to PowerShell, Terminal, or a Linux shell.

## 2. Accounts required

### Docker Hub

1. Create an account at <https://hub.docker.com/>.
2. Verify your email address.
3. Record your Docker Hub username.
4. Sign in from a terminal:

   ```text
   docker login
   ```

Use a Docker Hub access token instead of your password if your account uses
multi-factor authentication.

### GitHub

A GitHub account is recommended for downloading workshop material and saving
your work:

<https://github.com/signup>

## 3. Software to install

Install all the following tools:

1. Docker Desktop or Docker Engine
2. Git
3. Visual Studio Code
4. Python 3.10 or later
5. `kubectl`
6. kind

The commands in this guide use `kind` in lowercase. The project name is often
written as **kind**, meaning **Kubernetes IN Docker**.

## 4. Windows setup

### 4.1 Enable WSL 2

Open **PowerShell as Administrator** and run:

```powershell
wsl --install
```

Restart the computer when requested. After restarting, verify WSL:

```powershell
wsl --status
wsl --version
```

If WSL is already installed, update it:

```powershell
wsl --update
```

### 4.2 Install Docker Desktop

Download Docker Desktop:

<https://www.docker.com/products/docker-desktop/>

During installation:

1. Select the WSL 2 backend when prompted.
2. Start Docker Desktop.
3. Accept the license terms if applicable.
4. Wait until Docker Desktop reports that the engine is running.
5. In **Settings > General**, keep **Use the WSL 2 based engine** enabled.
6. Do not enable Docker Desktop Kubernetes; the workshop uses kind.

Verify Docker from a normal PowerShell window:

```powershell
docker version
docker compose version
docker run --rm hello-world
```

### 4.3 Install tools with WinGet

Open PowerShell and run:

```powershell
winget install --id Git.Git -e
winget install --id Microsoft.VisualStudioCode -e
winget install --id Python.Python.3.12 -e
winget install --id Kubernetes.kubectl -e
winget install --id Kubernetes.kind -e
```

Close and reopen PowerShell after installation so that updated `PATH`
settings are loaded.

If WinGet is unavailable, use the official installation pages:

- Git: <https://git-scm.com/downloads>
- VS Code: <https://code.visualstudio.com/download>
- Python: <https://www.python.org/downloads/>
- kubectl: <https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/>
- kind: <https://kind.sigs.k8s.io/docs/user/quick-start/#installation>

## 5. macOS setup

Install Docker Desktop:

<https://www.docker.com/products/docker-desktop/>

Install Homebrew if it is not already available:

<https://brew.sh/>

Install the remaining tools:

```bash
brew install git python kubectl kind
brew install --cask visual-studio-code
```

Start Docker Desktop and verify it:

```bash
docker version
docker compose version
docker run --rm hello-world
```

## 6. Linux setup

Install Docker Engine using the instructions for your distribution:

<https://docs.docker.com/engine/install/>

Complete Docker's Linux post-installation steps so Docker can run without
`sudo`:

<https://docs.docker.com/engine/install/linux-postinstall/>

Install the remaining tools from their official documentation:

- Git: <https://git-scm.com/download/linux>
- VS Code: <https://code.visualstudio.com/docs/setup/linux>
- Python: use the package manager provided by your distribution
- kubectl: <https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/>
- kind: <https://kind.sigs.k8s.io/docs/user/quick-start/#installation>

Log out and back in after adding your user to the `docker` group. Then verify:

```bash
docker version
docker compose version
docker run --rm hello-world
```

## 7. Verify all command-line tools

Open a new terminal and run:

```text
docker version
docker compose version
git --version
python --version
kubectl version --client
kind version
```

On some Linux or macOS systems, use this command if `python` is not available:

```bash
python3 --version
```

All commands must complete successfully. The exact versions may differ, but
Python must be version 3.10 or later.

## 8. Configure Docker Desktop resources

Where resource settings are available, allocate at least:

- 2 CPUs;
- 4 GB memory;
- 10 GB free disk space.

For better workshop performance, use 4 CPUs and 6-8 GB memory if the laptop
has at least 16 GB RAM.

## 9. Create the kind Kubernetes cluster

### 9.1 Confirm Docker is running

Run:

```text
docker info
```

Do not continue until this command succeeds.

### 9.2 Review the cluster configuration

The repository includes `kind-workshop-config.yaml` with this content:

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
    extraPortMappings:
      - containerPort: 30080
        hostPort: 8080
        protocol: TCP
  - role: worker
```

This creates:

- one Kubernetes control-plane node;
- one worker node;
- a port mapping from `localhost:8080` to NodePort `30080` in the cluster.

### 9.3 Create the cluster

Run this command from the workshop repository root:

```text
kind create cluster --name workshop --config kind-workshop-config.yaml
```

Cluster creation can take several minutes during the first run because kind
must download its Kubernetes node image.

### 9.4 Verify the cluster

Run:

```text
kind get clusters
kubectl cluster-info --context kind-workshop
kubectl get nodes -o wide
kubectl get pods --all-namespaces
```

Expected results:

- `kind get clusters` includes `workshop`;
- the current context is `kind-workshop`;
- both nodes eventually show `Ready`;
- Kubernetes system Pods eventually show `Running` or `Completed`.

If another Kubernetes context is selected, switch to the workshop cluster:

```text
kubectl config use-context kind-workshop
```

Wait for both nodes to become ready:

```text
kubectl wait --for=condition=Ready nodes --all --timeout=180s
```

## 10. Run a Kubernetes smoke test

Create a small web server:

```text
kubectl create deployment prerequisite-check --image=nginx:alpine
kubectl expose deployment prerequisite-check --type=NodePort --port=80
kubectl wait --for=condition=Available deployment/prerequisite-check --timeout=180s
kubectl get deployments,pods,services
```

Forward a local port to the test service:

```text
kubectl port-forward service/prerequisite-check 8081:80
```

Keep that terminal open and visit:

<http://localhost:8081>

The nginx welcome page confirms that Docker, kind, Kubernetes, networking, and
`kubectl` are working. Press **Ctrl+C** to stop port forwarding.

Remove the smoke-test resources:

```text
kubectl delete service prerequisite-check
kubectl delete deployment prerequisite-check
```

## 11. Test loading a local Docker image into kind

kind nodes are Docker containers and cannot automatically see images stored in
the host Docker image cache. Local workshop images must be loaded explicitly.

Create a small local image:

```text
docker pull nginx:alpine
docker tag nginx:alpine workshop-local-test:v1
kind load docker-image workshop-local-test:v1 --name workshop
```

Verify that the image exists on the kind nodes:

```text
docker exec workshop-control-plane crictl images
docker exec workshop-worker crictl images
```

During the workshop, the equivalent command for the workshop application will
look like:

```text
kind load docker-image docker-ml-api:v1 --name workshop
```

When using an image loaded directly into kind, Kubernetes manifests should
normally use:

```yaml
imagePullPolicy: IfNotPresent
```

## 12. Download and prepare the workshop material

1. Download or clone the workshop package.
2. Extract the ZIP file completely.
3. Move the extracted `docker-kubernetes-workshop` directory to a simple local
   path.
4. Do not run the workshop directly from a ZIP archive.
5. Avoid OneDrive-synchronized directories if possible.

Example Windows location:

```text
C:\workshops\docker-kubernetes-workshop
```

Example macOS or Linux location:

```text
~/workshops/docker-kubernetes-workshop
```

If a Git repository URL is provided, use:

```text
git clone <WORKSHOP_REPOSITORY_URL>
cd docker-kubernetes-workshop
```

## 13. Prepare the Python environment

From the workshop root directory, create a virtual environment.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r .\sample-app\requirements.txt
```

If PowerShell blocks activation, run this command once in the current terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again.

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r ./sample-app/requirements.txt
```

Verify the sample application:

```text
python -m uvicorn app.main:app --app-dir sample-app
```

Open:

- API documentation: <http://localhost:8000/docs>
- Health endpoint: <http://localhost:8000/health>

Press **Ctrl+C** to stop the application.

## 14. Pre-download workshop images

Run these commands before arriving at the workshop:

```text
docker pull python:3.12-slim
docker pull nginx:alpine
kind create cluster --name image-cache
kind delete cluster --name image-cache
```

The temporary cluster creation downloads the kind node image and confirms that
kind can create and remove clusters. It does not affect the `workshop` cluster.

If the instructor provides an application image, pull it as well:

```text
docker pull <DOCKERHUB_USERNAME>/docker-ml-api:v1
```

## 15. Useful kind commands

| Task | Command |
| --- | --- |
| List kind clusters | `kind get clusters` |
| List cluster nodes | `kind get nodes --name workshop` |
| Create the workshop cluster | `kind create cluster --name workshop --config kind-workshop-config.yaml` |
| Load a local image | `kind load docker-image IMAGE:TAG --name workshop` |
| Export diagnostic logs | `kind export logs --name workshop` |
| Delete the cluster | `kind delete cluster --name workshop` |

Deleting a kind cluster removes its Kubernetes workloads and cluster state, but
does not remove Docker images from the host.

## 16. Common problems

### `docker` is not recognized

- Close and reopen the terminal.
- Restart Docker Desktop.
- Confirm Docker was added to `PATH`.
- On Windows, restart the computer after installing Docker Desktop or WSL.

### Cannot connect to the Docker daemon

- Start Docker Desktop or the Docker Engine service.
- Wait for Docker to report that the engine is running.
- Run `docker info` again.
- On Linux, confirm that your user belongs to the `docker` group.

### kind cluster creation fails

Run:

```text
docker info
kind delete cluster --name workshop
kind create cluster --name workshop --config kind-workshop-config.yaml --verbosity 1
```

Also check:

- virtualization is enabled;
- Docker has enough CPU, memory, and disk space;
- VPN, proxy, firewall, or antivirus software is not blocking downloads;
- no other application is using port `8080`.

### Port `8080` is already in use

Change `hostPort` in `kind-workshop-config.yaml`, for example:

```yaml
hostPort: 8088
```

Then recreate the cluster:

```text
kind delete cluster --name workshop
kind create cluster --name workshop --config kind-workshop-config.yaml
```

### Kubernetes nodes remain `NotReady`

Wait two minutes and run:

```text
kubectl get nodes
kubectl get pods --all-namespaces
```

If they remain unavailable:

```text
kind export logs --name workshop
kind delete cluster --name workshop
```

Restart Docker and recreate the cluster.

### Docker Hub pull-rate or authentication error

Sign in again:

```text
docker logout
docker login
```

Confirm that your Docker Hub email is verified.

### Corporate proxy, VPN, or TLS certificate errors

- Try the setup before the workshop network is required.
- Record the exact error message.
- Check whether Docker Desktop requires proxy configuration.
- Ask your institution's IT team whether Docker Hub, GitHub, PyPI, and
  Kubernetes registries are permitted.
- If allowed by your organization, temporarily disconnect from a VPN and retry.

Do not disable certificate validation as a workaround.

## 17. Final readiness checklist

Complete every item before the workshop:

- [ ] My laptop has at least 8 GB RAM and 10 GB free disk space.
- [ ] Hardware virtualization is enabled.
- [ ] Docker starts successfully.
- [ ] `docker run --rm hello-world` succeeds.
- [ ] `docker compose version` succeeds.
- [ ] Git is installed.
- [ ] VS Code is installed.
- [ ] Python 3.10 or later is installed.
- [ ] `kubectl version --client` succeeds.
- [ ] `kind version` succeeds.
- [ ] I have a verified Docker Hub account.
- [ ] `docker login` succeeds.
- [ ] The `workshop` kind cluster is created.
- [ ] Both kind nodes show `Ready`.
- [ ] The nginx Kubernetes smoke test succeeds.
- [ ] The workshop ZIP is fully extracted or the repository is cloned.
- [ ] The Python dependencies are installed.
- [ ] The sample application opens at `http://localhost:8000/docs`.
- [ ] I have downloaded the required container images.
- [ ] I will bring my laptop and charger.

## 18. Information to send if setup fails

Share the following with the instructor before the workshop:

1. Operating system and version.
2. Screenshot or copied text of the error.
3. Output of:

   ```text
   docker version
   docker info
   kubectl version --client
   kind version
   kind get clusters
   kubectl get nodes -o wide
   kubectl get pods --all-namespaces
   ```

Remove usernames, tokens, passwords, and other private information before
sharing terminal output.
