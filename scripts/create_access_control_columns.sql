alter table referral_referralattach add (only_professionals tinyint(1));

update referral_referralattach set only_professionals = 0;

alter table referral_referralattach modify only_professionals  tinyint(1) not null;

alter table referral_referralattach add (only_psychologists tinyint(1));

update referral_referralattach set only_psychologists = 0;

alter table referral_referralattach modify only_psychologists  tinyint(1) not null;