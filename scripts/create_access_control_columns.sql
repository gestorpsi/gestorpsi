alter table referral_referralattach add (is_locked tinyint(1));

update referral_referralattach set is_locked = 0;

alter table referral_referralattach modify is_locked  tinyint(1) not null;