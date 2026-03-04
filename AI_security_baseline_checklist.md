AI Security Baseline Checklist
1. Secure the training data
•	Validate data sources and control who can contribute data
•	Scan datasets for poisoning attempts and anomalies
•	Keep dataset lineage and versioning to detect tampering
•	Apply access control to raw datasets and feature stores

2. Protect the model itself
•	Store models in signed and integrity checked registries
•	Restrict download and modification permissions
•	Use model watermarking or fingerprinting to detect theft
•	Monitor for abnormal inference patterns indicating extraction attempts

3. Secure the inference pipeline
•	Validate all inputs to prevent adversarial or malformed inputs
•	Apply rate limiting and authentication on APIs
•	Log requests and responses for forensic analysis
•	Use runtime monitoring to detect output manipulation or drift

4. Defend against AI specific attacks
•	Adversarial robustness testing before deployment
•	Red teaming focused on prompt injection and jailbreak attempts
•	Detection mechanisms for model extraction or membership inference
•	Periodic re evaluation of model behavior after updates

5. Governance and lifecycle controls
•	Maintain model cards documenting risks and intended usage
•	Perform threat modeling during design phase
•	Establish rollback capability for compromised models
•	Separate development, training, and production environments

6. Monitoring and response
•	Continuous monitoring of prediction distributions and anomalies
•	Alerting for unusual usage spikes or behavior changes
•	Incident response playbooks specific to AI attacks
