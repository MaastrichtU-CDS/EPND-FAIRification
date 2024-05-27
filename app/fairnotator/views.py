import csv
from django.shortcuts import render
from .forms import CSVUploadForm
import logging


log = logging.getLogger(__name__)


def upload_csv(request):
    data = None
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            data = []
            read_csv = csv.reader(uploaded_file.read().decode('utf-8').splitlines())
            for row in read_csv:
                log.info(row)
                data.append(row)
    else:
        form = CSVUploadForm()

    context = {
        'form': form,
        'data': data
    }
    return render(request, 'index.html', context)
