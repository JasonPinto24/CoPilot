# Standard Operating Procedure (SOP) for API Rate Limits Management at Northwind Systems

## Overview

API rate limits are essential to ensure that our services remain robust and performant, while also preventing abuse. This SOP outlines the procedures for managing API rate limits within the Northwind Systems environment. The primary goal is to prevent excessive requests from causing service degradation or outages.

### Prerequisites

- Familiarity with the Northwind API Gateway (NAG) tool.
- Access to the NAG dashboard via `https://api-gateway.northwindsystems.com`.
- Knowledge of basic network and system administration skills.
- Role-based access control permissions to modify rate limit settings.

## Step-by-Step Instructions

### 1. Log in to the API Gateway Dashboard
- Navigate to the URL: `https://api-gateway.northwindsystems.com`.
- Use your Northwind Systems credentials to log in.

### 2. Identify the Target Service
- From the NAG dashboard, locate and select the specific service for which you need to manage rate limits.
- Example: For a service named "Customer Portal," click on its corresponding tile or search for it using the search bar.

### 3. Access Rate Limit Settings
- Click on the "Settings" tab of the selected service.
- Within this tab, find and select the "Rate Limits" sub-tab.

### 4. Define Rate Limit Rules
#### Example Scenario: Setting a Rate Limit for "Customer Portal"
1. **Define Request Thresholds**:
    - Set a maximum number of requests per minute (e.g., 500).
    - Define a burst allowance to allow some flexibility in request spikes (e.g., 200).

2. **Apply Filters**:
    - Add filters based on IP address, user agent, or other relevant criteria.
    - Example: Filter by user agent to differentiate between different client types.

3. **Set Action Upon Exceeding Limits**:
    - Choose the action that should be taken when a rate limit is exceeded (e.g., log the event, throttle requests).

### 5. Save and Test
- After defining the rules, click "Save" to apply them.
- Perform a test by making a series of requests within the defined limits and verify that they are handled as expected.
- Example: Use Postman or cURL commands with appropriate headers and payloads.

### 6. Document Changes for Future Reference
- Record the changes made in the rate limit settings, including timestamps and reasons for the change.
- Maintain these records in a dedicated documentation repository within GitLab.

## Troubleshooting

### Issue: Requests Exceeding Rate Limits Not Being Handled Correctly
1. **Check Filters**:
    - Ensure that all necessary filters are correctly applied and not conflicting with each other.
2. **Review Action Settings**:
    - Verify the action settings to ensure they are configured as intended.
3. **Examine Logs**:
    - Check NAG logs for any unexpected behavior or errors related to rate limits.
4. **Contact Support Team**
    - If issues persist, contact the Northwind Systems DevOps support team at `devops-support@northwindsystems.com` for further assistance.

### Issue: Rate Limit Changes Not Reflecting in Real-Time
1. **Verify Save Action**:
    - Ensure that you have saved the changes before testing.
2. **Clear Cache or Browsers**:
    - Clear any cached data from your browser or API client tools.
3. **Restart NAG Service (if necessary)**:
    - In rare cases, a service restart may be required to apply rate limit changes.

## Conclusion

By following this SOP, you can effectively manage API rate limits for Northwind Systems services, ensuring optimal performance and security. Regularly reviewing and adjusting these settings will help maintain the reliability of our applications and protect against potential abuse.