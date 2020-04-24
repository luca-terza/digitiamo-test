# README #

this is an implementation of the digitiamo test

* Version 0.1.0



## FRONTEND
    
Per il frontend ho usato 
    
* vuejs (è la prima volta che lo uso)
* vue bootstrap 
* sccs
* axios   

### Per lanciare il frontend 
    
       cd frontend
       npm install
       npm run dev
### cosa non c'è
* non ho implementato i due grafici con lo pagina a scomparsa
* il layout è simile ma non perfettamente identico a quello delle immagini del pdf
* non ho scritto i test per la parte di frontend

## Backend

Per il backend ho usato
* Python 3.8
* Flask
* sqllite
* pytest (per i test)
* flask-cors

Ho usato la libreria *requests* per le chiamate verso gli url passati alle API. durante lo sviluppo ho scoperto che *requests* supporta solo HTTP/1.1. Per poter utilizzare HTTP/2 avrei potuto usare una liberia di più basso livello come urllib e reimplementare alcune feature come il redirect, ma ho seguito un'altra strada usando un adapter per *requests* fornito dlla libreria hyper. Purtroppo questa versione è in beta e mi ha tradito: Ho dovuto creare patch a hyper per farlo funzionare veramente con *requests*. La patch è in 
    
    backend/hyper_monkey_patch.py

Per evitare DDOS e abusi da un unico IP ho implementato una piccola coda che trovate in 

    backend/helpers.py

###lanciare il backend

        
        cd backend
        python -m venv myenv # se volete usare un virtual env e python3 se siete macOS        
        source myenv/bin/activate
        pip install -r requirements.txt
        FLASK_ENV=development flask run
        
due piccoli db sql3 sono compresi nel repository. Non li lascerei normalmente, ma in quesyo caso mi pare che semplifichino l'installazione.

Se dovesse servire creare un db vuoto si può usare il comando di flask-alembic

    FLASK_ENV=development flask db upgrade
    
o per il db di test

    FLASK_ENV=testing flask db upgrade
    
### lanciare i test

I test coprono l'API */api/v1.0/request_url/<method>*
e il buffer delle chiamate. 
Sono un po' lenti perché testano anche il timeout sulle chiamate massive e su quelle dallo stesso indirizzo IP.
    
    cd backend
    pytest    
