import csv
from typing import *


score_mapping = {
    'S1': 1, # nõrk
    'S2': 2, # mõõdukas
    'S3': 3, # tugev
    'S4': 0  # puudub
}
ex1 = {
    'abs': 'T1',
    'info': 'T2',
    'aeg': 'T3'
}
ex2 = {
    'afek': 'T1',
    'form': 'T2',
    'inter': 'T3'
}
ex3 = {'abs': 'T1',
       'info': 'T2',
       'aeg': 'T3'
}
ex4 = {
    'inst': 'T1',
    'keer': 'T2',
    'subj': 'T3'
}
ex5 = {
    'afek': 'T1',
    'form': 'T2',
    'inter': 'T3'
}
ex6 = {
    'spont': 'T1',
    'imp': 'T2',
    'arg': 'T3'
}
ex7 = {
    'spont': 'T1',
    'imp': 'T2',
    'arg': 'T3'
}
ex8 = {
    'inst': 'T1',
    'keer': 'T2',
    'subj': 'T3'
}

# URLid eksperimendis 1 ja 2
exp_12_text_urls = [
['www_ekspress_ee.ela_177019.txt','www_vorumaateataja_ee.ela_494965.txt'],
['et_wikipedia_org.ela_191506.txt','arhiiv_koolielu_ee.ela_481254.txt'],
['www_politsei_ee.ela_163441.txt','et_wikipedia_org.ela_219301.txt'],
['reisiajakiri_gomaailm_ee.ela_530539.txt','www_vsport_ee.ela_120496.txt'],
['eok_ee.ela_435890.txt','www_advent_ee.ela_658698.txt'],
['www_tallegg_ee.ela_33687.txt','www_tarbijakaitse_ee.ela_199918.txt'],
['www_lemmik_ee.ela_519214.txt','www_soudeliit_ee.ela_547578.txt'],
['www_xn--eestimngula-q8a_ee.ela_40079.txt','www_bioneer_ee.ela_243230.txt'],
['arvamusaed_ee.ela_6007.txt','rahvahaal_delfi_ee.ela_388979.txt'],
['blablabla_ee.ela_504829.txt','www_tootukassa_ee.ela_395777.txt'],
['forte_delfi_ee.ela_88079.txt','rahvahaal_delfi_ee.ela_258274.txt'],
['mesindus_ee.ela_210638.txt','www_porterracing_ee.ela_609577.txt'],
['www_horisont_ee.ela_455809.txt','www_pealinn_ee.ela_132426.txt'],
['www_nami-nami_ee.ela_456341.txt','www_3dnews_ee.ela_435253.txt'],
['www_post_ee.ela_149870.txt','www_kohus_ee.ela_34731.txt'],
['www_seduction_ee.ela_642092.txt','stiimul_ee.ela_330566.txt'],
['www_delfi_ee.ela_361703.txt','www_linnateater_ee.ela_612249.txt'],
['www_eramets_ee.ela_479405.txt','www_eestisport_ee.ela_196071.txt'],
['herba_folklore_ee.ela_93408.txt','unitedkiters_ee.ela_78733.txt'],
['www_linnaleht_ee.ela_420357.txt','rahvahaal_delfi_ee.ela_499379.txt'],
['www_bsd_ee.ela_638246.txt','www_aialeht_ee.ela_457123.txt'],
['www_horsemarket_ee.ela_436247.txt','et_wikipedia_org.ela_467359.txt'],
['www_auto24_ee.ela_469677.txt','www_director_ee.ela_529643.txt'],
['www_lapsemure_ee.ela_140896.txt','www_unesco_ee.ela_630384.txt'],
['www_ilm_err_ee.ela_196894.txt','www_riigikogu_ee.ela_224866.txt'],
['valitsus_ee.ela_604239.txt','www_politsei_ee.ela_40109.txt'],
['www_vnl_ee.ela_670256.txt','www_hambaarst_ee.ela_475731.txt'],
['video_usk_ee.ela_152445.txt','kalah_zzz_ee.ela_52237.txt'],
['sport_autonet_ee.ela_515760.txt','ylle_mrt_ee.ela_101705.txt'],
['www_puuinfo_ee.ela_279876.txt','www_eestikirik_ee.ela_530609.txt'],
['www_epl_ee.ela_679018.txt','www_emta_ee.ela_522725.txt'],
['blog_maaleht_ee.ela_73268.txt','bhr_balanss_ee.ela_565106.txt'],
['www_employers_ee.ela_617415.txt','www_kasutatudraamat_ee.ela_68759.txt'],
['nami-nami_ee.ela_372868.txt','reform_ee.ela_24983.txt'],
['www_nami-nami_ee.ela_173054.txt','www_mesindus_ee.ela_33384.txt'],
['www_vm_ee.ela_81604.txt','www_lounaleht_ee.ela_576969.txt'],
['www_mulje_ee.ela_177932.txt','et_wikipedia_org.ela_519819.txt'],
['www_jeesusekristusekirik_ee.ela_65555.txt','www_kv_ee.ela_199481.txt'],
['ekspress_online_2020.txt','www_admiralmarkets_ee.ela_456804.txt'],
['www_meiekirik_ee.ela_286284.txt','www_helen_ee.ela_520035.txt'],
['arvamusaed_ee.ela_274676.txt','uudised_err_ee.ela_541051.txt'],
['kalah_zzz_ee.ela_73709.txt','www_mod_gov_ee.ela_178680.txt'],
['www_ajakiri_ut_ee.ela_429007.txt','no_spam_ee.ela_2227.txt'],
['valitsus_ee.ela_132104.txt','www_lillelapsed_ee.ela_607751.txt'],
['www_naisteleht_ee.ela_355886.txt','www_sirp_ee.ela_651305.txt'],
['forte_delfi_ee.ela_222312.txt','www_alphagis_ee.ela_403490.txt'],
['www_admiralmarkets_ee.ela_333517.txt','uuseesti_ee.ela_112397.txt'],
['www_vorumaateataja_ee.ela_241120.txt','www_easl_ee.ela_201171.txt'],
['www_eestigiid_ee.ela_530847.txt','www_hambaarst_ee.ela_423040.txt'],
['www_ekspress_ee.ela_495829.txt','www_syndikaat_ee.ela_469373.txt'],
['static_inimene_ee.ela_194968.txt','kaja_ekstreem_ee.ela_71641.txt'],
['www_europarl_ee.ela_36110.txt','et_wikipedia_org.ela_624820.txt'],
['arvamus_postimees_ee.ela_5946.txt','www_le_ee.ela_240831.txt'],
['valitsus_ee.ela_480708.txt','www_dragon_ee.ela_303548.txt'],
['www_epl_ee.ela_685672.txt','www_tuuleenergia_ee.ela_40373.txt'],
['rahvahaal_delfi_ee.ela_135048.txt','www_epl_ee.ela_495381.txt'],
['www_autoleht_ee.ela_469280.txt','www_maaleht_ee.ela_246360.txt'],
['toompark_pri_ee.ela_458650.txt','www_reklaamitrikk_ee.ela_315713.txt'],
['www_tooelu_ee.ela_624263.txt','www_med24_ee.ela_557549.txt'],
['untitled.txt','www_snap_ee.ela_623342.txt']
]
exp_34_text_urls = [
['www_tooelu_ee.ela_624263.txt', 'www_easl_ee.ela_201171.txt'],
['www_autoleht_ee.ela_469280.txt', 'www_syndikaat_ee.ela_469373.txt'],
['ylle_mrt_ee.ela_101705.txt', 'rahvahaal_delfi_ee.ela_499379.txt'],
['www_admiralmarkets_ee.ela_456804.txt', 'www_linnateater_ee.ela_612249.txt'],
['static_inimene_ee.ela_194968.txt', 'www_bioneer_ee.ela_243230.txt'],
['www_tarbijakaitse_ee.ela_199918.txt', 'www_vorumaateataja_ee.ela_494965.txt'],
['www_delfi_ee.ela_361703.txt', 'www_3dnews_ee.ela_435253.txt'],
['www_ajakiri_ut_ee.ela_429007.txt', 'ekspress_online_2020.txt'],
['www_hambaarst_ee.ela_423040.txt', 'uudised_err_ee.ela_541051.txt'],
['www_eramets_ee.ela_479405.txt', 'www_unesco_ee.ela_630384.txt'],
['www_epl_ee.ela_495381.txt', 'www_epl_ee.ela_679018.txt'],
['valitsus_ee.ela_604239.txt', 'sport_autonet_ee.ela_515760.txt'],
['www_politsei_ee.ela_163441.txt', 'arvamusaed_ee.ela_6007.txt'],
['stiimul_ee.ela_330566.txt', 'www_seduction_ee.ela_642092.txt'],
['www_kohus_ee.ela_34731.txt', 'www_lapsemure_ee.ela_140896.txt'],
['et_wikipedia_org.ela_624820.txt', 'et_wikipedia_org.ela_519819.txt'],
['blablabla_ee.ela_504829.txt', 'www_director_ee.ela_529643.txt'],
['et_wikipedia_org.ela_219301.txt', 'www_politsei_ee.ela_40109.txt'],
['www_lounaleht_ee.ela_576969.txt', 'rahvahaal_delfi_ee.ela_258274.txt'],
['arvamusaed_ee.ela_274676.txt', 'www_ekspress_ee.ela_495829.txt'],
['www_ekspress_ee.ela_177019.txt', 'www_aialeht_ee.ela_457123.txt'],
['www_puuinfo_ee.ela_279876.txt', 'www_kv_ee.ela_199481.txt'],
['www_snap_ee.ela_623342.txt', 'www_riigikogu_ee.ela_224866.txt'],
['www_eestikirik_ee.ela_530609.txt', 'www_jeesusekristusekirik_ee.ela_65555.txt'],
['www_nami-nami_ee.ela_456341.txt', 'www_vnl_ee.ela_670256.txt'],
['www_maaleht_ee.ela_246360.txt', 'uuseesti_ee.ela_112397.txt'],
['kalah_zzz_ee.ela_73709.txt', 'rahvahaal_delfi_ee.ela_388979.txt'],
['www_med24_ee.ela_557549.txt', 'www_ilm_err_ee.ela_196894.txt'],
['www_tootukassa_ee.ela_395777.txt', 'www_mod_gov_ee.ela_178680.txt'],
['www_pealinn_ee.ela_132426.txt', 'www_advent_ee.ela_658698.txt'],
['www_auto24_ee.ela_469677.txt', 'www_tuuleenergia_ee.ela_40373.txt'],
['www_bsd_ee.ela_638246.txt', 'www_le_ee.ela_240831.txt'],
['www_xn--eestimngula-q8a_ee.ela_40079.txt', 'www_vorumaateataja_ee.ela_241120.txt'],
['www_mesindus_ee.ela_33384.txt', 'www_horsemarket_ee.ela_436247.txt'],
['www_eestisport_ee.ela_196071.txt', 'forte_delfi_ee.ela_88079.txt'],
['www_vm_ee.ela_81604.txt', 'et_wikipedia_org.ela_191506.txt'],
['www_hambaarst_ee.ela_475731.txt', 'arhiiv_koolielu_ee.ela_481254.txt'],
['mesindus_ee.ela_210638.txt', 'www_emta_ee.ela_522725.txt'],
['www_alphagis_ee.ela_403490.txt', 'www_meiekirik_ee.ela_286284.txt'],
['www_soudeliit_ee.ela_547578.txt', 'bhr_balanss_ee.ela_565106.txt'],
['www_sirp_ee.ela_651305.txt', 'www_helen_ee.ela_520035.txt'],
['www_europarl_ee.ela_36110.txt', 'nami-nami_ee.ela_372868.txt'],
['video_usk_ee.ela_152445.txt', 'blog_maaleht_ee.ela_73268.txt'],
['forte_delfi_ee.ela_222312.txt', 'www_eestigiid_ee.ela_530847.txt'],
['www_dragon_ee.ela_303548.txt', 'arvamus_postimees_ee.ela_5946.txt'],
['www_porterracing_ee.ela_609577.txt', 'www_naisteleht_ee.ela_355886.txt'],
['toompark_pri_ee.ela_458650.txt', 'reisiajakiri_gomaailm_ee.ela_530539.txt'],
['et_wikipedia_org.ela_467359.txt', 'www_horisont_ee.ela_455809.txt'],
['untitled.txt', 'www_tallegg_ee.ela_33687.txt'],
['eok_ee.ela_435890.txt', 'kalah_zzz_ee.ela_52237.txt'],
['valitsus_ee.ela_480708.txt', 'www_kasutatudraamat_ee.ela_68759.txt'],
['www_epl_ee.ela_685672.txt', 'unitedkiters_ee.ela_78733.txt'],
['www_linnaleht_ee.ela_420357.txt', 'www_nami-nami_ee.ela_173054.txt'],
['www_mulje_ee.ela_177932.txt', 'rahvahaal_delfi_ee.ela_135048.txt'],
['valitsus_ee.ela_132104.txt', 'www_vsport_ee.ela_120496.txt'],
['www_lemmik_ee.ela_519214.txt', 'no_spam_ee.ela_2227.txt'],
['reform_ee.ela_24983.txt', 'www_admiralmarkets_ee.ela_333517.txt'],
['www_post_ee.ela_149870.txt', 'www_reklaamitrikk_ee.ela_315713.txt'],
['www_lillelapsed_ee.ela_607751.txt', 'kaja_ekstreem_ee.ela_71641.txt'],
['herba_folklore_ee.ela_93408.txt', 'www_employers_ee.ela_617415.txt']
]
exp_56_text_urls = [
['www_alphagis_ee.ela_403490.txt', 'www_aialeht_ee.ela_457123.txt'],
['www_admiralmarkets_ee.ela_456804.txt', 'www_dragon_ee.ela_303548.txt'],
['www_vorumaateataja_ee.ela_241120.txt', 'www_syndikaat_ee.ela_469373.txt'],
['www_politsei_ee.ela_40109.txt', 'www_ilm_err_ee.ela_196894.txt'],
['www_emta_ee.ela_522725.txt', 'bhr_balanss_ee.ela_565106.txt'],
['rahvahaal_delfi_ee.ela_258274.txt', 'www_eramets_ee.ela_479405.txt'],
['www_porterracing_ee.ela_609577.txt', 'www_eestigiid_ee.ela_530847.txt'],
['www_lapsemure_ee.ela_140896.txt', 'uuseesti_ee.ela_112397.txt'],
['www_eestikirik_ee.ela_530609.txt', 'www_linnateater_ee.ela_612249.txt'],
['www_meiekirik_ee.ela_286284.txt', 'www_unesco_ee.ela_630384.txt'],
['valitsus_ee.ela_132104.txt', 'unitedkiters_ee.ela_78733.txt'],
['www_hambaarst_ee.ela_423040.txt', 'www_bsd_ee.ela_638246.txt'],
['nami-nami_ee.ela_372868.txt', 'www_bioneer_ee.ela_243230.txt'],
['www_kasutatudraamat_ee.ela_68759.txt', 'blog_maaleht_ee.ela_73268.txt'],
['www_3dnews_ee.ela_435253.txt', 'untitled.txt'],
['www_pealinn_ee.ela_132426.txt', 'www_europarl_ee.ela_36110.txt'],
['kalah_zzz_ee.ela_73709.txt', 'www_ekspress_ee.ela_495829.txt'],
['reisiajakiri_gomaailm_ee.ela_530539.txt', 'www_maaleht_ee.ela_246360.txt'],
['rahvahaal_delfi_ee.ela_499379.txt', 'www_tallegg_ee.ela_33687.txt'],
['www_le_ee.ela_240831.txt', 'valitsus_ee.ela_480708.txt'],
['arvamusaed_ee.ela_6007.txt', 'et_wikipedia_org.ela_467359.txt'],
['www_epl_ee.ela_679018.txt', 'et_wikipedia_org.ela_219301.txt'],
['www_mesindus_ee.ela_33384.txt', 'www_hambaarst_ee.ela_475731.txt'],
['no_spam_ee.ela_2227.txt', 'www_sirp_ee.ela_651305.txt'],
['www_auto24_ee.ela_469677.txt', 'valitsus_ee.ela_604239.txt'],
['www_epl_ee.ela_685672.txt', 'www_horsemarket_ee.ela_436247.txt'],
['www_horisont_ee.ela_455809.txt', 'www_vorumaateataja_ee.ela_494965.txt'],
['www_easl_ee.ela_201171.txt', 'www_lillelapsed_ee.ela_607751.txt'],
['www_naisteleht_ee.ela_355886.txt', 'forte_delfi_ee.ela_88079.txt'],
['www_tarbijakaitse_ee.ela_199918.txt', 'www_employers_ee.ela_617415.txt'],
['www_eestisport_ee.ela_196071.txt', 'eok_ee.ela_435890.txt'],
['arhiiv_koolielu_ee.ela_481254.txt', 'ylle_mrt_ee.ela_101705.txt'],
['www_kohus_ee.ela_34731.txt', 'toompark_pri_ee.ela_458650.txt'],
['www_autoleht_ee.ela_469280.txt', 'www_nami-nami_ee.ela_173054.txt'],
['uudised_err_ee.ela_541051.txt', 'www_med24_ee.ela_557549.txt'],
['mesindus_ee.ela_210638.txt', 'www_post_ee.ela_149870.txt'],
['www_xn--eestimngula-q8a_ee.ela_40079.txt', 'www_mulje_ee.ela_177932.txt'],
['static_inimene_ee.ela_194968.txt', 'www_lemmik_ee.ela_519214.txt'],
['www_lounaleht_ee.ela_576969.txt', 'et_wikipedia_org.ela_519819.txt'],
['forte_delfi_ee.ela_222312.txt', 'arvamus_postimees_ee.ela_5946.txt'],
['www_seduction_ee.ela_642092.txt', 'www_reklaamitrikk_ee.ela_315713.txt' ],
['www_vsport_ee.ela_120496.txt', 'www_mod_gov_ee.ela_178680.txt'],
['rahvahaal_delfi_ee.ela_135048.txt', 'kalah_zzz_ee.ela_52237.txt'],
['www_helen_ee.ela_520035.txt', 'www_delfi_ee.ela_361703.txt'],
['reform_ee.ela_24983.txt', 'www_tooelu_ee.ela_624263.txt'],
['blablabla_ee.ela_504829.txt', 'www_jeesusekristusekirik_ee.ela_65555.txt'],
['www_politsei_ee.ela_163441.txt', 'www_kv_ee.ela_199481.txt'],
['www_ekspress_ee.ela_177019.txt', 'www_tootukassa_ee.ela_395777.txt'],
['www_soudeliit_ee.ela_547578.txt', 'et_wikipedia_org.ela_191506.txt'],
['video_usk_ee.ela_152445.txt', 'www_director_ee.ela_529643.txt'],
['www_vnl_ee.ela_670256.txt', 'www_nami-nami_ee.ela_456341.txt'],
['www_ajakiri_ut_ee.ela_429007.txt', 'www_snap_ee.ela_623342.txt'],
['ekspress_online_2020.txt', 'www_linnaleht_ee.ela_420357.txt'],
['www_admiralmarkets_ee.ela_333517.txt', 'www_vm_ee.ela_81604.txt'],
['herba_folklore_ee.ela_93408.txt', 'www_tuuleenergia_ee.ela_40373.txt'],
['www_epl_ee.ela_495381.txt', 'rahvahaal_delfi_ee.ela_388979.txt'],
['sport_autonet_ee.ela_515760.txt', 'arvamusaed_ee.ela_274676.txt'],
['et_wikipedia_org.ela_624820.txt', 'stiimul_ee.ela_330566.txt'],
['kaja_ekstreem_ee.ela_71641.txt', 'www_puuinfo_ee.ela_279876.txt'],
['www_riigikogu_ee.ela_224866.txt', 'www_advent_ee.ela_658698.txt']
]
exp_78_text_urls = [
['www_mod_gov_ee.ela_178680.txt', 'www_hambaarst_ee.ela_475731.txt'],
['arvamusaed_ee.ela_6007.txt', 'www_eestigiid_ee.ela_530847.txt'],
['www_syndikaat_ee.ela_469373.txt', 'www_mesindus_ee.ela_33384.txt'],
['www_soudeliit_ee.ela_547578.txt', 'www_ekspress_ee.ela_495829.txt'],
['forte_delfi_ee.ela_222312.txt', 'www_eestisport_ee.ela_196071.txt'],
['www_vorumaateataja_ee.ela_241120.txt', 'kalah_zzz_ee.ela_73709.txt'],
['reform_ee.ela_24983.txt', 'herba_folklore_ee.ela_93408.txt'],
['www_eramets_ee.ela_479405.txt', 'www_ilm_err_ee.ela_196894.txt'],
['et_wikipedia_org.ela_467359.txt', 'www_snap_ee.ela_623342.txt'],
['rahvahaal_delfi_ee.ela_499379.txt', 'blog_maaleht_ee.ela_73268.txt'],
['static_inimene_ee.ela_194968.txt', 'www_linnaleht_ee.ela_420357.txt'],
['ylle_mrt_ee.ela_101705.txt', 'www_bsd_ee.ela_638246.txt'],
['forte_delfi_ee.ela_88079.txt', 'www_emta_ee.ela_522725.txt'],
['www_advent_ee.ela_658698.txt', 'www_post_ee.ela_149870.txt'],
['kalah_zzz_ee.ela_52237.txt', 'www_meiekirik_ee.ela_286284.txt'],
['www_eestikirik_ee.ela_530609.txt', 'www_mulje_ee.ela_177932.txt'],
['www_ajakiri_ut_ee.ela_429007.txt', 'www_puuinfo_ee.ela_279876.txt'],
['www_lapsemure_ee.ela_140896.txt', 'www_tuuleenergia_ee.ela_40373.txt'],
['www_vnl_ee.ela_670256.txt', 'et_wikipedia_org.ela_219301.txt'],
['et_wikipedia_org.ela_191506.txt', 'www_politsei_ee.ela_163441.txt'],
['www_vsport_ee.ela_120496.txt', 'bhr_balanss_ee.ela_565106.txt'],
['kaja_ekstreem_ee.ela_71641.txt', 'www_kasutatudraamat_ee.ela_68759.txt'],
['www_porterracing_ee.ela_609577.txt', 'www_horisont_ee.ela_455809.txt'],
['www_aialeht_ee.ela_457123.txt', 'unitedkiters_ee.ela_78733.txt'],
['et_wikipedia_org.ela_519819.txt', 'sport_autonet_ee.ela_515760.txt'],
['uuseesti_ee.ela_112397.txt', 'www_admiralmarkets_ee.ela_456804.txt'],
['www_tallegg_ee.ela_33687.txt', 'www_riigikogu_ee.ela_224866.txt'],
['nami-nami_ee.ela_372868.txt', 'www_alphagis_ee.ela_403490.txt'],
['www_dragon_ee.ela_303548.txt', 'rahvahaal_delfi_ee.ela_258274.txt'],
['www_xn--eestimngula-q8a_ee.ela_40079.txt', 'rahvahaal_delfi_ee.ela_135048.txt'],
['eok_ee.ela_435890.txt', 'toompark_pri_ee.ela_458650.txt'],
['et_wikipedia_org.ela_624820.txt', 'www_horsemarket_ee.ela_436247.txt'],
['www_naisteleht_ee.ela_355886.txt', 'www_delfi_ee.ela_361703.txt'],
['www_le_ee.ela_240831.txt', 'www_tootukassa_ee.ela_395777.txt'],
['www_kv_ee.ela_199481.txt', 'video_usk_ee.ela_152445.txt'],
['www_helen_ee.ela_520035.txt', 'uudised_err_ee.ela_541051.txt'],
['www_vm_ee.ela_81604.txt', 'arhiiv_koolielu_ee.ela_481254.txt'],
['www_epl_ee.ela_679018.txt', 'www_nami-nami_ee.ela_173054.txt'],
['rahvahaal_delfi_ee.ela_388979.txt', 'www_tarbijakaitse_ee.ela_199918.txt'],
['www_kohus_ee.ela_34731.txt', 'arvamusaed_ee.ela_274676.txt'],
['www_unesco_ee.ela_630384.txt', 'www_epl_ee.ela_685672.txt'],
['www_maaleht_ee.ela_246360.txt', 'www_3dnews_ee.ela_435253.txt'],
['stiimul_ee.ela_330566.txt', 'www_lounaleht_ee.ela_576969.txt'],
['www_lemmik_ee.ela_519214.txt', 'www_hambaarst_ee.ela_423040.txt'],
['www_bioneer_ee.ela_243230.txt', 'www_ekspress_ee.ela_177019.txt'],
['www_seduction_ee.ela_642092.txt', 'blablabla_ee.ela_504829.txt'],
['reisiajakiri_gomaailm_ee.ela_530539.txt', 'arvamus_postimees_ee.ela_5946.txt'],
['www_vorumaateataja_ee.ela_494965.txt', 'www_nami-nami_ee.ela_456341.txt'],
['www_politsei_ee.ela_40109.txt', 'www_jeesusekristusekirik_ee.ela_65555.txt'],
['valitsus_ee.ela_132104.txt', 'www_pealinn_ee.ela_132426.txt'],
['www_europarl_ee.ela_36110.txt', 'no_spam_ee.ela_2227.txt'],
['valitsus_ee.ela_604239.txt', 'www_reklaamitrikk_ee.ela_315713.txt'],
['www_med24_ee.ela_557549.txt', 'valitsus_ee.ela_480708.txt'],
['www_autoleht_ee.ela_469280.txt', 'www_director_ee.ela_529643.txt'],
['mesindus_ee.ela_210638.txt', 'untitled.txt'],
['www_admiralmarkets_ee.ela_333517.txt', 'www_epl_ee.ela_495381.txt'],
['www_auto24_ee.ela_469677.txt', 'www_lillelapsed_ee.ela_607751.txt'],
['www_linnateater_ee.ela_612249.txt', 'www_tooelu_ee.ela_624263.txt'],
['www_easl_ee.ela_201171.txt', 'www_sirp_ee.ela_651305.txt'],
['www_employers_ee.ela_617415.txt', 'ekspress_online_2020.txt']
]


def generate_dcts(input_file, session_urls):
    """
    genereerib igale eksperimendi vastuste põhjal vastuste sõnastiku (key=vastaja, value=vastused)
    vastused on zipitud koos küsimuse sisu (ehk kaks võrdluse alla olevat teksti) ja neile antud vastused
    (eksperimendis kokku 3 dimensiooni ja dimensiooni kohta 2 küsimust: 3 * 2 = 6)
    """
    answer_export = list(csv.reader(open(input_file, 'r'), delimiter='\t'))
    respondent_answers = []

    def get_chunks(lst, n):
        """genereerib kuuesed indeksiblokid, sest per küsimus on 6 vastust"""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    for i, ls in enumerate(answer_export[2:], 1):
        ans_dct = {i: list(zip(get_chunks(ls[5:], 6), session_urls))}
        respondent_answers.append(ans_dct)
    return respondent_answers



"""
Sisend: vastuste csv'd (need on Limesurvey'st eksporditud) per sessioon

Eesmärk: krippendorfi arvutamine + skooride ümbertegemine. Enne oli 0 'missing data',
aga nüüd tuleb tekst1-tekst2 vahel valida ja kui valituks osutunud tekst sai skooriks nt 3, siis teine tekst saab skooriks 1
(võimalikud skoorid on 2, 1 ja 0 ehk keskmine), kui nt skooriks sai 2, siis teine saab 0.5 (1 ja 0). Kui kummatki teksti ei valitud,
siis mõlevmad 0.

Iga sessiooni kohta väljastatakse kõik skoorid koos õige järjestusega, mida on lihtsasti võimalik kopeerida.
Nii tekib kaks kausta: dimensioonide_vastused (seal on iga dimnsiooni fail, kus on õige järjestusega vastused) jas vastajate_vastused 
(seal on iga vastaja fail, kus on kõik tema avstused per dimensioon)

Vastuste järjekord igas sessioonis:
sessioon 1: Hanna, Mari, Ana, Annely, Karmen
sessioon 2: Piret, Käbi, Aleks, Janek, Mailis
sessiioon 3: Piret, Käbi, Janek, Aleks, Mailis
sessioon 4: Hanna, Mari, Ana, Nalley, Karmen
sessioon 5: hanna, Mari, Ana, Annely, Karmen
sessioon 6: Piret, Käbi, Mailis, Aleks, Janek
sessioon 7: Hanna, Mari, Ana, Annely, Karmen
sessioon 8: Piret, Käbi, Mailis, Aleks, Janek (sellest on kaks faili, sessioon8_II sisaldab vaid ühe inimese (Piret)
vastuseid. Põhjus: limesurvey interface'is oli väike viga ja selle parandamiseks pidi vastused eksportima)

EDIT:
hetkel on skoor ümbertehtud: nimelt tekivad ennikud, kus on (tekst1, tekst2, skoor). Skoor sõltub sellest kumb tekst valiti.
Kui tekst1, siis skoor on 1; kui tekst2, siis skoor on -1; kui ei valitud ei üht ega teist, siis skoor on 0.

"""


def get_dicts(input_f, ex_urls):
    # dim_lst = [k for k in mapping.keys()]
    answers: List[
        Dict[
            int,  # vastuse ID
            Tuple[
                Tuple[str, str, str, str, str, str],  # T_i1, S_i1, T_i2, S_i2, T_i3, S_i3
                Tuple[str, str],  # url1, url2
            ]
        ]
    ] = generate_dcts(input_f, ex_urls)

    return answers


def get_scores(dim_lst, aggregated_answers):
    for participant in aggregated_answers:
        dim1, dim1_scores = [], []
        dim2, dim2_scores = [], []
        dim3, dim3_scores = [], []
        dim4, dim4_scores = [], []
        dim5, dim5_scores = [], []
        dim6, dim6_scores = [], []
        dim7, dim7_scores = [], []
        dim8, dim8_scores = [], []
        dim9, dim9_scores = [], []
        dim10, dim10_scores = [], []
        dim11, dim11_scores = [], []
        dim12, dim12_scores = [], []
        vastaja_nr = list(participant.keys())[0]
        print(f'vastaja nr: {vastaja_nr}')
        for line in participant.values():
            for answer in line:
                text_urls = answer[1]
                row_answers = (
                    (dim_lst[0], answer[0][0:2]),
                    (dim_lst[1], answer[0][2:4]),
                    (dim_lst[2], answer[0][4:6])
                )
                # skooride ümberarvutamine koos abifunktsiooniga
                for dimension, text_and_score in row_answers:
                    text_id = text_and_score[0]
                    score_id = text_and_score[1]
                    text_url_first = text_urls[0]
                    text_url_second = text_urls[1]
                    if text_id == 'T1':
                        texts = [text_url_first, text_url_second]
                        scores = [score_mapping[score_id], -1]

                    elif text_id == 'T2':
                        texts = [text_url_second, text_url_first]
                        scores = [score_mapping[score_id], -1]
                    elif text_id == 'T3':
                        texts = [text_url_first, text_url_second]
                        scores = [0, 0]
                        # first = [text_url_first, 0]
                        # second = [text_url_second, 0]

                    # neid peab käsitsi sättima, vastavalt sellele, mis see konkreetne mapping on konkreetses sessioonis
                    if dimension == 'abs':
                        dim1.append(texts)
                        dim1_scores.append(scores)
                    elif dimension == 'info':
                        dim2.append(texts)
                        dim2_scores.append(scores)
                    elif dimension == 'aeg':
                        dim3.append(texts)
                        dim3_scores.append(scores)
                    elif dimension == 'afek':
                        dim4.append(texts)
                        dim4_scores.append(scores)
                    elif dimension == 'form':
                        dim5.append(texts)
                        dim5_scores.append(scores)
                    elif dimension == 'inter':
                        dim6.append(texts)
                        dim6_scores.append(scores)
                    elif dimension == 'inst':
                        dim7.append(texts)
                        dim7_scores.append(scores)
                    elif dimension == 'keer':
                        dim8.append(texts)
                        dim8_scores.append(scores)
                    elif dimension == 'subj':
                        dim9.append(texts)
                        dim9_scores.append(scores)
                    elif dimension == 'spont':
                        dim10.append(texts)
                        dim10_scores.append(scores)
                    elif dimension == 'imp':
                        dim11.append(texts)
                        dim11_scores.append(scores)
                    elif dimension == 'arg':
                        dim12.append(texts)
                        dim12_scores.append(scores)


        # abs = '; '.join([str(d) for dim in dim1 for d in dim])
        # abs_scores = '; '.join([str(d) for dim in dim1_scores for d in dim])
        # print(f'abs; {abs}; {abs_scores}')
        # info = '; '.join([str(d) for dim in dim2 for d in dim])
        # info_scores = '; '.join([str(d) for dim in dim2_scores for d in dim])
        # print(f'info; {info}; {info_scores}')
        # aeg = '; '.join([str(d) for dim in dim3 for d in dim])
        # aeg_scores = '; '.join([str(d) for dim in dim3_scores for d in dim])
        # print(f'aeg; {aeg}; {aeg_scores}')

        # afek = '; '.join([str(d) for dim in dim4 for d in dim])
        # afek_scores = '; '.join([str(d) for dim in dim4_scores for d in dim])
        # print(f'afek; {afek}; {afek_scores}')
        # form = '; '.join([str(d) for dim in dim5 for d in dim])
        # form_scores = '; '.join([str(d) for dim in dim5_scores for d in dim])
        # print(f'form; {form}; {form_scores}')
        # inter = '; '.join([str(d) for dim in dim6 for d in dim])
        # inter_scores = '; '.join([str(d) for dim in dim6_scores for d in dim])
        # print(f'inter; {inter}; {inter_scores}')

        # inst = '; '.join([str(d) for dim in dim7 for d in dim])
        # inst_scores = '; '.join([str(d) for dim in dim7_scores for d in dim])
        # print(f'inst; {inst}; {inst_scores}')
        # keer = '; '.join([str(d) for dim in dim8 for d in dim])
        # keer_scores = '; '.join([str(d) for dim in dim8_scores for d in dim])
        # print(f'keer; {keer}; {keer_scores}')
        # subj = '; '.join([str(d) for dim in dim9 for d in dim])
        # subj_scores = '; '.join([str(d) for dim in dim9_scores for d in dim])
        # print(f'subj; {subj}; {subj_scores}')
        #
        spont = '; '.join([str(d) for dim in dim10 for d in dim])
        spont_scores = '; '.join([str(d) for dim in dim10_scores for d in dim])
        print(f'spont; {spont}; {spont_scores}')
        imp = '; '.join([str(d) for dim in dim11 for d in dim])
        imp_scores = '; '.join([str(d) for dim in dim11_scores for d in dim])
        print(f'imp; {imp}; {imp_scores}')
        arg = '; '.join([str(d) for dim in dim12 for d in dim])
        arg_scores = '; '.join([str(d) for dim in dim12_scores for d in dim])
        print(f'arg; {arg}; {arg_scores}')


if __name__ == "__main__":

    # input_files = [
    #     #     ['originaalfailid/vvexport_sessioon1.csv', ex1, exp_12_text_urls],
    #     #      ['originaalfailid/vvexport_sessioon2.csv', ex2, exp_12_text_urls],
    #     #     ['originaalfailid/vvexport_sessioon3.csv', ex3, exp_34_text_urls],
    #     #     ['originaalfailid/vvexport_sessioon4.csv', ex4, exp_34_text_urls],
    #     #     ['originaalfailid/vvexport_sessioon5.csv', ex5, exp_56_text_urls],
    #     #     ['originaalfailid/vvexport_sessioon6.csv', ex6, exp_56_text_urls],
    #     #     ['originaalfailid/vvexport_sessioon7.csv', ex7, exp_78_text_urls],
    #     ['limesurvey_exports/vvexport_sessioon8_I.csv', ex8, exp_78_text_urls],
    # ]

    experiment_answers = get_dicts('limesurvey_exports/vvexport_sessioon6.csv', exp_56_text_urls)
    get_scores([k for k in ex6.keys()], experiment_answers)










