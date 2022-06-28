from __future__ import division
import json
import os, csv, traceback, sys
from datetime import datetime
from os import path
import argparse
from urlparse import urlparse

#BaseLine = "C:\\Users\\ankyadav3\\PycharmProjects\\lighthouse\\Result_2020_01_22-09_20_44.csv"
#CurrentResult = "C:\\Users\\ankyadav3\\PycharmProjects\\lighthouse\\Result_2020_03_11-09_45_39.csv"


# TestUrl = 'http://www.flipkart.com'
try:
    # initiate the parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Pass Urls input csv file")

    ### Adding argument for buildnumber
    parser.add_argument("-b", "--buildnumber", help="Jenkins job will provide this input")

    parser.add_argument("-a", "--agent", default="desktop", help="Pass the Browser Type like |mobile| or |desktop|")
    parser.add_argument("-t", "--threshold", default="5", type=int, help="Pass threshold value for First Meaning full content in Seconds ")
    parser.add_argument("-q", "--quota", default="70", type=int, help="Set the Quota percentage for Test case fail or pass")
    #parser.add_argument("-b", "--baseline", help="If you want to compare the results Please provide Baseline Results File path")
    # read arguments from the command line
    args = parser.parse_args()
    #if args.baseline:
        #BaseLine = args.baseline
    #print(args.baseline)

except BaseException as baseeror:
    print(baseeror)
    exit(1)

#exit(0)
if path.isfile(args.input):
    inputfile = open(args.input, 'r')
else:
    print("input file does not exist = %s" % (args.input))
    exit(1)

Fullpath = ''
FinalHtmlFilesList = []
FinalJsonFilesList = []
thresholdValue = float(str(args.threshold).strip(' '))
Quota = args.quota
TestResult = {}
for InputfileUrls in inputfile.readlines():
    TestUrl = InputfileUrls.strip('\n')
    ResultSum = {}
    thresholdResult = {}
    try:

        if TestUrl.startswith('http'):
            #   ''''
            # emulatertype = 'desktop'      #    desktop and mobile
            emulatertype = str(args.agent).strip(' ')
            buildnumber = str(args.buildnumber).strip(' ')
            #Litehouse Arguments for headerless Jenkins run
            LitehouseArgs = "--chrome-flags='--headless --disable-gpu --disable-dev-shm-usage --no-sandbox' --config-path=/report/lighthouse-config.js --output=json --output=html"
            #LitehouseArgs = "--chrome-flags='--headless --no-sandbox' --preset="

            #Litehouse Arguments for Windows
            #LitehouseArgs = "--output=json --output=html --emulated-form-factor"
            LitehouseArgs = TestUrl + ' ' + LitehouseArgs
            #command = '~/.nvm/versions/node/v16.13.1/bin/lighthouse ' + LitehouseArgs
            command = '/usr/bin/lighthouse ' + LitehouseArgs
            print("Going to run the command \"%s\"" % (command))
            pr, iny = os.popen4(command)
            #print (pr)
            #print("Iny %s" % (iny))
            #HtmlOutputFilepath = r''
            JsonOutputFilepath = r''
            for data in iny.readlines():
                #print("data test = %s" % (data))
                if 'Printer json output written to ' in data:
                    #print("data test = %s" % (data))
                    JsonOutputFilepath = data.split('written to')[1].strip('\n').strip(' ')
                if 'Printer html output written to' in data:
                    HtmlOutputFilepath = data.split('written to')[1].strip('\n')

            # print("LightHouse test has been finished and Output file has been Created at below Path \nJsonfilepath = %s \n HTMLfilepath = %s" %(JsonOutputFilepath,HtmlOutputFilepath))
            print("LightHouse test has been finished and Output file has been Created at below Path \nJSONfilepath = %s" % (JsonOutputFilepath ))
            FinalJsonFilesList.append(JsonOutputFilepath)
            print("LightHouse test has been finished and Output file has been Created at below Path \nHTMLfilepath = %s" % (HtmlOutputFilepath ))
            FinalHtmlFilesList.append(HtmlOutputFilepath)
            # '''

            # print "Results are below"
            # JsonOutputFilepath = r'C:\Users\ankyadav3\PycharmProjects\lighthouse\www.flipkart.com_2020-01-20_11-03-22.report.json'
            RequiresAduits = ['first-contentful-paint', 'first-meaningful-paint', 'speed-index', 'interactive', 'max-potential-fid']
            JsonFile = JsonOutputFilepath

            js = json.load(open(JsonFile))
            JsonObj = js['audits']
            Result = {}
            loopexit = 0
            for MetrixId in RequiresAduits:
                title = JsonObj[MetrixId]['title']
                if 'numericValue' in JsonObj[MetrixId]:
                    stats = JsonObj[MetrixId]['numericValue']
                    # if MainMat not 'max-potential-fid':
                    stats = float(stats) / 1000
                    stats = round(stats, 3)
                    Result[title] = stats
                    ResultSum[title] = stats
                    # print("%s = %s  Sec" % (title, stats))
                else:
                    loopexit = 1

            if loopexit == 1:
                print("Lighthouse is not able to Generate the Result please check URL and connectivity for %s " % (TestUrl))
                continue
            ###Gather main Performance Scores
            Scorestitles = ['performance', 'accessibility', 'best-practices', 'seo', 'pwa']
            Scores = {}
            MainPerformanceMatrix = js['categories']
            for MainMat in Scorestitles:
                MainMatrixdata = MainPerformanceMatrix[MainMat]
                PerformanceTitle = MainMatrixdata['title']
                score = MainMatrixdata['score']
                # if score is null place to value
                if score:
                    PerformanceScore = int(score * 100)
                    Scores[PerformanceTitle] = PerformanceScore
                    ResultSum[PerformanceTitle] = PerformanceScore
                    # print("%s = %s  " %(PerformanceTitle, PerformanceScore))
                else:
                    print('Score data not availible')
                    Scores[PerformanceTitle] = ''

            if not Fullpath:
                #OutPutCsvFileName = datetime.now().strftime('%Y_%m_%d-%H_%M_%S') + '.csv'
                #filePath, filename = os.path.split(JsonOutputFilepath)
                #Fullpath = filePath + '/Result_' + OutPutCsvFileName
                OutPutCsvFileName = 'lighthouse' + '.csv'
                Fullpath = OutPutCsvFileName
                mode = 'wb'
                Headers = ['TestUrl']
            else:
                mode = 'ab'

            # check the first Meaning full content lies within Threashold Value
            CurentFMP = float(ResultSum['First Meaningful Paint'])
            if CurentFMP >= thresholdValue:
                Testurlstatus = 'Fail'
            else:
                Testurlstatus = 'Pass'

            with open(Fullpath, mode=mode) as ResultFile:
                csv_writerObj = csv.writer(ResultFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                # csv_writerObj.writerow(['ScoreName', 'Score Percentage'])

                values = [TestUrl]
                for Scorehead in Scores:
                    Headers.append(Scorehead)
                    values.append(Scores[Scorehead])

                for result21 in Result:
                    Headers.append(result21)
                    values.append(Result[result21])

                Headers.append('Test Status')
                values.append(Testurlstatus)
                Headers.append('Html report path')
                values.append(HtmlOutputFilepath)

                #Append header & for build number
                Headers.append('Build Number')
                values.append(buildnumber)

                #For the first time, add headers
                #if mode == 'wb':
                    #csv_writerObj.writerow(Headers)
                
                #Write result values
                csv_writerObj.writerow(values)

                ResultSum['Test Status'] = TestResult

                # csv_writerObj.write(['Metrix', 'Metrix in Seconds'])
                # for result31 in Result:
                # csv_writerObj.write([result31, Result[result31]])
            ResultFile.close()
            ResultSum['Test Status'] = Testurlstatus
            TestResult[TestUrl] = ResultSum
            # print "Removing JsonFile = ", JsonOutputFilepath
            os.remove(JsonOutputFilepath)
        else:
            print
            "Invalid URl kinldy add http before URL"


    except Exception as B:
        print('Got exception for  %s' % (TestUrl))
        traceback.print_exc(file=sys.stdout)
# print TestResult.keys()

if TestResult.keys():
    CaseDict = {}
    Passcasecount = 0
    for Keys in TestResult:
        ResultDict = TestResult[Keys]
        CaseDict[Keys] = ResultDict['Test Status']
        if ResultDict['Test Status'] == 'Pass':
            Passcasecount = Passcasecount + 1
    Totalcase = CaseDict.__len__()
    # print('Percentage Count div ' + str(Passcasecount))
    Percentage = float(Passcasecount / Totalcase)
    # print('Percentage after div ' + str(Percentage) )
    Percentage = int(Percentage * 100)
    # print('Percentage after Multiply ' + str(Percentage))
    # print('Percentage Quota %s' % (Quota))
    if Percentage >= Quota:
        print("Test Pass because %s Percent of URL's FMP above %s Sec" % (Percentage, thresholdValue))
        print("Result File path is =%s" % (Fullpath))
        quotaexitstatus = 0
    else:
        print("Test Fail because %s Percent of URL's FMP above %s Sec which is less than Given quota" % (Percentage, thresholdValue))
        print("Result File path is =%s" % (Fullpath))
        quotaexitstatus = 1

else:
    print('Not able to get Result cases')
    exit(1)


def CSVtoDB(BaseLineCsvFilepath):
    with open(BaseLineCsvFilepath) as BaselineFile:
        BaseLineRead = csv.reader(BaselineFile)
        basedataArray = []

        for row in BaseLineRead:
            basedataArray.append(row)

        baselineheader = basedataArray[0]
        # print(baselineheader)
        baselinedata = basedataArray[1::]
        # print(baselinedata)

        BaselineDB = {}
        for col in baselinedata:
            index = 1
            url = col[0]
            # print(col)
            RowArray = {}
            for data in col[1::]:
                Header = baselineheader[index]

                # print("head= %s ----data=%s" %(Header,data))
                RowArray[Header] = data
                index = index + 1
            BaselineDB[url] = RowArray
        return BaselineDB

# print(CurrentResultfileparse)

def CompareMatrix(Baselinefilemap, CurrentResultmap):
    Metrixtcompare = ['Performance', 'SEO', 'Best Practices', 'Accessibility']
    CompareResultArray = []
    compareExitStatus = 0
    for metrixdata in Baselinefilemap:
        metrix = Baselinefilemap[metrixdata]
        if Baselinefilemap.has_key(metrixdata) and CurrentResultmap.has_key(metrixdata):
            # comparing data from Current Result
            for Met in Metrixtcompare:
                urltext = metrixdata
                dataarray = []
                if CurrentResultmap[urltext][Met] < Baselinefilemap[urltext][Met]:
                    dataarray.append(urltext)
                    dataarray.append(Met)
                    dataarray.append(Baselinefilemap[urltext][Met])
                    dataarray.append(CurrentResultmap[urltext][Met])
                    #print('baselineurl= %s  %s:%s' % (urltext, Met, str(Baselinefilemap[urltext][Met])))
                    #print('Currenturl=%s %s:%s' % (urltext, Met, str(CurrentResultmap[urltext][Met])))
                    CompareResultArray.append(dataarray)
                    compareExitStatus = 1
        else:
            print('value not found for =%s' % (urltext))

    CompareHeaders = ['TestUrl', 'Matrix Name', 'Metrix Base Value', 'Metrix Current Value']
    CurrentDirpath = os.getcwd()
    # if Windows
    #CompareFileName = CurrentDirpath + '\\' + 'CompareResult_' + datetime.now().strftime('%Y_%m_%d-%H_%M_%S') + '.csv'
    # ifLinux
    CompareFileName = CurrentDirpath + '/' + 'CompareResult_' + datetime.now().strftime('%Y_%m_%d-%H_%M_%S') + '.csv'
    # print(CompareFileName)

    #CompareFileName = 'CompareResult' + datetime.now().strftime('%Y_%m_%d-%H_%M_%S') + '.csv'
    CompareResultFile = CompareFileName
    if compareExitStatus == 1:
        print("Build fail due to current metrix is high compare to baseline data")
    try:
        with open(CompareResultFile, mode='wb') as CompareResultFiledata:
            csv_writerObj1 = csv.writer(CompareResultFiledata, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writerObj1.writerow(CompareHeaders)
            # csv_writerObj1.writerow(CompareResultArray)
            for line in CompareResultArray:
                csv_writerObj1.writerow(line)

            print("Compare results save in file= %s" %(CompareResultFile))
            return (compareExitStatus)
    except BaseException as e:
        print(e)
        return(1)

#print(args.baseline)

'''
if BaseLine:
    baselinefileparse = CSVtoDB(BaseLine)
    # print(baselinefileparse)
    CurrentResult = Fullpath
    CurrentResultfileparse = CSVtoDB(CurrentResult)
    compareresult = CompareMatrix(baselinefileparse, CurrentResultfileparse)
if (quotaexitstatus == 1 and compareresult == 1 ):
    print("Build fail due to Quota and baseline")
    exit(1)
elif (quotaexitstatus == 0 and compareresult == 1 ):
    print("Build fail due to baseline comparison")
    exit(1)
'''
