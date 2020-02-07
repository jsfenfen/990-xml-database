-- Assumes that directors was already run. 

-- Schedule I

-- The schedule I variables are defined in the [irsx documentation](http://www.irsx.info/metadata/groups/SkdIRcpntTbl.html).

--  Here's a query to a temp table


DROP TABLE IF EXISTS grants;

SELECT 
       return_SkdIRcpntTbl.object_id as object_id,
       address_table."RtrnHdr_TxPrdEndDt",
       address_table."RtrnHdr_TxYr",
       address_table."BsnssOffcr_SgntrDt",
       address_table."BsnssNm_BsnssNmLn1Txt" as "Donor_BsnssNmLn1",
       address_table."BsnssNm_BsnssNmLn2Txt" as "Donor_BsnssNmLn2",
       address_table."BsnssOffcr_PrsnNm" as "Donor_BsnssOffcr_PrsnNm",
       address_table."BsnssOffcr_PrsnTtlTxt" as "Donor_BsnssOffcr_PrsnTtlTxt",
       address_table."BsnssOffcr_PhnNm" as "Donor_BsnssOffcr_PhnNm" ,
       address_table."BsnssOffcr_EmlAddrssTxt"  as "Donor_BsnssOffcr_EmlAddrssTxt" ,
       address_table."USAddrss_AddrssLn1Txt" as "Donor_AddrssLn1Txt",
       address_table."USAddrss_AddrssLn2Txt" as "Donor_AddrssLn2Txt",
       address_table."USAddrss_CtyNm" as "Donor_CtyNm",
       address_table."USAddrss_SttAbbrvtnCd" as "Donor_SttAbbrvtnCd",
       address_table."USAddrss_ZIPCd" as "Donor_ZIPCd",
       address_table."FrgnAddrss_AddrssLn1Txt" as "Donor_FrgnAddrss_AddrssLn1Txt",
       address_table."FrgnAddrss_AddrssLn2Txt" as "Donor_FrgnAddrss_AddrssLn2Txt",
       address_table."FrgnAddrss_CtyNm" as "Donor_FrgnAddrss_CtyNm",
       address_table."FrgnAddrss_PrvncOrSttNm" as "Donor_PrvncOrSttNm",
       address_table."FrgnAddrss_CntryCd" as "Donor_CntryCd",
       return_SkdIRcpntTbl.ein as "Donor_EIN",
   	   '' as "RcpntPrsnNm", 
   	   return_SkdIRcpntTbl."RcpntTbl_RcpntEIN" as "Rcpnt_EIN",
       return_SkdIRcpntTbl."RcpntBsnssNm_BsnssNmLn1Txt"  as "Rcpnt_BsnssNmLn1",
       return_SkdIRcpntTbl."RcpntBsnssNm_BsnssNmLn2Txt"  as "Rcpnt_BsnssNmLn2",
       trim(concat(return_SkdIRcpntTbl."USAddrss_AddrssLn1Txt", ' ', return_SkdIRcpntTbl."FrgnAddrss_AddrssLn1Txt")) as "Rcpnt_AddrssLn1",
       trim(concat(return_SkdIRcpntTbl."USAddrss_AddrssLn2Txt", ' ', return_SkdIRcpntTbl."FrgnAddrss_AddrssLn2Txt")) as "Rcpnt_AddrssLn2",
       trim(concat(return_SkdIRcpntTbl."USAddrss_CtyNm", ' ', return_SkdIRcpntTbl."FrgnAddrss_CtyNm")) as "Rcpnt_CtyNm",
       trim(concat(return_SkdIRcpntTbl."USAddrss_SttAbbrvtnCd", ' ', return_SkdIRcpntTbl."FrgnAddrss_PrvncOrSttNm")) as "Rcpnt_SttAbbrvtnCd",
	   return_SkdIRcpntTbl."RcpntTbl_CshGrntAmt" as "Rcpnt_Amt",
	   return_SkdIRcpntTbl."RcpntTbl_PrpsOfGrntTxt" as "Rcpnt_PrpsTxt",
       trim(concat(return_SkdIRcpntTbl."USAddrss_ZIPCd", ' ', return_SkdIRcpntTbl."FrgnAddrss_FrgnPstlCd")) as "Rcpnt_ZIPCd",
        ''   as "Rcpnt_Rltnshp",
		return_SkdIRcpntTbl."RcpntTbl_IRCSctnDsc" as "Rcpnt_FndtnStts"
	INTO TEMPORARY TABLE grants
	FROM return_SkdIRcpntTbl
	LEFT JOIN address_table 
	ON return_SkdIRcpntTbl.object_id = address_table.object_id
	AND return_SkdIRcpntTbl.ein = address_table.ein;




-- Add org type data
select "Orgnztn501c3Ind", "Orgnztn501cInd", "Orgnztn49471NtPFInd", "Orgnztn527Ind", url_base,  '/IRS990ScheduleI' as form, grants.* into temporary table grants_types from grants left join org_types on grants.object_id = org_types.object_id and grants."Donor_EIN" = org_types.ein;

-- Then copy to local with \copy: 

\copy grants_types to '/data/file_exports/skedigrants.csv' with csv header;




--------
--  Form PF Part XV "Grant or Contribution Paid During Year"
--
-- See the IRSX documentation for form PPF Part XV [Grant or Contribution Paid During Year](http://www.irsx.info/metadata/groups/PFGrntOrCntrbtnPdDrYr.html)
--
-- Note that there's also a different section for grants of contributions approved for future years that we aren't using to avoid double-counting; see [the form instructions](https://www.irs.gov/instructions/i990pf#idm140486306377296) for (not much) more info. 
--------


DROP TABLE IF EXISTS pfgrants;

SELECT 
       return_PFGrntOrCntrbtnPdDrYr.object_id as object_id,
       address_table."RtrnHdr_TxPrdEndDt",
       address_table."RtrnHdr_TxYr",
       address_table."BsnssOffcr_SgntrDt",
       address_table."BsnssNm_BsnssNmLn1Txt" as "Donor_BsnssNmLn1",
       address_table."BsnssNm_BsnssNmLn2Txt" as "Donor_BsnssNmLn2",
       address_table."BsnssOffcr_PrsnNm" as "Donor_BsnssOffcr_PrsnNm",
       address_table."BsnssOffcr_PrsnTtlTxt" as "Donor_BsnssOffcr_PrsnTtlTxt",
       address_table."BsnssOffcr_PhnNm" as "Donor_BsnssOffcr_PhnNm" ,
       address_table."BsnssOffcr_EmlAddrssTxt"  as "Donor_BsnssOffcr_EmlAddrssTxt" ,
       address_table."USAddrss_AddrssLn1Txt" as "Donor_AddrssLn1Txt",
       address_table."USAddrss_AddrssLn2Txt" as "Donor_AddrssLn2Txt",
       address_table."USAddrss_CtyNm" as "Donor_CtyNm",
       address_table."USAddrss_SttAbbrvtnCd" as "Donor_SttAbbrvtnCd",
       address_table."USAddrss_ZIPCd" as "Donor_ZIPCd",
       address_table."FrgnAddrss_AddrssLn1Txt" as "Donor_FrgnAddrss_AddrssLn1Txt",
       address_table."FrgnAddrss_AddrssLn2Txt" as "Donor_FrgnAddrss_AddrssLn2Txt",
       address_table."FrgnAddrss_CtyNm" as "Donor_FrgnAddrss_CtyNm",
       address_table."FrgnAddrss_PrvncOrSttNm" as "Donor_PrvncOrSttNm",
       address_table."FrgnAddrss_CntryCd" as "Donor_CntryCd",
       return_PFGrntOrCntrbtnPdDrYr.ein as "Donor_EIN",
       '' as "Rcpnt_EIN",
       return_PFGrntOrCntrbtnPdDrYr."GrntOrCntrbtnPdDrYr_RcpntPrsnNm"   as "RcpntPrsnNm",
       return_PFGrntOrCntrbtnPdDrYr."RcpntBsnssNm_BsnssNmLn1Txt"   as "Rcpnt_BsnssNmLn1",
       return_PFGrntOrCntrbtnPdDrYr."RcpntBsnssNm_BsnssNmLn2Txt"   as "Rcpnt_BsnssNmLn2",
       trim(concat(return_PFGrntOrCntrbtnPdDrYr."RcpntUSAddrss_AddrssLn1Txt", ' ', return_PFGrntOrCntrbtnPdDrYr."RcpntFrgnAddrss_AddrssLn1Txt")) as "Rcpnt_AddrssLn1",
       trim(concat(return_PFGrntOrCntrbtnPdDrYr."RcpntUSAddrss_AddrssLn2Txt", ' ', return_PFGrntOrCntrbtnPdDrYr."RcpntFrgnAddrss_AddrssLn2Txt")) as "Rcpnt_AddrssLn2",
       trim(concat(return_PFGrntOrCntrbtnPdDrYr."RcpntUSAddrss_CtyNm", ' ', return_PFGrntOrCntrbtnPdDrYr."RcpntFrgnAddrss_CtyNm")) as "Rcpnt_CtyNm",
       trim(concat(return_PFGrntOrCntrbtnPdDrYr."RcpntUSAddrss_SttAbbrvtnCd", ' ', return_PFGrntOrCntrbtnPdDrYr."RcpntFrgnAddrss_PrvncOrSttNm")) as "Rcpnt_SttAbbrvtnCd",
	   return_PFGrntOrCntrbtnPdDrYr."GrntOrCntrbtnPdDrYr_Amt" as "Rcpnt_Amt",
	   return_PFGrntOrCntrbtnPdDrYr."GrntOrCntrbtnPdDrYr_GrntOrCntrbtnPrpsTxt" as "Rcpnt_PrpsTxt",
       trim(concat(return_PFGrntOrCntrbtnPdDrYr."RcpntUSAddrss_ZIPCd", ' ', return_PFGrntOrCntrbtnPdDrYr."RcpntFrgnAddrss_FrgnPstlCd")) as "Rcpnt_ZIPCd",
       return_PFGrntOrCntrbtnPdDrYr."GrntOrCntrbtnPdDrYr_RcpntRltnshpTxt"   as "Rcpnt_Rltnshp",
       return_PFGrntOrCntrbtnPdDrYr."GrntOrCntrbtnPdDrYr_RcpntFndtnSttsTxt"   as "Rcpnt_FndtnStts"
		INTO TEMPORARY TABLE pfgrants
			FROM return_PFGrntOrCntrbtnPdDrYr
			LEFT JOIN address_table ON return_PFGrntOrCntrbtnPdDrYr.object_id = address_table.object_id
			AND return_PFGrntOrCntrbtnPdDrYr.ein = address_table.ein;

-- Add org type data
select "Orgnztn501c3Ind", "Orgnztn501cInd", "Orgnztn49471NtPFInd", "Orgnztn527Ind", url_base,  '/IRS990PF' as form, pfgrants.* into temporary table pfgrants_types from pfgrants left join org_types on pfgrants.object_id = org_types.object_id and pfgrants."Donor_EIN" = org_types.ein;

-- Copy to local 

\copy pfgrants_types to '/data/file_exports/pfgrants.csv' with csv header;
