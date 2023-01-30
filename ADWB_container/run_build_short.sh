## Copy webapp folder here
cp -R ../management_webpage ./app

rm -Rf app/cedar_embeddable_editor/cedar-embeddable-editor-release-2.6.18/node_modules
rm -Rf app/node_modules
rm -Rf app/venv

## build the actual container
docker build -t jvsoest/adwb --no-cache ./

## Remove temp webapp folder
rm -Rf ./app

# docker run -it --rm \
#     -p 7200:7200 \
#     -p 8080:8080 \
#     -p 5000:5000 \
#     jvsoest/adwb