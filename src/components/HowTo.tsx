import React from 'react';
import { Container, Card } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

const HowTo = () => {
    return (
      <Container className="mt-5">
        <Card className="mt-4">
          <Card.Body>
            <Card.Text>
                <h2 className="mt-3 mb-2">Adding a Terminology Sheet</h2>
                <p className="mb-3">In the left pane, copy a link to a google sheet containing the terminology to which your data will be mapped. The current version assumes a rigid structure identical to <a href="https://github.com/MaastrichtU-CDS/EPND-FAIRification/blob/main/EPNDCS1Terminology.xls" className="text-primary">this sheet</a>. You can use the url from your address bar or the share link from the google sheet, just make sure to include the 'gid=xxxxx' part of the link. This refers to the sheet/tab to be used inside the spreadsheet. If not provided, the default gid=0 will be used.</p>
                <h2 className="mt-3 mb-2">Providing Local Data</h2>
                <p className="mb-3">Either drag and drop or click and select a CSV on your local device. Columns can be added or removed as needed. The 'possible values' inputs are used for mapping categorical values in your data.</p>
                <h2 className="mt-3 mb-2">Mapping</h2>
                <p className="mb-3">Select one of the terminology entries on the left pane to start mapping. Based on the type of data, additional data can be provided such as date formats in the case of dates, units in the case of numbers or further mappings for each value in the case of categorical variables.</p>
                <h2 className="mt-3 mb-2">Exporting</h2>
                <p className="mb-3">Once all mappings are complete, click the 'Generate JSON-LD' button to export the mappings to a JSON-LD file. This file can be used as an input for further ETL processes.</p>
            </Card.Text>
          </Card.Body>
        </Card>
      </Container>
    );
  };
  
  export default HowTo;