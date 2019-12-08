-- Write out reference charts: address and org_types

DROP TABLE if exists address_table;

SELECT  
   return_returnheader990x_part_i.ein,
   return_returnheader990x_part_i.object_id,
   return_returnheader990x_part_i."RtrnHdr_TxPrdEndDt",
   return_returnheader990x_part_i."RtrnHdr_TxYr",
   return_returnheader990x_part_i."BsnssNm_BsnssNmLn1Txt",
   return_returnheader990x_part_i."BsnssNm_BsnssNmLn2Txt",
   return_returnheader990x_part_i."BsnssOffcr_PrsnNm",
   return_returnheader990x_part_i."BsnssOffcr_PrsnTtlTxt",
   return_returnheader990x_part_i."BsnssOffcr_PhnNm",
   return_returnheader990x_part_i."BsnssOffcr_EmlAddrssTxt",
   return_returnheader990x_part_i."BsnssOffcr_SgntrDt",
   return_returnheader990x_part_i."USAddrss_AddrssLn1Txt",
   return_returnheader990x_part_i."USAddrss_AddrssLn2Txt",
   return_returnheader990x_part_i."USAddrss_CtyNm",
   return_returnheader990x_part_i."USAddrss_SttAbbrvtnCd",
   return_returnheader990x_part_i."USAddrss_ZIPCd",
   return_returnheader990x_part_i."FrgnAddrss_AddrssLn1Txt",
	return_returnheader990x_part_i."FrgnAddrss_AddrssLn2Txt",
	return_returnheader990x_part_i."FrgnAddrss_CtyNm",
	return_returnheader990x_part_i."FrgnAddrss_PrvncOrSttNm",
	return_returnheader990x_part_i."FrgnAddrss_CntryCd"      
INTO address_table
FROM return_returnheader990x_part_i;


DROP INDEX IF EXISTS xx_990_address_oid_ein;
CREATE INDEX xx_990_address_oid_ein ON address_table (object_id, ein);


drop table if exists org_types;

select distinct "Orgnztn501c3Ind", "Orgnztn501cInd", "Orgnztn49471NtPFInd", "Orgnztn527Ind", ein, object_id, concat(ein, '/', object_id) as url_base into org_types from return_part_0;

insert into org_types select distinct "Orgnztn501c3Ind", "Orgnztn501cInd", "Orgnztn49471NtPFInd", "Orgnztn527Ind", ein, object_id, concat(ein, '/', object_id) as url_base  from return_ez_part_0;

insert into org_types("Orgnztn501c3Ind", "Orgnztn501cInd", "Orgnztn49471NtPFInd", ein, object_id, url_base) select distinct "Orgnztn501c3ExmptPFInd" as "Orgnztn501c3Ind",  "Orgnztn501c3TxblPFInd" as "Orgnztn501cInd", "Orgnztn49471TrtdPFInd" as "Orgnztn49471NtPFInd", ein, object_id, concat(ein, '/', object_id) as url_base from return_pf_part_0;

DROP INDEX IF EXISTS xx_990_entity_oid_ein;
CREATE INDEX xx_990_entity_oid_ein ON org_types (object_id, ein);
