from django.shortcuts import render
from .forms import CSVUploadForm
import logging
from .file_service import determine_encoding
import pandas
import io


log = logging.getLogger('django')

def upload_csv(request):
    columns = None
    context = None
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            blob = uploaded_file.read()
            encoding = determine_encoding(blob)
            data_frame = pandas.read_csv(io.StringIO(blob.decode(encoding)),delimiter=',')
            columns = [{'field': f, 'title': f} for f in data_frame.head()]
            context = {
                'form': form,
                'data': data_frame,
                'columns': columns
                }
            return render(request, 'index.html', context)
        else:
            return render(request, 'index.html', None)
    else:
        context = {
             'form': CSVUploadForm(),
            }
        return render(request, 'index.html', context)
