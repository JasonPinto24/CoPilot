# Kafka Troubleshooting SOP for Northwind Systems

## Overview

This Standard Operating Procedure (SOP) provides detailed steps and best practices for troubleshooting issues related to Apache Kafka in our environment. The aim is to ensure that system administrators, developers, and operations teams can effectively diagnose and resolve issues quickly.

### Prerequisites

- **Kafka Version**: 3.0.2
- **Operating System**: CentOS 8.x
- **Northwind Systems Tools**:
  - Kafdrop (v1.7.0) for visualizing Kafka topics and messages.
  - Confluent Control Center (v5.6.1) for monitoring, managing, and troubleshooting clusters.
  - Kafka Manager (v2.3.4) for topic management.

### Step-by-Step Instructions

#### 1. Initial Assessment
   - **Check Service Status**: Ensure that the Kafka broker service is running by using `systemctl`:
     ```bash
     sudo systemctl status kafka-broker.service
     ```
   - **Review Logs**: Check the Kafka logs for any error messages or warnings. Logs can be found at `/var/log/kafka/`.

#### 2. Verify Configuration
   - **Check Configurations**: Ensure that the Kafka configuration files (`server.properties`, `zookeeper.connect`) are correctly set up and do not contain syntax errors.
     ```bash
     sudo cat /etc/kafka/server.properties | grep -i "bootstrap"
     ```

#### 3. Monitor Cluster Health
   - **Use Confluent Control Center**: Navigate to the Confluent Control Center URL (`https://control-center.northwindsystems.local:8443`) and check the Kafka cluster health, including:
     - Broker status
     - Topic replication factors
     - Message throughput

#### 4. Examine Topic Performance
   - **Topic Details**: Use `kafka-topics.sh` to list all topics and their details:
     ```bash
     kafka-topics.sh --describe --topic <topic-name> --zookeeper localhost:2181
     ```
   - **Message Rate**: Monitor message rates using Kafdrop URL (`http://localhost:9000`). Look for any anomalies or sudden drops in throughput.

#### 5. Inspect Consumer Groups
   - **Consumer Group Info**: Use the `kafka-consumer-groups.sh` script to check consumer group offsets and lag:
     ```bash
     kafka-consumer-groups.sh --describe --group <consumer-group-name> --zookeeper localhost:2181
     ```

#### 6. Analyze Network Traffic
   - **Network Tools**: Use `netstat`, `iftop`, or `nethogs` to inspect network traffic between Kafka brokers and other services:
     ```bash
     sudo netstat -tnp | grep kafka
     ```

### Troubleshooting

#### Common Issues and Solutions

1. **Broker Unreachable**
   - **Issue**: A broker is not responding.
   - **Solution**: Check the broker logs for any errors, ensure Zookeeper connection settings are correct, and restart the broker if necessary.

2. **Topic Replication Issues**
   - **Issue**: Topics have insufficient replication factor or leader election failures.
   - **Solution**: Adjust the `replica.fetch.max.bytes` and `num.partitions` parameters in `server.properties`. Use Confluent Control Center to rebalance partitions manually.

3. **Message Delays**
   - **Issue**: Messages are taking longer than expected to process.
   - **Solution**: Increase the `message.timeout.ms`, `request.timeout.ms`, and `batch.num.messages` settings. Ensure that consumer group offsets are being committed properly.

4. **Consumer Lag**
   - **Issue**: Consumers lag behind producers, indicating potential performance bottlenecks.
   - **Solution**: Optimize consumer configurations such as `fetch.min.bytes`, `max.poll.interval.ms`. Increase the number of consumer instances if necessary.

5. **Resource Limitations**
   - **Issue**: Out-of-memory (OOM) errors or high CPU usage.
   - **Solution**: Monitor resource utilization using tools like `top` and `htop`. Adjust Kafka configurations to allocate more memory (`log.retention.bytes`, `log.flush.interval.messages`) and optimize broker settings.

### Contact Information

For further assistance, please contact the IT Helpdesk at:
- Email: support@northwindsystems.com
- Phone: +1 (555) 1234-5678

--- 

This SOP is intended to serve as a comprehensive guide for troubleshooting Kafka issues within Northwind Systems. Regular updates and reviews should be conducted to ensure the document remains relevant and effective.