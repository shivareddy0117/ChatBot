Chatbot Applications
====================

This repository contains multiple chatbot applications designed for various purposes such as banking, question and answering, and user interaction. Each chatbot is built using Flask, Groq model, Llama3-8b-8192, and MongoDB.


Overview
--------

This project comprises multiple chatbots designed for specific tasks:
---------------------------------------------------------------------

*   A banking chatbot that interacts with users and provides information related to their bank accounts.
*   An application information chatbot that stores and retrieves user application information.
*   A question and answer chatbot that understands various types of user queries and pulls out the relevant information.

Features
--------

*   User interaction through natural language processing.
*   Retrieval of user-specific information.
*   Storage and management of application data.
*   Handling multiple types of user queries.
*   Built with Flask for easy deployment.
*   Utilizes advanced models like Groq and Llama3-8b-8192.
*   Data stored in MongoDB for efficient access and management.



Usage
-----

Once the application is running, you can interact with the different chatbots via the provided endpoints. Each chatbot has a dedicated endpoint for interaction.

Chatbot Descriptions
--------------------

### Banking Chatbot

*   **Description**: Interacts with users and provides information related to their bank accounts.
*   **Endpoint**: `/banking-chatbot`
*   **Features**:
    *   Check account balance
    *   Retrieve transaction history
    *   Provide account-related information

### Application Information Chatbot

*   **Description**: Stores and retrieves user application information.
*   **Endpoint**: `/application-info-chatbot`
*   **Features**:
    *   Store new application data
    *   Retrieve stored application information
    *   Update existing application data

### Question and Answer Chatbot

*   **Description**: Understands various types of user queries and pulls out the relevant information.
*   **Endpoint**: `/qa-chatbot`
*   **Features**:
    *   Answer user queries
    *   Provide detailed responses based on the context
    *   Understand different types of questions and provide accurate information

Technologies Used
-----------------

*   **Flask**: A micro web framework used for building the web application.
*   **Groq Model**: Utilized for natural language processing and understanding.
*   **Llama3-8b-8192**: An advanced model used for generating responses and handling queries.
*   **MongoDB**: A NoSQL database used for storing and managing application data.

Contributing
------------

Contributions are welcome! Please open an issue or submit a pull request with your changes. For major changes, please discuss them in an issue first.
