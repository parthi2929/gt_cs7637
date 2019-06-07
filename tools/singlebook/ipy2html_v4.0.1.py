"""
1. Read the list of .ipynb files from list_ipynb.csv in same folder
2. For each file, create respective html 
3. Fix 100% width issue for SVG element (CSS) for each html
4. write html in current folder (could also write in origin folder)
"""

import nbformat
import nbconvert
import sys
import os
import ntpath
import csv

def exec_ipy2html(filelist, out_dir, gen_report):
    # 1. Read the list of .ipynb files from list_ipynb.csv in same folder
    result_paths = []
    with open(filelist) as csvfile:
        ipynb_reader = csv.reader(csvfile)
        for each_row in ipynb_reader:
            current_file =  each_row[0]
            # print(current_file)

            """
            2. For each file, create respective html 
            https://github.com/jupyter/nbconvert/issues/699
            """
            with open(current_file, 'rb') as nb_file:
                nb_contents = nb_file.read().decode('utf8')  

            # Convert using the ordinary exporter
            notebook = nbformat.reads(nb_contents, as_version=4)      
            inname = ntpath.basename(current_file)
            # outpath = os.path.dirname(current_file) # let outpath be selected by user..
            outname = inname.split('.ipynb')[0] + '.html'            
            outpath = os.path.join(out_dir,outname)  # outputting in same folder as ipynb file 
            print("\nInput:{} \nOutput:{} \nPath:{}".format(inname, outname, outpath))
            result_paths.append(outpath)  # to write list of htmls in a file
            exporter = nbconvert.HTMLExporter()
            exporter.template_file = 'hidecode.tpl'  # if you hide any code in notebook, we hide in output html too
            body, res = exporter.from_notebook_node(notebook)        

            # Create a list saving all image attachments to their base64 representations
            images = []
            for cell in notebook['cells']:
                if 'attachments' in cell:
                    attachments = cell['attachments']
                    for filename, attachment in attachments.items():
                        for mime, base64 in attachment.items():
                            # print(len(base64))
                            images.append( [f'attachment:{filename}', f'data:{mime};base64,{base64}'] )
                            # images.append( ['attachment:{0}'.format(filename), 'data:{0};base64,{1}'.format(mime, base64)] )
            
            

            # Fix up the HTML and write it to disk
            for itmes in images:
                src = itmes[0]
                base64 = itmes[1]
                body = body.replace(f'src="{src}"', f'src="{base64}"', 1)
                # body = body.replace('src="{}"'.format(src), 'src="{}"'.format(base64), 1)  

            
            with open(outpath, 'w', encoding='utf8') as output_file:
                output_file.write(body)   

            #print('{} is done'.format(each_row[0]))   

    if gen_report == True:
        list_str = ''
        for each_html in result_paths:
            list_str += each_html + '\n'

        with open('list_html.csv','w') as output_listfile:
            output_listfile.write(list_str)


# MAIN..
# https://stackoverflow.com/questions/11604653/add-command-line-arguments-with-flags-in-python3
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-fl", "--filelist",dest ="filelist", help="Enter file containing list of notebooks to be processed", nargs='?' , default='list_ipynb.csv')
parser.add_argument("-o", "--out_dir",dest ="out_dir", help="Enter output directory where htmls should go", nargs='?' , default=os.getcwd())
parser.add_argument("-g", "--gen_report",dest ="gen_report", help="Enter if html file list needed", nargs='?' , default=True)
args = parser.parse_args()
print( "File list: {} \nOutput Dir: {}".format(args.filelist, args.out_dir))

print('\nWARNING: ENSURE YOUR ATTACHMENT IMAGES IN NOTEBOOK ARE NAMED DIFFERENTLY. THIS WILL HAPPEN IF YOU DIRECTLY PASTED IN NOTEBOOK. INSTEAD RENAME AND PASTE\n')
print('Calling the notebook to html converter..')
exec_ipy2html(args.filelist, args.out_dir, args.gen_report)
print('Coversion finished!')