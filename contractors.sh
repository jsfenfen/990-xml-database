-- Contractor compensation


-- Form 990: 


DROP TABLE IF EXISTS contractor_comp_990;

SELECT 
	address_table.ein,
	address_table.object_id,
	address_table."RtrnHdr_TxPrdEndDt",
	address_table."RtrnHdr_TxYr",
	address_table."BsnssOffcr_SgntrDt",
	address_table."BsnssNm_BsnssNmLn1Txt" as "Org_BsnssNmLn1",
	address_table."BsnssNm_BsnssNmLn2Txt" as "Org_BsnssNmL21",
	address_table."BsnssOffcr_PrsnNm" as "Org_BsnssOffcr_PrsnNm",
	address_table."BsnssOffcr_PrsnTtlTxt" as "Org_ BsnssOffcr_PrsnTtlTxt",
	address_table."BsnssOffcr_PhnNm" as "Org_ BsnssOffcr_PhnNm" ,
	address_table."BsnssOffcr_EmlAddrssTxt"  as "Org_ BsnssOffcr_EmlAddrssTxt" ,
	address_table."USAddrss_AddrssLn1Txt" as "Org_AddrssLn1Txt",
	address_table."USAddrss_AddrssLn2Txt" as "Org_AddrssLn2Txt",
	address_table."USAddrss_CtyNm" as "Org_CtyNm",
	address_table."USAddrss_SttAbbrvtnCd" as "Org_SttAbbrvtnCd",
	address_table."USAddrss_ZIPCd" as "Org_ZIPCd",
	address_table."FrgnAddrss_AddrssLn1Txt" as "Org_FrgnAddrss_AddrssLn1Txt",
	address_table."FrgnAddrss_AddrssLn2Txt" as "Org_FrgnAddrss_AddrssLn2Txt",
	address_table."FrgnAddrss_CtyNm" as "Org_FrgnAddrss_CtyNm",
	address_table."FrgnAddrss_PrvncOrSttNm" as "Org_PrvncOrSttNm",
	address_table."FrgnAddrss_CntryCd" as "Org_CntryCd",
	return_CntrctrCmpnstn."CntrctrNm_PrsnNm" as "CntrctrNm_PrsnNm",
	trim(concat(return_CntrctrCmpnstn."BsnssNm_BsnssNmLn1Txt", ' ', return_CntrctrCmpnstn."BsnssNm_BsnssNmLn2Txt")) as "Cntrctr_Business",
	trim(concat(return_CntrctrCmpnstn."USAddrss_AddrssLn1Txt", ' ', return_CntrctrCmpnstn."FrgnAddrss_AddrssLn1Txt")) as "Cntrctr_Address1",
	trim(concat(return_CntrctrCmpnstn."USAddrss_AddrssLn2Txt", ' ', return_CntrctrCmpnstn."FrgnAddrss_AddrssLn2Txt")) as "Cntrctr_Address2",
	trim(concat(return_CntrctrCmpnstn."USAddrss_CtyNm", ' ', return_CntrctrCmpnstn."FrgnAddrss_CtyNm")) as "Cntrctr_City",
	trim(concat(return_CntrctrCmpnstn."USAddrss_ZIPCd", ' ', return_CntrctrCmpnstn."FrgnAddrss_FrgnPstlCd")) as "Cntrctr_ZIP",
	trim(concat(return_CntrctrCmpnstn."USAddrss_SttAbbrvtnCd" , ' ',  return_CntrctrCmpnstn."FrgnAddrss_PrvncOrSttNm")) as "Cntrctr_State",
	return_CntrctrCmpnstn."FrgnAddrss_CntryCd" as "Cntrctr_FrgnAddrss_CntryCd",
	return_CntrctrCmpnstn."CntrctrCmpnstn_SrvcsDsc" as "SrvcsDsc",
	return_CntrctrCmpnstn."CntrctrCmpnstn_CmpnstnAmt" as "CmpnstnAmt"	      
	INTO TEMPORARY TABLE contractor_comp_990
	FROM return_CntrctrCmpnstn
	LEFT JOIN address_table ON return_CntrctrCmpnstn.object_id = address_table.object_id
	AND return_CntrctrCmpnstn.ein = address_table.ein;


select "Orgnztn501c3Ind", "Orgnztn501cInd", "Orgnztn49471NtPFInd", "Orgnztn527Ind", url_base,  '/IRS990' as form, contractor_comp_990.* into temporary table contractor_comp_990_types from contractor_comp_990 left join org_types on contractor_comp_990.object_id = org_types.object_id and contractor_comp_990.ein = org_types.ein;


\copy contractor_comp_990_types to '/data/file_exports/contractors_990.csv' with csv header;



-- 990 PF

DROP TABLE IF EXISTS contractor_comp_990_pf;
	
SELECT 
	address_table.ein,
	address_table.object_id,
	address_table."RtrnHdr_TxPrdEndDt",
	address_table."RtrnHdr_TxYr",
	address_table."BsnssOffcr_SgntrDt",
	address_table."BsnssNm_BsnssNmLn1Txt" as "Org_BsnssNmLn1",
	address_table."BsnssNm_BsnssNmLn2Txt" as "Org_BsnssNmL21",
	address_table."BsnssOffcr_PrsnNm" as "Org_BsnssOffcr_PrsnNm",
	address_table."BsnssOffcr_PrsnTtlTxt" as "Org_ BsnssOffcr_PrsnTtlTxt",
	address_table."BsnssOffcr_PhnNm" as "Org_ BsnssOffcr_PhnNm" ,
	address_table."BsnssOffcr_EmlAddrssTxt"  as "Org_ BsnssOffcr_EmlAddrssTxt" ,
	address_table."USAddrss_AddrssLn1Txt" as "Org_AddrssLn1Txt",
	address_table."USAddrss_AddrssLn2Txt" as "Org_AddrssLn2Txt",
	address_table."USAddrss_CtyNm" as "Org_CtyNm",
	address_table."USAddrss_SttAbbrvtnCd" as "Org_SttAbbrvtnCd",
	address_table."USAddrss_ZIPCd" as "Org_ZIPCd",
	address_table."FrgnAddrss_AddrssLn1Txt" as "Org_FrgnAddrss_AddrssLn1Txt",
	address_table."FrgnAddrss_AddrssLn2Txt" as "Org_FrgnAddrss_AddrssLn2Txt",
	address_table."FrgnAddrss_CtyNm" as "Org_FrgnAddrss_CtyNm",
	address_table."FrgnAddrss_PrvncOrSttNm" as "Org_PrvncOrSttNm",
	address_table."FrgnAddrss_CntryCd" as "Org_CntryCd",
	return_PFCmpnstnOfHghstPdCntrct."CmpnstnOfHghstPdCntrct_PrsnNm" as "CntrctrNm_PrsnNm",
	trim(concat(return_PFCmpnstnOfHghstPdCntrct."CmpnstnOfHghstPdCntrct_BsnssNmLn1", ' ', return_PFCmpnstnOfHghstPdCntrct."CmpnstnOfHghstPdCntrct_BsnssNmLn2")) as "Cntrctr_Business",
	trim(concat(return_PFCmpnstnOfHghstPdCntrct."USAddrss_AddrssLn1Txt", ' ', return_PFCmpnstnOfHghstPdCntrct."FrgnAddrss_AddrssLn1Txt")) as "Cntrctr_Address1",
	trim(concat(return_PFCmpnstnOfHghstPdCntrct."USAddrss_AddrssLn2Txt", ' ', return_PFCmpnstnOfHghstPdCntrct."FrgnAddrss_AddrssLn2Txt")) as "Cntrctr_Address2",
	trim(concat(return_PFCmpnstnOfHghstPdCntrct."USAddrss_CtyNm", ' ', return_PFCmpnstnOfHghstPdCntrct."FrgnAddrss_CtyNm")) as "Cntrctr_City",
	trim(concat(return_PFCmpnstnOfHghstPdCntrct."USAddrss_ZIPCd", ' ', return_PFCmpnstnOfHghstPdCntrct."FrgnAddrss_FrgnPstlCd")) as "Cntrctr_ZIP",
	trim(concat(return_PFCmpnstnOfHghstPdCntrct."USAddrss_SttAbbrvtnCd" , ' ',  return_PFCmpnstnOfHghstPdCntrct."FrgnAddrss_PrvncOrSttNm")) as "Cntrctr_State",
	return_PFCmpnstnOfHghstPdCntrct."FrgnAddrss_CntryCd" as "Cntrctr_FrgnAddrss_CntryCd",
	return_PFCmpnstnOfHghstPdCntrct."CmpnstnOfHghstPdCntrct_SrvcTxt" as "SrvcsDsc",
	return_PFCmpnstnOfHghstPdCntrct."CmpnstnOfHghstPdCntrct_CmpnstnAmt" as "CmpnstnAmt"	      
	INTO TEMPORARY TABLE contractor_comp_990_pf
	FROM return_PFCmpnstnOfHghstPdCntrct
	LEFT JOIN address_table ON return_PFCmpnstnOfHghstPdCntrct.object_id = address_table.object_id
	AND return_PFCmpnstnOfHghstPdCntrct.ein = address_table.ein;


select "Orgnztn501c3Ind", "Orgnztn501cInd", "Orgnztn49471NtPFInd", "Orgnztn527Ind", url_base, '/IRS990PF' as form, contractor_comp_990_pf.* into temporary table contractor_comp_990_pf_types from contractor_comp_990_pf left join org_types on contractor_comp_990_pf.object_id = org_types.object_id and contractor_comp_990_pf.ein = org_types.ein;

	
\copy contractor_comp_990_pf_types to '/data/file_exports/contractor_comp_990_pf.csv' with csv header;
	

-- 990EZ

DROP TABLE IF EXISTS contractor_comp_990_ez;
	
SELECT 
	address_table.ein,
	address_table.object_id,
	address_table."RtrnHdr_TxPrdEndDt",
	address_table."RtrnHdr_TxYr",
   address_table."BsnssOffcr_SgntrDt",
	address_table."BsnssNm_BsnssNmLn1Txt" as "Org_BsnssNmLn1",
	address_table."BsnssNm_BsnssNmLn2Txt" as "Org_BsnssNmL21",
	address_table."BsnssOffcr_PrsnNm" as "Org_BsnssOffcr_PrsnNm",
	address_table."BsnssOffcr_PrsnTtlTxt" as "Org_ BsnssOffcr_PrsnTtlTxt",
	address_table."BsnssOffcr_PhnNm" as "Org_ BsnssOffcr_PhnNm" ,
	address_table."BsnssOffcr_EmlAddrssTxt"  as "Org_ BsnssOffcr_EmlAddrssTxt" ,
	address_table."USAddrss_AddrssLn1Txt" as "Org_AddrssLn1Txt",
	address_table."USAddrss_AddrssLn2Txt" as "Org_AddrssLn2Txt",
	address_table."USAddrss_CtyNm" as "Org_CtyNm",
	address_table."USAddrss_SttAbbrvtnCd" as "Org_SttAbbrvtnCd",
	address_table."USAddrss_ZIPCd" as "Org_ZIPCd",
	address_table."FrgnAddrss_AddrssLn1Txt" as "Org_FrgnAddrss_AddrssLn1Txt",
	address_table."FrgnAddrss_AddrssLn2Txt" as "Org_FrgnAddrss_AddrssLn2Txt",
	address_table."FrgnAddrss_CtyNm" as "Org_FrgnAddrss_CtyNm",
	address_table."FrgnAddrss_PrvncOrSttNm" as "Org_PrvncOrSttNm",
	address_table."FrgnAddrss_CntryCd" as "Org_CntryCd",
	return_EZCmpnstnOfHghstPdCntrct ."CmpnstnOfHghstPdCntrct_PrsnNm" as "CntrctrNm_PrsnNm",
	trim(concat(return_EZCmpnstnOfHghstPdCntrct ."CmpnstnOfHghstPdCntrct_BsnssNmLn1", ' ', return_EZCmpnstnOfHghstPdCntrct ."CmpnstnOfHghstPdCntrct_BsnssNmLn2")) as "Cntrctr_Business",
	trim(concat(return_EZCmpnstnOfHghstPdCntrct ."USAddrss_AddrssLn1Txt", ' ', return_EZCmpnstnOfHghstPdCntrct ."FrgnAddrss_AddrssLn1Txt")) as "Cntrctr_Address1",
	trim(concat(return_EZCmpnstnOfHghstPdCntrct ."USAddrss_AddrssLn2Txt", ' ', return_EZCmpnstnOfHghstPdCntrct ."FrgnAddrss_AddrssLn2Txt")) as "Cntrctr_Address2",
	trim(concat(return_EZCmpnstnOfHghstPdCntrct ."USAddrss_CtyNm", ' ', return_EZCmpnstnOfHghstPdCntrct ."FrgnAddrss_CtyNm")) as "Cntrctr_City",
	trim(concat(return_EZCmpnstnOfHghstPdCntrct ."USAddrss_ZIPCd", ' ', return_EZCmpnstnOfHghstPdCntrct ."FrgnAddrss_FrgnPstlCd")) as "Cntrctr_ZIP",
	trim(concat(return_EZCmpnstnOfHghstPdCntrct ."USAddrss_SttAbbrvtnCd" , ' ',  return_EZCmpnstnOfHghstPdCntrct ."FrgnAddrss_PrvncOrSttNm")) as "Cntrctr_State",
	return_EZCmpnstnOfHghstPdCntrct ."FrgnAddrss_CntryCd" as "Cntrctr_FrgnAddrss_CntryCd",
	return_EZCmpnstnOfHghstPdCntrct ."CmpnstnOfHghstPdCntrct_SrvcTxt" as "SrvcsDsc",
	return_EZCmpnstnOfHghstPdCntrct ."CmpnstnOfHghstPdCntrct_CmpnstnAmt" as "CmpnstnAmt"	      
	INTO TEMPORARY TABLE contractor_comp_990_ez
	FROM return_EZCmpnstnOfHghstPdCntrct 
	LEFT JOIN address_table ON return_EZCmpnstnOfHghstPdCntrct .object_id = address_table.object_id
	AND return_EZCmpnstnOfHghstPdCntrct .ein = address_table.ein;

select "Orgnztn501c3Ind", "Orgnztn501cInd", "Orgnztn49471NtPFInd", "Orgnztn527Ind", url_base,  '/IRS990EZ' as form, contractor_comp_990_ez.* into temporary table contractor_comp_990_ez_types from contractor_comp_990_ez left join org_types on contractor_comp_990_ez.object_id = org_types.object_id and contractor_comp_990_ez.ein = org_types.ein;

\copy contractor_comp_990_ez_types to '/data/file_exports/contractor_comp_990_ez.csv' with csv header;

