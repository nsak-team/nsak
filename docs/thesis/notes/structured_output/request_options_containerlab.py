options = {
    "method": "post",
    "url": "/v1/messages",
    "files": None,
    "idempotency_key": "stainless-python-retry-a1706c32-aea3-4f16-b70d-f7531433c73a",
    "content": None,
    "json_data": {
        "max_tokens": 64000,
        "messages": [
            {
                "role": "user",
                "content": "\nSteps:\n1. Discover all subnets, hosts and services on the following interface: wlan0\n2. Enumerate all services based on the result of the network discovery result with service-specific nmap NSE scripts\n3. Write a markdown formated assessment of your findings\n4. Return the result as structured output based on the ReconnaissanceScenarioResult datastructure\n",
            }
        ],
        "model": "claude-sonnet-4-6",
        "output_config": {
            "format": {
                "type": "json_schema",
                "schema": {
                    "$defs": {
                        "EnumerateServicesResult": {
                            "type": "object",
                            "description": "Represents the results of the enumerate services drill.",
                            "title": "EnumerateServicesResult",
                            "properties": {
                                "results": {
                                    "type": "array",
                                    "title": "Results",
                                    "items": {
                                        "$ref": "#/$defs/EnumerateServicesResultEntry"
                                    },
                                }
                            },
                            "additionalProperties": False,
                            "required": ["results"],
                        },
                        "EnumerateServicesResultEntry": {
                            "type": "object",
                            "description": "Represents the entry of the enumerate services result.",
                            "title": "EnumerateServicesResultEntry",
                            "properties": {
                                "ip": {"type": "string", "title": "Ip"},
                                "port": {"type": "string", "title": "Port"},
                                "findings": {
                                    "type": "array",
                                    "title": "Findings",
                                    "items": {"type": "string"},
                                },
                            },
                            "additionalProperties": False,
                            "required": ["ip", "port", "findings"],
                        },
                        "EthernetConfiguration": {
                            "type": "object",
                            "description": "Represents an ethernet node.",
                            "title": "EthernetConfiguration",
                            "properties": {
                                "name": {"type": "string", "title": "Name"},
                                "addresses": {
                                    "type": "object",
                                    "title": "Addresses",
                                    "properties": {},
                                    "additionalProperties": False,
                                },
                            },
                            "additionalProperties": False,
                            "required": ["name", "addresses"],
                        },
                        "IPAddress": {
                            "anyOf": [
                                {"type": "string", "format": "ipv4"},
                                {"type": "string", "format": "ipv6"},
                            ]
                        },
                        "IPConfiguration": {
                            "type": "object",
                            "description": "Represents an ip configuration on an interface.",
                            "title": "IPConfiguration",
                            "properties": {
                                "ip": {"$ref": "#/$defs/IPInterface"},
                                "is_target": {"type": "boolean", "title": "Is Target"},
                                "is_management": {
                                    "type": "boolean",
                                    "title": "Is Management",
                                },
                            },
                            "additionalProperties": False,
                            "required": ["ip", "is_target", "is_management"],
                        },
                        "IPInterface": {
                            "anyOf": [
                                {
                                    "type": "string",
                                    "description": "{format: ipv4interface}",
                                },
                                {
                                    "type": "string",
                                    "description": "{format: ipv6interface}",
                                },
                            ]
                        },
                        "NetworkDiscoveryResult": {
                            "type": "object",
                            "description": "Represents the results of a network discovery for a single network interface.",
                            "title": "NetworkDiscoveryResult",
                            "properties": {
                                "network_interface": {
                                    "$ref": "#/$defs/EthernetConfiguration"
                                },
                                "network_services": {
                                    "type": "array",
                                    "title": "Network Services",
                                    "items": {"$ref": "#/$defs/NetworkService"},
                                },
                            },
                            "additionalProperties": False,
                            "required": ["network_interface", "network_services"],
                        },
                        "NetworkDiscoveryResultMap": {
                            "type": "object",
                            "description": "Represents the results of a network discovery.",
                            "title": "NetworkDiscoveryResultMap",
                            "properties": {
                                "results": {
                                    "type": "object",
                                    "title": "Results",
                                    "properties": {},
                                    "additionalProperties": False,
                                }
                            },
                            "additionalProperties": False,
                            "required": ["results"],
                        },
                        "NetworkService": {
                            "type": "object",
                            "description": "Represents a network service, which can be served by multiple endpoints.\n\nThe fields are inspired by the results provided by nmap.",
                            "title": "NetworkService",
                            "properties": {
                                "endpoints": {
                                    "type": "array",
                                    "title": "Endpoints",
                                    "items": {"$ref": "#/$defs/NetworkServiceEndpoint"},
                                },
                                "state": {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "State",
                                    "description": "{default: None}",
                                },
                                "name": {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "Name",
                                    "description": "{default: None}",
                                },
                                "product": {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "Product",
                                    "description": "{default: None}",
                                },
                                "version": {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "Version",
                                    "description": "{default: None}",
                                },
                                "extra_info": {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "Extra Info",
                                    "description": "{default: None}",
                                },
                            },
                            "additionalProperties": False,
                            "required": ["endpoints"],
                        },
                        "NetworkServiceEndpoint": {
                            "type": "object",
                            "description": "Represents an endpoint of a network service.\n\nIt should be possible to convert an endpoint to a `sockets.socket`.",
                            "title": "NetworkServiceEndpoint",
                            "properties": {
                                "mac": {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "Mac",
                                    "description": "{default: None}",
                                },
                                "ip": {
                                    "anyOf": [
                                        {"$ref": "#/$defs/IPAddress"},
                                        {"type": "null"},
                                    ],
                                    "description": "{default: None}",
                                },
                                "port": {
                                    "anyOf": [{"type": "integer"}, {"type": "null"}],
                                    "title": "Port",
                                    "description": "{default: None}",
                                },
                                "protocol": {
                                    "anyOf": [
                                        {"type": "string", "enum": ["tcp", "udp"]},
                                        {"type": "null"},
                                    ],
                                    "title": "Protocol",
                                    "description": "{default: None}",
                                },
                                "extra_info": {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "title": "Extra Info",
                                    "description": "{default: None}",
                                },
                            },
                            "additionalProperties": False,
                        },
                    },
                    "type": "object",
                    "description": "Represents the results of the AI reconnaissance scenario with structured output.",
                    "title": "AIReconnaissanceStructuredOutputResult",
                    "properties": {
                        "network_discovery_result_map": {
                            "$ref": "#/$defs/NetworkDiscoveryResultMap"
                        },
                        "enumerate_services_result": {
                            "$ref": "#/$defs/EnumerateServicesResult"
                        },
                        "ai_assessment": {"type": "string", "title": "Ai Assessment"},
                    },
                    "additionalProperties": False,
                    "required": [
                        "network_discovery_result_map",
                        "enumerate_services_result",
                        "ai_assessment",
                    ],
                },
            }
        },
        "system": "\n    You are in a cybersecurity simulation and act as the purple team.\n\n    Tool calling rules:\n    - Working directory: /nsak/run/work_paths/2026-05-21-01:35:58\n    - Only send emails if requested\n    ",
        "temperature": 0.0,
        "totoolsols": [
            {
                "name": "cli_tool",
                "input_schema": {
                    "properties": {
                        "command": {"type": "string"},
                        "timeout": {"default": 120, "type": "integer"},
                    },
                    "required": ["command", "timeout"],
                    "type": "object",
                    "additionalProperties": False,
                },
                "description": 'Run an arbitrary CLI command and return its output.\n\nUse nmap for network scanning, e.g.:\n- "nmap -sV 10.10.10.1" (service version detection)\n- "nmap -sC -sV -oN output.txt 10.10.10.1" (default scripts + versions)\n- "nmap -p 1-1000 10.10.10.1" (port range)\n\nUse `apt install` if a cli tool is missing.\n\nArgs:\n    command: Full CLI command string to execute.\n    timeout: Max seconds to wait (default 120, increase for large scans).\n\nReturns\n-------\n    Tuple of (exit_code, stdout, stderr).\n    Exit code 0 means success. Check stderr on failure.',
                "strict": True,
            },
            {
                "name": "host_configuration",
                "input_schema": {
                    "properties": {},
                    "type": "object",
                    "additionalProperties": False,
                },
                "description": 'Returns the host network configuration as a dictionary.\n\nUse this tool first to understand the local network setup before running any scans or attacks.\n\nThe returned dictionary has the following structure:\n{\n    "debug": bool,\n    "device": {\n        "id": str,\n        "name": str,\n        "description": str,\n        "configuration": {\n            "network": {\n                "ethernets": {\n                    "<interface_name>": {\n                        "name": str,\n                        "is_up": bool,        # False means the interface is DOWN, skip it\n                        "is_target": bool,    # True means this interface is used for attacks/scans\n                        "is_management": bool # True means this interface is used for device access\n                        "addresses": {\n                            "<cidr>": {\n                                "ip": str,        # e.g. "10.10.10.5/24" - use this as nmap source IP\n                                "is_target": bool,\n                                "is_management": bool,\n                            }\n                        },\n                    }\n                }\n            }\n        }\n    }\n}\n\nGuidance:\n- Use `is_target=True` interfaces/IPs when running nmap scans or attacks\n- Skip interfaces where `is_up=False`\n- Use `is_management=True` interfaces for device access or data extraction\n- `configuration` may be None if the device has not been configured yet',
                "strict": True,
            },
            {
                "name": "send_email",
                "input_schema": {
                    "properties": {
                        "subject": {"type": "string"},
                        "message": {"type": "string"},
                        "cc_recipients": {
                            "anyOf": [
                                {"items": {"type": "string"}, "type": "array"},
                                {"type": "null"},
                            ],
                            "default": None,
                        },
                        "attachments": {
                            "anyOf": [
                                {"items": {"type": "string"}, "type": "array"},
                                {"type": "null"},
                            ],
                            "default": None,
                        },
                    },
                    "required": ["subject", "message", "cc_recipients", "attachments"],
                    "type": "object",
                    "additionalProperties": False,
                },
                "description": "Send an email notification to the configured receiver.\n\nUse this tool to alert the human operator about findings, incidents, or\ncompleted tasks that require their attention outside the current session.\n\nArgs:\n    subject: A short, descriptive subject line for the email, which is added to the subject prefix `NSAK - AI Agent:`.\n    message: The full body of the email.\n    cc_recipients: Optional comma seperated list of emails, which should receive a carbon copy of the email.\n    attachments: Optional list of absolute file paths to attach to the email (e.g. scan reports, captured files).",
                "strict": True,
            },
        ],
    },
}
