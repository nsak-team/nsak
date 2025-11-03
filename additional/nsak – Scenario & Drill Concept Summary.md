## 1. System Purpose
The **nsak (Network Sniffer Appliance Kit)** is a containerized environment that automates the preparation, simulation, and analysis of security-related scenarios.
Each *Scenario* consists of several *Drills* (e.g., port-scan, IP-spoofing) that together form a test setup (e.g., WLAN spoofing).

**Goals:**
- Modular structure (drill-based)
- Reproducible security simulations
- Automatic container builds per scenario
- Compatible with *systemd* (autostart / timer)

---

## 2. Directory Structure
```
scenarios/
 └─ wlan-spoofing/
     ├─ scenario.yaml
     ├─ scenario.py
     └─ README.md

drills/
 └─ ip-spoofing/
     ├─ drill.yaml
     ├─ drill.py
     └─ README.md
```
Drills are distributed as **.drill zip packages** containing YAML, code, and documentation.

---

## 3. YAML Definition Structure

### scenario.yaml
```yaml
scenario: v1
metadata:
  author: frank@bfh.ch
  repository: github.com/franky/superdrill.git

drills:
  - port-scan
  - ip-spoofing
  - ...

# default entrypoint:
#   scenario.py

interface:
  arguments: prepare scenario
  return value: none -> output
```

### drill.yaml
```yaml
drill: v1
metadata:
  author: frank@bfh.ch
  repository: github.com/franky/superdrill.git

dependencies:
  - nmap

# default entrypoint:
#   drill.py

interface:
  arguments:
  return value: data-structure
```

---

## 4. System Workflow (Scenario Preparation)
**Base Image:** Kali Linux

**Workflow (nsak prepare scenario):**
1. Collect referenced drills from scenario  
2. Aggregate dependencies from drills  
3. Build container image (Podman/Docker)  
4. Output: ready-to-run scenario image  

---

## 5. nsak CLI – Subcommands Overview
| Command | Description |
|----------|-------------|
| `nsak scenario` | Entry command group |
| `nsak prepare wlan-spoofing` | Collect drills and build image |
| `nsak start wlan-spoofing` | Start the scenario container |
| `nsak stop wlan-spoofing` | Stop a running scenario |
| `nsak autostart enable wlan-spoofing` | Enable systemd autostart |
| `nsak autostart disable wlan-spoofing` | Disable systemd autostart |
| `nsak verify scenario/drill` | Validate YAML and dependencies |
| `nsak simulate wlan-spoofing` | Dry-run scenario with test data |
| `nsak list` | List all detected scenarios |
| `nsak status` | Show system and scenario status |
| `nsak help` | Show available commands |
| `nsak version` | Show nsak version and build info |

---

## 6. Scenario & Status Management
Status and metadata are stored in a YAML/JSON state file (e.g., `/var/lib/nsak/` or `$XDG_STATE_HOME/nsak`).

**State fields:**
- scenario-id  
- status: *prepared / running / stopped*  
- container-id / pid  
- timestamps (started_at / finished_at)  
- last_error  

The CLI manages scenario lifecycle (`prepare`, `start`, `stop`, `status`, `list`) using this state.

---

## 7. Configuration (nsak.yaml)
```yaml
authorized-keys:
  - ssh-rsa AAAA... user@example.com

wlan-configuration:
  ssid: <SSID>
  pwd: <PASSWORD>
  ip: <static-ip or dhcp>
  open-only-when-ready: true
```

 **Advanced Feature:** WLAN opens only when required, data is transmitted once connected.


---

## 8. Required Diagrams
- Use-Case Diagram  
- Component Diagram  
- Sequence Diagram  
- System Environment Diagram  
- Process Environment Diagram  
- Process Model  
- Activity Diagram  
