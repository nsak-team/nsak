-- Corporate database seed — intentionally contains sensitive data for Blue team detection exercises

CREATE TABLE IF NOT EXISTS employees (
    id       INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50)  NOT NULL,
    password VARCHAR(100) NOT NULL COMMENT 'plaintext — intentional misconfiguration',
    email    VARCHAR(100),
    role     VARCHAR(50)
);

INSERT INTO employees (username, password, email, role) VALUES
    ('alice',  'alice123',   'alice@corp.local',   'developer'),
    ('bob',    'Password1',  'bob@corp.local',     'admin'),
    ('svcweb', 'webservice!','svcweb@corp.local',  'service');

CREATE TABLE IF NOT EXISTS secrets (
    id    INT AUTO_INCREMENT PRIMARY KEY,
    name  VARCHAR(100),
    value TEXT
);

INSERT INTO secrets (name, value) VALUES
    ('vpn_psk',        's3cr3t_vpn_key_2024'),
    ('api_key_prod',   'prod-api-AAAABBBBCCCCDDDD'),
    ('backup_passphrase', 'BackupPass!2024');

GRANT ALL PRIVILEGES ON corpdb.* TO 'appuser'@'%';
FLUSH PRIVILEGES;
