

-- 990 Employees


DROP TABLE IF EXISTS tmp_990_employees;
SELECT address_table.*,
	'/IRS990' as form,
   "PrsnNm",
   "TtlTxt",
   "RprtblCmpFrmOrgAmt" as "CmpnstnAmt"
INTO temporary table tmp_990_employees
FROM return_Frm990PrtVIISctnA
LEFT JOIN address_table ON return_Frm990PrtVIISctnA.ein = address_table.ein
AND return_Frm990PrtVIISctnA.object_id=address_table.object_id;

DROP TABLE IF EXISTS tmp_990_employees_types;

select "Orgnztn501c3Ind", "Orgnztn501cInd", "Orgnztn49471NtPFInd", "Orgnztn527Ind", url_base,  tmp_990_employees.* into temporary table tmp_990_employees_types from tmp_990_employees left join org_types on tmp_990_employees.object_id = org_types.object_id and tmp_990_employees.ein = org_types.ein;
\copy tmp_990_employees_types to '/data/file_exports/990_employees.csv' with csv header;


-- EZ



DROP TABLE IF EXISTS tmp_990ez_employees;
SELECT address_table.*,
	'/IRS990EZ' as form,
   "PrsnNm",
   "TtlTxt",
   "CmpnstnAmt" 
   INTO temporary table tmp_990EZ_employees
   FROM return_EZOffcrDrctrTrstEmpl
	LEFT JOIN address_table ON return_EZOffcrDrctrTrstEmpl.ein = address_table.ein
	AND return_EZOffcrDrctrTrstEmpl.object_id= address_table.object_id;

select "Orgnztn501c3Ind", "Orgnztn501cInd", "Orgnztn49471NtPFInd", "Orgnztn527Ind", url_base,  tmp_990EZ_employees.* into temporary table tmp_990EZ_employees_types from tmp_990EZ_employees left join org_types on tmp_990EZ_employees.object_id = org_types.object_id and tmp_990EZ_employees.ein = org_types.ein;
\copy tmp_990EZ_employees_types to '/data/file_exports/990EZ_employees.csv' with csv header;


-- PF


DROP TABLE IF EXISTS tmp_990PF_employees;
SELECT address_table.*,
		'/IRS990PF' as form,
       "OffcrDrTrstKyEmpl_PrsnNm" AS "PrsnNm",
       "OffcrDrTrstKyEmpl_TtlTxt" AS "TtlTxt",
       "OffcrDrTrstKyEmpl_CmpnstnAmt" AS "CmpnstnAmt" 
INTO temporary table tmp_990PF_employees
FROM return_PFOffcrDrTrstKyEmpl
LEFT JOIN address_table ON return_PFOffcrDrTrstKyEmpl.ein = address_table.ein
AND return_PFOffcrDrTrstKyEmpl.object_id= address_table.object_id;

select "Orgnztn501c3Ind", "Orgnztn501cInd", "Orgnztn49471NtPFInd", "Orgnztn527Ind", url_base,  tmp_990PF_employees.* into temporary table tmp_990PF_employees_types from tmp_990PF_employees left join org_types on tmp_990PF_employees.object_id = org_types.object_id and tmp_990PF_employees.ein = org_types.ein;
\copy tmp_990PF_employees_types to '/data/file_exports/990PF_employees.csv' with csv header;



