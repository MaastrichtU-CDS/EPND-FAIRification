## build triplifier
sudo rm -Rf triplifier/ # clean old build first

docker run --rm -it \
    -v $(pwd)/triplifier:/output \
    -v $(pwd)/build_triplifier_boot.sh:/build.sh \
    --workdir / \
    maven:3.8-eclipse-temurin-11 /bin/bash build.sh
sudo mv triplifier/triplifier-boot-0.0.1-SNAPSHOT.jar ../triplifier-boot-0.0.1-SNAPSHOT.jar

## Do final container build
sh run_build_short.sh