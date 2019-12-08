-- Assumes that directors was already run. 

-- Schedule I

-- The schedule I variables are defined in the [irsx documentation](http://www.irsx.info/metadata/groups/SkdIRcpntTbl.html).

--  Here's a query to a temp table


DROP TABLE IF EXISTS grants;

SELECT 
       address_table."RtrnHdr_TxPrdEndDt",
       address_table."RtrnHdr_TxYr",
       address_table."BsnssOffcr_SgntrDt",
       address_table."BsnssNm_BsnssNmLn1Txt" as "Donor_BsnssNmLn1",
       address_table."BsnssNm_BsnssNmLn2Txt" as "Donor_BsnssNmL21",
       address_table."BsnssOffcr_PrsnNm" as "Donor_BsnssOffcr_PrsnNm",
       address_table."BsnssOffcr_PrsnTtlTxt" as "Donor_ BsnssOffcr_PrsnTtlTxt",
       address_table."BsnssOffcr_PhnNm" as "Donor_ BsnssOffcr_PhnNm" ,
       address_table."BsnssOffcr_EmlAddrssTxt"  as "Donor_ BsnssOffcr_EmlAddrssTxt" ,
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
       return_SkdIRcpntTbl.* 
INTO TEMPORARY TABLE grants
FROM return_SkdIRcpntTbl
LEFT JOIN address_table 
ON return_SkdIRcpntTbl.object_id = address_table.object_id
AND return_SkdIRcpntTbl.ein = address_table.ein;




-- Add org type data
select "Orgnztn501c3Ind", "Orgnztn501cInd", "Orgnztn49471NtPFInd", "Orgnztn527Ind", url_base,  '/IRS990ScheduleI' as form, grants.* into temporary table grants_types from grants left join org_types on grants.object_id = org_types.object_id and grants.ein = org_types.ein;

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
       address_table."RtrnHdr_TxPrdEndDt",
       address_table."RtrnHdr_TxYr",
       address_table."BsnssOffcr_SgntrDt",
       address_table."BsnssNm_BsnssNmLn1Txt" as "Donor_BsnssNmLn1",
       address_table."BsnssNm_BsnssNmLn2Txt" as "Donor_BsnssNmLn2",
       address_table."BsnssOffcr_PrsnNm" as "Donor_BsnssOffcr_PrsnNm",
       address_table."BsnssOffcr_PrsnTtlTxt" as "Donor_ BsnssOffcr_PrsnTtlTxt",
       address_table."BsnssOffcr_PhnNm" as "Donor_ BsnssOffcr_PhnNm" ,
       address_table."BsnssOffcr_EmlAddrssTxt"  as "Donor_ BsnssOffcr_EmlAddrssTxt" ,
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
        return_PFGrntOrCntrbtnPdDrYr.*
       
		INTO TABLE pfgrants
			FROM return_PFGrntOrCntrbtnPdDrYr
			LEFT JOIN address_table ON return_PFGrntOrCntrbtnPdDrYr.object_id = address_table.object_id
			AND return_PFGrntOrCntrbtnPdDrYr.ein = address_table.ein;

-- Add org type data
select "Orgnztn501c3Ind", "Orgnztn501cInd", "Orgnztn49471NtPFInd", "Orgnztn527Ind", url_base,  '/IRS990PF' as form, pfgrants.* into temporary table pfgrants_types from pfgrants left join org_types on pfgrants.object_id = org_types.object_id and pfgrants.ein = org_types.ein;

-- Copy to local 

\copy pfgrants_types to '/data/file_exports/pfgrants.csv' with csv header;
