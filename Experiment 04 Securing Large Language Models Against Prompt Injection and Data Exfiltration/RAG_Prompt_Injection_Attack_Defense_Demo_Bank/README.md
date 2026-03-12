#<<<<<<< HEAD:Experiment 04 Securing Large Language Models Against Prompt Injection and Data Exfiltration/#RAG_Prompt_Injection_Attack_Defense_Demo_Bank/README.md
# Securing a RAG System Against Prompt Injection
### Case Study – NovaTrust AI Platform

This project demonstrates how a Retrieval Augmented Generation (RAG) system can be manipulated through prompt injection and how defensive mechanisms can mitigate the attack.

The scenario is based on a fictional company called **NovaTrust**, which provides AI powered compliance assistance to financial institutions.

---

# Context

NovaTrust develops an AI platform used by banks to assist with regulatory compliance and risk analysis.

The platform integrates financial data, regulatory documentation, and internal policies to generate compliance recommendations for banking clients.

To provide accurate responses, the system relies on a **Retrieval Augmented Generation (RAG)** architecture that retrieves relevant documents before generating answers with a language model.

Because the platform processes sensitive financial and regulatory data, ensuring the security of the AI system is critical.

---

# Consultant Mission

NovaTrust hired a security consulting team to assess the robustness of its AI platform.

The mission includes:

• analyzing the AI architecture  
• identifying potential attack surfaces  
• simulating realistic adversarial attacks  
• proposing defensive strategies  

The objective is to evaluate whether the system could be manipulated by malicious inputs or compromised data sources.

---

# System Architecture

The NovaTrust platform operates through the following pipeline:

1. Banking systems send queries to the AI platform
2. A retriever searches the internal document repository
3. Retrieved documents are injected into the LLM context
4. The model generates a compliance response

This architecture allows the system to combine large language models with internal knowledge sources.

However, it also introduces new security risks.

---

# Threat Model

The security assessment identified several potential risks:

• **Prompt injection attacks** through malicious documents  
• **Sensitive information disclosure** through manipulated model outputs  
• **Data manipulation** within the document repository  

These risks correspond to the OWASP AI Top 10 risks for LLM systems.

---

# Attack Scenario – RAG Hijacking

One critical scenario identified during the assessment is a **RAG hijacking attack**.

Attack steps:

1. An attacker inserts a malicious document into the knowledge base
2. The retriever selects the document during a query
3. The malicious instructions are injected into the LLM context
4. The language model produces a manipulated response

This attack exploits the **retrieval pipeline rather than the language model itself**.

---

# Experiment

To illustrate this risk, we implemented a simplified experiment.

The experiment demonstrates:

• a minimal RAG pipeline  
• a malicious document injection  
• a compromised model response  
• a defensive filtering mechanism  

The demonstration is implemented in the notebook:
=======
# Securing a RAG System Against Prompt Injection
### Case Study – NovaTrust AI Platform

This project demonstrates how a Retrieval Augmented Generation (RAG) system can be manipulated through prompt injection and how defensive mechanisms can mitigate the attack.

The scenario is based on a fictional company called **NovaTrust**, which provides AI powered compliance assistance to financial institutions.

---

# Context

NovaTrust develops an AI platform used by banks to assist with regulatory compliance and risk analysis.

The platform integrates financial data, regulatory documentation, and internal policies to generate compliance recommendations for banking clients.

To provide accurate responses, the system relies on a **Retrieval Augmented Generation (RAG)** architecture that retrieves relevant documents before generating answers with a language model.

Because the platform processes sensitive financial and regulatory data, ensuring the security of the AI system is critical.

---

# Consultant Mission

NovaTrust hired a security consulting team to assess the robustness of its AI platform.

The mission includes:

• analyzing the AI architecture  
• identifying potential attack surfaces  
• simulating realistic adversarial attacks  
• proposing defensive strategies  

The objective is to evaluate whether the system could be manipulated by malicious inputs or compromised data sources.

---

# System Architecture

The NovaTrust platform operates through the following pipeline:

1. Banking systems send queries to the AI platform
2. A retriever searches the internal document repository
3. Retrieved documents are injected into the LLM context
4. The model generates a compliance response

This architecture allows the system to combine large language models with internal knowledge sources.

However, it also introduces new security risks.

---

# Threat Model

The security assessment identified several potential risks:

• **Prompt injection attacks** through malicious documents  
• **Sensitive information disclosure** through manipulated model outputs  
• **Data manipulation** within the document repository  

These risks correspond to the OWASP AI Top 10 risks for LLM systems.

---

# Attack Scenario – RAG Hijacking

One critical scenario identified during the assessment is a **RAG hijacking attack**.

Attack steps:

1. An attacker inserts a malicious document into the knowledge base
2. The retriever selects the document during a query
3. The malicious instructions are injected into the LLM context
4. The language model produces a manipulated response

This attack exploits the **retrieval pipeline rather than the language model itself**.

---

# Experiment

To illustrate this risk, we implemented a simplified experiment.

The experiment demonstrates:

• a minimal RAG pipeline  
• a malicious document injection  
• a compromised model response  
• a defensive filtering mechanism  

The demonstration is implemented in the notebook:
>>>>>>> 2b304e47e51b6a7418b627a71a641130530df8ef:Experiment 04 Securing Large Language Models Against Prompt Injection and Data Exfiltration/12_RAG_Prompt_Injection_Attack_Defense_Demo/README.md
