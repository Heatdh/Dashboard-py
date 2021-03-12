'''ymax=max(max(BY["Cases_Last_Week"]),max(BE["Cases_Last_Week"]), max(NW["Cases_Last_Week"]), max(SN["Cases_Last_Week"]), max(TH["Cases_Last_Week"]) )
state=""
max_by= max(BY["Cases_Last_Week"])
max_be=max(BE["Cases_Last_Week"])
max_nw=max(NW["Cases_Last_Week"])
max_sn=max(SN["Cases_Last_Week"])
max_th=max(TH["Cases_Last_Week"])
xmax=0
if max_by==ymax :
    state='BY'
    s = BY["Cases_Last_Week"].idxmax()
    xmax=BY.iloc[s,1]
if max_be==ymax :
    state='BE'
    s = BE["Cases_Last_Week"].idxmax()
    xmax=BE.iloc[s,1]
if max_nw==ymax :
    state='NW'
    s = NW["Cases_Last_Week"].idxmax()
    xmax=NW.iloc[s,1]
if max_sn==ymax :
    state='SN'
    s = SN["Cases_Last_Week"].idxmax()
    xmax=SN.iloc[s,1]
if max_th==ymax :
    state='TH'
    s = TH["Cases_Last_Week"].idxmax()
    xmax=TH.iloc[s,1]'''


'''fig.add_annotation(x=xmax, y=ymax,
            text='Maximum n={} in {} \n @{}'.format(ymax, state, xmax),
            showarrow=True,
            arrowhead=1,
            yshift=ymax+10)'''