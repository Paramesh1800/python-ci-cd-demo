# Python CI/CD Deployment to AWS EC2

This repository contains a simple Flask web application with a fully automated CI/CD pipeline using GitHub Actions to test and deploy the application to an AWS EC2 instance.

---

## Project Structure

```text
├── .github/
│   └── workflows/
│       └── Python-ci-cd.yml   # GitHub Actions workflow configuration
├── app.py                     # Flask web application entry point
├── test_app.py                # Unit tests for the Flask application
├── requirements.txt           # Python application dependencies
└── README.md                  # Project documentation
```

---

## Technical Features

1. **Unit Testing**: Automated testing using `pytest` to verify Flask endpoints before deployment.
2. **Secure SSH Deployment**: GitHub Actions connects securely to the EC2 server over SSH.
3. **Graceful Reloads**: Deployment scripts cleanly stop previous web server instances using `fuser` before deploying new ones to avoid port conflicts.
4. **Background Service execution**: Run the application continuously in the background using `nohup` and standard stream detachment.
5. **Private Training Setup**: Configured security group boundaries restricting app access (Port 8000) only to your personal IP.

---

## How the CI/CD Pipeline Works

The workflow [.github/workflows/Python-ci-cd.yml](.github/workflows/Python-ci-cd.yml) is divided into two main jobs:

### 1. Test Job
Runs automatically on every `push` and `pull_request` to the `main` branch.
* Spins up a Linux container.
* Sets up Python 3.13.
* Installs dependencies from `requirements.txt`.
* Runs `pytest -v` to check that all tests pass.

### 2. Deploy Job
Runs automatically after a successful test job, only on pushes to the `main` branch.
* SSHes into the EC2 instance using your secrets.
* Pulls the latest code from GitHub.
* Stops the old app instance on Port 8000.
* Starts the new Flask app in the background.

---

## Setup Guide

### 1. AWS EC2 Instance Configuration
1. Launch an EC2 Instance (Ubuntu or Amazon Linux).
2. Configure **Security Group** Inbound Rules:
   * **Port 22 (SSH)**: Source `Anywhere-IPv4` (`0.0.0.0/0`) or GitHub Actions IPs.
   * **Port 8000 (Custom TCP)**: Source `My IP` (to keep it private for training).

### 2. GitHub Secrets Setup
Add the following secrets to your GitHub repository under **Settings > Secrets and variables > Actions**:
* `EC2_HOST`: The Public IP of your EC2 instance.
* `EC2_USER`: The default username (e.g. `ubuntu` or `ec2-user`).
* `EC2_SSH_KEY`: The complete contents of your private key `.pem` file.

### 3. One-Time EC2 Server Setup
Connect to your EC2 instance once via SSH to initialize the directory and virtual environment:
```bash
# Connect to your instance
ssh -i "your-key.pem" ubuntu@<your-ec2-ip>

# Create folder and clone repo
mkdir -p ~/app
cd ~/app
git clone https://github.com/Paramesh1800/python-ci-cd-demo.git
cd python-ci-cd-demo

# Install Python packages and environment tools
sudo apt update
sudo apt install python3-pip python3-venv -y

# Setup virtual environment and dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Deployment and Verification
Once the steps above are completed, pushing any changes to `main` will automatically deploy them:
1. Modify `app.py` or codebase on your local machine.
2. Push your changes: `git push origin main`.
3. View the pipeline status on the **Actions** tab of your repository.
4. Navigate to your app in a browser to verify: `http://<your-ec2-public-ip>:8000`.
