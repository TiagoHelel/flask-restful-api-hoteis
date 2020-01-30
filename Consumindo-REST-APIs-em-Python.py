cursodeflask@2

#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import requests


# # GET /hoteis

# In[2]:


URL = 'http://127.0.0.1:5000'


# In[106]:


resposta_hoteis = requests.request('GET', URL + '/hoteis?cidade=Santos')


# In[61]:


resposta_hoteis.status_code


# In[62]:


hoteis = resposta_hoteis.json()


# In[107]:


hoteis


# In[7]:


hoteis['hoteis'][0]


# In[8]:


len(hoteis['hoteis'])


# In[9]:


lista_hoteis = hoteis['hoteis']


# In[10]:


for hotel in lista_hoteis:
    print(hotel['nome'])


# # Mercado Livre

# In[11]:


ML_URL = 'https://api.mercadolibre.com/sites'


# In[12]:


ML_URL = 'https://api.mercadolibre.com/sites/MLB/categories'


# In[13]:


lista_sites = requests.request('GET', ML_URL)


# In[14]:


lista_sites


# In[15]:


lista_sites.json()


# # POST /cadastro

# In[16]:


endpoint_cadastro = URL + '/cadastro'


# In[17]:


endpoint_cadastro


# In[18]:


body_cadastro = {
    'login': 'danilo',
    'senha': 'abc123'
}


# In[19]:


headers_cadastro = {
    'Content-Type': 'application/json'
}


# In[20]:


resposta_cadastro = requests.request('POST', endpoint_cadastro, json=body_cadastro, headers=headers_cadastro)


# In[21]:


resposta_cadastro.status_code


# In[22]:


resposta_cadastro.json()


# # /login

# In[23]:


endpoint_login = URL + '/login'


# In[24]:


endpoint_login


# In[25]:


body_login = {
    'login': 'danilo',
    'senha': 'abc123'
}


# In[26]:


headers_login = {
    'Content-Type': 'application/json'
}


# In[96]:


resposta_login = requests.request('POST', endpoint_login, json=body_login, headers=headers_login)


# In[97]:


resposta_login.status_code


# In[98]:


token = resposta_login.json()


# In[99]:


token['access_token']


# # CRUD /hoteis/{hotel_id}

# In[82]:


endpoint_hotel_id = URL + '/hoteis/meuhotel2'


# In[83]:


endpoint_hotel_id


# In[84]:


body_hotel_id = {
    'nome': 'Meu Hotel Alterado',
    'estrelas': 4.8,
    'diaria': 398.90,
    'cidade': 'Santos'
}


# In[100]:


headers_hotel_id = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token['access_token']
}


# In[ ]:


# resposta_hotel_id = requests.request('POST', endpoint_hotel_id, json=body_hotel_id, headers=headers_hotel_id)


# In[101]:


# resposta_hotel_id = requests.request('PUT', endpoint_hotel_id, json=body_hotel_id, headers=headers_hotel_id)


# In[102]:


# resposta_hotel_id = requests.request('GET', endpoint_hotel_id)


# In[103]:


resposta_hotel_id = requests.request('DELETE', endpoint_hotel_id, headers=headers_hotel_id)


# In[104]:


resposta_hotel_id


# In[105]:


resposta_hotel_id.json()


# In[ ]:





# # /usuarios/{user_id}

# In[118]:


endpoint_user_id = URL + '/usuarios/5'


# In[119]:


endpoint_user_id


# In[120]:


headers_user_id = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token['access_token']
}


# In[130]:


resposta_user_id = requests.request('GET', endpoint_user_id)


# In[131]:


# resposta_user_id = requests.request('DELETE', endpoint_user_id, headers=headers_user_id)


# In[132]:


resposta_user_id.status_code


# In[133]:


resposta_user_id.json()


# In[ ]:




