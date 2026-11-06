from pathlib import Path
import json

# KRW 10,000; official 2026 salary averages, not external development quotes.
rates = dict(app=775.4124, ux=690.1660, tester=405.3137, pm=1008.6804)
work = dict(app=(2,3),ux=(0.5,0.8),tester=(0.5,1),pm=(0.25,0.5))
common = [sum(rates[key]*work[key][i] for key in rates) for i in (0,1)]
mechanical_month = (600,900)  # Analyst assumption, not KOSA SW salary.

scenarios = {
 'kit': dict(name='기능평가 키트',app=(0.5,1.5),mech=(0,0),hardware=(350,600),protocol=(100,300),validation=(100,300),integration=(0,0),weeks=(8,12),pilot=(500,1200)),
 'station': dict(name='가이드형 측정 스테이션',app=(1,3),mech=(1,3),hardware=(800,1800),protocol=(100,300),validation=(250,600),integration=(0,0),weeks=(12,20),pilot=(1200,3000)),
 'hospital': dict(name='병원 평가·관리 보조',app=(1,2),mech=(0,0),hardware=(50,150),protocol=(500,1200),validation=(200,500),integration=(300,800),weeks=(10,16),pilot=(300,1000)),
 'feedback': dict(name='운동 피드백 시스템',app=(1.5,3),mech=(0,0),hardware=(300,900),protocol=(300,800),validation=(300,800),integration=(0,0),weeks=(10,16),pilot=(500,1500)),
 'service': dict(name='정기 기능평가 서비스',app=(0.5,1),mech=(0,0),hardware=(700,1200),protocol=(200,500),validation=(200,500),integration=(0,0),weeks=(8,12),pilot=(1300,2500)),
}
for key,item in scenarios.items():
    total=[]
    incremental=[]
    for i in (0,1):
        extra=item['app'][i]*rates['app']+item['mech'][i]*mechanical_month[i]
        extra+=sum(item[field][i] for field in ('hardware','protocol','validation','integration'))
        incremental.append(extra)
        total.append(common[i]+extra)
    item['incremental']=incremental
    item['direct']=total
    item['with_reserve']=[value*1.2 for value in total]
    item['rounded']=[round(value/100)*100 for value in item['with_reserve']]
    assert total[0] <= total[1]

day_inputs=dict(operator=(2*10*3,2*10*5),reviewer=(20*5/60*8,20*5/60*15),prepost=(4*3,4*5),travel=(10,20),consumables=(20*0.3,20*0.5),depreciation=(3,8))
day_total=[sum(value[i] for value in day_inputs.values()) for i in (0,1)]
person_total=[value/20 for value in day_total]
data=dict(currency='KRW_10000',rates=rates,common_work=work,common_direct=common,mechanical_month_assumption=mechanical_month,scenarios=scenarios,service_day_inputs=day_inputs,service_day_total=day_total,service_person_total=person_total,planning_fx=dict(USD=1500,EUR=1650),fx_is_market_quote=False)
assert round(day_total[0],1)==104.3 and day_total[1]==183
assert len(scenarios)==5
path=Path(__file__).with_name('specs-budget.json')
path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(common_direct_manwon=common,MVP_with_20pct_reserve_manwon={k:v['rounded'] for k,v in scenarios.items()},service_day_manwon=day_total,service_person_manwon=person_total),ensure_ascii=True,indent=2))
