## build triplifier
git clone --recurse-submodules https://github.com/MaastrichtU-CDS/triplifier-boot
cd triplifier-boot
docker run --rm -it \
    -v $(pwd):/triplifier-boot \
    -v $(pwd)/../build_triplifier_boot.sh:/triplifier-boot/build.sh \
    --workdir /triplifier-boot \
    maven:3.6.0-jdk-11-slim /bin/bash build.sh
mv target/triplifier-boot-0.0.1-SNAPSHOT.jar ../triplifier-boot-0.0.1-SNAPSHOT.jar
cd ../ && rm -Rf triplifier-boot

cp -R ../management_webpage ./app

## build the actual container
docker build -t jvsoest/adwb ./

rm -Rf ./app

docker run -it --rm \
    -p 7200:7200 \
    -p 8080:8080 \
    -p 5000:5000 \
    jvsoest/adwb
