from fuzzywuzzy import fuzz # pip install fuzzywuzzy[speedup]

def StringMatching(Threshold=80,QR_Code_dict={},OCR_dict={},key_list=[],DEBUG=False):
    """ 
    StringMatching Method will return Boolean
    parameters:
        Threshold: type=Number, default=75
        QR_Code_dict: type=dict
        OCR_dict : type=dict
        key_list : type=list, default=QR_Code_dict.keys()
        DEBUG    : type=Boolean, help= set DebugMode (print ratio score list & average score)
    eaxmple:
        >>> StringMatching(80,{"name":"AAA","ID":"BBB","date":"ddd"},{"name":"ABA","ID":"BBB","date":"ddd"},["name","ID"])
        `False`
    """

    if len(key_list) == 0:key_list= QR_Code_dict.keys()
    clean_char_list = ["\r","\n","\b","\t"]
    ratio_dict={}
    for k in key_list:
        if QR_Code_dict.get(k) and OCR_dict.get(k):

            # clean  String
            strQR = QR_Code_dict.get(k).lower()
            strOCR = OCR_dict.get(k).lower()
            for char in clean_char_list:
                strQR = strQR.replace(char,"")
                strOCR = strOCR.replace(char,"")
            # compute ratio
            ratio_dict[k] = fuzz.ratio(strQR,strOCR)
    
    score = ratio_dict.values()
    avg = sum(score) / len(score)
    threshold_partial = [s >= Threshold for s in score]
    if DEBUG: print("ratio_dict:",ratio_dict,"\navg:",avg,"\nthreshold_partial:",threshold_partial,end='\n\n')
    
    ## check only caee threshold_partial
    # return not (False in threshold_partial)

    ## check only case avg >= Threshold
    # return avg >= Threshold

    ## check main case is threshold_partial and second case is avg >= Threshold
    return not (False in threshold_partial) or avg >= Threshold

    ## check both case
    # return not (False in threshold_partial) and avg >= Threshold

def findThreshold(Tmin=None,Tmax=None,dict_list=[],actual_list=[],key_list=[]):
    if len(key_list) == 0:key_list= dict_list[0][0].keys()
    
    if (Tmin is None) and (Tmax is not None): 
        decrease_mode,T,Tmin = True,Tmax,0
    elif (Tmax is None) and (Tmin is not None): 
        decrease_mode,T,Tmax = False,Tmin,100
    elif(Tmin is not None) and (Tmax is not None): 
        decrease_mode,T = False,Tmin
    else: 
        decrease_mode,Tmin,T,Tmax=False,0,0,100

    while Tmin <= T <= Tmax:
        for (qr,ocr),actual in zip(dict_list,actual_list):
            result = StringMatching(round(T,3),qr,ocr,key_list)
            if result != actual: break
        else:
            return round(T,3)
            break
        if decrease_mode: T-=.05
        else: T+=.05

    return None
            

    

if __name__ == '__main__':
    true_dict_list=[
          ({"name":"นาง สุวิภา อยู่สุข","ID":"HN43218","date":"23/02/62","tmp1":"tmp1"},
          {"name":"นา สุวิา อยุสข","ID":"HN43211","date":"23/02/63","tmp1":"tmp1"}),

          ({"name":"นาง สุวิภา อยู่สุข","ID":"HN43882","date":"23/02/62","tmp1":"tmp1"},
          {"name":"นา สุวิา อยุสข","ID":"HN43  2","date":"23/02/63","tmp1":"tmp1"}),

          ({"name":"นาสุวิา  อยสุข","ID":"HN48211","date":"2412/63","tmp1":"tmp1"},
          {"name":"นา สุวิา อยุสข","ID":"HN43211","date":"23/02/63","tmp1":"tmp1"}),

          ({"name":"นาง สุวิภา อยู่สุข","ID":"HN43882","date":"23/02/62","tmp1":"tmp1"},
          {"name":"นา สุวิา อยุสข","ID":"HN43833","date":"23/02/63","tmp1":"tmp1"}),
        ]

    false_dict_list=[
          ({"name":"นาย กลม แซ่ตั้ง","ID":"HN43218","date":"23/02/62","tmp1":"tmp1"},
          {"name":"นา สุวิา อยุสข","ID":"HN43211","date":"23/02/63","tmp1":"tmp1"}),

          ({"name":"นาย กลม แซ่ตั้ง","ID":"HN43218","date":"23/02/62","tmp1":"tmp1"},
          {"name":"นาย สวัสดี อยุสข","ID":"HN43411","date":"23/02/63","tmp1":"tmp1"}),

          ({"name":"นาย กลม แซ่ตั้ง","ID":"HN48211","date":"2412/63","tmp1":"tmp1"},
          {"name":"นา ขแบเขต บุญมี","ID":"Hห43211","date":"2412/63","tmp1":"tmp1"}),

          ({"name":"นาย กลม แซ่ตั้ง","ID":"HN43854","date":"23/02/62","tmp1":"tmp1"},
          {"name":"นาง กลมวัลย์ แซ่ตั้ง","ID":"HN46831","date":"24/03/63","tmp1":"tmp1"}),

          ({"name":"นางสุวณสีย์ เที่ยงแท้","ID":"HN4485","date":"22/02/62","tmp1":"tmp1"},
          {"name":"นางทองประสม เที่ยงแท้","ID":"HN4481","date":"23/02/62","tmp1":"tmp1"}),

          ({"name":"นาง กมล บางเลน","ID":"HN43825","date":"23/02/63","tmp1":"tmp1"},
          {"name":"นา สุวิา อยุสข","ID":"HN43211","date":"23/02/63","tmp1":"tmp1"}),
        ]
    actual_list = [True for _ in range(len(true_dict_list))] + [False for _ in range(len(false_dict_list))]
    dict_list = true_dict_list + false_dict_list
    key_list = ["name","ID","date"]
    T = findThreshold(Tmin=30,
                      dict_list=dict_list,key_list=key_list,
                      actual_list=actual_list)
    print("found T:",T)

    # case avg >= Threshold test with dict_list : should use  79.35 <=T <= 79.65
    # case threshold_partial test with dict_list: don't found T
    # case threshold_partial test with false_dict_list only: should use T >= 67.05
    # case threshold_partial test with true_dict_list only: should use T <= 67.0
    
    # So,case threshold_partial or avg >= Threshold : should use 79.35 <=T <= 79.65
    # case threshold_partial and avg >= Threshold : don't found T

    print(" Example StringMatching Mathod ".center(70,"#"))
    QR_Code_dict={"name":"นาย กลม แซ่ตั้ง","ID":"HN43218","date":"23/02/62","tmp1":"tmp1"}
    OCR_dict={"name":"นาง กลมวัลย์ แซ่ตั้ง","ID":"HN46831","date":"24/03/63","tmp1":"tmp1"}
    isMatch = StringMatching(Threshold=T,QR_Code_dict=QR_Code_dict,OCR_dict=OCR_dict,
                    key_list=key_list,DEBUG=True)
    print("isMatch:",isMatch)
    print("".center(70,"#"))