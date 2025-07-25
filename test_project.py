from project import get_wiki_page
from project import classify_topic
from project import extract_timeline_with_topics
import pytest



def test_classify_topic():
    assert classify_topic("As of February 2024, Fridman lives in Texas and is still paid by MIT.") ==" -"
    assert classify_topic("Alexei Lex Fridman ( born 15 August 1983) is an American computer scientist and podcaster.") == "CAREER"
    assert classify_topic("Jennifer Lynn Connelly (born December 12, 1970) is an American actress.") =="ACTING"



def test_extract_timeline_with_topics():
  assert extract_timeline_with_topics("Alexei Lex Fridman ( born 15 August 1983) is an American computer scientist and podcaster.") == [{'Date': '1983',
  'Topic': 'CAREER',
  'Event': 'Alexei Lex Fridman ( born 15 August 1983) is an American computer scientist and podcaster.'}]
  assert extract_timeline_with_topics("He was awarded the Nobel Prize in Physics in 1921 for his explanation of the photoelectric effect.") ==[{'Date': '1921',
  'Topic': 'AWARD',
  'Event': 'He was awarded the Nobel Prize in Physics in 1921 for his explanation of the photoelectric effect.'}]

def test_get_wiki_page():
    user_agent = "MyProjectName/1.0"
    assert get_wiki_page("lexi7",user_agent ) == None
    #assert get_wiki_page("Andy",user_agent ) == None





