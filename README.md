# README #

this is an implementation of the digitiamo test

* Version 0.0.1



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
non ho implementato i due grafici con lo pagina a scomparsa
il layout è simile ma non perfettamente identico a quello delle immagini del pdf
non ho scritto i test per la parte di frontend

## Backend

Per il backend ho usato
Python 3.8
Flask
sqllite
pytest (per i test)
FLASK-CORS
ho usato requirements per le  chiamate verso gli url passati alle API. durante lo sviluppo ho scoperto che requiremnts supporta solo HTTP/1.1. Per poter utilizzare HTTP/2 avrei potuto usare una liberia di più basso livello come urllib e reimplementare alcune feature come il redirect. Purtroppo ho seguito un'altra strada usando un Adapter per requirements fornito da un'altra libreria (hyper) .purtroppo questa versione è in alfa per cui ho una patch a hyper per farlo funzionare veramente con requirements. La patch è in 
    
    backend/hyper_monkey_patch.py

per evitare DDOS e abusi da un unico IP ho implementato una piccola coda che trovate in 

    backend/helpers.py

###lanciare il backend

come sempre consiglio di usare un virtual env  
        
        cd backend
        python -m venv myenv 
        source myenv/bin/activate
        pip install -r requirements.txt
        FLASK_ENV=development flask run
        
due piccoli db sql3 sono compresi nel repository. Si dovesse servire creare un db vuoto si può usare il comando di flask-alembic

    FLASK_ENV=development flask db upgrade
    
o per il db di test

    FLASK_ENV=testing flask db upgrade
    
### lanciare i test

i test coprono la API principale ('/api/v1.0/request_url/<method>')
e il buffer delle chiamate. suno un po' leenti perché testano anche il timeout sulle chimate numerose e su quelle dallo stesso indirizzo.
    
    cd backend
    pytest    
