## build triplifier
git clone --recurse-submodules https://github.com/MaastrichtU-CDS/triplifier-boot
cd triplifier-boot
docker run --rm -it \
    -v $(pwd):/triplifier-boot \
    -v $(pwd)/../build_triplifier_boot.sh:/triplifier-boot/build.sh \
    --workdir /triplifier-boot \
    maven:3.6.0-jdk-11-slim /bin/bash build.sh

cp -R ../management_webpage ./app

## build the actual container
docker build -t jvsoest/adwb ./

rm -Rf ./app

docker run -it --rm \
    --entrypoint /bin/bash \
    -p 7200:7200 \
    jvsoest/adwb
