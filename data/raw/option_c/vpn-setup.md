# Standard Operating Procedure (SOP) for Setting Up a Virtual Private Network (VPN)

## Overview

Northwind Systems uses FortiClient, a secure and reliable software solution provided by Fortinet to facilitate remote access to our network. This SOP provides detailed instructions on setting up a FortiClient VPN connection for employees who need to work remotely or from external locations.

## Prerequisites

Before you begin the setup process:

1. **Hardware**: Ensure that your device meets the minimum system requirements for running FortiClient.
2. **Internet Connection**: A stable internet connection is required to establish and maintain the secure connection.
3. **Northwind Systems Account**: You must have an active employee account with valid credentials.
4. **Company Email Address**: This will be used as a secondary authentication factor if enabled.

## Step-by-Step Instructions

### 1. Download and Install FortiClient

1. Visit the official Northwind Systems download page: <https://www.northwindsystems.com/downloads>
2. Select "FortiClient" from the list of available tools.
3. Choose the appropriate version for your operating system (Windows, macOS, or Linux).
4. Click on the "Download Now" button and follow the prompts to install FortiClient.

### 2. Launch FortiClient

1. Open the application from your desktop shortcut or search for it in your start menu.
2. Enter your Northwind Systems username and password when prompted.
3. If two-factor authentication is enabled, you will be asked to enter a code sent to your company email address.

### 3. Configure Your Connection Settings

1. Once logged into FortiClient, click on the **Settings** icon in the top right corner.
2. Navigate to the **General** tab and ensure that "Always connect" is selected for remote access.
3. Go to the **Advanced** tab:
   - In the **Local IP Address** field, enter your internal IP address or a valid network range if you are on an internal network (e.g., 192.168.0.0/24).
   - In the **Remote Gateway** field, input `vpn.northwindsystems.com`.
4. Click **Save** to apply your changes.

### 4. Connect to the Network

1. Go back to the main FortiClient window.
2. Click on the **Connect** button to initiate the connection process.
3. If prompted, enter your Northwind Systems username and password again.
4. Once connected, you should see a green checkmark next to the network icon in your system tray.

## Troubleshooting

### Connection Issues

1. **Check Your Internet**: Ensure that your internet connection is stable.
2. **Verify Credentials**: Double-check that you have entered the correct username and password.
3. **Network Configuration**: Make sure your local IP address and remote gateway settings are correctly configured.
4. **Restart FortiClient**: Close the application, wait for 10 seconds, and then launch it again.

### Security Alerts

1. **Two-Factor Authentication Prompt**: If you receive a prompt asking to enter a code from your company email:
   - Check your company email for the authentication code.
   - Enter the correct code in the FortiClient interface.
2. **Firewall or Antivirus Interference**: Some security software may block FortiClient connections. Disable your firewall temporarily and try reconnecting.

### Performance Issues

1. **Optimize Network Settings**: If you experience slow performance:
   - Adjust your network settings to prioritize business traffic over personal activities.
   - Use a wired connection instead of Wi-Fi if possible.

For further assistance, contact the IT Support Team at `itsupport@northwindsystems.com` or call 555-1234 during office hours.