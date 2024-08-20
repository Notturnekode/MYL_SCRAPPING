#!/usr/bin/env python
# coding: utf-8

# In[126]:


from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import requests
import pandas as pd


# In[127]:


column_names = ['N°', 'Nombre', 'Imagen', 'Tipo', 'Coste de oro', 'Frecuencia', 'Edición', 'Habilidad', 'Código', 'Arte', 'Texto épico']

decksFirstEra = {'El_Reto', 'Mundo_G%C3%B3tico', 'La_Ira_del_Nahual', 'Ragnarok' , 'La_Cofrad%C3%ADa', 'Esp%C3%ADritu_de_Drag%C3%B3n'}


# In[128]:


root = 'https://myl.fandom.com'
deckList = f'{root}/es/wiki/Categor%C3%ADa:Lista_de_Cartas'
page_html = requests.get(deckList)
page_soup = soup(page_html.text, "lxml")


# In[129]:


box = page_soup.find('div' , class_='category-page__members')
deckList = box.findAll('a', class_= 'category-page__member-link', href=True)
#deckList


# In[130]:


deckLinks = []
for link in deckList:
        deckLinks.append(link['href'])


# In[131]:


decksLinkFE = []
for link in deckLinks:
    if any(i in link for i in decksFirstEra):
        decksLinkFE.append(link)


# In[132]:


cardList = f'{root}{decksLinkFE[1]}'
#print(cardList)
page_html = requests.get(cardList)
page_soup = soup(page_html.text, "lxml")
page_table = page_soup.find_all('table')[1] 

cardLinks= []
for row in page_table.find_all('tr'):
    cardRow = []
    for td in row.find_all('td'):
        td_check = td.find('a')
        if td_check is not None:
            link = td.a['href']
            cardRow.append(link)
        else:
            not_link = ''.join(td.stripped_strings)
            if not_link == '':
                 not_link = None
            cardRow.append(not_link)
    cardLinks.append(cardRow)


cardLinkList = []
for i in range(len(cardLinks)-1):
    cardLinkList.append(cardLinks[i+1][1])
    
print(cardLinkList)
print(cardList)


# In[ ]:





# In[133]:


cardDetail =[]

title = ''
cardImage = ''
cardDescription = []
cardHability = ''
cardCode = ''
cardArtist = ''
cardHistory = ''

for i in range(len(cardLinkList)):
    #print(f'{root}{cardLinkList[i]}')
    cardList = f'{root}{cardLinkList[i]}'
    print(cardList)
    page_html = requests.get(cardList)
    page_soup = soup(page_html.text, "lxml")
    card_tables = page_soup.findAll('table', class_='table_black')

# Primera Tabla [0]... Header contiene nombre de Carta / Image contiene imagen / Description contiene: Tipo, Coste, Edición, Frecuencia
    table_header = card_tables[0].find('tr', class_='table_head_black')
    table_image = card_tables[0].find('tr', class_='table_body_black') 
    table_description = card_tables[0].findAll('tr', class_='') 

    title = table_header.find('b').getText()
    #cardDetail.append((i, title))
    cardImage = table_image.find('a', class_='image')

    #cardDetail.append((i, cardImage['href']))

    #for row in table_description:
     #   for th in row.find_all('th'):
      #      if th.text not in column_names:
       #         cardDescription.append(th.text.strip('\n'))
                 
    tr = card_tables[0].findAll('tr', class_='')

    typeFlag = 0
    costFlag = 0
    frecFlag = 0
    editionFlag = 0

    typeCard = ''
    costCard = ''
    frecCard = ''
    editionCard = ''

    for row in tr:
    #print(row)
        th = row.find('th')
        if th.getText().strip() == "Tipo":
            #print('Entre Tipo')
            typeCard = th.find_next('th').getText().strip('\n')
            typeFlag = 1
        elif th.getText().strip() == "Coste de oro":
            #print('Entre Coste')
            costCard = th.find_next('th').getText().strip('\n')
            costFlag = 1
        elif th.getText().strip() == "Frecuencia":
            #print('Entre Frecuencia')
            frecCard = th.find_next('th').getText().strip('\n')
            frecFlag = 1
        elif th.getText().strip() == "Edición":
            #print('Entre Edicion')
            editionCard = th.find_next('th').getText().strip('\n')
            editionFlag = 1
    
    if costFlag != 0:
     cardDescription.append(typeCard)
     cardDescription.append(costCard)
     cardDescription.append(frecCard)
     cardDescription.append(editionCard)
    else:
     cardDescription.append(typeCard)
     cardDescription.append('Sin Costo')
     cardDescription.append(frecCard)
     cardDescription.append(editionCard)
 
    #print(card_description)

# Impresión Segunda y tercera Tabla [1]...
#Para Cartas con Habilidad: Header contiene Label Habilidad / Body descripción de la habilidad.
#Para Cartas sin Habilidad: Contiene el Código y Arte  


#Valido si la carta tiene Habilidad#

    card_with_hability = card_tables[1].find('td')
    #card_with_No_hability = card_tables[1].find('td')

    if (card_with_hability.getText().strip('\n') == "Habilidad"):
        #print('Si tengo')
        hability_flag = 1
        tr = card_tables[1].find('tr')
        td = tr.find('td')
        #cardDetail.append((i, td.find_next('td').text.strip()))
        cardHability = td.find_next('td').text.strip()
    
        more_details = card_tables[2].find('tr', class_='table_body_black')
    #print(more_details)
        for td in more_details.find('td'):
            cardCode = td.text.strip()
            cardArtist = td.find_next('td').text.strip()
            #cardDetail.append((i,td.text.strip()))
            #cardDetail.append((i,td.find_next('td').text.strip()))
        card_history = card_tables[3].find('tr', class_='table_body_black')
    #print(more_details)
        for td in card_history.find('td'):
            cardHistory = td.text.strip()
            #cardDetail.append((i,td.text.strip()))
            #cardDetail.append(td.find_next('td').text.strip())
        
        #cardDetail.append((i, title, cardImage['href']))
        
#Carta sin Habilidad#            
    else: 
    #print('No tengo')
        #cardDetail.append('Sin Habilidad')
        cardHability = 'Sin Habilidad'
        more_details = card_tables[1].find('tr', class_='table_body_black')
    #print(more_details)
        for td in more_details.find('td'):
            cardCode = td.text.strip()
            cardArtist = td.find_next('td').text.strip()
            #cardDetail.append((i,td.text.strip()))
            #cardDetail.append((i,td.find_next('td').text.strip()))
        card_history = card_tables[2].find('tr', class_='table_body_black')
    #print(more_details)
        for td in card_history.find('td'):
            cardHistory = td.text.strip()
            #cardDetail.append((i,td.text.strip()))
        
    cardDetail.append((i, title, cardImage['href'], cardDescription[0], cardDescription[1], cardDescription[2], cardDescription[3], cardHability, cardCode, cardArtist, cardHistory))
    cardDescription = []
        
print('Estoy al final')
print(cardDetail)





# In[134]:


df = pd.DataFrame(cardDetail)
df.columns = column_names
df.head(10)


#cardTable = card_page_soup.find('table', class_='lista sortable mergetable col2cen col3cen col4cen center')
#cardList = cardTable.findAll('tr', class_= '')
#print(cardList[0])


# In[135]:


#filename = cardLinkList[0].replace('https://myl.fandom.com/es/wiki/', '')
df.to_csv('Listado_Cartas_El_Reto_Extension' + '.csv', index=False)
#df = pd.DataFrame(columns=['N', 'Nombre', 'Tipo', 'Frecuencia', 'Arte'])

# Collecting Ddata
#for row in cardTable.tbody.find_all('tr'):    
    # Find all data for each column
 #   columns = row.find_all('td')
  #  if(columns != []):
   #     N = columns[0].text.strip()
    #    Nombre = columns[1].text.strip()
     #   Tipo = columns[2].text.strip()
      #  Frecuencia = columns[3].text.strip()
       # Arte = columns[4].text.strip()

        
        #output = df.concat({'N': N, 'Nombre': Nombre})


# In[11]:


#df = pd.DataFrame(columns=['N', 'Nombre'])

# Collecting Ddata
#for row in cardTable.tbody.find_all('tr'):    
    # Find all data for each column
    #columns = row.find_all('td')
    #if(columns != []):
    #    N = columns[0].text.strip()
    #    Nombre = columns[1].text.strip()
        
    #    output = df.concat({'N': N, 'Nombre': Nombre})


# In[12]:


#///// ACTUALIZAR CUANDO LOGRE OBTENER LINKS DE TABLAS

#for link in decksLinkFE:
#    cardList = f'{root}{link}'
#    #print (cardList)
#    df = pd.read_html(cardList)
#    #print (df)
#    filename = cardList.replace('https://myl.fandom.com/es/wiki/', '')
#    print(filename)
#    df[1].to_csv(filename + '.csv', index=False)


# In[13]:


#cardList = f'{root}{decksLinkFE[0]}'

#sp = bs.BeautifulSoup(cardList, 'lxml')
#tb = sp.find_all('table')[56] 
#df = pd.read_html(str(tb),encoding='utf-8', header=0)[0]

#print (cardList)
#df = pd.read_html(cardList)
#df['href'] = [np.where(tag.has_attr('href'),tag.get('href'),"no link") for tag in tb.find_all('a')]

    #print (df)


# In[110]:


cardList = f'{root}{cardLinks[2][1]}'
#print(cardList)
page_html = requests.get(cardList)
page_soup = soup(page_html.text, "lxml")
card_tables = page_soup.findAll('table', class_='table_black')


cardDetail =[]

#print(card_tables[3])

# Primera Tabla [0]... Header contiene nombre de Carta / Image contiene imagen / Description contiene: Tipo, Coste, Edición, Frecuencia
table_header = card_tables[0].find('tr', class_='table_head_black')
table_image = card_tables[0].find('tr', class_='table_body_black') 
#table_description = card_tables[0].findAll('tr', class_='') 

title = table_header.find('b').getText()
cardDetail.append(title)
cardImage = table_image.find('a', class_='image')

cardDetail.append(cardImage['href'])

#print(table_description)
#print(len(table_description))
#for row in table_description:
#a = table_description[0].find('th').text.strip('\n')
#b = table_description[1].find_next('th').text.strip('\n')
#c = table_description[2].find('th').text.strip('\n')
#d = table_description[3].find('th').text.strip('\n')
#e = table_description[4].find('th').text.strip('\n')


card_description = []
table_description = card_tables[0].findAll('tr', class_='') 
#print(table_description)
tr = card_tables[0].findAll('tr', class_='')

typeFlag = 0
costFlag = 0
frecFlag = 0
editionFlag = 0

typeCard = ''
costCard = ''
frecCard = ''
editionCard = ''

for row in tr:
    #print(row)
    th = row.find('th')
    if th.getText().strip() == "Tipo":
        print('Entre Tipo')
        typeCard = th.find_next('th').getText().strip('\n')
        typeFlag = 1
    elif th.getText().strip() == "Coste de oro":
        print('Entre Coste')
        costCard = th.find_next('th').getText().strip('\n')
        costFlag = 1
    elif th.getText().strip() == "Frecuencia":
        print('Entre Frecuencia')
        frecCard = th.find_next('th').getText().strip('\n')
        frecFlag = 1
    elif th.getText().strip() == "Edición":
        print('Entre Edicion')
        editionCard = th.find_next('th').getText().strip('\n')
        editionFlag = 1
    
if costFlag != 0:
 card_description.append(typeCard)
 card_description.append(costCard)
 card_description.append(frecCard)
 card_description.append(editionCard)
else:
 card_description.append(typeCard)
 card_description.append('Sin Costo')
 card_description.append(frecCard)
 card_description.append(editionCard)
 
print(card_description)

# table_description = card_tables[0].findAll('tr', class_='') 
#print(table_description)
#tr = card_tables[0].find('tr', class_='')
#print(tr)
#th = tr.find('th')
#if th.getText().strip() == "Tipo":
#        print(th.find_next('th').getText().strip('\n'))
#if th.getText().strip() == "Coste de Oro":
#        print(th.find_next('th').getText().strip('\n'))
                

# Impresión Segunda y tercera Tabla [1]...
#Para Cartas con Habilidad: Header contiene Label Habilidad / Body descripción de la habilidad.
#Para Cartas sin Habilidad: Contiene el Código y Arte  


#Valido si la carta tiene Habilidad#

card_with_hability = card_tables[1].find('td')

if (card_with_hability.getText().strip('\n') == "Habilidad"):
    #print('Si tengo')
    hability_flag = 1
    tr = card_tables[1].find('tr')
    td = tr.find('td')
    cardDetail.append(td.find_next('td').text.strip())
    
    more_details = card_tables[2].find('tr', class_='table_body_black')
    #print(more_details)
    for td in more_details.find('td'):
        cardDetail.append(td.text.strip())
        cardDetail.append(td.find_next('td').text.strip())
        
    card_history = card_tables[3].find('tr', class_='table_body_black')
    #print(more_details)
    for td in card_history.find('td'):
        #print(td.text.strip())
        cardDetail.append(td.text.strip())
        #cardDetail.append(td.find_next('td').text.strip())
        
#Carta sin Habilidad#            
else: 
    #print('No tengo')
    cardDetail.append('Sin Habilidad')
    more_details = card_tables[1].find('tr', class_='table_body_black')
    #print(more_details)
    for td in more_details.find('td'):
        cardDetail.append(td.text.strip())
        cardDetail.append(td.find_next('td').text.strip())
 
    card_history = card_tables[2].find('tr', class_='table_body_black')
    #print(more_details)
    for td in card_history.find('td'):
        #print(td.text.strip())
        cardDetail.append(td.text.strip())
        
        
#print(cardDetail)


# In[ ]:





# In[ ]:




