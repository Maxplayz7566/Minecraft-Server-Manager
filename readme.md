# Manage Self-Hosted Minecraft Servers

A tool designed to help you easily manage multiple self-hosted Minecraft servers. This project currently supports **PaperMC**, **Folia**, **Fabric**, **Waterfall**, **Bungee** and **Velocity** servers, with **Forge** support coming soon!

> **Note:** *Forge is a work in progress!*

## Features

- [ ] Easily manage multiple Minecraft servers
- [x] Gui application for desktop enviroments
- [x] Low memory usage
- [ ] Simple configuration of server properties
- [ ] Ability to specify custom `.jar` files
- [ ] Track server statuses and ports

## Prerequisites

- Java 8 or higher
- Python

## Getting started

1. Clone the repository:
    ```bash
    git clone https://github.com/Maxplayz7566/Minecraft-Server-Manager.git
    cd Minecraft-Server-Manager
    ```
2. Creating venv: 
    > **Note:** *This is only required by linux*
   
    ```bash
    python3 -m venv .venv
    source .venv/Scripts/activate
    ```
3. Installing packages:
    ```bash
   pip install -r requirements.txt
   ```
4. Running:
    ```bash
   python3 main.py
    ```