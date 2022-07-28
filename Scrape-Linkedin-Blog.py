from bs4 import BeautifulSoup
import requests
import pandas as pd 

# 3 steps to get the data ETL(1.Extract 2.Trasform 3.Load)


# ___________ 1. Extract _____________
def extract(page):
    headers = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36'}
    url = f'https://www.linkedin.com//business/learning/blog?page0={page}#postlist0FocusPoint'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

# ___________  2. Transform ____________
def transform(soup):
    divs = soup.find_all('li', class_= 'post-list__item grid-post')
    for item in divs:        
        title = item.find('a', class_= 'grid-post__link t-20 t-black').text.strip().replace('\n','')
        # Here we are using try and except bcoz in few blog have none characters.
        try:
         category = item.find('a', class_='t-14 t-bold').text.strip().replace('\n','')
        except:
            category = ''
        try:
         author = item.find('p', class_= 'grid-post__author t-14 t-bold t-black').text.strip().replace('\n','')
        except:
            author = ''
        pub_date = item.find('p', class_= 'grid-post__date t-14 t-black--light').text.strip().replace('\n','')
        try:
            desc = item.find('p', class_ = 'grid-post__description t-14').text.strip().replace('\n','')
        except:
            desc = ''

        blog_data = {
            "Title": title,
            "Description": desc,
            "Category": category,
            "Author": author,
            "Publish_Date": pub_date
        }
        linkedin_blog.append(blog_data)
        #  ____________purpose to check execution ___________
        # print(f"{category} | {title} | {author} | {pub_date} | {description} ")
    return 


# Loop through fuction
linkedin_blog = []
for i in range(1,98):
    print(f'Extracting the page {i}')
    c = extract(i)
    transform(c)

# ____________ 3. Load _____________

df = pd.DataFrame(linkedin_blog)
df.to_csv('Linkedin_blog_data.csv',index=False)


