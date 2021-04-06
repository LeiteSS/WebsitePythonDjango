# Site desenvolvido usando a linguagem Python e o framework Django

**Objetivo:** Neste site será registrado frases em inglês que o usuário deverá traduzir

## Fases do Desenvolvimento

Após instalar o framework Django, é necessário começar um projeto usando o comando:
`$django-admin startproject <nomedosite>`

o projeto criado terá este formato:

mysite/
|---manage.py
|---mysite/
|---|---__init__.py
|---|---settings.py
|---|---urls.py
|---|---wsgi.py

Estes arquivos são:

**manage.py:** Permite interagir com o projeto Django em varias formas, através de linha-de-comando.
**mysite/__init__.py:** Um arquivo vazio que diz para o Python que este diretorio deve ser considerado como um pacote Python.
**mysite/settings.py:** Arquivo que permite configurar o projeto Django.
**mysite/urls.py:** Pode se dizer que este arquivo é uma "tabela de conteúdo", lugar onde as URLs são declaradas.
**mysite/wsgi.py:** Um ponto de entrado para o ***WSGI-compatible web server*** para o projeto.

Após entender os documentos que configuram o projeto, atráves da linha de comando a pasta com o website em si é criado: `$py manage.py startapp polls`

***polls*** também pode ser chamado de ***main***.

A estrutura da pasta polls será esta:

polls/
|---__init__.py
|---admin.py
|---apps.py
|---migrations/
|---|---__init__.py
|---models.py
|---tests.py
|---views.py

Contudo, nesta pasta é criado o documento urls.py para que as telas/views sejam declaradas. Embora tenha mais algumas etapas no 
desenvolvimento, pode ser dado o comando abaixo: `$py manage.py runserver`

Entretanto, é possivel conferir se o banco de dados está correto com o comando: `$py manage.py makemigrations polls`

ou mesmo com o comando: `$py manage.py shell`

Dentro do shell, siga este algoritmo, afim de ser realizado teste para conferir o banco de dados:

```
>>> from polls.models import Pergunta, Resposta  # Importa as classes modelos
>>> Pergunta.objects.all()
>>> aqui é esperado os objetos cadastrados
>>> Resposta.objects.all()</strong>
>>>aqui é esperado os objetos cadastrados
```

`



