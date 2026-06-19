# Kubernetes-Pods Standard Operating Procedure (SOP)

## Overview

Kubernetes-pods are the smallest deployable units of computing that can be created and managed in Kubernetes. Pods are typically used for grouping together application containers which need to share resources, such as storage or network. This SOP provides detailed instructions on how to manage pods within the Northwind Systems' Kubernetes cluster.

## Prerequisites

Before proceeding with this procedure, ensure you have:

- **Access to the Kubernetes Cluster**: Utilize your access credentials from the Northwind IT Services internal portal.
- **kubectl Installed and Configured**: Ensure `kubectl` is installed and configured correctly. The Northwind Systems Kubernetes cluster can be accessed via the following URL: `https://k8s-northwind-systems.cloud`.
- **Kubernetes Dashboard Access**: You should have an account with the Northwind IT Services Kubernetes Dashboard, available at `https://dashboard.k8s-northwind-systems.cloud`.

## Step-by-Step Instructions

### 1. Creating a Pod

**Objective:** To create a simple pod that runs a containerized application.

#### 1.1 Create a Deployment YAML File
Create a file named `webapp-deployment.yaml` with the following content:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: webapp
  template:
    metadata:
      labels:
        app: webapp
    spec:
      containers:
      - name: webapp
        image: nginx:latest
        ports:
        - containerPort: 80
```

#### 1.2 Apply the Deployment Using `kubectl`
Open a terminal and apply the deployment:

```bash
kubectl apply -f webapp-deployment.yaml
```

### 2. Managing Pods

**Objective:** To manage pods, including scaling up or down, and viewing pod logs.

#### 2.1 Scale Up the Deployment
Scale the deployment to run more replicas of the pod:

```bash
kubectl scale deployment/webapp --replicas=5
```

#### 2.2 Check Pod Status Using `kubectl`
Check the status of your pods using the following command:

```bash
kubectl get pods -o wide
```

This will provide a list of all pods along with their IP addresses and node names.

#### 2.3 View Pod Logs
View logs from one of the pods:

```bash
kubectl logs <pod-name> -n default
```

Replace `<pod-name>` with the actual name of your pod, e.g., `webapp-68f74b5c9b-5s78p`.

### 3. Deleting a Pod

**Objective:** To delete a specific pod.

#### 3.1 Delete a Pod
To delete a specific pod:

```bash
kubectl delete pod <pod-name> -n default
```

Replace `<pod-name>` with the name of the pod you wish to delete.

## Troubleshooting

### Issue: Pod Not Starting

**Symptom:** A pod does not start and remains in `ContainerCreating` state.

**Solution:** Check the pod logs for detailed error messages:

```bash
kubectl logs <pod-name> -n default
```

If it indicates an image pull issue, ensure the correct Docker image is available in your registry.

### Issue: Pod Failing to Scale

**Symptom:** The deployment does not scale as expected when using `kubectl scale`.

**Solution:** Verify that you have applied the correct scaling command and check if there are any resource constraints on the nodes:

```bash
kubectl get nodes -o wide
```

Ensure sufficient resources (CPU, memory) are available.

### Issue: Pod Not Responding

**Symptom:** Services relying on a pod do not respond as expected.

**Solution:** Check the service configuration and verify that it is correctly referencing the pods. Use `kubectl describe` to get detailed information about the service:

```bash
kubectl describe svc <service-name>
```

Replace `<service-name>` with the actual name of your service.

## Contact Information

For further assistance, please contact:
- **Northwind IT Services Team**: [it-support@northwindsystems.com](mailto:it-support@northwindsystems.com)
- **Kubernetes Support Slack Channel**: #k8s-support on our internal Slack platform

This SOP is intended to provide a comprehensive guide for managing Kubernetes pods at Northwind Systems. If you encounter any issues not covered here, please seek support from the IT Services team immediately.

---

By following this SOP, employees can effectively manage Kubernetes pods and ensure smooth operations within the Northwind Systems environment.