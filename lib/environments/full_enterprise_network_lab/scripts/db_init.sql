-- db_init.sql — MariaDB bootstrap for enterprise-network-lab2
-- Database: appdb
-- Recon findings: table names visible via information_schema
--                 appuser can SELECT on appdb.*
--                 Schema reveals application structure

USE appdb;

-- ── Web application users ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    username      VARCHAR(64) NOT NULL UNIQUE,
    email         VARCHAR(128) NOT NULL,
    password_hash VARCHAR(255) NOT NULL COMMENT 'bcrypt hash',
    role          ENUM('admin','staff','readonly') DEFAULT 'staff',
    department    VARCHAR(64),
    last_login    DATETIME,
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    active        TINYINT(1) DEFAULT 1
);

INSERT INTO users (username, email, password_hash, role, department, last_login) VALUES
    ('jsmith',      'jsmith@lab.local',     '$2y$10$examplehash1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'staff',    'Finance',  '2024-03-15 08:22:11'),
    ('bjones',      'bjones@lab.local',     '$2y$10$examplehash2xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'admin',    'IT',       '2024-03-15 09:01:44'),
    ('mwilson',     'mwilson@lab.local',    '$2y$10$examplehash3xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'staff',    'HR',       '2024-03-14 17:55:03'),
    ('dtaylor',     'dtaylor@lab.local',    '$2y$10$examplehash4xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'admin',    'IT',       '2024-03-15 07:48:32'),
    ('svc_web',     'svc_web@lab.local',    '$2y$10$examplehash5xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'readonly', 'Service',  '2024-03-15 00:00:01'),
    ('svc_backup',  'svc_backup@lab.local', '$2y$10$examplehash6xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'readonly', 'Service',  '2024-03-15 03:00:01');

-- ── Application config (reveals infrastructure) ───────────────────────────────
CREATE TABLE IF NOT EXISTS app_config (
    key_name  VARCHAR(128) PRIMARY KEY,
    value     TEXT,
    updated   DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO app_config (key_name, value) VALUES
    ('smtp_host',       'mail.lab.local'),
    ('smtp_port',       '25'),
    ('smtp_from',       'app@acmecorp.lab.local'),
    ('ldap_host',       'dc01.lab.local'),
    ('ldap_base_dn',    'DC=lab,DC=local'),
    ('ldap_bind_user',  'svc_web'),
    ('ad_domain',       'LAB.LOCAL'),
    ('file_server',     '\\\\FILESERVER\\public'),
    ('backup_target',   '\\\\FILESERVER\\backup'),
    ('app_version',     '1.3.2'),
    ('environment',     'production');

-- ── Audit log ─────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS audit_log (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    timestamp  DATETIME DEFAULT CURRENT_TIMESTAMP,
    username   VARCHAR(64),
    action     VARCHAR(128),
    source_ip  VARCHAR(45),
    details    TEXT
);

INSERT INTO audit_log (username, action, source_ip, details) VALUES
    ('bjones',   'USER_LOGIN',        '192.168.10.101', 'Login from ws2.lab.local'),
    ('jsmith',   'USER_LOGIN',        '192.168.10.100', 'Login from ws1.lab.local'),
    ('svc_web',  'SERVICE_AUTH',      '172.16.1.10',    'Web app authenticated'),
    ('bjones',   'CONFIG_CHANGE',     '192.168.10.101', 'Updated smtp_host'),
    ('dtaylor',  'USER_CREATED',      '192.168.10.101', 'Created user svc_monitor'),
    ('svc_backup','BACKUP_COMPLETED', '192.168.10.20',  'Full backup to FILESERVER\\backup');

-- ── Sessions ──────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS sessions (
    session_id VARCHAR(128) PRIMARY KEY,
    username   VARCHAR(64),
    created    DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires    DATETIME,
    ip_address VARCHAR(45)
);

-- ── Grant appuser read access ─────────────────────────────────────────────────
GRANT SELECT, INSERT, UPDATE ON appdb.* TO 'appuser'@'%';
GRANT SELECT ON appdb.users TO 'appuser'@'%';

-- Allow web server (172.16.1.10) to connect
GRANT SELECT, INSERT, UPDATE ON appdb.* TO 'appuser'@'172.16.1.10' IDENTIFIED BY 'apppass';

FLUSH PRIVILEGES;
