# Postmortem Template Standard Operating Procedure (SOP)

## Overview

A postmortem is an essential tool for understanding, documenting, and learning from system failures or incidents. At Northwind Systems, we use a standardized template to ensure that all technical issues are thoroughly documented and lessons learned are shared across the organization. This document outlines the steps for creating a postmortem report.

## Prerequisites

- **Tool**: Jira is used as the project management tool for tracking postmortems.
- **Team**: The incident response team, consisting of IT Operations, Systems Engineers, and Network Administrators, will be responsible for conducting postmortems.
- **Access**: Ensure you have access to the relevant systems and logs. If not, contact the appropriate team or support channels.

## Step-by-Step Instructions

### 1. Incident Identification
- **Identify the Incident**: Note the time of occurrence, affected services, and any critical issues observed.
- **Document Key Details**:
  - Time: 2023-10-15 at 14:30 UTC
  - Service Affected: Web Application (www.northwindsystems.com)
  - Symptoms: Slow response times, application errors

### 2. Gather Information
- **Collect Logs**: Use Splunk to gather logs from relevant services.
  - Example URL: `https://logs.splunk.northwindsystems.com`
- **Contact Affected Users**: If the incident impacted end-users, reach out to them for feedback.
  - Email: support@northwindsystems.com

### 3. Root Cause Analysis
- **Analyze Logs and Metrics**:
  - Review logs from Splunk for signs of the issue.
    ```plaintext
    # Example Log Entry
    [2023-10-15 14:30:00] ERROR: /api/v1/orders: Database connection failed
    ```
  - Check Prometheus metrics for unusual spikes or anomalies.

### 4. Impact Assessment
- **Quantify the Impact**:
  - Number of users affected: 2,345
  - Duration of downtime: 2 hours and 15 minutes

### 5. Mitigation Steps Taken
- **Immediate Actions**: What steps were taken to mitigate the issue during the incident.
  - Restarted web application servers at 14:45 UTC
  - Switched to a backup server at 15:00 UTC

### 6. Long-term Mitigation
- **Preventive Measures**: Steps that can be implemented to prevent future occurrences.
  - Added database connection retry logic
  - Enhanced monitoring for database health

### 7. Lessons Learned
- **Document Improvements**:
  - Improved log rotation policies
  - Enhanced communication channels with end-users
  - Increased redundancy in the web application infrastructure

### 8. Next Steps
- **Action Items**: Define next steps and assign responsibilities.
  - Task: Update database connection scripts (Assigned to DevOps Team)
  - Task: Implement improved monitoring tools (Assigned to Network Admins)

## Troubleshooting

### Common Issues
- **Inconsistent Log Entries**:
  - Ensure all systems are logging consistently. Use a unified logging standard like ELK Stack.
- **Failed to Identify Root Cause**:
  - Revisit the timeline of events and cross-reference with other teams (e.g., Security, Network).

### Contact Information
- **Support Team**: support@northwindsystems.com
- **IT Operations Lead**: itops_lead@northwindsystems.com

## Conclusion

Following this SOP will help ensure that postmortems are conducted efficiently and effectively. Regular reviews of the process can further improve its effectiveness.

---

This document is a living document; please update as necessary based on feedback from your team members.