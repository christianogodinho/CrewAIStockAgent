# CrewAi - StockAgent

## Description

CrewAI - StockAgent is an application for consulting the stock market using GPT3.5-TURBO. After selecting the ticket of your choice, you'll receive stock price history, news and predictions in the simple but efficient user interface.

## Functionalities

- **User-Friendly Interface**: Easy to use clean UI with fast response.
- **Stock Market Ticket Analysis**: Checks price history and create a trend analysis - up, down or sideways.
- **News Analysis**: Checks latest news about desired asset, generating a summary of the overall market and asset. Also informs a fear/greed score based on reeded news.
- **Predictions**: Based on the information gathered previously, considerations about the future of the asset will be included in the summary of the research.

## Technologies Used

- **Python**
- **OpenAI LLM**
- **CrewAI Python Library**
- **Streamlit**
- **StreamlitCloud**

## Instalation

Follow these steps to configure the project locally:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/christianogodinho/CrewAIStockAgent.git
   cd CrewAIStockAgent
   ```
   
2. **Access project folder:**

   ```bash
   cd webappStocks
   ```

3. **Create and activate virtual environment:**

   ```bash
   python -m venv venv
   source venv\Scripts\activate #No MacOS: venv/bin/activate
   ```

4. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Execute application:**

   ```bash
   python crewai_stocks.py
   ```

6. **Access application at 'http://localhost:5000' in your browser**

## How to use:

1. **Open the application in your browser**
2. **Insert ticket of desired asset**
3. **Click in 'Run Research' to receive the market analysis on desired ticket**

## Contribution

More than welcome! If you wish to make the project even better don't be ashamed to open an _issue_ or send me a _pull request__.

# DISCLAIMER
The information presented in the application's response was generated through queries made by an artificial intelligence model and should not be considered when making decisions to buy any asset for any portfolio. Please consult a properly accredited financial market specialist to work with your portfolio.
