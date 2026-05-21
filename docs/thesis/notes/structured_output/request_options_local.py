options = {
    "method": "post",
    "url": "/v1/messages",
    "files": None,
    "idempotency_key": "stainless-python-retry-88bf09e5-d95e-43a9-b7d4-c8b7d5818356",
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
        "system": "\n    You are in a cybersecurity simulation and act as the purple team.\n\n    Tool calling rules:\n    - Working directory: /home/lukas/CLionProjects/swiss-army-knife-network-sniffer/run/work_paths/2026-05-21-13:03:09\n    - Only send emails if requested\n    ",
        "temperature": 0.0,
        "tool_choice": {"type": "any"},
        "tools": [
            {
                "name": "cli_tool",
                "input_schema": {
                    "properties": {
                        "command": {"type": "string"},
                        "timeout": {"default": 120, "type": "integer"},
                    },
                    "required": ["command"],
                    "type": "object",
                },
                "description": 'Run an arbitrary CLI command and return its output.\n\nUse nmap for network scanning, e.g.:\n- "nmap -sV 10.10.10.1" (service version detection)\n- "nmap -sC -sV -oN output.txt 10.10.10.1" (default scripts + versions)\n- "nmap -p 1-1000 10.10.10.1" (port range)\n\nUse `apt install` if a cli tool is missing.\n\nArgs:\n    command: Full CLI command string to execute.\n    timeout: Max seconds to wait (default 120, increase for large scans).\n\nReturns\n-------\n    Tuple of (exit_code, stdout, stderr).\n    Exit code 0 means success. Check stderr on failure.',
            },
            {
                "name": "host_configuration",
                "input_schema": {"properties": {}, "type": "object"},
                "description": 'Returns the host network configuration as a dictionary.\n\nUse this tool first to understand the local network setup before running any scans or attacks.\n\nThe returned dictionary has the following structure:\n{\n    "debug": bool,\n    "device": {\n        "id": str,\n        "name": str,\n        "description": str,\n        "configuration": {\n            "network": {\n                "ethernets": {\n                    "<interface_name>": {\n                        "name": str,\n                        "is_up": bool,        # False means the interface is DOWN, skip it\n                        "is_target": bool,    # True means this interface is used for attacks/scans\n                        "is_management": bool # True means this interface is used for device access\n                        "addresses": {\n                            "<cidr>": {\n                                "ip": str,        # e.g. "10.10.10.5/24" - use this as nmap source IP\n                                "is_target": bool,\n                                "is_management": bool,\n                            }\n                        },\n                    }\n                }\n            }\n        }\n    }\n}\n\nGuidance:\n- Use `is_target=True` interfaces/IPs when running nmap scans or attacks\n- Skip interfaces where `is_up=False`\n- Use `is_management=True` interfaces for device access or data extraction\n- `configuration` may be None if the device has not been configured yet',
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
                    "required": ["subject", "message"],
                    "type": "object",
                },
                "description": "Send an email notification to the configured receiver.\n\nUse this tool to alert the human operator about findings, incidents, or\ncompleted tasks that require their attention outside the current session.\n\nArgs:\n    subject: A short, descriptive subject line for the email, which is added to the subject prefix `NSAK - AI Agent:`.\n    message: The full body of the email.\n    cc_recipients: Optional comma seperated list of emails, which should receive a carbon copy of the email.\n    attachments: Optional list of absolute file paths to attach to the email (e.g. scan reports, captured files).",
            },
            {
                "name": "AIReconnaissanceStructuredOutputResult",
                "input_schema": {
                    "properties": {
                        "provider": {"type": "string"},
                        "model": {"type": "string"},
                        "tools_called": {
                            "additionalProperties": {
                                "items": {"type": "string"},
                                "type": "array",
                            },
                            "type": "object",
                        },
                        "prompt_tokens": {"type": "integer"},
                        "completion_tokens": {"type": "integer"},
                        "network_discovery_result_map": {
                            "properties": {
                                "results": {
                                    "additionalProperties": {
                                        "properties": {
                                            "network_interface": {
                                                "properties": {
                                                    "name": {"type": "string"},
                                                    "addresses": {
                                                        "additionalProperties": {
                                                            "properties": {
                                                                "ip": {
                                                                    "anyOf": [
                                                                        {
                                                                            "format": "ipv4interface",
                                                                            "type": "string",
                                                                        },
                                                                        {
                                                                            "format": "ipv6interface",
                                                                            "type": "string",
                                                                        },
                                                                    ]
                                                                },
                                                                "is_target": {
                                                                    "type": "boolean"
                                                                },
                                                                "is_management": {
                                                                    "type": "boolean"
                                                                },
                                                            },
                                                            "required": [
                                                                "ip",
                                                                "is_target",
                                                                "is_management",
                                                            ],
                                                            "type": "object",
                                                        },
                                                        "type": "object",
                                                    },
                                                },
                                                "required": ["name", "addresses"],
                                                "type": "object",
                                            },
                                            "network_services": {
                                                "items": {
                                                    "properties": {
                                                        "endpoints": {
                                                            "items": {
                                                                "properties": {
                                                                    "mac": {
                                                                        "anyOf": [
                                                                            {
                                                                                "type": "string"
                                                                            },
                                                                            {
                                                                                "type": "null"
                                                                            },
                                                                        ],
                                                                        "default": None,
                                                                    },
                                                                    "ip": {
                                                                        "anyOf": [
                                                                            {
                                                                                "anyOf": [
                                                                                    {
                                                                                        "format": "ipv4",
                                                                                        "type": "string",
                                                                                    },
                                                                                    {
                                                                                        "format": "ipv6",
                                                                                        "type": "string",
                                                                                    },
                                                                                ]
                                                                            },
                                                                            {
                                                                                "type": "null"
                                                                            },
                                                                        ],
                                                                        "default": None,
                                                                    },
                                                                    "port": {
                                                                        "anyOf": [
                                                                            {
                                                                                "type": "integer"
                                                                            },
                                                                            {
                                                                                "type": "null"
                                                                            },
                                                                        ],
                                                                        "default": None,
                                                                    },
                                                                    "protocol": {
                                                                        "anyOf": [
                                                                            {
                                                                                "enum": [
                                                                                    "tcp",
                                                                                    "udp",
                                                                                ],
                                                                                "type": "string",
                                                                            },
                                                                            {
                                                                                "type": "null"
                                                                            },
                                                                        ],
                                                                        "default": None,
                                                                    },
                                                                    "extra_info": {
                                                                        "anyOf": [
                                                                            {
                                                                                "type": "string"
                                                                            },
                                                                            {
                                                                                "type": "null"
                                                                            },
                                                                        ],
                                                                        "default": None,
                                                                    },
                                                                },
                                                                "type": "object",
                                                            },
                                                            "type": "array",
                                                        },
                                                        "state": {
                                                            "anyOf": [
                                                                {"type": "string"},
                                                                {"type": "null"},
                                                            ],
                                                            "default": None,
                                                        },
                                                        "name": {
                                                            "anyOf": [
                                                                {"type": "string"},
                                                                {"type": "null"},
                                                            ],
                                                            "default": None,
                                                        },
                                                        "product": {
                                                            "anyOf": [
                                                                {"type": "string"},
                                                                {"type": "null"},
                                                            ],
                                                            "default": None,
                                                        },
                                                        "version": {
                                                            "anyOf": [
                                                                {"type": "string"},
                                                                {"type": "null"},
                                                            ],
                                                            "default": None,
                                                        },
                                                        "extra_info": {
                                                            "anyOf": [
                                                                {"type": "string"},
                                                                {"type": "null"},
                                                            ],
                                                            "default": None,
                                                        },
                                                    },
                                                    "required": ["endpoints"],
                                                    "type": "object",
                                                },
                                                "type": "array",
                                            },
                                        },
                                        "required": [
                                            "network_interface",
                                            "network_services",
                                        ],
                                        "type": "object",
                                    },
                                    "type": "object",
                                }
                            },
                            "required": ["results"],
                            "type": "object",
                        },
                        "enumerate_services_result": {
                            "properties": {
                                "results": {
                                    "items": {
                                        "properties": {
                                            "ip": {"type": "string"},
                                            "port": {"type": "string"},
                                            "findings": {
                                                "items": {"type": "string"},
                                                "type": "array",
                                            },
                                        },
                                        "required": ["ip", "port", "findings"],
                                        "type": "object",
                                    },
                                    "type": "array",
                                }
                            },
                            "required": ["results"],
                            "type": "object",
                        },
                        "ai_assessment": {"type": "string"},
                    },
                    "required": [
                        "provider",
                        "model",
                        "tools_called",
                        "prompt_tokens",
                        "completion_tokens",
                        "network_discovery_result_map",
                        "enumerate_services_result",
                        "ai_assessment",
                    ],
                    "type": "object",
                },
                "description": "\nRepresents the results of the AI reconnaissance scenario with structured output.\n",
            },
        ],
    },
}
