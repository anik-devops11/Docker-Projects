# 🐳 Docker-Based Developer Environment

A fully customizable **Docker-based development environment** with VS Code integration.

This project sets up a complete developer workstation inside a Docker container. Whether you're using Windows, macOS, or Linux, this allows you to spin up the same isolated environment containing all necessary development tools like Python, Node.js, Docker CLI, Git, and more — without needing to install them directly on your system.

It’s especially useful for:

- 🔁 Consistency across teams – everyone develops in the same environment.

- 🧪 Trying out a new stack – without affecting your base system.

- 🧼 Keeping your host OS clean – no polluting system-wide installations.

- 💻 Developing with VS Code using the Remote - Containers extension.


This project is a great starting point for building language-specific environments (Python, JavaScript, Go, Rust, etc.), adding databases (MySQL, PostgreSQL), or working on microservices with Docker Compose.

---

## 📁 Project Structure

```
docker-dev-environment/
├── Dockerfile
├── docker-compose.yml
├── .devcontainer/
│   └── devcontainer.json
├── README.md
└── example/
    ├── hello.py
    └── app.js
```

---

## 🛠️ What’s Included

| Tool         | Purpose                      |
| ------------ | ---------------------------- |
| Ubuntu 22.04 | Base OS                      |
| Python3/pip  | Run Python apps              |
| Node.js/npm  | Run JavaScript/Node apps     |
| Git, curl    | Basic dev tools              |
| Docker CLI   | Docker commands in container |

---

## ✍️ How I Created This Project (Author Guide)

### 1. Create Project Folder

```bash
mkdir docker-dev-environment
cd docker-dev-environment
```

### 2. Add Dockerfile

```Dockerfile
FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    git curl wget vim build-essential \
    python3 python3-pip nodejs npm docker.io \
    && apt-get clean
RUN useradd -ms /bin/bash devuser
USER devuser
WORKDIR /home/devuser
CMD ["bash"]
```

**Detailed Explanation:**

* `FROM ubuntu:22.04`: Uses the official Ubuntu 22.04 image as the base.
* `ENV DEBIAN_FRONTEND=noninteractive`: Disables interactive prompts during package installs.
* `RUN apt-get update ...`: Installs required developer tools (Git, Python, Node.js, etc.) and then cleans up cache.
* `RUN useradd -ms /bin/bash devuser`: Creates a non-root user for secure execution.
* `USER devuser`: Switches to the newly created user instead of running as root.
* `WORKDIR /home/devuser`: Sets the working directory inside the container.
* `CMD ["bash"]`: Runs the Bash shell when the container starts.

---

### 3. Add docker-compose.yml

```yaml
version: "3.8"

services:
  dev:
    build: .
    container_name: dev-env
    volumes:
      - .:/workspace
      - /var/run/docker.sock:/var/run/docker.sock
    working_dir: /workspace
    stdin_open: true
    tty: true
```

**Detailed Explanation:**

* `version: "3.8"`: Uses Docker Compose specification version 3.8.
* `services`: Defines the containerized services. Here, we only have `dev`.
* `build: .`: Builds the Docker image from the current directory.
* `container_name`: Gives the container a name (`dev-env`).
* `volumes`:

  * `.:/workspace`: Mounts the current directory to `/workspace` in the container.
  * `/var/run/docker.sock:/var/run/docker.sock`: Allows the container to use Docker CLI commands.
* `working_dir: /workspace`: Sets the container’s default working directory.
* `stdin_open` and `tty`: Keeps the terminal open for interaction.

---

### 4. Add VS Code dev container config

**.devcontainer/devcontainer.json**:

```json
{
  "name": "Dev Environment",
  "context": "..",
  "dockerFile": "../Dockerfile",
  "workspaceFolder": "/workspace",
  "mounts": [
    "source=${localWorkspaceFolder},target=/workspace,type=bind"
  ],
  "settings": {
    "terminal.integrated.defaultProfile.linux": "bash"
  }
}
```

**Explanation:**

* Defines a VS Code Remote Container setup.
* Points to the Dockerfile and sets the workspace location.
* Mounts the current folder into the container.
* Uses Bash as the default shell.

---

### 5. Add Example Files (optional)

```python
# example/hello.py
print("Hello from Python inside Docker container!")
```

```javascript
// example/app.js
console.log("Hello from Node.js inside Docker container!");
```

---

## 👨‍💻 How **You** Can Use This Project (Cloner Guide)

### ✅ Prerequisites

* Docker installed and running
* Visual Studio Code installed
* VS Code extension: **Remote - Containers**

---

### ▶️ Steps to Use

#### 1. Clone the Repository

```bash
git clone https://github.com/anik-devops11/docker-dev-environment.git
cd docker-dev-environment
```

#### 2. Build & Run the Container

```bash
docker compose up --build -d
```

#### 3. Open the Project in VS Code

* Launch VS Code
* Press `Ctrl + Shift + P`
* Choose: `Remote-Containers: Reopen in Container`
* Select this folder

#### 4. Run Code

Open terminal inside VS Code (`Ctrl + ~`) and run:

```bash
# Python
python3 example/hello.py

# Node.js
node example/app.js
```

---

## 💡 Benefits

* All tools pre-installed in a container
* Run isolated dev environments
* Avoid cluttering your host machine
* Portable & team-friendly

---

## 📌 Notes

* Files are saved to your local folder (`.:/workspace` volume bind)
* You can add any other tools to `Dockerfile` as needed
* Docker CLI works inside the container

---

## 🔗 Resources

* [VS Code Remote Containers Docs](https://code.visualstudio.com/docs/remote/containers)
* [Docker Compose Docs](https://docs.docker.com/compose/)
* [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)

---

> Made with 💙 by Anik Dash
