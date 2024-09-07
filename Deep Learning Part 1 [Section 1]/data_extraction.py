#import necessary packages...
import requests
from bs4 import BeautifulSoup
import re
import csv

for count in range(4000):

  # URL (any)
  url = "https://www.wikihow.com/Special:Randomizer"

  # send an HTTP request
  response = requests.get(url)

  # Parse the HTML content usinf bs4
  soup = BeautifulSoup(response.text, 'html.parser')
  article_title = soup.find('title').text.strip()
  print(article_title+" "+str(count))
  # Extract the subheadings and para
  subheadings = []
  paragraphs = []
  steps = soup.find_all('div', class_='step')

  for step in steps:

      # Remove all <sup> elements and their contents
      for sup_tag in step.find_all('sup'):
          sup_tag.extract()

      subheading_element = step.find('b')
      if subheading_element is not None:

          # Process subheading
          subheading_text = subheading_element.text.strip().replace('\n', '')
          subheading_text = re.sub(r'[^\w\s]', '', subheading_text)  # Example: Remove special characters
          subheadings.append(subheading_text)

          # Remove titles and extra lines
          subheading_element.extract()
          
          # Clean up paragraph text
          for span_tag in step.find_all('span'):
              span_tag.extract()
              
          paragraph_text = step.text.strip().replace('\n', '')
          paragraph_text = paragraph_text.encode('ascii', errors='ignore').decode()  # Remove non-ASCII characters
          paragraph_text = re.sub(r'[^\w\s]', '', paragraph_text)  # Example: Remove special characters
          paragraphs.append(paragraph_text)

  if len(subheadings):
    with open('/content/drive/MyDrive/Code Cycle/wikiHow.csv', mode='a', newline='', encoding='utf-8') as csvfile:
      writer = csv.writer(csvfile)
      for i in range(len(subheadings)):
        writer.writerow([article_title, subheadings[i], paragraphs[i]])   