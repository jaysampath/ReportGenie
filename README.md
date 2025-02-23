# ReportGenie

An innovative AI-powered chatbot that dynamically generates SQL queries and reports based on merchant inputs. This project leverages state-of-the-art technologies to enable automated data visualization, interactive graph generation, and a streamlined report subscription workflow.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This project is designed to empower merchants by providing an intuitive interface to generate custom SQL queries and interactive reports. The chatbot uses advanced natural language processing (NLP) to understand user inputs, generate SQL statements, and deliver visual insights in real time. Merchants can preview sample reports and subscribe for regular updates, ensuring they always have access to the latest data insights.

---

## Features

- **Dynamic SQL Query Generation:**  
  Transform merchant inputs into executable SQL queries on-the-fly.

- **Interactive Data Visualization:**  
  Automatically generate interactive graphs and visual insights from user queries.

- **Report Subscription Workflow:**  
  Validate sample reports before subscribing to receive automated, scheduled reports.

- **User-Friendly Interface:**  
  Built using Streamlit, ensuring an engaging and intuitive user experience.

- **Scalable and Robust:**  
  Powered by Meta Llama for AI, integrated with Databricks and Snowflake for efficient data processing and storage.

---

## Tech Stack

- **Meta Llama:** AI and NLP capabilities for understanding merchant inputs.
- **Streamlit:** Rapid development of interactive web applications.
- **Python:** Core programming language for backend logic and integrations.
- **Databricks:** Managed Apache Spark platform for big data processing.
- **OpenAPI:** API standard for building and consuming RESTful services.
- **Snowflake:** Cloud data warehousing solution for storing and querying large datasets.

---

## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8 or later installed.
- Access to a Snowflake account.
- Databricks workspace credentials.
- Streamlit installed (`pip install streamlit`).
- Other dependencies as listed in `requirements.txt`.

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/jaysampath/ReportGenie.git
   cd ReportGenie
   ```

2. **Create a Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**

   Create a `.env` file at the root of the project and add your configuration details (Snowflake credentials, Databricks tokens, API keys, etc.):

   ```env
   SNOWFLAKE_USER=your_user
   SNOWFLAKE_PASSWORD=your_password
   SNOWFLAKE_ACCOUNT=your_account
   DATABRICKS_URL=your_databricks_url
   DATABRICKS_TOKEN=your_token
   # Add any additional environment variables here
   ```

---

## Usage

### Running the Chatbot

To start the Streamlit application, run:

```bash
streamlit run Login.py
```

This command will launch the chatbot interface in your default web browser. Interact with the chatbot by typing natural language queries to generate SQL commands and receive visual data reports.

### Report Subscription Workflow

1. **Generate a Sample Report:**  
   Use the chatbot to create a sample report based on your query.

2. **Validate the Report:**  
   Review the generated interactive graphs and insights.

3. **Subscribe to Reports:**  
   If satisfied with the sample, subscribe to receive automated, scheduled reports via email or your preferred communication channel.

---

## Architecture

The project architecture is designed for scalability and modularity:

- **Frontend:**  
  Built with Streamlit for a responsive and interactive user interface.

- **Backend:**  
  Python scripts integrated with Meta Llama for NLP, and OpenAPI to interact with external data services.

- **Data Processing:**  
  Databricks handles large-scale data processing tasks while Snowflake serves as the primary data warehouse.

- **APIs:**  
  RESTful services allow smooth communication between the chatbot, data processing layers, and visualization components.

---

## Contributing

We welcome contributions! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

For major changes, please open an issue first to discuss what you would like to change.

---

Feel free to reach out if you have any questions or need further assistance. Happy coding!

