from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .huffman_class import HuffmanCoding as HuffmanCoding
import os
import zipfile
import ast
from django.http import FileResponse
from .models import Contactus


def index(request):
    return render(request, 'Huffman_coding_app/index.html' )

def upload(request):
    # Deleting all the files present in the media folder
    all_file_list = os.listdir('media')
    for file in all_file_list:
        print(file)
        path = os.path.join('media', file)
        os.remove(path)
    # uploading the file and compress it and download he zip file
    try:
        if request.method == 'POST':
            uploaded_file = request.FILES['input_file']
            fs = FileSystemStorage()
            name = fs.save(uploaded_file.name,uploaded_file)
            path = "media/"+uploaded_file.name
            extension = uploaded_file.name[-3:]
            if(extension == 'txt'):
                d = {}
                h = HuffmanCoding(path,d)
                output_path ,output_path_code,zip_file_path = h.compress()
                print(output_path_code)
                print(output_path)
                print(zip_file_path)
                finalFile = open(zip_file_path, 'rb')
                return FileResponse(finalFile)
            else:
                messages.info(request,'Note: Upload ".txt" file')
                return  redirect('compression')
        else:
            messages.info(request, 'Note: Upload ".txt" file')
            return redirect('compression')
    except:
        messages.info(request,'Note: Upload ".txt" file')
        return redirect('compression')

def compression(request):
    return render(request,'Huffman_coding_app/compression.html')

def decompression(request):
    # Remove all the file from the media folder
    all_file_list = os.listdir('media')
    for file in all_file_list:
        print(file)
        path = os.path.join('media', file)
        os.remove(path)
    if request.method == 'POST':
        try:
            uploaded_code = request.FILES['zip_file']
            fs = FileSystemStorage()
            names = fs.save(uploaded_code.name,uploaded_code)
            extension = uploaded_code.name[-5:]
            if(extension == 'textc'):
                file_path = "media/" + uploaded_code.name
                with zipfile.ZipFile(file_path,'r') as zip:
                    name = zip.printdir()
                    zip.extractall()
                directory_path = "media/"
                all_file_list = os.listdir(directory_path)
                print(all_file_list)
                if(len(all_file_list ) == 0):
                    pass
                else:
                    for each_file in all_file_list:
                        if(each_file.endswith('.bin')):
                            bin_file_name = each_file
                        elif(each_file.endswith('.txt')):
                            code_file_name = each_file
                bin_file_path = "media/"+bin_file_name
                code_path = "media/"+code_file_name
                file = open(code_path, 'r')
                if file.mode == 'r':
                    contents = file.read()
                d = ast.literal_eval(contents)
                h = HuffmanCoding(bin_file_path,d)
                decompress_file = h.decompress(bin_file_path)
                print(decompress_file)
                finalFile = open(decompress_file,'rb')
                return FileResponse(finalFile,content_type="text/csv")
            else:
                messages.info(request, 'Note: Upload ".textc" file')
                return redirect('decompression')
        except:
            messages.info(request,'Note: Upload ".textc" file')
            return redirect('decompression')
    return render(request,'Huffman_coding_app/decompression.html')

def contactus(request):
    if request.method=="POST":
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        msg=request.POST.get('message','')
        contactus=Contactus(name=name,email=email,message=msg)
        contactus.save()
        messages.info(request,"We wil get back to you soon")
        return  redirect('contactus')
    return render(request,'Huffman_coding_app/contactus.html')

def aboutus(request):
    return render(request,'Huffman_coding_app/aboutus.html')