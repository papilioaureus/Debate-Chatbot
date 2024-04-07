## Important Concepts applied to our models

- Fine-tuning:
Fine-tuning refers to the process of taking a pre-trained machine learning model and further training it on a specific dataset or task. This process allows the model to adapt its parameters to better fit the nuances of the new dataset or task, thereby improving its performance on that particular task. Fine-tuning is commonly used in transfer learning scenarios, where a pre-trained model is utilized as a starting point for a new task, saving time and computational resources compared to training a model from scratch.

- PEFT-Based Transformer Model:
A PEFT-based transformer model employs the Parameter Efficient Fine-Tuning (PEFT) technique to streamline the fine-tuning process of large transformer architectures. Unlike traditional fine-tuning methods, which adjust all parameters of the model, PEFT selectively updates parameters in specific layers or attention heads, focusing on those most relevant to the task at hand. This targeted approach reduces computational costs and memory requirements while still allowing the model to adapt effectively to task-specific data. By optimizing parameter utilization and training efficiency, PEFT-based transformer models offer faster training times and improved performance on downstream tasks, making them particularly suitable for resource-constrained environments and applications requiring rapid experimentation.

- Importing quantized models:
Quantization is a technique used to reduce the memory footprint and computational requirements of machine learning models. In the context of neural networks, quantization involves reducing the precision of numerical values used to represent model parameters and computations. Importing quantized models refers to loading models that have undergone quantization, typically resulting in smaller model sizes and faster inference times. However, reduced precision may lead to a trade-off in model accuracy and performance.

- Lora Configuration:
Lora (Long-Range Attention) is an attention mechanism designed to capture long-range dependencies in sequences more effectively. In the context of transformer-based models, Lora attention mechanisms are used to improve the model's ability to attend to distant parts of the input sequence during computation. Lora Configuration involves setting parameters and hyperparameters specific to Lora attention mechanisms, such as the attention range, to tailor the model's behavior according to the requirements of the task or dataset.

- Caching and storing of data/checkpoints:
Caching and storing of data/checkpoints involve saving intermediate results or model parameters during training or inference for later reuse. This practice can enhance efficiency by reducing redundant computations and enabling faster access to previously processed data or model states. Caching is commonly used to store preprocessed data or computed features, while storing checkpoints allows for saving and restoring model parameters at different stages of training, facilitating model retraining, debugging, and deployment. Efficient caching and storage mechanisms are crucial for managing large datasets and complex models effectively.


## Proposed and finetuned models

- For Model 1, we chose *DialoGPT* for its strong performance in natural language generation tasks,
fine-tuning it on our dataset to adapt it to our specific needs. Additionally, we implemented 
caching and storing of data/checkpoints to enhance efficiency and facilitate easier retraining
and deployment. While DialoGPT excels in generating coherent and contextually relevant responses, its limitations 
include potential generation of generic or nonsensical responses, especially when faced with out-of-domain or ambiguous inputs.

- For Model 2, we opted for *Falcon*, a transformer variant optimized for performance efficiency, and 
loaded a quantized model with reduced precision (4-bit parameters, 16-bit computation) to improve memory
usage and computation speed. We configured Falcon with Lora attention mechanisms to capture long-range 
dependencies effectively. Pushing the model to Hugging Face's model hub ensures its accessibility to the broader community. 
While Falcon's optimization techniques offer significant advantages in terms of resource efficiency, the reduced precision 
may lead to a trade-off in model accuracy and performance, particularly in tasks requiring fine-grained representations.

- For Model 3, we utilized *Gemma*, a PEFT-based transformer model, and employed Lora attention mechanisms for efficient 
long-range dependency modeling. Fine-tuning with Lora further enhanced the model's representational power and flexibility.
Pushing the model to Hugging Face's model hub enables wider dissemination and usage. Gemma's utilization of PEFT techniques
offers notable improvements in training efficiency and computational cost, but potential limitations may arise from the complexity 
of configuring and fine-tuning models with multiple optimization techniques.

- For Model 4, we integrated *Mistral*, specifically the Mistral 7B-Instruct variant, to leverage its advanced language generation
capabilities. Our implementation included fine-tuning with HuggingFace and LangChain embeddings to enhance semantic 
coherence and context sensitivity. The significant challenge we faced was determining an optimal method for saving and managing 
the model's state, debating between local storage and cloud-based platforms like Hugging Face's model hub. Efforts to streamline
model-frontend communication through a Flask server in a Colab environment were unsuccessful, highlighting the technical complexities 
in deploying large AI models and the necessity for efficient model management solutions.

## Challenges Encountered in Model Experimentation
1. Resource Limitations Impeding Gemma's Fine-Tuning:
Despite initial success in fine-tuning Gemma on a portion of our dataset, attempting to scale up training to the entire dataset proved challenging due to constraints on GPU resources provided by Colab. Despite employing a quantized version of Gemma and leveraging a Lora configuration for enhanced memory and compute efficiency, the process remained incomplete. This limitation hindered our ability to fully optimize Gemma's performance and explore its potential on a broader scale.

2. Incoherent Outputs from Falcon and Dialo:
While Falcon and Dialo models were capable of generating outputs, the quality of the responses fell short in coherence and contextual relevance. Despite our efforts to fine-tune and optimize these models, the outputs remained disjointed and lacking in meaningful content. Addressing this challenge would require further investigation and refinement of the training process to improve the models' ability to generate coherent and contextually relevant responses.

3. Model Weight Persistence Hindering Mistral's Deployment:
Although Mistral demonstrated promising results with high-quality answers and the ability to summarize generated responses, technical difficulties arose in persisting the model's weights. This obstacle prevented us from effectively saving and deploying Mistral for practical use. Given adequate computational resources, such as ample compute power, we would prioritize addressing these challenges to harness Mistral's capabilities effectively and integrate it into our workflow for enhanced performance and efficiency.

## Dataset selection 

After investigation, the data which was best suited for our model was the [DebateSum Database](https://huggingface.co/datasets/Hellisotherpeople/DebateSum)
. DebateSum is an open source database which contains over 100,000 archives of debates which were extracted over a seven year period. Due to computational power limitations and issues with using Azure ML Studio and cloud computing resources, we found ourselves forced to narrow the scope of the documents fed into the model. However, in a future iteration, our goal is to scale our computational power into the cloud and leverage cloud computing to process more documents and allow the chatbot to gain more 'intelligence'. 
