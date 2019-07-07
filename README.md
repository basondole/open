# About basondoletools
Network application for automating tasks in service provider environments offering a set of network tool designed for service providers NOC.

# What is it?

- Software solution that provides network administrators a quick and easy way to manage customer services in the network.
- Handles tasks such as provisioning of services on edge routers, scheduling of bandwidth changes and deploying of configs.
- Provides the user with a single unified interface for edge routers CLI, Netdot and Solarwinds Orion NPM where applicable.
- Aims to offload manual and time consuming repetitive tasks from net operators.

# Key features
- Quickly deploy new service by collecting data from your IT infrastructure in a few minutes.
- Maintain consistent configuration and data records for your infrastructure databases
- Issue commands to all network devices at once via centralized interface to quickly pinpoint issues or gather information.
- Automatically schedule bandwidth changes for different services at any time
- Get email alerts on bandwidth changes performed automatically
- Store and archive logs for audit and tracking purposes
- Interface with existing systems with supported APIs
- Get simple access to relevant data from your entire network
- Easy to setup and requires no costly training for installation and user education

# Tools available
- Service search
- VLAN operations
- IPv4 operations
- Service provisioning
- Burst packages management
- Bandwidth on demand management

### Service search
- The search can be performed against a vlan-id, service description or ipv4 address.
- The tool uses an algorithm to search for interesting sections of running/active configuration in each active edge router in the network.

### IPv4 & VLANs operations
- Offers the ability to query all active edge routers in the network and find out if an IPv4 prefix or its subnet has been used.
- Helps in identifying rogue IPv4 addresses configured in the network consequently resolving address and routing conflicts in the network.
- Allows an operator to locate the edge at which a certain vlan-id has been used.
- On edge routers with high customer density this tools automates the task of finding free vlans to use for new service provisioning.

### Service provisioning
- Auto provisioning of internet and L2MPLS services on edge routers on a single click.
- Automatically assigns a vlan-id and IPv4 addresses and adds node to NPM
- Drastically reduces the amount of time (at least 50%) an administrator would use to gather config details and extra time to update documentation/monitoring databases

### Burst packages management
- Offers a client-server relation between the client application running on admin workstation and the server hosting the clients database and config changes.
- Network admin can easily make use of this unified interface to manage burst clients in a user friendly manner.
- Offers ability to view clients and their packages, add or remove clients and moving clients between packages.

### Bandwidth on demand management
- Admin can add and schedule bandwidth changes to be carried out or reverted at a later time without requiring manual intervention.
- User has the ability to view scheduled bandwidth changes and to delete or modify them.
- Offloads manual tracking of temporary bandwidth change requests that is not very efficient.

# Supported platforms for edge routers
- JunOS 11.4R9 and later
- Cisco IOS 12 and IOS XE and later

# Supported API
- Solarwinds Orion Swis
- Netdot REST
