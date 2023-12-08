# RAG (Retrieval-Augmented Generation) on SQuAD 2.0 using Elasticsearch
This project aims to implement Retrieval-Augmented Generation (RAG) for question answering using SQuAD 2.0 dataset and Elasticsearch for search functionalities.

## Steps
### 1. Data Import
- Data from SQuAD 2.0 was imported successfully.
### 2. Data Cleaning
- Conducted data cleaning procedures, however, minimal impact observed.
### 3. Setting Up Search Engine
- Configured and set up Elasticsearch for efficient searching.
### 4. Testing Search
- Successfully tested the functionality of the search engine.
### 5. Question Answering with GPT Model
- Utilized GPT-based model for question answering tasks.
### 6. Knowledge Graph Integration
- Attempted integration with a knowledge graph using SPARQLWrapper, but encountered issues.
### 7. Test Performance
- The RAG model demonstrated improved performance compared to previous methods across the additional five test examples. The BLEU and ROUGE scores for these examples further support the model's enhanced accuracy in generating answers.

## Test Result
I test five examples, using BLEU and ROUGE to evaluate the performace.
|   BLEU         |    Original           |   RAG             |
|---|---|---|
| Example 1:     |       0.0064          |        0.0862     |
| Example 2:     |       0.00            |        0.1961     |
| Example 3:     |       0.0417          |        0.4767     |
| Example 4:     |       0.0095          |        0.5753     |
| Example 5:     |       0.1451          |        0.5117     |

### EXAMPLE 1: 
- Question: How has computer science helped science as a whole?
- Original answer: "Computer science has had a major impact on science as a whole by providing new tools and technologies that have revolutionized research and analysis. Here are some specific ways in which computer science has helped science:
  1. Data Analysis: With the advent of computers, scientists can now store, process, and analyze vast amounts of data. This has led to new insights and discoveries in fields such as genomics, astronomy, and climate science.
  2. Simulation and Modeling: Computer simulations and modeling have enabled scientists to simulate complex systems and predict how they will behave under different conditions. This has been particularly useful in fields such as physics, chemistry, and engineering.
  3. Automation: Computers have made it possible to automate many scientific processes that were once done by hand. This has led to increased efficiency and accuracy in fields such as biology, chemistry, and physics.
  4. Collaboration: Computers have also made it easier for scientists to collaborate and share data, ideas, and research findings. This has led to greater cooperation and interdisciplinary research.
  
  Overall, computer science has enabled scientists to do things that were once impossible, and has opened up new frontiers in scientific research and discovery."
- rag_answer: Computer science has contributed to more general scientific development by facilitating large-scale archiving of scientific data. It has also led to advancements in fields such as artificial intelligence, database design, and computer networking, which have aided scientific research and analysis. Additionally, computer science has allowed for the development of advanced computer hardware, which has increased the speed and accuracy of scientific simulations and calculations.
- reference answer: by facilitating large-scale archiving of scientific data
#### BLUE Score:
- Original Score: 0.006466530409101146
- rag Score: 0.08625819491779424
#### ROUGE Score:
- Original Score: [{'rouge-1': {'r': 0.03305785123966942, 'p': 0.5714285714285714, 'f': 0.062499998966064466}, 'rouge-2': {'r': 0.0, 'p': 0.0, 'f': 0.0}, 'rouge-l': {'r': 0.03305785123966942, 'p': 0.5714285714285714, 'f': 0.062499998966064466}}]
- rag Score: [{'rouge-1': {'r': 0.15217391304347827, 'p': 1.0, 'f': 0.26415094110359566}, 'rouge-2': {'r': 0.09836065573770492, 'p': 1.0, 'f': 0.1791044759812876}, 'rouge-l': {'r': 0.15217391304347827, 'p': 1.0, 'f': 0.26415094110359566}}]

### EXAMPLE 2: 
- Question: Who developed a situated perspective on emotion along with Andrea Scarantino?
- Original answer: Lucy L. Johnston developed a situated perspective on emotion along with Andrea Scarantino.
- rag_answer: Paul E. Griffiths developed a situated perspective on emotion along with Andrea Scarantino.
- reference answer: Paul E. Griffiths
#### BLUE Score:
- Original Score: 0
- rag Score: 0.19611613513818407
#### ROUGE Score:
- Original Score: [{'rouge-1': {'r': 0.0, 'p': 0.0, 'f': 0.0}, 'rouge-2': {'r': 0.0, 'p': 0.0, 'f': 0.0}, 'rouge-l': {'r': 0.0, 'p': 0.0, 'f': 0.0}}]
- rag Score: [{'rouge-1': {'r': 0.23076923076923078, 'p': 1.0, 'f': 0.374999996953125}, 'rouge-2': {'r': 0.16666666666666666, 'p': 1.0, 'f': 0.2857142832653061}, 'rouge-l': {'r': 0.23076923076923078, 'p': 1.0, 'f': 0.374999996953125}}]

### EXAMPLE 3: 
- Question: What type of art does Jiangsu Art Gallery contain?
- Original answer: As an AI language model, I do not have access to the latest updates or current exhibitions at Jiangsu Art Gallery. However, Jiangsu Art Gallery is a comprehensive art museum that showcases various types of art, including traditional Chinese painting, calligraphy, sculpture, and contemporary art. It also hosts various thematic exhibitions throughout the year.
- rag_answer: Jiangsu Art Gallery contains both traditional and contemporary art pieces of China.
- reference answer: traditional and contemporary art pieces of China
#### BLUE Score:
- Original Score: 0.041797488547959935
- rag Score: 0.4767312946227961
#### ROUGE Score:
- Original Score: [{'rouge-1': {'r': 0.10638297872340426, 'p': 0.7142857142857143, 'f': 0.1851851829286694}, 'rouge-2': {'r': 0.0392156862745098, 'p': 0.3333333333333333, 'f': 0.07017543671283476}, 'rouge-l': {'r': 0.0851063829787234, 'p': 0.5714285714285714, 'f': 0.1481481458916324}}]
- rag Score: [{'rouge-1': {'r': 0.5833333333333334, 'p': 1.0, 'f': 0.7368421006094183}, 'rouge-2': {'r': 0.5454545454545454, 'p': 1.0, 'f': 0.7058823483737025}, 'rouge-l': {'r': 0.5833333333333334, 'p': 1.0, 'f': 0.7368421006094183}}]

### EXAMPLE 4: 
- Question: Intellectual history and social history are used in what?
- Original answer: Intellectual history and social history are used in the field of historiography, which is the study of how history is written and how historical knowledge is constructed. They are also used in academic disciplines such as history, sociology, anthropology, and cultural studies to provide insights into how people and societies have developed over time, and to understand the cultural, social, and political contexts in which ideas and movements emerged.
- rag_answer: Historiography of science.
- reference answer: Historiography of science
#### BLUE Score:
- Original Score: 0.009499524940557587
- rag Score: 0.5773502691896257
#### ROUGE Score:
- Original Score: [{'rouge-1': {'r': 0.020833333333333332, 'p': 0.3333333333333333, 'f': 0.0392156851672434}, 'rouge-2': {'r': 0.0, 'p': 0.0, 'f': 0.0}, 'rouge-l': {'r': 0.020833333333333332, 'p': 0.3333333333333333, 'f': 0.0392156851672434}}]
- rag Score: [{'rouge-1': {'r': 1.0, 'p': 1.0, 'f': 0.999999995}, 'rouge-2': {'r': 1.0, 'p': 1.0, 'f': 0.999999995}, 'rouge-l': {'r': 1.0, 'p': 1.0, 'f': 0.999999995}}]

### EXAMPLE 5: 
- Question: Who attacked logical positivism?
- Original answer: Several philosophers and thinkers have attacked logical positivism, including Willard Van Orman Quine, Thomas Kuhn, Karl Popper, and Ludwig Wittgenstein.
- rag_answer: Thinkers such as Nelson Goodman, W.V. Quine, Hilary Putnam, Karl Popper, and Richard Rorty attacked logical positivism after World War II.
- reference answer: Nelson Goodman, W.V. Quine, Hilary Putnam, Karl Popper, and Richard Rorty
#### BLUE Score:
- Original Score: 0.14509525002200235
- rag Score: 0.511766315719159
#### ROUGE Score:
- Original Score: [{'rouge-1': {'r': 0.21052631578947367, 'p': 0.3333333333333333, 'f': 0.2580645113839751}, 'rouge-2': {'r': 0.10526315789473684, 'p': 0.18181818181818182, 'f': 0.13333332868888906}, 'rouge-l': {'r': 0.21052631578947367, 'p': 0.3333333333333333, 'f': 0.2580645113839751}}]
- rag Score: [{'rouge-1': {'r': 0.5454545454545454, 'p': 1.0, 'f': 0.7058823483737025}, 'rouge-2': {'r': 0.5238095238095238, 'p': 1.0, 'f': 0.6874999954882813}, 'rouge-l': {'r': 0.5454545454545454, 'p': 1.0, 'f': 0.7058823483737025}}]
--------
