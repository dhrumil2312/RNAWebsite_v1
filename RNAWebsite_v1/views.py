from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from RNAWebsite_v1.forms import *
from RNAWebsite_v1.models import *
from pytz import timezone

import os
from django.conf import settings
import urllib.parse
import datetime
import ENTRNA
import ReadCtFile

from QLRNA.QLRNA import *
from GeneratePlot.plot_percentile import plot_per


format = "%Y-%m-%d %H:%M:%S"


def saveResults(seq,struct,f,e,mf,mf_s):
    resultDataObject = Entrna_Resutls()
    resultDataObject.sequence = seq
    resultDataObject.structure = struct
    resultDataObject.foldability = f
    resultDataObject.e = e
    resultDataObject.mf = mf
    resultDataObject.mf_s = mf_s
    resultDataObject.save()
    return


def saveObject(sequence, structure):
    inputDataObject = UserInput()  # model object
    inputDataObject.inputText = sequence
    inputDataObject.structure = structure
    inputDataObject.timestamp = datetime.datetime.now().astimezone(timezone('US/Arizona'))
    inputDataObject.save()
    return


def saveInputObjectQLRNA(structure, emailId):
    inputDataObject = QLRNA_Input()  # model object
    inputDataObject.structure = structure
    inputDataObject.emailId = emailId
    inputDataObject.timestamp = datetime.datetime.now().astimezone(timezone('US/Arizona'))
    inputDataObject.save()
    return


def check_constraints(sequence, structure):
    valid_comb = []
    invalid_comb = []
    for seq, struct in zip(sequence, structure):
        if len(seq) != len(struct):
            invalid_comb.append([seq, struct])
        elif struct.count('(') != struct.count(')'):
            invalid_comb.append([seq, struct])
        elif len(set(seq).union(set('AUGC'))) != 4:
            invalid_comb.append([seq, structure])
        else:
            valid_comb.append([seq, struct])

    return valid_comb, invalid_comb


def sendEmail(emailId, sequence, structure, result):
    to_email = emailId
    subject = "Results for the sequence submitted"
    from_email = settings.DEFAULT_FROM_EMAIL
    r_email = [to_email]
    body = "Hey there you received the result of the sequence submitted. \n"
    content = ""
    for seq, struct, fold in zip(sequence, structure, result):
        content += "Sequence submitted : " + seq + " \n Structure submitted : " + struct + " \n Foldability of the sequence :" + str(
            fold) + ".\n\n"

    send_mail(subject=subject, from_email=from_email, recipient_list=r_email, message=body + content,
              fail_silently=False)
    return

# Below file content function is only for ENTRNA
def fileContent(file, batchMode=False, ctFile=False):
    fileSystem = FileSystemStorage()
    filename = fileSystem.save(file.name, file)
    uploaded_file_url = fileSystem.url(filename)
    parsed_url = urllib.parse.unquote(uploaded_file_url[7:])  # parsing the url
    fileObject = open(os.path.join(settings.MEDIA_ROOT, parsed_url), 'r')  # File reader object
    if ctFile == True:
        ctFileName = os.path.join(settings.MEDIA_ROOT, parsed_url)
        sequence , structure = ReadCtFile.read_ct_files(ctFileName)
        return sequence, structure
    if batchMode == False :
        data = fileObject.readline()
        return data
    else:
        sequence = fileObject.readline().replace("\n", "").split(",")
        structure = fileObject.readline().replace("\n", "").split(",")
        return sequence, structure


#Below file content function is for QLRNA

def fileContentQLRNA(file, batchMode = False):
    fileSystem = FileSystemStorage()
    filename = fileSystem.save(file.name, file)
    uploaded_file_url = fileSystem.url(filename)
    parsed_url = urllib.parse.unquote(uploaded_file_url[7:])  # parsing the url
    fileObject = open(os.path.join(settings.MEDIA_ROOT, parsed_url), 'r')
    if batchMode == False:
        structure = fileObject.readline()
        return structure
    else:
        structure = fileObject.readline().replace("\n", "").split(",")
        return structure


def mainpage(request):
    if request.method == "GET":
        return render(request, "index.html", {})


def qlRNA(request):
    if request.method == "GET":
        return render(request, "qlrna.html", {})
    else:
        print(request.POST)
        print(request.FILES)

        qlrnaTextForm = QLRNA_text(request.POST)
        qlrnaFileForm = QLRNA_file(request.POST, request.FILES)

        qlrnaBatchMode = QLRNA_BatchMode(request.POST, request.FILES)

        batchMode = False
        structure_list = list()
        if qlrnaTextForm.is_valid():
            structure = qlrnaTextForm.cleaned_data['structure']
            emailID = qlrnaTextForm.cleaned_data['emailId']


        elif qlrnaFileForm.is_valid():
            file = request.FILES['structureFile']
            emailID = qlrnaFileForm.cleaned_data['emailId']
            structure = fileContentQLRNA(file)

        elif qlrnaBatchMode.is_valid():
            batchMode = True
            file = request.FILES['structureBatchMode']
            emailID = qlrnaBatchMode.cleaned_data['emailId']
            structure_list = fileContentQLRNA(file , batchMode= True)

        if batchMode == False:
            structure_list.append(structure)

        sequence_list = list()
        errorMessage = ""
        isError = False

        for i in structure_list:
            try:
                saveInputObjectQLRNA(i,emailID)
                sequence = qlrna(i)
                sequence_list.append(sequence)
            except (RuntimeError, TypeError, NameError, ValueError):
                errorMessage="Error in the structure submitted"
                isError = True


        allContent = zip(structure_list , sequence_list)

        invalid = list()

        content = {
            "allContent": allContent,
            "submitted_time": datetime.datetime.now().strftime(format),
            "invlaid": invalid,
            "errorMessage" : errorMessage,
            "isError" : isError

        }
        return render(request, "resultsQTRNA.html", content)


def rnaModeler(request):
    global structure
    if request.method == "GET":
        return render(request, "entrna.html", {})
    else:
        print(request.POST)
        print(request.FILES)
        batchMode = ENTRNA_BatchMode(request.POST, request.FILES)
        bothText = BothTextData_Form(request.POST)
        ctform = CTForm(request.POST, request.FILES)

        batch_mode = False
        sequence_list = list()
        structure_list = list()

        print(bothText.is_valid())
        print(bothText)

        if bothText.is_valid():
            print("Both text Called")
            sequence = bothText.cleaned_data['sequence']
            structure = bothText.cleaned_data['structure']
            emailId = bothText.cleaned_data['emailId']

        elif ctform.is_valid():
            print("In CT form")
            file = request.FILES['ct_file']
            emailId = ctform.cleaned_data['ct_emailId']
            sequence, structure = fileContent(file, ctFile=True)
            print(sequence)
            print(structure,"structure--------------------------")

        elif batchMode.is_valid():
            print("In BatchMode")
            batch_mode = True
            file = request.FILES['file']
            sequence_list, structure_list = fileContent(file, batchMode=True)
            emailId = batchMode.cleaned_data['emailId']
            if len(sequence_list) != len(structure_list):
                return render(request, "entrna.html", {"<p> Different number of Sequence and Structure Entered. </p>"})

        if batch_mode == False:
            sequence_list.append(sequence)
            structure_list.append(structure)

        print(sequence_list, structure_list)

        valid, invalid = check_constraints(sequence_list, structure_list)
        print(valid, invalid)
        fold = list()
        fe = list()
        mfe = list()
        mfe_struct = list()
        #script_list = list()
        #div_list = list()
        for seq, struct in valid:
            saveObject(seq, struct)
            f, e, mf, mf_s = ENTRNA.calculateFoldability(seq, struct)
            fold.append(f)
            fe.append(e)
            mfe.append(mf)

            mfe_struct.append(mf_s)
            saveResults(seq,struct,f,e,mf,mf_s)

        script, div = plot_per(fold)
        # sendEmail(emailId, sequence_list, structure_list, fold)

        allContent = zip(sequence_list, structure_list, fold, fe, mfe, mfe_struct )
        content = {"allContent": allContent,
                   "submitted_time": datetime.datetime.now().strftime(format),
                   "invalid" : invalid,
                   "script": script,
                   "div": div}



        return render(request, "resultsENTRNA.html", content)


def contactUs(request):
    return render(request, "contact_us.html", {})
