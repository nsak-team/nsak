# NSAK Framework: Configuration Management

GitLab: https://gitlab.ti.bfh.ch/groups/gausf1-vonal3/-/milestones/5
Start date: 10.03.2026
Due date: 19.03.2026

This milestone defines the configuration model and execution framework for NSAK scenarios. It introduces a structured approach for configuring scenarios and drills, including drill definitions, reusable presets, and the generation of a resolved run configuration.

The goal is to provide a flexible and reproducible configuration system that allows scenarios to expose parameters, merge configuration layers, and execute drills in a defined order.

Setup — new configuration approach:
- [ ] Drills and scenarios can expose build and runtime parameters as configuration objects
- [ ] The configuration objects can be set interactively during `nsak scenario build` or `nsak scenario run`
- [ ] Alternatively the configuration objects can be set as CLI parameters
- [ ] Alternatively the configuration objects can be provided via file

Goals:
- [x] A configuration management is implemented into the NSAK Framework
