import json
import os
from datetime import datetime

import yfinance as yf

from crewai import Agent, Task, Crew, Process

from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchResults

import streamlit as st

#Criando Yahoo Finance Tool
def fetch_stock_price(ticket):
    stock = yf.download(ticket, start="2023-08-08", end="2024-08-08")
    return stock

yahoo_finance_tool = Tool(
    name = "Yahoo Finance Tool",
    description = "Fetches stock prices for {ticket} from the last year about a specific stock from Yahoo Finance API",
    func = lambda ticket: fetch_stock_price(ticket)
)

#response = yahoo_finance_tool.run("AAPL")

#print(response)

# Importando OpenAi LLM - GPT
os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
llm = ChatOpenAI(model = "gpt-3.5-turbo")


# In[5]:


seniorStockPriceAnalyst = Agent(
    role = "Senior Stock Price Analyst",
    goal = "Find the {ticket} stock price and analyses trends",
    backstory = """You're highly experienced in analyzing the price of an 
    specific stock and make predictions about its future price""",
    verbose = True,
    llm = llm,
    max_iter = 5,
    memory = True,
    tools = [yahoo_finance_tool],
    allow_delegation = False
)


# In[6]:


getStockPrice = Task(
    description ="Analyze the stock {ticket} price history and create a trend analysis of up, down or sideways",
    expected_output = """"Specify the current trend stock price - up, down or sideways. 
    eg. stock = 'AAPL, price UP'
    """,
    agent = seniorStockPriceAnalyst

)

# Importando a Tool de Busca
search_tool = DuckDuckGoSearchResults(backend = 'news', num_results = 10)

seniorStockNewsAnalyst = Agent(
    role = "Senior Stock News Analyst",
    goal = """Create a short summary of the market news related to the stock {ticket} company. Specify the current trend - up, down
    or sideways - with the news context. For each requested stock, specify a number between 0 and 100 - where 0 is extreme fear
    and 100 is extreme greed.""",
    backstory = """You're highly experienced in analyzing the market trends and news, and have tracked assets for more than 10 years. 

    You're also a master level analyst in the traditional markets and have deep understanding of human psychology.
    
    You understand news, their titles and information, but you look at theses with a healthy dose of skepticism. 
    You also consider the source of the news.""",
    verbose = True,
    llm = llm,
    max_iter = 10,
    memory = True,
    tools = [search_tool],
    allow_delegation = False
)

get_news = Task(
    description = f"""Take the stock and always include BTC to it (even if not requested).
    Use the search tool to search each one individually.
    
    The current date is {datetime.now()}.
    
    Compose the results into a helpfull report.""",
    expected_output = """A summary of the overall market and one sentence summary for each requested asset. 
    Include a fear/greed score for each asset based on the news. Use format:
    <STOCK ASSET>
    <SUMMARY BASED ON NEWS>
    <TREND PREDICTION>
    <FEAR/GREED SCORE>""",
    agent = seniorStockNewsAnalyst
)

seniorStockAnalystWriter = Agent(
    role = "Senior Stock Analyst Writer",
    goal = """Analyze the trends price, news and write an insightfull compelling and informative 3 paragraph long newsletter based on the stock report and price trend.""",
    backstory = """You're widely accepted as the best stock analyst in the market. You understand complex concepts and create compelling
    stories and narratives that resonate with a huge variety of audiences.
    
    You understand macro factors and combine multiple theories - eg. cycle theory and fundamental analysis. You're able to hold
    multiple opinions when analyzing anything.""",
    verbose = True,
    llm = llm,
    max_iter = 5,
    memory = True,
    allow_delegation = True
)

writeAnalysis = Task(
    description = """Use the stock price trend and the stock news report to create an analysis and write the newsletter about the {ticket} 
    company that is brief and highlights the most important points.
    Focus on the stock price trend, news and fear/greed score. What are the near future considerations?
    Include the previous analysis of the stock trend and news summary.""",
    expected_output = """An eloquent three paragraph newsletter formated as markdown in an easy and readable manner. 
    It must contain:
    
    - three bullets executive summay
    - Introduction setting the overall picture while spiking up the interest
    - main part provides the meat of the analysis, including the news summary and fear/greed scores
    - summary containing the key facts and cocrete future trend predictions - up, down or sideways""",
    agent = seniorStockAnalystWriter,
    context= [getStockPrice,get_news]
)

crew = Crew(
    agents = [seniorStockPriceAnalyst,seniorStockNewsAnalyst,seniorStockAnalystWriter],
    tasks = [getStockPrice,get_news,writeAnalysis],
    verbose = 2,
    process = Process.hierarchical,
    full_output = True,
    share_crew=False,
    manager_llm=llm,
    max_iter = 15
)

#results = crew.kickoff(inputs = {'ticket': 'AAPL}'})

#list(results.keys())

with st.sidebar:
    st.header("Enter the Stock to Research")

    with st.form(key='research_form'):
        topic = st.text_input("Select the ticket")
        submit_button = st.form_submit_button(label= "Run Research")

if submit_button:
    if not topic:
        st.error("Please fill the ticket field")
    else:
        results = crew.kickoff(inputs = {'ticket' : topic})

        st.subheader("Results of your research:")
        st.write(results['final_output'])