git clone --recurse-submodules https://github.com/MaastrichtU-CDS/triplifier-boot
cd triplifier-boot

cd triplifier/javaTool
mvn install

cd ../../
mvn clean package

cp target/triplifier-boot-0.0.1-SNAPSHOT.jar /output/triplifier-boot-0.0.1-SNAPSHOT.jar