
import unicodecsv as csv
from irsx.xmlrunner import XMLRunner

from irsx.filing import FileMissingException
from stream_extractor import StreamExtractor



output_streams = {

    '990_part_0': {
        'filename':'990_part_0',
        'headers': ["ein", "object_id", 'Orgnztn527Ind', 'Orgnztn501cInd', 'Orgnztn49471NtPFInd', 'Orgnztn501c3Ind', 'WbstAddrssTxt', 'OfOrgnztnTrstInd', 'OthrOrgnztnDsc', 'OfOrgnztnCrpInd', 'OfOrgnztnOthrInd', 'OfOrgnztnAsscInd', 'FrmtnYr', 'LglDmclSttCd', 'LglDmclCntryCd']
    },
    '990_part_i': {
        'filename':'990_part_i',
        'headers': ["ein", "object_id", "CntrctTrmntnInd", "TtlEmplyCnt", "TtlVlntrsCnt", "CYInvstmntIncmAmt", "CYTtlRvnAmt", "CYTtlExpnssAmt", "CYRvnsLssExpnssAmt", "TtlAsstsEOYAmt", "ActvtyOrMssnDsc" ]
    },
    '990_part_iv': {
        'filename':'990_part_iv',
        'headers': ["ein", "object_id", "PrtlLqdtnInd"]
    },
    '990ez_part_0': {
        'filename':'990ez_part_0',
        'headers': ["ein", "object_id", "WbstAddrssTxt", "Orgnztn527Ind", "Orgnztn501c3Ind", "Orgnztn49471NtPFInd", "Orgnztn501cInd", "OfOrgnztnOthrDsc", "OfOrgnztnOthrInd", "OfOrgnztnCrpInd", "OfOrgnztnTrstInd", "OfOrgnztnAsscInd", "GrssRcptsAmt"]
    },
    '990ez_part_i': {
        'filename':'990ez_part_i',
        'headers': ["ein", "object_id", "TtlExpnssAmt", "TtlRvnAmt"]
    },
    '990pf_part_0': {
        'filename':'990pf_part_0',
        'headers': ["ein", "object_id","PFSttsTrmSct507b1AInd", "Orgnztn501c3TxblPFInd", "Orgnztn501c3ExmptPFInd", "Orgnztn49471TrtdPFInd", "FMVAsstsEOYAmt"]
    },
    '990pf_part_i': {
        'filename':'990pf_part_i',
        'headers': ["ein", "object_id", 'TtlRvAndExpnssAmt', 'CmpOfcrDrTrstRvAndExpnssAmt', 'OthEmplSlrsWgsRvAndExpnssAmt', 'TtOprExpnssRvAndExpnssAmt', 'CntrPdRvAndExpnssAmt', 'TtlExpnssRvAndExpnssAmt']
    },
    '990pf_part_viia': {
        'filename':'990pf_part_viia',
        'headers': ["ein", "object_id", "SttmntsRgrdngActy_WbstAddrssTxt"]
    },
    'employees_990': {  
        'filename':'employees_990', # will output to employees_detailedYYYY.csv where year is specified below
        'headers':["ein", "object_id", "name", "business_name1", "business_name2", "title", "org_comp", "related_comp", "other_cmp", "form", "source", "IndvdlTrstOrDrctrInd","InstttnlTrstInd","OffcrInd","KyEmplyInd","HghstCmpnstdEmplyInd","FrmrOfcrDrctrTrstInd"]
    },
    'employees_990PF': {  
        'filename':'employees_990PF', # will output to employees_detailedYYYY.csv where year is specified below
        'headers':["ein", "object_id", "name", "business_name1", "business_name2", "title", "org_comp", "related_comp", "other_cmp", "form", "source", "IndvdlTrstOrDrctrInd","InstttnlTrstInd","OffcrInd","KyEmplyInd","HghstCmpnstdEmplyInd","FrmrOfcrDrctrTrstInd"]
    },
    'employees_990EZ': {  
        'filename':'employees_990EZ', # will output to employees_detailedYYYY.csv where year is specified below
        'headers':["ein", "object_id", "name", "business_name1", "business_name2", "title", "org_comp", "related_comp", "other_cmp", "form", "source", "IndvdlTrstOrDrctrInd","InstttnlTrstInd","OffcrInd","KyEmplyInd","HghstCmpnstdEmplyInd","FrmrOfcrDrctrTrstInd"]
    },
    'header_metadata': {
        'filename':'header_metadata', # will output to employees_detailedYYYY.csv where year is specified below
        'headers':["ein", "object_id", "BsnssNm_BsnssNmLn1Txt", "BsnssNm_BsnssNmLn2Txt", "USAddrss_AddrssLn1Txt", "USAddrss_AddrssLn2Txt", "USAddrss_CtyNm",  "USAddrss_SttAbbrvtnCd", "RtrnHdr_TxPrdBgnDt", "RtrnHdr_TxPrdEndDt", "BsnssOffcr_SgntrDt", "Flr_PhnNm", "RtrnHdr_RtrnTs"]
    }
    ,
    '990L_loans': {
        'filename':'990L_loans', # will output to employees_detailedYYYY.csv where year is specified below
        'headers':[ 'ein', 'object_id', 'BsnssNmLn1Txt', 'BsnssNmLn2Txt', 'PrsnNm', 'RltnshpWthOrgTxt', 'LnPrpsTxt', 'LnFrmOrgnztnInd', 'LnTOrgnztnInd', 'OrgnlPrncplAmt', 'BlncDAmt', 'DfltInd', 'BrdOrCmmttApprvlInd', 'WrttnAgrmntInd']
    }
    ,
    '990L_grants': {
        'filename':'990L_grants', # will output to employees_detailedYYYY.csv where year is specified below
        'headers':["ein", "object_id",  "PrsnNm", "BsnssNmLn1Txt", "BsnssNmLn2Txt", "RltnshpWthOrgTxt", "CshGrntAmt", "OfAssstncTxt", "AssstncPrpsTxt"]
    },
    '990L_trans': {
        'filename':'990L_trans', # will output to employees_detailedYYYY.csv where year is specified below
        'headers':["ein", "object_id", "BsnssNmLn1Txt", "PrsnNm", "BsnssNmLn2Txt", "RltnshpDscrptnTxt", "TrnsctnAmt", "TrnsctnDsc", "ShrngOfRvnsInd"]
    }
    # 'diversions': {  
    #     'filename':'diversions', # will output to diversionsYYYY.csv where year is specified below
    #     'headers':["year", "ein", "object_id", "taxpayer_name", "diversion_ind"]
    # }
}

data_capture_dict = {
    'IRS990': {
        'parts': {
            'part_0': {
                'stream_key': '990_part_0',  # 'stream_key' specifies where the output goes--must exist as a key in output_streams
                'ein': {'header':'ein'},
                'object_id': {'header':'object_id'},
                'Orgnztn527Ind':{'header':'Orgnztn527Ind'},
                'Orgnztn501cInd':{'header':'Orgnztn501cInd'},
                'Orgnztn49471NtPFInd':{'header':'Orgnztn49471NtPFInd'},
                'Orgnztn501c3Ind' :{'header':'Orgnztn501c3Ind'},
                'WbstAddrssTxt' :{'header':'WbstAddrssTxt'},
                'OfOrgnztnTrstInd' :{'header':'OfOrgnztnTrstInd'},
                'OthrOrgnztnDsc' :{'header':'OthrOrgnztnDsc'},
                'OfOrgnztnCrpInd' :{'header':'OfOrgnztnCrpInd'},
                'OfOrgnztnOthrInd' :{'header':'OfOrgnztnOthrInd'},
                'OfOrgnztnAsscInd' :{'header':'OfOrgnztnAsscInd'},
                'FrmtnYr' :{'header':'FrmtnYr'},
                'LglDmclSttCd' :{'header':'LglDmclSttCd'},
                'LglDmclCntryCd' :{'header':'LglDmclCntryCd'},
            },
            'part_i': {
                'stream_key': '990_part_i',
                'ein': {'header':'ein'},
                'object_id': {'header':'object_id'},
                'CntrctTrmntnInd': {'header': "CntrctTrmntnInd"},
                'ActvtyOrMssnDsc': {'header': "ActvtyOrMssnDsc"},
                'TtlEmplyCnt': {'header': "TtlEmplyCnt"},
                'TtlVlntrsCnt': {'header': "TtlVlntrsCnt"},
                'CYInvstmntIncmAmt': {'header': "CYInvstmntIncmAmt"},
                'CYTtlRvnAmt': {'header': "CYTtlRvnAmt"},
                'CYTtlExpnssAmt': {'header': "CYTtlExpnssAmt"},
                'CYRvnsLssExpnssAmt': {'header': "CYRvnsLssExpnssAmt"},
                'TtlAsstsEOYAmt': {'header': "TtlAsstsEOYAmt"}
            },
            'part_iv': {
                "stream_key": '990_part_iv',
                "ein": {'header': "ein"},
                "object_id": {'header': "object_id"},
                "PrtlLqdtnInd": {'header': "PrtlLqdtnInd"}
            }
        },
        ## The remaining logic is for capturing salaries wherever they appear in 
        ## the 990, 990PF and 990EZ
        'groups': {
             'Frm990PrtVIISctnA': {
                'stream_key': 'employees_990',  # 'stream_key' specifies where the output goes--must exist as a key in output_streams
                'ein': {'header':'ein'},
                'object_id': {'header':'object_id'},
                'PrsnNm': {'header':'name'},
                'BsnssNmLn1Txt':{'header':'business_name1'},
                'BsnssNmLn2Txt':{'header':'business_name2'},
                'TtlTxt': {'header':'title'},
                'RprtblCmpFrmOrgAmt': {
                    'header':'org_comp',
                    'default':0  # set numeric if missing
                },
                'RprtblCmpFrmRltdOrgAmt': {
                    'header':'related_comp',
                    'default':0
                },
                'OthrCmpnstnAmt':{
                    'header':'other_cmp',
                    'default':0
                },
                'IndvdlTrstOrDrctrInd':{'header':'IndvdlTrstOrDrctrInd'},
                'InstttnlTrstInd':{'header':'InstttnlTrstInd'},
                'OffcrInd':{'header':'OffcrInd'},
                'KyEmplyInd':{'header':'KyEmplyInd'},
                'HghstCmpnstdEmplyInd':{'header':'HghstCmpnstdEmplyInd'},
                'FrmrOfcrDrctrTrstInd':{'header':'FrmrOfcrDrctrTrstInd'}
            }
        }
    },
    'IRS990EZ': {
        'parts': {
            'ez_part_0':{
                'stream_key': '990ez_part_0',
                'ein': {'header':'ein'},
                'object_id': {'header':'object_id'},
                "WbstAddrssTxt": {'header':'WbstAddrssTxt'},
                "Orgnztn527Ind": {'header':'Orgnztn527Ind'},
                "Orgnztn501c3Ind": {'header':'Orgnztn501c3Ind'}, 
                "Orgnztn49471NtPFInd": {'header':'Orgnztn49471NtPFInd'},
                "Orgnztn501cInd": {'header':'Orgnztn501cInd'},
                "OfOrgnztnOthrDsc": {'header':'OfOrgnztnOthrDsc'},
                "OfOrgnztnOthrInd": {'header':'OfOrgnztnOthrInd'},
                "OfOrgnztnCrpInd": {'header':'OfOrgnztnCrpInd'},
                "OfOrgnztnTrstInd": {'header':'OfOrgnztnTrstInd'},
                "OfOrgnztnAsscInd": {'header':'OfOrgnztnAsscInd'},
                "GrssRcptsAmt": {'header':'GrssRcptsAmt'}
            }, 
            'ez_part_i': {
                'stream_key': '990ez_part_i',
                'ein': {'header':'ein'},
                'object_id': {'header':'object_id'},
                "TtlExpnssAmt": {'header':'TtlExpnssAmt'},
                "TtlRvnAmt": {'header':'TtlRvnAmt'},
            }
        },
        'groups': {
            'EZOffcrDrctrTrstEmpl': {
                'stream_key': 'employees_990EZ',
                'ein': {'header':'ein'},
                'object_id': {'header':'object_id'},
                'PrsnNm': {'header':'name'},
                'BsnssNmLn1': {'header':'business_name1'},
                'BsnssNmLn2': {'header':'business_name2'},


                'TtlTxt': {'header':'title'},
                'CmpnstnAmt': {
                    'header':'org_comp',
                    'default':0
                },
                'composite': {  # other compensation includes benefits and other allowances for EZ, PF filers
                    'other_cmp': {
                        'EmplyBnftPrgrmAmt': {
                            'default':0
                        },
                        'ExpnsAccntOthrAllwncAmt': {
                            'default':0
                        }
                    }
                }
            },
            'EZCmpnstnHghstPdEmpl': {
                'stream_key': 'employees_990EZ',
                'ein': {'header':'ein'},
                'object_id': {'header':'object_id'},
                'PrsnNm': {'header':'name'},
                'TtlTxt': {'header':'title'},
                'CmpnstnAmt': {
                    'header':'org_comp',
                    'default':0
                },
                'composite': {
                    'other_cmp': {
                        'EmplyBnftsAmt': {
                            'default':0
                        },
                        'ExpnsAccntAmt': {
                            'default':0
                        }
                    }
                }
            }
        }
    },
    'ReturnHeader990x': {
        'parts': {
            'returnheader990x_part_i': {
                'stream_key': 'header_metadata',  # 'stream_key' specifies where the output goes--must exist as a key in output_streams
                'ein': {'header':'ein'},
                'object_id': {'header':'object_id'},
                'RtrnHdr_TxYr':{'header':'RtrnHdr_TxYr'},
                'BsnssNm_BsnssNmLn2Txt': {'header':'BsnssNm_BsnssNmLn2Txt'},
                'BsnssNm_BsnssNmLn1Txt': {'header':'BsnssNm_BsnssNmLn1Txt'},
                'USAddrss_AddrssLn1Txt': {'header':'USAddrss_AddrssLn1Txt'},
                'USAddrss_AddrssLn2Txt': {'header':'USAddrss_AddrssLn2Txt'},
                'USAddrss_CtyNm': {'header':'USAddrss_CtyNm'},
                'USAddrss_SttAbbrvtnCd': {'header':'USAddrss_SttAbbrvtnCd'},
                'RtrnHdr_TxPrdBgnDt': {'header':'RtrnHdr_TxPrdBgnDt'},
                'RtrnHdr_TxPrdEndDt': {'header':'RtrnHdr_TxPrdEndDt'},
                'BsnssOffcr_SgntrDt': {'header': 'BsnssOffcr_SgntrDt'},
                'Flr_PhnNm': {'header': 'Flr_PhnNm'},
                'RtrnHdr_RtrnTs': {'header':  'RtrnHdr_RtrnTs'}
            }
        }
    },
    'IRS990ScheduleL': {
        'parts': {
        },
        'groups': {
            'SkdLLnsBtwnOrgIntrstdPrsn': {
                'stream_key': '990L_loans', 
                'ein': {'header':'ein'},
                'object_id': {'header':'object_id'},
                'BsnssNmLn1Txt': {'header':'BsnssNmLn1Txt'},
                'BsnssNmLn2Txt': {'header':'BsnssNmLn2Txt'},
                'PrsnNm': {'header':'PrsnNm'},
                'RltnshpWthOrgTxt': {'header':'RltnshpWthOrgTxt'},
                'LnPrpsTxt': {'header':'LnPrpsTxt'},
                'LnFrmOrgnztnInd': {'header':'LnFrmOrgnztnInd'},
                'LnTOrgnztnInd': {'header':'LnTOrgnztnInd'},
                'OrgnlPrncplAmt': {'header':'OrgnlPrncplAmt'},
                'BlncDAmt': {'header':'BlncDAmt'},
                'DfltInd': {'header':'DfltInd'},
                'BrdOrCmmttApprvlInd': {'header':'BrdOrCmmttApprvlInd'},
                'WrttnAgrmntInd': {'header':'WrttnAgrmntInd'}
            },
            'SkdLGrntAsstBnftIntrstdPrsn': {
                'stream_key': '990L_grants', 
                'ein': {'header':'ein'},
                'object_id': {'header':'object_id'},
                "PrsnNm": {'header':'PrsnNm'},
                "BsnssNmLn1Txt": {'header':'BsnssNmLn1Txt'}, 
                "BsnssNmLn2Txt": {'header':'BsnssNmLn2Txt'},
                "RltnshpWthOrgTxt": {'header':'RltnshpWthOrgTxt'},
                "CshGrntAmt": {'header':'CshGrntAmt'},
                "OfAssstncTxt": {'header':'OfAssstncTxt'},
                "AssstncPrpsTxt": {'header':'AssstncPrpsTxt'},
            },
            'SkdLBsTrInvlvIntrstdPrsn': {
                'stream_key': '990L_trans', 
                'ein': {'header':'ein'},
                'object_id': {'header':'object_id'},
                "BsnssNmLn1Txt": {'header':'BsnssNmLn1Txt'},
                "PrsnNm": {'header':'PrsnNm'},
                "BsnssNmLn2Txt": {'header':'BsnssNmLn2Txt'},
                "RltnshpDscrptnTxt": {'header':'RltnshpDscrptnTxt'},
                "TrnsctnAmt": {'header':'TrnsctnAmt'},
                "TrnsctnDsc": {'header':'TrnsctnDsc'},
                "ShrngOfRvnsInd": {'header':'ShrngOfRvnsInd'}
            }
        }
    },        

    'IRS990PF': {
        'parts': {
            'pf_part_0': {
                'stream_key': '990pf_part_0',  # 'stream_key' specifies where the output goes--must exist as a key in output_streams
                'ein': {'header':'ein'},
                'object_id': {'header':'object_id'},
                "PFSttsTrmSct507b1AInd": {'header':'PFSttsTrmSct507b1AInd'},
                "Orgnztn501c3TxblPFInd": {'header':'Orgnztn501c3TxblPFInd'},
                "Orgnztn501c3ExmptPFInd": {'header':'Orgnztn501c3ExmptPFInd'},
                "Orgnztn49471TrtdPFInd": {'header':'Orgnztn49471TrtdPFInd'},
                "FMVAsstsEOYAmt": {'header':'FMVAsstsEOYAmt'},
            },
            'pf_part_i': {
                'stream_key': '990pf_part_i',  # 'stream_key' specifies where the output goes--must exist as a key in output_streams
                'ein': {'header':'ein'},
                'object_id': {'header':'object_id'},
                'TtlRvAndExpnssAmt': {'header':'TtlRvAndExpnssAmt'},
                'CmpOfcrDrTrstRvAndExpnssAmt': {'header':'CmpOfcrDrTrstRvAndExpnssAmt'},
                'OthEmplSlrsWgsRvAndExpnssAmt': {'header':'OthEmplSlrsWgsRvAndExpnssAmt'},
                'TtOprExpnssRvAndExpnssAmt': {'header':'TtOprExpnssRvAndExpnssAmt'},
                'CntrPdRvAndExpnssAmt': {'header':'CntrPdRvAndExpnssAmt'},
                'TtlExpnssRvAndExpnssAmt': {'header':'TtlExpnssRvAndExpnssAmt'}
            },
            'pf_part_viia': {
                'stream_key': '990pf_part_viia',  # 'stream_key' specifies where the output goes--must exist as a key in output_streams
                'ein': {'header':'ein'},
                'object_id': {'header':'object_id'},
                'SttmntsRgrdngActy_WbstAddrssTxt': {'header':'SttmntsRgrdngActy_WbstAddrssTxt'}
            }
        },
        'groups': {
            'PFOffcrDrTrstKyEmpl': {
                'stream_key': 'employees_990PF',

                'ein': {'header':'ein'},
                'object_id': {'header':'object_id'},
                'OffcrDrTrstKyEmpl_PrsnNm': {'header':'name'},
                'OffcrDrTrstKyEmpl_BsnssNmLn1': {'header':'business_name1'},
                'OffcrDrTrstKyEmpl_BsnssNmLn2': {'header':'business_name2'},
                'OffcrDrTrstKyEmpl_TtlTxt': {'header':'title'},
                'OffcrDrTrstKyEmpl_CmpnstnAmt': {
                    'header':'org_comp',
                    'default':0  # set numeric if missing
                },
                'composite': {
                    'other_cmp': {
                        'OffcrDrTrstKyEmpl_EmplyBnftPrgrmAmt': {
                            'default':0
                        },
                        'OffcrDrTrstKyEmpl_ExpnsAccntOthrAllwncAmt': {
                            'default':0
                        }
                    }
                }
            },
            'PFCmpnstnHghstPdEmpl': {
                'stream_key': 'employees_990PF',

                'ein': {'header':'ein'},
                'object_id': {'header':'object_id'},
                'CmpnstnHghstPdEmpl_PrsnNm': {'header':'name'},
                'CmpnstnHghstPdEmpl_TtlTxt': {'header':'title'},
                'CmpnstnHghstPdEmpl_CmpnstnAmt': {
                    'header':'org_comp',
                    'default':0  # set numeric if missing
                },
                'composite': {
                    'other_cmp': {
                        'CmpnstnHghstPdEmpl_EmplyBnftsAmt': {
                            'default':0
                        },
                        'CmpnstnHghstPdEmpl_ExpnsAccntAmt': {
                            'default':0
                        }
                    }
                }
            }
        }
    }
}

if __name__ == '__main__':

    input_file = "initial_manifest.csv"



    # read the whole file in here, it's not very long
    file_rows = [] 

    # We're using the output of part 1
    with open(input_file, 'rb') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            file_rows.append(row)
        

    extractor = StreamExtractor(output_streams, data_capture_dict)


    filing_count = 0
    for metadata_row in file_rows:

        try:
            object_id = metadata_row['object_id']
            if object_id:
                #print("Running %s " % metadata_row['object_id'])
                extractor.run_filing(object_id, taxpayer_name=metadata_row['name'])

                filing_count += 1
                if filing_count % 100 == 0:
                    print("Processed %s filings" % filing_count)


        except FileMissingException:
            pass
            #print("Missing %s skipping " % metadata_row['object_id'])


