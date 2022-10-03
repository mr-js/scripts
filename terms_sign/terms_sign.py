import os
import time
import tempfile
import PyPDF2
import datetime
from reportlab.pdfgen import canvas
import configparser


def _get_tmp_filename(suffix=".pdf"):
    with tempfile.NamedTemporaryFile(suffix=".pdf") as fh:
        return fh.name


def main():
    # read common config
    config = configparser.RawConfigParser()
    config.read('terms_sign.ini')
    terms_source = str(config.get('SOURCE', 'TermsSource'))
    stamp_image = str(config.get('SOURCE', 'StampImage'))
    stamp_height = int(config.get('SOURCE', 'StampHeight'))
    stamp_width = int(config.get('SOURCE', 'StampWidth'))    
    sign_image = str(config.get('SOURCE', 'SignImage'))
    sign_height = int(config.get('SOURCE', 'SignHeight'))
    sign_width = int(config.get('SOURCE', 'SignWidth'))
    # read targets config
    fig_queries = []
    fig_p = 0; fig_x = 0; fig_y = 0; fig_w = 0; fig_h = 0; fig_i = ''
    for section_name in config:
        if 'SOURCE' not in section_name and 'DEFAULT' not in section_name:
            fig_p = int(config.get(section_name, 'Page'))
            fig_x = int(config.get(section_name, 'X'))
            fig_y = int(config.get(section_name, 'Y'))
            if 'Stamp' in str(config.get(section_name, 'Type')):
                fig_w = stamp_width
                fig_h = stamp_height
                fig_i = stamp_image
            else:
                fig_w = sign_width
                fig_h = sign_height
                fig_i = sign_image
            # create targets querie: page, image, x, y, width, height
            fig_queries.append({'p': fig_p, 'i': fig_i, 'x': fig_x, 'y': fig_y, 'w': fig_w, 'h': fig_h})
    # prepare engine
    output_filename = "{}_signed.pdf".format(terms_source)
    pdf_fh = open(terms_source, 'rb')
    sig_tmp_fh = None
    pdf = PyPDF2.PdfFileReader(pdf_fh)
    writer = PyPDF2.PdfFileWriter()
    sig_tmp_filename = None
    # create sign/stamp
    for i in range(0, pdf.getNumPages()):
        page = pdf.getPage(i)
        page_figs = list(fig for fig in fig_queries if i == fig.get('p')-1)
        if page_figs != []:
            # create pdf
            sig_tmp_filename = _get_tmp_filename()
            c = canvas.Canvas(sig_tmp_filename, pagesize=page.cropBox)
            # print sign/stamp on page
            for fig in page_figs:
                c.drawImage(fig.get('i'), fig.get('x'), fig.get('y'), fig.get('w'), fig.get('h'))
            c.showPage()
            c.save()
            # merge pdf
            sig_tmp_fh = open(sig_tmp_filename, 'rb')
            sig_tmp_pdf = PyPDF2.PdfFileReader(sig_tmp_fh)
            sig_page = sig_tmp_pdf.getPage(0)
            sig_page.mediaBox = page.mediaBox
            sig_page.mergePage(page)
        else:
            sig_page = page
        writer.addPage(sig_page)
    # flash changes
    with open(output_filename, 'wb') as fh:
        writer.write(fh)
    for handle in [pdf_fh, sig_tmp_fh]:
        if handle:
            handle.close()
    if sig_tmp_filename:
        os.remove(sig_tmp_filename)


if __name__ == "__main__":
    main()
