# convert html to headless ,and change format to markdown to use in mkdocs.. 
# this is useful only in our highly customized mkdocs environment
import csv
import os
import ntpath
from bs4 import BeautifulSoup

def exec_html2headlessmd(filelist, out_dir, del_src):

    with open(filelist) as csvfile:
        ipynb_reader = csv.reader(csvfile)

        # for each file, create respective md in out_dir
        for each_row in ipynb_reader:

            current_file =  each_row[0]
            with open(current_file, 'rb') as html_file:
                html_contents = html_file.read().decode('utf8')  

            # strip
            html_soup = BeautifulSoup(html_contents, features="html5lib")
            [s.extract() for s in html_soup('head')]
            headless_html = str(html_soup)
            headless_html = headless_html.replace('<!DOCTYPE html>\n<html>\n<body>','')
            headless_html = headless_html.replace('</body></html>','')
            k = headless_html.rfind('</div>')
            headless_html = headless_html[:k]
            k = headless_html.rfind('</div>')
            headless_html = headless_html[:k]

            # export
            inname = ntpath.basename(current_file)
            outname = inname.split('.html')[0] + '.md'
            outpath = os.path.join(out_dir,outname)
            print("\nInput:{} \nOutput:{} \nPath:{}".format(inname, outname, outpath))
            with open(outpath, 'w', encoding='utf8') as output_file:
                output_file.write(headless_html)  

            #delte source
            if del_src:
                cur_dir = os.path.dirname(current_file)
                cur_path = os.path.join(cur_dir,current_file)
                os.remove(cur_path)
                print('Deleted: {}'.format(cur_path))



# MAIN..
# https://stackoverflow.com/questions/11604653/add-command-line-arguments-with-flags-in-python3
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-fl", "--filelist",dest ="filelist", help="Enter file containing list of notebooks to be processed", nargs='?' , default='list_html.csv')
parser.add_argument("-o", "--out_dir",dest ="out_dir", help="Enter output directory where htmls should go", nargs='?' , default=os.getcwd())
parser.add_argument("-d", "--del_src",dest ="del_src", help="Enter if source files to be deleted after conversion", nargs='?' , default=False)
args = parser.parse_args()
print( "File list: {} \nOutput Dir: {}".format(args.filelist, args.out_dir))

print('Calling the html to headless md converter..')
exec_html2headlessmd(args.filelist, args.out_dir, args.del_src)
print('Coversion finished!')
