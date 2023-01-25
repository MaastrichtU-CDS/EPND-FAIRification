## build triplifier
sudo rm -f triplifier*.jar # clean old build first

git clone --recurse-submodules https://github.com/MaastrichtU-CDS/triplifier-boot
cd triplifier-boot
docker run --rm -it \
    -v $(pwd):/triplifier-boot \
    -v $(pwd)/../build_triplifier_boot.sh:/triplifier-boot/build.sh \
    --workdir /triplifier-boot \
    maven:3.8-eclipse-temurin-11 /bin/bash build.sh
sudo mv target/triplifier-boot-0.0.1-SNAPSHOT.jar ../triplifier-boot-0.0.1-SNAPSHOT.jar
cd ../ && sudo rm -Rf triplifier-boot

## Do final container build
sh run_build_short.sh