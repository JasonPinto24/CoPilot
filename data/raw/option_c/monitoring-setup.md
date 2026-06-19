# Monitoring Setup SOP for Northwind Systems

## Overview

The Monitoring Setup SOP outlines the process of configuring and setting up monitoring tools to ensure the health, performance, and availability of Northwind Systems' IT infrastructure. This procedure is crucial for maintaining operational efficiency and ensuring timely response to any issues that may arise.

## Prerequisites

Before proceeding with the setup, ensure you have the following:

- Access to the Northwind Systems internal network
- Administrator-level access to the monitoring tools and systems
- A list of critical services and applications to monitor
- Necessary credentials for creating new alerts and configuring notifications

## Step-by-Step Instructions

### Step 1: Access the Monitoring Tool

1. **Log in**: Use your credentials to log into the [Northwind IT Monitoring Portal](https://itmonitoring.northwindsystems.com/login).
2. **Navigate to Setup Section**: Once logged in, go to the "Monitoring Setup" section.

### Step 2: Define Critical Services and Applications

1. **Create Service Catalog**: In the monitoring tool, create a new service catalog by clicking on "Service Management" > "Add New Service".
2. **Input Details**: For each critical application or service:
   - **Name**: Enter the name of the service (e.g., `Web Server`).
   - **Description**: Provide a brief description.
   - **Criticality Level**: Assign a level from 1 to 5 based on its importance.

### Step 3: Set Up Monitoring Rules

1. **Select Service for Monitoring**: From the service catalog, select the service you wish to monitor.
2. **Configure Monitoring Rules**:
   - **Performance Metrics**: Define performance thresholds (e.g., CPU usage > 80%).
   - **Alerting Conditions**: Set up conditions under which an alert should be triggered (e.g., disk space < 10 GB).

### Step 4: Configure Notifications

1. **Set Up Notification Channels**:
   - Go to "Notification Management" > "Add New Channel".
   - Choose a channel type such as email, SMS, or webhook.
2. **Define Recipients**: For each service and alert condition, define the recipients who will receive notifications (e.g., `it-support@northwindsystems.com`).

### Step 5: Validate Setup

1. **Test Alerting**:
   - Trigger a test alert by manually failing over or performing an action that should trigger the alert.
   - Verify that notifications are sent to the correct recipients.
2. **Review Logs**: Check the monitoring tool's logs for any errors or issues during setup.

### Step 6: Document and Review

1. **Document Setup Details**: Record all steps taken, including service names, criticality levels, thresholds, and notification details.
2. **Review with Team Lead**: Ensure that all configurations meet the requirements and are reviewed by your team lead for approval.

## Troubleshooting

### Common Issues and Solutions

**Issue 1: Failed Alert Triggers**

- **Symptom**: Alerts do not trigger as expected.
- **Solution**: 
  - Verify that the monitoring rules and conditions are correctly set up.
  - Check if any dependencies (e.g., network connectivity) are causing issues.

**Issue 2: Missing Notifications**

- **Symptom**: Notified parties do not receive alerts.
- **Solution**: 
  - Ensure that the notification channels are properly configured and tested.
  - Verify email server configurations or check for firewall rules blocking outbound traffic.

### Contact Information

For further assistance, contact:

- IT Support Team: `it-support@northwindsystems.com`
- Helpdesk: `+1 (555) 123-4567`

## Conclusion

Following this SOP will ensure that Northwind Systems' monitoring setup is robust and effective. Regular reviews and updates to the monitoring configuration are crucial for maintaining system health and performance.

--- 

This document provides a detailed procedure for setting up monitoring tools within Northwind Systems, ensuring all necessary steps are covered from initial access to final validation and documentation.