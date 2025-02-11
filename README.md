**#Usage of LLM :-**
Initially, the project aimed to use a structured and annotated legal dataset for offense classification. However, we decided to transition to a Large Language Model (LLM) due to the following reasons:

Insufficient Dataset Coverage

The extracted dataset lacked comprehensive legal cases, contextual understanding, and real-world variability needed for accurate classification.
Scalability & Generalization

A dataset-based model would require continuous updates, whereas an LLM can generalize across diverse legal scenarios without retraining.
Contextual Understanding

LLMs can analyze queries in a broader legal context, considering case precedents, related sections, and nuanced interpretations that a dataset alone cannot capture.
Real-Time Adaptability

Using an LLM via Hugging Face’s API allows for on-the-fly responses, reducing dependency on static, pre-annotated datasets.
Faster Development & Deployment

Training a custom legal model would require significant time and computational resources, whereas integrating an LLM ensures quick and efficient deployment.
By leveraging an LLM, LawAssist provides dynamic, scalable, and accurate legal query responses without the limitations of a pre-existing dataset. 🚀
