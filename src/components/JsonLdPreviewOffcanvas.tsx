import React, { useState, useEffect } from 'react';
import { Offcanvas } from 'react-bootstrap';
import hljs from 'highlight.js';
import 'highlight.js/styles/github.min.css';

const JsonLdPreviewOffcanvas = ({ isOpen, onToggle, jsonLdObject }) => {
  const [jsonLdContent, setJsonLdContent] = useState("");

  useEffect(() => {
    if (isOpen && jsonLdObject) {
        const formattedJsonLd = JSON.stringify(jsonLdObject, null, 2);
        const highlightedJson = hljs.highlight(formattedJsonLd, { language: 'json' }).value;
        setJsonLdContent(highlightedJson);
    }
  }, [jsonLdObject, isOpen]);

  return (
    <Offcanvas show={isOpen} onReveal={onToggle} onHide={onToggle} placement="end" scroll={true} backdrop={false}>
        <div className="offcanvas-header d-flex justify-content-between">
          <div className="offcanvas-title h5">JSON-LD Preview</div>
          <button type="button" className="btn-close" aria-label="Close" onClick={onToggle}></button>
        </div>
      <Offcanvas.Body>
        <div className="overflow-auto" style={{ maxHeight: 'calc(100vh - 200px)' }}>
          <div className="card">
            <div className="card-body">
              <pre><code dangerouslySetInnerHTML={{ __html: jsonLdContent }} /></pre>
            </div>
          </div>
        </div>
      </Offcanvas.Body>
    </Offcanvas>
  );
};

export default JsonLdPreviewOffcanvas;