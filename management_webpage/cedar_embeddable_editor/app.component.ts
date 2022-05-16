import {Component} from '@angular/core';

@Component({
  selector: 'app-component',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {

  ceeConfig = {
    showTemplateUpload: false,                              //do not show template upload option
    //templateUploadBaseUrl: 'http://localhost:8000',
    // templateUploadBaseUrl: 'https://api-php.cee.metadatacenter.orgx',
    //templateUploadEndpoint: '/upload.php',
    //templateDownloadEndpoint: '/download.php',
    //templateUploadParamName: '3520cf061bba4919a8ea4b74a07af01b',
    //templateDownloadParamName: '9ff482bacac84c499655ab58efdf590a',

    showDataSaver: true,
    dataSaverEndpointUrl: 'http://localhost:5000/api/cedar/store',

    sampleTemplateLocationPrefix: 'http://localhost:5000/api',
    // sampleTemplateLocationPrefix: 'https://component.staging.metadatacenter.org/cedar-embeddable-editor-sample-templates/',
    loadSampleTemplateName: 'cedar',                          //folder where template.json should be stored
    showSampleTemplateLinks: false,                          //shows template selection box
    expandedSampleTemplateLinks: false,                      //not sure what this one does? disabled for now
    showTemplateRenderingRepresentation: false,               //hide template render info for production

    // terminologyProxyUrl: 'https://api-php.cee.metadatacenter.orgx/index.php',
    // terminologyProxyUrl: 'http://localhost:8000/index.php',
    terminologyProxyUrl: 'https://terminology.metadatacenter.org/bioportal/integrated-search',
    showInstanceDataCore: false,                             //hide JSON-LD output core data for production
    showMultiInstanceInfo: false,

    collapseStaticComponents: false
  };

}