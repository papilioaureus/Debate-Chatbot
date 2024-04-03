For Model 1, we chose DialoGPT for its strong performance in natural language generation tasks,
fine-tuning it on our dataset to adapt it to our specific needs. Additionally, we implemented 
caching and storing of data/checkpoints to enhance efficiency and facilitate easier retraining
and deployment. While DialoGPT excels in generating coherent and contextually relevant responses, its limitations 
include potential generation of generic or nonsensical responses, especially when faced with out-of-domain or ambiguous inputs.

For Model 2, we opted for Falcon, a transformer variant optimized for performance efficiency, and 
loaded a quantized model with reduced precision (4-bit parameters, 16-bit computation) to improve memory
usage and computation speed. We configured Falcon with Lora attention mechanisms to capture long-range 
dependencies effectively. Pushing the model to Hugging Face's model hub ensures its accessibility to the broader community. 
While Falcon's optimization techniques offer significant advantages in terms of resource efficiency, the reduced precision 
may lead to a trade-off in model accuracy and performance, particularly in tasks requiring fine-grained representations.

For Model 3, we utilized Gemma, a PEFT-based transformer model, and employed Lora attention mechanisms for efficient 
long-range dependency modeling. Fine-tuning with Lora further enhanced the model's representational power and flexibility.
Pushing the model to Hugging Face's model hub enables wider dissemination and usage. Gemma's utilization of PEFT techniques
offers notable improvements in training efficiency and computational cost, but potential limitations may arise from the complexity 
of configuring and fine-tuning models with multiple optimization techniques.

For Model 4, we integrated Mistral, specifically the Mistral 7B-Instruct variant, to leverage its advanced language generation
capabilities. Our implementation included fine-tuning with HuggingFace and LangChain embeddings to enhance semantic 
coherence and context sensitivity. The significant challenge we faced was determining an optimal method for saving and managing 
the model's state, debating between local storage and cloud-based platforms like Hugging Face's model hub. Efforts to streamline
model-frontend communication through a Flask server in a Colab environment were unsuccessful, highlighting the technical complexities 
in deploying large AI models and the necessity for efficient model management solutions.
