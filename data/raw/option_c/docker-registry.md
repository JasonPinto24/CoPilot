# Standard Operating Procedure (SOP) for Docker Registry Management at Northwind Systems

## Overview

The Docker Registry SOP outlines the procedures for managing and operating the Docker registry within our IT infrastructure. This procedure ensures that all Docker images are stored, managed, and distributed securely and efficiently across various development environments. The primary objectives include ensuring data integrity, compliance with security standards, and facilitating seamless deployment processes.

## Prerequisites

Before proceeding with any Docker registry operations, ensure you have the following:

1. **Access**: Members of the DevOps team should be granted access to the internal Docker Registry.
2. **Tools**: Familiarity with Docker CLI (`docker`), GitLab CI/CD pipeline (if applicable), and the Docker registry interface at `https://registry.northwindsys.com`.
3. **Knowledge**: Basic understanding of Docker image tagging, pushing, and pulling processes.

## Step-by-Step Instructions

### 1. Logging into the Docker Registry

To access the Docker registry, use the following URL: `https://registry.northwindsys.com`.

**Login Credentials:**
- Username: `devops@northwindsys.com`
- Password: Provided by IT Security Team (change frequently)

**Command to Log in:**
```sh
docker login -u devops@northwindsys.com https://registry.northwindsys.com
```

### 2. Tagging and Pushing Images

#### Step 1: Build the Docker Image
Assuming you have a `Dockerfile` located at `/path/to/dockerfile`, run:
```sh
docker build -t myapp:v1 /path/to/dockerfile
```

#### Step 2: Tag the Image for Registry
Tag the image to match the repository and tag on the registry:
```sh
docker tag myapp:v1 https://registry.northwindsys.com/myapp:v1
```

#### Step 3: Push the Image to the Registry
Push the tagged image to the Docker registry:
```sh
docker push https://registry.northwindsys.com/myapp:v1
```

### 3. Pulling Images from the Registry

To pull an image from the registry, use the following command:
```sh
docker pull https://registry.northwindsys.com/myapp:v1
```

## Troubleshooting Common Issues

### Issue: Authentication Failed

**Symptom**: When attempting to push or pull images, you receive an authentication error.

**Resolution Steps:**
1. Verify your login credentials are correct.
2. Check if the Docker registry URL is accurate.
3. Ensure your access permissions have not been revoked.
4. Run `docker logout` and then try logging in again:
   ```sh
   docker logout https://registry.northwindsys.com
   ```

### Issue: Image Not Found

**Symptom**: When pulling an image, you receive a message indicating the image was not found.

**Resolution Steps:**
1. Double-check the repository name and tag.
2. Ensure the image has been pushed to the registry correctly.
3. If using GitLab CI/CD, verify that the job is configured to push images to the correct registry URL.

### Issue: Image Tagging Error

**Symptom**: The `docker tag` command fails with an error message.

**Resolution Steps:**
1. Ensure you have the necessary permissions to tag and push images.
2. Verify the format of your image name and tag.
3. Run `docker images` to confirm that the original image exists locally.

### Issue: Network Connectivity Issues

**Symptom**: Unable to access the Docker registry due to network issues.

**Resolution Steps:**
1. Check if the network is functioning correctly (ping the URL).
2. Ensure firewall rules are not blocking traffic.
3. Contact IT Support for further assistance with networking issues.

## Conclusion

By following this SOP, you can effectively manage and utilize the Docker registry within Northwind Systems. Regularly reviewing and updating your procedures will help maintain a secure and efficient workflow.

For any questions or further support, please contact the DevOps team at `devops@northwindsys.com`.

--- 

*Last Updated: 15th October 2023*