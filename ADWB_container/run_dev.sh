docker run -it --rm \
    -p 7200:7200 \
    -p 8080:8080 \
    -p 5000:5000 \
    -v $(pwd)/../management_webpage/flaskr:/app/flaskr \
    -e "TRIPLIFIER_LOCATION=http://localhost:8080" \
    -v $(pwd)/container_run.sh:/run.sh \
    --entrypoint=/bin/bash \
    jvsoest/adwb