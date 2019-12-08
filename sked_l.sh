
-- Schedule L - Transactions with interested parties

-- Part I: Excess Benefit Transactions 
-- See the repeating group docs [here](http://www.irsx.info/metadata/groups/SkdLDsqlfdPrsnExBnftTr.html)



DROP TABLE IF EXISTS excess_benefits;

SELECT 
       address_table."RtrnHdr_TxPrdEndDt",
       address_table."RtrnHdr_TxYr",
       address_table."BsnssOffcr_SgntrDt",
       address_table."BsnssNm_BsnssNmLn1Txt" as "Org_BsnssNmLn1",
       address_table."BsnssNm_BsnssNmLn2Txt" as "Org_BsnssNmL21",
       address_table."BsnssOffcr_PrsnNm" as "Org_BsnssOffcr_PrsnNm",
       address_table."BsnssOffcr_PrsnTtlTxt" as "Org_BsnssOffcr_PrsnTtlTxt",
       address_table."BsnssOffcr_PhnNm" as "Org_BsnssOffcr_PhnNm" ,
       address_table."BsnssOffcr_EmlAddrssTxt"  as "Org_BsnssOffcr_EmlAddrssTxt" ,
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
        return_SkdLDsqlfdPrsnExBnftTr.*
	INTO TEMPORARY TABLE excess_benefits
    FROM return_SkdLDsqlfdPrsnExBnftTr
    LEFT JOIN address_table ON return_SkdLDsqlfdPrsnExBnftTr.object_id = address_table.object_id
    AND return_SkdLDsqlfdPrsnExBnftTr.ein = address_table.ein;


DROP TABLE IF EXISTS excess_benefits_types;

select "Orgnztn501c3Ind", "Orgnztn501cInd", "Orgnztn49471NtPFInd", "Orgnztn527Ind", concat(org_types.ein, '/', org_types.object_id) as url_base, '/IRS990ScheduleL' as form,  excess_benefits.* into TEMPORARY TABLE excess_benefits_types from excess_benefits left join org_types on excess_benefits.object_id = org_types.object_id;

\copy excess_benefits_types to '/data/file_exports/excess_benefits.csv' with csv header;




-- Part II: Loans Between the Organization and Interested Persons

-- Loans from the org to an insider
-- See the repeating group docs [here](http://www.irsx.info/metadata/groups/SkdLLnsBtwnOrgIntrstdPrsn.html)



DROP TABLE IF EXISTS loans_from;
	
SELECT 
       address_table."RtrnHdr_TxPrdEndDt",
       address_table."RtrnHdr_TxYr",
       address_table."BsnssOffcr_SgntrDt",
       address_table."BsnssNm_BsnssNmLn1Txt" as "Org_BsnssNmLn1",
       address_table."BsnssNm_BsnssNmLn2Txt" as "Org_BsnssNmL21",
       address_table."BsnssOffcr_PrsnNm" as "Org_BsnssOffcr_PrsnNm",
       address_table."BsnssOffcr_PrsnTtlTxt" as "Org_BsnssOffcr_PrsnTtlTxt",
       address_table."BsnssOffcr_PhnNm" as "Org_BsnssOffcr_PhnNm" ,
       address_table."BsnssOffcr_EmlAddrssTxt"  as "Org_BsnssOffcr_EmlAddrssTxt" ,
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
        return_SkdLLnsBtwnOrgIntrstdPrsn.*

	INTO TEMPORARY TABLE loans_from
    FROM return_SkdLLnsBtwnOrgIntrstdPrsn
    LEFT JOIN address_table ON return_SkdLLnsBtwnOrgIntrstdPrsn.object_id = address_table.object_id
    AND return_SkdLLnsBtwnOrgIntrstdPrsn.ein = address_table.ein
	WHERE return_SkdLLnsBtwnOrgIntrstdPrsn."LnFrmOrgnztnInd" = 'X';
	

drop table if exists loans_from_types;

select "Orgnztn501c3Ind", "Orgnztn501cInd", "Orgnztn49471NtPFInd", "Orgnztn527Ind", concat(org_types.ein, '/', org_types.object_id) as url_base,  '/IRS990ScheduleL' as form, loans_from.* into temporary table loans_from_types from loans_from left join org_types on loans_from.object_id = org_types.object_id and loans_from.ein = org_types.ein;
  	

\copy loans_from_types to '/data/file_exports/loans_from.csv' with csv header;
            


-- Loans from an insider to the org



DROP TABLE IF EXISTS loans_to;
	
SELECT 
       address_table."RtrnHdr_TxPrdEndDt",
       address_table."RtrnHdr_TxYr",
       address_table."BsnssOffcr_SgntrDt",
       address_table."BsnssNm_BsnssNmLn1Txt" as "Org_BsnssNmLn1",
       address_table."BsnssNm_BsnssNmLn2Txt" as "Org_BsnssNmL21",
       address_table."BsnssOffcr_PrsnNm" as "Org_BsnssOffcr_PrsnNm",
       address_table."BsnssOffcr_PrsnTtlTxt" as "Org_BsnssOffcr_PrsnTtlTxt",
       address_table."BsnssOffcr_PhnNm" as "Org_BsnssOffcr_PhnNm" ,
       address_table."BsnssOffcr_EmlAddrssTxt"  as "Org_BsnssOffcr_EmlAddrssTxt" ,
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
        return_SkdLLnsBtwnOrgIntrstdPrsn.*
	INTO TEMPORARY TABLE loans_to
    FROM return_SkdLLnsBtwnOrgIntrstdPrsn
    LEFT JOIN address_table ON return_SkdLLnsBtwnOrgIntrstdPrsn.object_id = address_table.object_id
    AND return_SkdLLnsBtwnOrgIntrstdPrsn.ein = address_table.ein
	WHERE return_SkdLLnsBtwnOrgIntrstdPrsn."LnTOrgnztnInd" = 'X';

drop table if exists loans_to_types;

select "Orgnztn501c3Ind", "Orgnztn501cInd", "Orgnztn49471NtPFInd", "Orgnztn527Ind", concat(org_types.ein, '/', org_types.object_id) as url_base, '/IRS990ScheduleL' as form, loans_to.* into TEMPORARY TABLE loans_to_types from loans_to left join org_types on loans_to.object_id = org_types.object_id and loans_to.ein = org_types.ein;

  	
\copy loans_to_types to '/data/file_exports/loans_to.csv' with csv header;
	

-- Part III: Grants or Assistance Benefiting Interested Persons

-- http://www.irsx.info/metadata/groups/SkdLGrntAsstBnftIntrstdPrsn.html

DROP TABLE IF EXISTS insider_assistance;
	
SELECT 
       address_table."RtrnHdr_TxPrdEndDt",
       address_table."RtrnHdr_TxYr",
       address_table."BsnssOffcr_SgntrDt",
       address_table."BsnssNm_BsnssNmLn1Txt" as "Org_BsnssNmLn1",
       address_table."BsnssNm_BsnssNmLn2Txt" as "Org_BsnssNmL21",
       address_table."BsnssOffcr_PrsnNm" as "Org_BsnssOffcr_PrsnNm",
       address_table."BsnssOffcr_PrsnTtlTxt" as "Org_BsnssOffcr_PrsnTtlTxt",
       address_table."BsnssOffcr_PhnNm" as "Org_BsnssOffcr_PhnNm" ,
       address_table."BsnssOffcr_EmlAddrssTxt"  as "Org_BsnssOffcr_EmlAddrssTxt" ,
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
        return_SkdLGrntAsstBnftIntrstdPrsn.*
	INTO TEMPORARY TABLE insider_assistance
    FROM return_SkdLGrntAsstBnftIntrstdPrsn
    LEFT JOIN address_table ON return_SkdLGrntAsstBnftIntrstdPrsn.object_id = address_table.object_id
    AND return_SkdLGrntAsstBnftIntrstdPrsn.ein = address_table.ein


drop table if exists insider_assistance_types;

select "Orgnztn501c3Ind", "Orgnztn501cInd", "Orgnztn49471NtPFInd", "Orgnztn527Ind", concat(org_types.ein, '/', org_types.object_id) as url_base, '/IRS990ScheduleL' as form, insider_assistance.* into temporary table insider_assistance_types from insider_assistance left join org_types on insider_assistance.object_id = org_types.object_id and insider_assistance.ein = org_types.ein;


\copy insider_assistance_types to '/data/file_exports/insider_assistance.csv' with csv header;



-- Part IV:  Business Transactions Involving Interested Persons


-- http://www.irsx.info/metadata/groups/SkdLBsTrInvlvIntrstdPrsn.html

DROP TABLE IF EXISTS insider_transactions;
	
SELECT 
       address_table."RtrnHdr_TxPrdEndDt",
       address_table."RtrnHdr_TxYr",
       address_table."BsnssOffcr_SgntrDt",
       address_table."BsnssNm_BsnssNmLn1Txt" as "Org_BsnssNmLn1",
       address_table."BsnssNm_BsnssNmLn2Txt" as "Org_BsnssNmL21",
       address_table."BsnssOffcr_PrsnNm" as "Org_BsnssOffcr_PrsnNm",
       address_table."BsnssOffcr_PrsnTtlTxt" as "Org_BsnssOffcr_PrsnTtlTxt",
       address_table."BsnssOffcr_PhnNm" as "Org_BsnssOffcr_PhnNm" ,
       address_table."BsnssOffcr_EmlAddrssTxt"  as "Org_BsnssOffcr_EmlAddrssTxt" ,
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
        return_SkdLBsTrInvlvIntrstdPrsn.*
	INTO TEMPORARY TABLE insider_transactions
    FROM return_SkdLBsTrInvlvIntrstdPrsn
    LEFT JOIN address_table ON return_SkdLBsTrInvlvIntrstdPrsn.object_id = address_table.object_id
    AND return_SkdLBsTrInvlvIntrstdPrsn.ein = address_table.ein;

drop table if exists insider_transactions_types;

select "Orgnztn501c3Ind", "Orgnztn501cInd", "Orgnztn49471NtPFInd", "Orgnztn527Ind", concat(org_types.ein, '/', org_types.object_id) as url_base, '/IRS990ScheduleL' as form, insider_transactions.* into temporary table insider_transactions_types from insider_transactions left join org_types on insider_transactions.object_id = org_types.object_id and insider_transactions.ein = org_types.ein;


\copy insider_transactions_types to '/data/file_exports/insider_transactions.csv' with csv header;



