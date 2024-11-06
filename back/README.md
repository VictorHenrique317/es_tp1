sudo docker build -t meetinglm_image:latest .

sudo docker run --name meetinglm_container -p 80:80 meetinglm_image

FastAPI rodando na porta 80
caso queira ver um postman do FastAPI bem legal, abra http://localhost:80/docs no navegador