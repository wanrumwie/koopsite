from bs4 import BeautifulSoup

input_file_name = 'html_in.html'
s = input('Enter file name for input html [%s] ' % input_file_name)
if s:
    input_file_name = s
with open(input_file_name, encoding="UTF-8") as f:
    html_doc = f.read()

soup = BeautifulSoup(html_doc, 'html.parser')

print('-'*80)
print(soup.prettify())
print('-'*80)
