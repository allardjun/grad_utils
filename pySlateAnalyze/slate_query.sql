-- If Slate allows creation of a query from a SQL file, 

select 
	p.[last] as [Legal Last], 
	p.[first] as [Legal First], 
	(case p.[citizenship] when 'US' then 'US Citizen' when 'PR' then 'Permanent Resident' when 'FN' then 'Foreign National' end) as [Citizenship Status], 
	case when (select [value] from dbo.getFieldTopTable(a.[id], 'gd_pershistrequired')) = '1' then 'Domestic'
		when p.[citizenship] = 'US' then 'Domestic'
		when p.[citizenship] = 'PR' then 'Domestic'
		else 'International'
		end as [UCI Citizenship], 
	adw.[name] as [Country], 
	(select [value] from dbo.getFieldTopTable(a.[id], 'gd_program')) as [Academic Program], 
	(select [value] from dbo.getFieldTopTable(p.[id], 'uci_genderidentity')) as [Details - Gender Identity], 
	r.[export3] as [Degree Level], 
	(select [name] from [user] where ([id] = rf_c068_1.[user])) as [#1 User Name - Review Form - Applicant Review (Interdisciplinary)], 
	(select [value] from dbo.getFormResponseTable(rf_c068_1.[id], 'review_applicant_reviewform_comments')) as [#1 Comments - Review Form - Applicant Review (Interdisciplinary)], 
	(select [value] from dbo.getFormResponseTable(rf_c068_1.[id], 'rating')) as [#1 Overall applicant rating (with 5 as the high scale) - Review Form - Applicant Review (Interdisciplinary)], 
	(select [name] from [user] where ([id] = rf_c068_2.[user])) as [#2 User Name - Review Form - Applicant Review (Interdisciplinary)], 
	(select [value] from dbo.getFormResponseTable(rf_c068_2.[id], 'review_applicant_reviewform_comments')) as [#2 Comments - Review Form - Applicant Review (Interdisciplinary)], 
	(select [value] from dbo.getFormResponseTable(rf_c068_2.[id], 'rating')) as [#2 Overall applicant rating (with 5 as the high scale) - Review Form - Applicant Review (Interdisciplinary)], 
	(select [name] from [user] where ([id] = rf_c068_3.[user])) as [#3 User Name - Review Form - Applicant Review (Interdisciplinary)], 
	(select [value] from dbo.getFormResponseTable(rf_c068_3.[id], 'review_applicant_reviewform_comments')) as [#3 Comments - Review Form - Applicant Review (Interdisciplinary)], 
	(select [value] from dbo.getFormResponseTable(rf_c068_3.[id], 'rating')) as [#3 Overall applicant rating (with 5 as the high scale) - Review Form - Applicant Review (Interdisciplinary)], 
	(select [name] from [user] where ([id] = rf_c068_4.[user])) as [#4 User Name - Review Form - Applicant Review (Interdisciplinary)], 
	(select [value] from dbo.getFormResponseTable(rf_c068_4.[id], 'review_applicant_reviewform_comments')) as [#4 Comments - Review Form - Applicant Review (Interdisciplinary)], 
	(select [value] from dbo.getFormResponseTable(rf_c068_4.[id], 'rating')) as [#4 Overall applicant rating (with 5 as the high scale) - Review Form - Applicant Review (Interdisciplinary)], 
	(select [name] from [user] where ([id] = rf_c068_5.[user])) as [#5 User Name - Review Form - Applicant Review (Interdisciplinary)], 
	(select [value] from dbo.getFormResponseTable(rf_c068_5.[id], 'review_applicant_reviewform_comments')) as [#5 Comments - Review Form - Applicant Review (Interdisciplinary)], 
	(select [value] from dbo.getFormResponseTable(rf_c068_5.[id], 'rating')) as [#5 Overall applicant rating (with 5 as the high scale) - Review Form - Applicant Review (Interdisciplinary)]
from [application] a
Inner join [person] p on (p.[id] = a.[person])
left outer join [address] ad on (ad.[record] = p.[id]) and (ad.[type] is null) and (ad.[rank] = 1)
left outer join world.dbo.[country] adw on (adw.[id] = ad.[country])
left outer join [lookup.round] r on (r.[id] = a.[round])
left outer join [lookup.period] rp on (rp.[id] = r.[period])
left outer join [lookup.bin] b on (b.[id] = a.[bin])
left outer join [form.response] rf_c068_1 on (rf_c068_1.[record] = a.[id]) and (rf_c068_1.[form] = 'c068978c-c35b-4c8d-a496-d33ccbad6400') and (rf_c068_1.[rank_form] = 1)
left outer join [form.response] rf_c068_2 on (rf_c068_2.[record] = a.[id]) and (rf_c068_2.[form] = 'c068978c-c35b-4c8d-a496-d33ccbad6400') and (rf_c068_2.[rank_form] = 2)
left outer join [form.response] rf_c068_3 on (rf_c068_3.[record] = a.[id]) and (rf_c068_3.[form] = 'c068978c-c35b-4c8d-a496-d33ccbad6400') and (rf_c068_3.[rank_form] = 3)
left outer join [form.response] rf_c068_4 on (rf_c068_4.[record] = a.[id]) and (rf_c068_4.[form] = 'c068978c-c35b-4c8d-a496-d33ccbad6400') and (rf_c068_4.[rank_form] = 4)
left outer join [form.response] rf_c068_5 on (rf_c068_5.[record] = a.[id]) and (rf_c068_5.[form] = 'c068978c-c35b-4c8d-a496-d33ccbad6400') and (rf_c068_5.[rank_form] = 5)
where
(
	exists(
  select 1
  from dbo.getRights(@user) rts 
  inner join [population] a_pop on (a_pop.[record] = a.[id]) 
  inner join [lookup.population] lp_apop on (lp_apop.[id] = a_pop.[population]) 
  where (rts.[summary] = (lp_apop.[name]))
  union all select 1 from dbo.getRights(@user) where ([summary] = 'Administrator (All Access)')
  union all select 1 where (@user is null)
)
	and
	(
		/* Academic Program - Biological Sciences */
		(a.[id] IN (select [record] from [field] where ([field] = 'gd_program') and ([prompt] in ('20708fa1-2e02-42ac-9260-9cf8f1100aca', 'b912463c-9232-4226-a206-d97afef84c21'))))
		and
		/* Round */
		(a.[round] IN ('bf31224e-6943-4b34-bc83-6bf1f67c9160'))
	)
)
order by p.[last], p.[first]
option (recompile)
