# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 00:26:19 2023

@author: qingh
"""

#%%
# step 1: load data
import json

def load_squad_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        squad_data = json.load(file)
    return squad_data

def extract_qa_pairs(squad_data):
    qa_pairs = []
    for article in squad_data['data']:
        for paragraph in article['paragraphs']:
            context = paragraph['context']
            for qa in paragraph['qas']:
                question = qa['question']
                answers = [answer['text'] for answer in qa['answers']]
                qa_pairs.append({
                    "question": question,
                    "answers": answers,
                    "context": context
                })
    return qa_pairs

# Load and extract data
squad_data = load_squad_data('train-v2.0.json')
qa_pairs = extract_qa_pairs(squad_data)



#%%
# --- step 2: clean data
import re

def clean_text(text):
    # 去除无关字符
    text = re.sub(r'\s+', ' ', text)  # 替换空格
    #text = re.sub(r'\[.*?\]', '', text)  # 去除括号内文字
    #text = re.sub(r'[^\w\s]', '', text)  # 去除除字母数字外的字符
    #text = re.sub(r'<.*?>', '', text)  # 删除HTML标签
    #text = re.sub(r'http\S+', '', text)  # 去除URL
    #text = re.sub(r'\d+', '', text)  # 去除数字
    return text.strip()

def clean_qa_pairs(qa_pairs):
    cleaned_pairs = []
    for question, answers, context in qa_pairs:
        cleaned_question = clean_text(question)
        cleaned_answers = [clean_text(answer) for answer in answers]
        cleaned_context = clean_text(context)
        cleaned_pairs.append((cleaned_question, cleaned_answers, cleaned_context))
    return cleaned_pairs

cleaned_qa_pairs = clean_qa_pairs(qa_pairs)


# --- step 3: data normalization
def normalize_text(text):
    text = text.lower()  # 转换为小写
    #text = re.sub(r'\d{2}/\d{2}/\d{4}', '标准日期格式', text)  # 日期格式化
    #text = re.sub(r'(\d+)(\s?)(kg|kilograms)', r'\1 kilograms', text)  # 单位标准化
    
    return text

def normalize_qa_pairs(qa_pairs):
    normalized_pairs = []
    for question, answers, context in qa_pairs:
        normalized_question = normalize_text(question)
        normalized_answers = [normalize_text(answer) for answer in answers]
        normalized_context = normalize_text(context)
        normalized_pairs.append((normalized_question, normalized_answers, normalized_context))
    return normalized_pairs

normalized_qa_pairs = normalize_qa_pairs(cleaned_qa_pairs)


# --- step 4: save data
#import pandas as pd

#df = pd.DataFrame(normalized_qa_pairs, columns=['Question', 'Answer', 'Context'])
#df.to_csv('normalized_qa_pairs.csv', index=False)

#with open('normalized_qa_pairs.json', 'w', encoding='utf-8') as file:
#    json.dump(normalized_qa_pairs, file, ensure_ascii=False, indent=4)


#%%

# Search

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def index_documents_bulk(es, index_name, documents):
    actions = [
        {"_index": index_name, "_id": doc_id, "_source": doc}
        for doc_id, doc in enumerate(documents)
    ]
    bulk(es, actions)

# Connect to Elasticsearch
es = Elasticsearch(
    ["https://localhost:9200"],
    basic_auth=('elastic', 'jfdB956RVePSS0DDz=7Z'),
    verify_certs=False
    )

# Index documents
index_documents_bulk(es, 'squad', qa_pairs)


#%%

def search_question(es, index_name, query_text, num_documents=10):
    query = {
        "query": {
            "multi_match": {
                "query": query_text,
                "fields": ["question", "context"]
            }
        },
        "size": num_documents
    }
    response = es.search(index=index_name, body=query)
    return response['hits']['hits']

def enhanced_search_question(es, index_name, query_text, num_documents=10):
    query = {
        "query": {
            "bool": {
                "should": [
                    {"match": {"context": {"query": query_text, "boost": 2}}},
                    {"match": {"question": query_text}}
                ]
            }
        },
        "size": num_documents
    }
    response = es.search(index=index_name, body=query)
    return response['hits']['hits']


# 测试问题
test_question = "What causes rain?"

# 搜索结果
results = enhanced_search_question(es, 'squad', test_question)

# 测试打印前几个结果
for hit in results:
    print(f"Question: {hit['_source']['question']}")
    print(f"Answer: {hit['_source']['answers']}")
    print(f"Context: {hit['_source']['context']}\n")
   
    
#%%
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage
import os


# 初始化openai
os.environ["AZURE_OPENAI_API_KEY"] = "da03f41f8a48497f90c0f834ec6a1424"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://oh-ai-openai-scu.openai.azure.com"
model = AzureChatOpenAI(
    openai_api_version="2023-05-15",
    azure_deployment="gpt-35-turbo",
)

def ask_gpt(question, model):
    message = HumanMessage(content=question)
    return model([message])

def ask_rag_gpt(question, es, model):
    # 检索文档
    documents = search_question(es, 'squad', question, num_documents=10)
    # 构建上下文和问题
    contexts = [hit['_source']['context'] for hit in documents]
    link = "These are the information searched from database. Please answer the question:"
    prompt = "\n\n".join(contexts) + "\n" + link +"\nQ: " + question + "\nA:"
    
    # 生成回答
    message = HumanMessage(content=prompt)
    return model([message])
    
test_question = "what is rain?"

original_results = ask_gpt(test_question, model)
rag_results = ask_rag_gpt(test_question, es, model)

print("original:", original_results)
print("rag_result:", rag_results)
print("=" * 50)


#%%
'''
from SPARQLWrapper import SPARQLWrapper, JSON

def query_knowledge_graph(query):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

# 示例查询：查询关于“雨”的信息
query = """
SELECT ?item ?itemLabel 
WHERE 
{
  ?item wdt:P31 wd:Q796.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
LIMIT 10
"""
result = query_knowledge_graph(query)
'''
#%%
# BLEU (Bilingual Evaluation Understudy)
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge import Rouge

# Load and extract data
squad_dev_data = load_squad_data('dev-v2.0.json')
dev_qa_pairs = extract_qa_pairs(squad_dev_data)
# Index documents
index_documents_bulk(es, 'squad_dev', dev_qa_pairs)

test_questions = ["Science",
                  "Emotion",
                  "art",
                  "history",
                  "logical"
                  ]


# 示例数据，模型生成的文本和参考文本

for test_question in test_questions:
    questions = search_question(es, 'squad', test_question, num_documents=1)
    question = questions[0]['_source']['question']
    original_result = ask_gpt(question, model)
    rag_result = ask_rag_gpt(question, es, model)
    reference = questions[0]['_source']['answers'][0]

    # 计算 BLEU 分数
    smoothie = SmoothingFunction().method4
    original_score = sentence_bleu([reference.split()], original_result.content.split(), weights=(0.5, 0.5), smoothing_function=smoothie)
    rag_score = sentence_bleu([reference.split()], rag_result.content.split(), weights=(0.5, 0.5), smoothing_function=smoothie)
    print(question)
    print("original answer:",original_result.content)
    print("rag_answer:",rag_result.content)
    print("reference answer:", reference)
    print("BLUE Score:")
    print(f"Original Score: {original_score}")
    print(f"rag Score: {rag_score}")
    print("-"*20)
    
    
    # 计算 ROUGE 分数
    # 初始化 ROUGE 计算器
    rouge = Rouge() 
    original_score = rouge.get_scores(reference, original_result.content)
    rag_score = rouge.get_scores(reference, rag_result.content)
    print("ROUGE Score:")
    print(f"Original Score: {original_score}")
    print(f"rag Score: {rag_score}")
    print("="*20)
    

#