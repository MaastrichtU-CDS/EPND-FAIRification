## Copy webapp folder here
cp -R ../management_webpage ./app

rm -Rf app/cedar_embeddable_editor/cedar-embeddable-editor-release-2.6.18/node_modules
rm -Rf app/node_modules
rm -Rf app/venv

## build the actual container
docker build -t ghcr.io/maastrichtu-cds/epnd-fairification/adwb:single --no-cache ./

## Remove temp webapp folder
rm -Rf ./app

docker run -it --rm \
    -p 7200:7200 \
    -p 8080:8080 \
    -p 5000:5000 \
    -e "TRIPLIFIER_LOCATION=http://fairnotator-single-triplifier-epnd.apps.dsri2.unimaas.nl" \
    ghcr.io/maastrichtu-cds/epnd-fairification/adwb:single-quick-build