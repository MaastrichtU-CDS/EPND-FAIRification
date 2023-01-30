version='2.6.18'
os=$(uname -s)

sed=sed
if [[ $os == "Darwin" ]]; then
    sed=gsed
fi
echo $sed

cd "$( dirname "${BASH_SOURCE[0]}" )"

rm -Rf cedar-embeddable-editor*
rm -Rf release-*.zip

# Download and unzip release version of CEE
curl -L -o release-$version.zip https://github.com/metadatacenter/cedar-embeddable-editor/archive/refs/tags/release-$version.zip
unzip release-$version.zip

# Override files needed to work in our situation
cp app.component.ts cedar-embeddable-editor-release-$version/src/app/app.component.ts
cp app.module.ts cedar-embeddable-editor-release-$version/src/app/app.module.ts

# Build project
cd cedar-embeddable-editor-release-$version
$sed -i "/this.messageHandlerService.traceObject/ a window.location.href = '\\/metadata';" src/app/modules/shared/components/cedar-data-saver/cedar-data-saver.component.ts
npm install
node_modules/@angular/cli/bin/ng build --configuration production --baseHref="/static/cee/"

rm -Rf node_modules/

# # Copy to flaskr
rm -R ../../flaskr/static/cee
mkdir -p ../../flaskr/static/cee
cp -R dist/cedar-embeddable-editor/* ../../flaskr/static/cee/
cp ../../flaskr/static/cee/index.html ../../flaskr/templates/cedar/add.html
