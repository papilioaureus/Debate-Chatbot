# Debatebot

## Overview

This project introduces a sophisticated debate simulator designed to broaden your horizons and challenge your perspective. It serves as an educational tool suitable for anyone keen on understanding viewpoints distinct from their own. Through interactive and engaging discussions, it presents a unique opportunity to explore a wide array of ideas, arguments, facts, and even fallacies.

## Features

- **Interactive Chatbot**: Engage with an intelligent chatbot that was trained on data from real debates! The integration of the 'DebateSum' dataset allows the chatbot to consistently generate intelligent text which offers insights into the stance it is prompted to take. 

- **Real-time Interactive Screen**: A dynamic display showcases key points from discussions. In future iterations its goal will be to highlight the relationships between different arguments and the conclusions drawn from them. This visual aid enhances understanding and retention of complex discussions.

- **Diverse Perspectives**: By simulating debates and presenting a variety of perspectives, the tool encourages users to learn about and understand positions different from their own, thereby promoting a more empathetic and well-rounded worldview.

## Ideal for :

This tool is perfect for educators, students, debate enthusiasts, or anyone interested in expanding their knowledge and understanding of various subjects and perspectives. It's designed to encourage curiosity, facilitate learning, and foster the growth of a knowledgeable mind by exploring the rich landscape of diverse ideas.

## System Architecture and Levegeraged Tools : 

The Debate-Chatbot project employs a modular architecture that integrates an interactive chatbot and real-time discussion display. This setup is designed to engage users in meaningful debate simulations, providing insights from various perspectives. The architecture is built on Python for backend operations, managing chatbot interactions and data processing on a web platform. The frontend is built using React.js.  

We explored four open source models as candidates for the debate chatbot agent: DialoGPT was fine-tuned for natural language tasks but faced issues with generic responses. Falcon, optimized for efficiency, used quantized models but potentially compromised on accuracy. Gemma applied PEFT and Lora attention for improved training efficiency, with challenges in complexity. Lastly, Mistral 7B-Instruct was fine-tuned for advanced language generation, with difficulties in model management and deployment. Each model showcased distinct advantages in performance and efficiency, along with specific limitations related to precision, complexity, and deployment. As of right now our application is connected to the OpenAI API which is trained on the DebateSum data uploaded to [Hugging Face](https://huggingface.co/asaurasieu/debatebot/tree/main). 
 
## Code Testing :

Unit and functional testing was implemented for the backend functions, and these tests were executed using PyTest. 
## Getting Started

## How to run :

To get started with this innovative debate simulator, download the repository and run `app.py` for the backend in your local environment after running `npm start` to initialize the frontend. In case you want to try it out online, visit our [azure webapp](debatebot.azurewebsites.net). 




