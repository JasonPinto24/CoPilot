# LDAP Setup Standard Operating Procedure (SOP) for Northwind Systems

## Overview

This SOP outlines the process to set up and configure an LDAP server for Northwind Systems, ensuring secure and efficient user authentication. The LDAP setup is critical for maintaining a unified identity management system across various applications and services within our organization.

### Prerequisites

- **Hardware Requirements:**
  - A dedicated server or virtual machine (VM) with sufficient resources.
  - Network connectivity to the internal Northwind network.

- **Software Requirements:**
  - OpenLDAP Server
  - LDAP Admin Tool (e.g., LDAP Browser)
  - Certificate Signing Request (CSR) and SSL/TLS certificates for secure communication.

- **Team Members Involved:**
  - IT Infrastructure Team
  - Security Team

### Step-by-Step Instructions

#### 1. Prepare the Environment

1. **Install OpenLDAP Server:**
   ```sh
   sudo apt update
   sudo apt install slapd ldap-utils
   ```

2. **Configure LDAP Database:**
   - Run `slapd` to start the server and follow the prompts:
     ```sh
     sudo dpkg-reconfigure slapd
     ```
   - Set up the domain name, organizational units (OUs), and ensure a strong root password is set.

3. **Install LDAP Admin Tool:**
   - Download and install `LDAP Browser` from its official website or repository.
   - Configure it to connect to the local LDAP server using the root DSE (Distinguished System Entry).

#### 2. Set Up User Accounts

1. **Create an Organizational Unit (OU):**
   ```sh
   ldapadd -x -W -D "cn=admin,dc=northwind,dc=com" -f ou_setup.ldif
   ```
   Where `ou_setup.ldif` contains:
   ```ldif
   dn: ou=Users,dc=northwind,dc=com
   objectClass: organizationalUnit
   ou: Users
   ```

2. **Add User Accounts:**
   ```sh
   ldapadd -x -W -D "cn=admin,dc=northwind,dc=com" -f user_add.ldif
   ```
   Where `user_add.ldif` contains:
   ```ldif
   dn: cn=John Doe,ou=Users,dc=northwind,dc=com
   objectClass: inetOrgPerson
   objectClass: person
   cn: John Doe
   sn: Doe
   uid: jdoe
   userPassword: {SSHA}password_hash
   ```

#### 3. Configure SSL/TLS Certificates

1. **Generate CSR:**
   ```sh
   openssl req -newkey rsa:2048 -nodes -keyout key.pem -out csr.csr
   ```

2. **Request and Install SSL/TLS Certificate:**
   - Submit `csr.csr` to your certificate authority.
   - After receiving the certificate, install it on the server:
     ```sh
     sudo cp cert.crt /etc/ssl/certs/
     sudo cp key.pem /etc/ssl/private/
     ```

3. **Update LDAP Server Configuration:**
   - Edit `/etc/ldap/slapd.d/cn=config.ldif` to enable TLS and specify the certificate paths:
     ```sh
     tls_certfile /etc/ssl/certs/cert.crt
     tls_keyfile /etc/ssl/private/key.pem
     ```

4. **Restart LDAP Service:**
   ```sh
   sudo systemctl restart slapd
   ```

#### 4. Test LDAP Configuration

1. **Verify User Accounts:**
   - Use `ldapsearch` to verify user accounts are correctly added:
     ```sh
     ldapsearch -x -LLL -b "ou=Users,dc=northwind,dc=com" -D "cn=admin,dc=northwind,dc=com"
     ```

2. **Test Authentication:**
   - Use the LDAP Admin Tool to bind as a user and test authentication.

### Troubleshooting

1. **Connection Issues:**
   - Ensure network connectivity between the client and server.
   - Check firewall rules to allow LDAP traffic (default port 389).

2. **Configuration Errors:**
   - Verify all configuration files (`ou_setup.ldif`, `user_add.ldif`, `/etc/ldap/slapd.d/cn=config.ldif`) for syntax errors.
   - Use `slaptest` to check the slapd configuration:
     ```sh
     sudo slaptest -f /etc/ldap/slapd.conf -F /etc/ldap/slapd.d/
     ```

3. **User Authentication Issues:**
   - Ensure user passwords are correctly hashed and stored.
   - Check for any permissions issues in LDAP.

4. **SSL/TLS Certificate Errors:**
   - Verify the certificate is properly installed and accessible.
   - Check for common SSL/TLS errors such as incorrect paths or mismatched domains.

For further assistance, contact the IT Infrastructure Team at `infrastructure@northwind.com` or the Security Team at `security@northwind.com`.

--- 

This SOP provides a comprehensive guide to setting up an LDAP server within Northwind Systems. Follow these steps carefully to ensure a secure and efficient identity management system.