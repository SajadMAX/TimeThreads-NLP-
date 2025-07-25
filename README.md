
#### TimeThreads

#### Description:
The Timeline Generator transforms unstructured Wikipedia biography text and other Wikipedia content into structured, visually compelling timelines using NLP spaCy Library and other python librares. By automating the extraction and classification of life events, it creates visual representations (text tables) that reveal the narrative arc of a person's life at a glance.

## Core Architecture

1.Text Processing Pipeline

Input: Raw Wikipedia biography text

Cleaning: Removes citations , non-biographical sections, and irrelevant markup

Sentence Segmentation: Splits text into individual events using NLP sentence boundaries

2.Event Extraction Engine

3.AI-Powered Classification

Uses NLP tokenize word  to extract words from sentences and then write a python function to categorize events:
BIRTH, DEATH, EDUCATION, CAREER, AWARD, PUBLICATION, MARRIAGE
Context-aware classification:
"Elected to Royal Society" → AWARD
Timeline Assembly
Chronological sorting with fuzzy date handling
Text Output Features

The Plain Text Timeline provides a minimalist, information-dense representation:
Structural Advantages
Fixed-width columns ensure perfect alignment
Machine-readable format (pipe-delimited)

#Smart Formatting Rules
Date normalization: "c. 1945" → 1945
Event summarization:
Original: "He was awarded the Nobel Prize in Physics in 1921 for his explanation of the photoelectric effect"
Output: "Nobel Prize in Physics (photoelectric effect)"

here is example of data output in .txt format:

| Date       | Topic      | Event                          |
|------------|------------|--------------------------------|
| 1912-06-03 | BIRTH      | Born in London, UK             |
| 1934-07-01 | EDUCATION  | Mathematics degree, Cambridge  |
| 1940-02-14 | CAREER     | Joined Bletchley Park          |
| 1952-03-15 | AWARD      | OBE for wartime service        |
