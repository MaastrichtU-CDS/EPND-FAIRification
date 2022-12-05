docker build -t jvsoest/adwb ./

docker run -it --rm \
    --entrypoint /bin/bash \
    -p 7200:7200 \
    jvsoest/adwb
