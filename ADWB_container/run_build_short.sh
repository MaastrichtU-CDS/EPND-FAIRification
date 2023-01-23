## Copy webapp folder here
cp -R ../management_webpage ./app

## build the actual container
docker build -t jvsoest/adwb ./

## Remove temp webapp folder
rm -Rf ./app

docker run -it --rm \
    -p 7200:7200 \
    -p 8080:8080 \
    -p 5000:5000 \
    jvsoest/adwb