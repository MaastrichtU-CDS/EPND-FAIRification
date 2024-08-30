import React from 'react';
import moment from 'moment';

function DateFormatSelect({ selectedFormat, onSelectChange }) {
  const dateFormats = [
    'YYYY-MM-DD',
    'YYYY/MM/DD',
    'DD-MM-YYYY',
    'DD/MM/YYYY',
    'MM-DD-YYYY',
    'MM/DD/YYYY',
    'YYYY-MM-DD HH:mm',
    'YYYY/MM/DD HH:mm',
    'DD-MM-YYYY HH:mm',
    'DD/MM/YYYY HH:mm',
    'MM-DD-YYYY HH:mm',
    'MM/DD/YYYY HH:mm',
    'YYYY-MM-DD hh:mm A',
    'YYYY/MM/DD hh:mm A',
    'DD-MM-YYYY hh:mm A',
    'DD/MM/YYYY hh:mm A',
    'MM-DD-YYYY hh:mm A',
    'MM/DD/YYYY hh:mm A',
    'dddd, MMMM Do YYYY',
    'ddd, MMMM D, YYYY',
    'dddd, MMM D, YYYY',
    'ddd, MMM D, YYYY',
    'MMMM Do, YYYY',
    'MMM Do, YYYY',
    'MMMM D, YYYY',
    'MMM D, YYYY',
    'dddd, MMMM Do YYYY, h:mm:ss a',
    'ddd, MMMM D, YYYY, h:mm:ss a',
    'dddd, MMM D, YYYY, h:mm:ss a',
    'ddd, MMM D, YYYY, h:mm:ss a',
    'YYYYMMDD',
    'DDMMYYYY',
    'MMDDYYYY',
    'YY/MM/DD',
    'DD/MM/YY',
    'MM/DD/YY',
    'YY-MM-DD',
    'DD-MM-YY',
    'MM-DD-YY',
    'DD MMMM YYYY',
    'MMMM DD, YYYY',
    'MMMM DD YYYY',
    'DD MMM YYYY',
    'MMM DD, YYYY',
    'MMM DD YYYY',
    'DD.MM.YYYY',
    'YYYY.MM.DD',
    'YYYY-MM-DD HH:mm:ss',
    'DD-MM-YYYY HH:mm:ss',
    'MM-DD-YYYY HH:mm:ss',
    'DD/MM/YYYY HH:mm:ss',
    'MM/DD/YYYY HH:mm:ss',
    'YYYY.MM.DD',
    'DD.MM.YYYY',
    'MM.DD.YYYY',
    'YYYY.MM.DD HH:mm',
    'DD.MM.YYYY HH:mm',
    'MM.DD.YYYY HH:mm',
    'ddd, DD-MM-YYYY',
    'dddd, DD-MM-YYYY',
    'ddd, MM-DD-YYYY',
    'dddd, MM-DD-YYYY',
    'YYYY [Week] W',
    'YYYY [Week] WW',
    'YYYY-MM-DD HH:mm Z',
    'YYYY-MM-DD HH:mm ZZ',
    'YYYY-MM-DDTHH:mm:ssZ',
    'ddd, MMM D YYYY HH:mm:ss Z',
    'ddd, MMM D YYYY HH:mm:ss ZZ',
    'X',
    'x',
    'MMMM Do YYYY',
    'Do MMMM YYYY',
    'dddd, Do MMMM YYYY',
    'YYYY-MM-DDTHH:mm:ss.SSSZ',
    'ddd, D MMM YYYY HH:mm:ss Z',
    'MMMM Do, YYYY, h:mm:ss a',
    'MMMM D, YYYY, h:mm:ss a',
    'MMM D, YYYY, h:mm:ss a',
    'YYYY',
    'MMMM YYYY',
    'MMM YYYY',
  ];

  const getFormattedExample = (format) => {
    try {
      return moment().format(format);
    } catch (error) {
      return 'Invalid format';
    }
  };

  return (
    <select id="columnSelect" className="form-control" value={selectedFormat} onChange={(e) => onSelectChange(e.target.value)}>
      {dateFormats.map((format, index) => (
        <option key={index} value={format}>
          {format} ({getFormattedExample(format)})
        </option>
      ))}
    </select>
  );
}

export default DateFormatSelect;