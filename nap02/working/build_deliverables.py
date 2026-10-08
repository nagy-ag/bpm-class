from pathlib import Path
import xml.etree.ElementTree as E
import copy, json

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT/'nap02'/'docs'
OUT = ROOT/'deliverables'
NS = {'bpmn':'http://www.omg.org/spec/BPMN/20100524/MODEL','bpmndi':'http://www.omg.org/spec/BPMN/20100524/DI','dc':'http://www.omg.org/spec/DD/20100524/DC','di':'http://www.omg.org/spec/DD/20100524/DI','qbp':'http://www.qbp-simulator.com/Schema201212'}
for prefix,uri in NS.items(): E.register_namespace(prefix,uri)
def tag(name):
    prefix,local=name.split(':'); return '{'+NS[prefix]+'}'+local
def sub(parent,qname,**attrs): return E.SubElement(parent,tag(qname),{k:str(v) for k,v in attrs.items()})
def normalize(root):
    for p in root.findall('bpmn:process',NS):
        flows=p.findall('bpmn:sequenceFlow',NS)
        for n in p:
            if n.tag in [tag('bpmn:'+x) for x in ['sequenceFlow','laneSet','documentation']]: continue
            for child in list(n):
                if child.tag in [tag('bpmn:incoming'),tag('bpmn:outgoing')]: n.remove(child)
            for flow in flows:
                if flow.get('targetRef')==n.get('id'): sub(n,'bpmn:incoming').text=flow.get('id')
                if flow.get('sourceRef')==n.get('id'): sub(n,'bpmn:outgoing').text=flow.get('id')
    return root
def save(root,name):
    normalize(root); E.indent(root); E.ElementTree(root).write(OUT/name,encoding='utf-8',xml_declaration=True)
def load(name): return E.parse(SRC/name).getroot()
def make_model(name,nodes,flows):
    root=E.Element(tag('bpmn:definitions'),{'id':'Defs_'+name,'targetNamespace':'http://fsega.ubbcluj.ro/bpa'})
    p=sub(root,'bpmn:process',id='Process_'+name,isExecutable='false')
    bounds={}
    for id,kind,label,x,y in nodes:
        node=sub(p,'bpmn:'+kind,id=id,name=label) if label else sub(p,'bpmn:'+kind,id=id)
        if kind=='messageCatch': raise ValueError('use intermediateCatchEvent')
        if kind in ['startEvent','endEvent','intermediateCatchEvent']: w=h=36
        elif kind.endswith('Gateway'): w=h=50
        else: w,h=120,70
        bounds[id]=(x,y,w,h)
    for f in flows:
        id,s,t,*label=f
        flow=sub(p,'bpmn:sequenceFlow',id=id,sourceRef=s,targetRef=t)
        if label and label[0]: flow.set('name',label[0])
    diagram=sub(root,'bpmndi:BPMNDiagram',id='Diagram_'+name)
    plane=sub(diagram,'bpmndi:BPMNPlane',id='Plane_'+name,bpmnElement=p.get('id'))
    for id,(x,y,w,h) in bounds.items():
        shape=sub(plane,'bpmndi:BPMNShape',id='Shape_'+id,bpmnElement=id)
        if p.find("*[@id='%s']"%id).tag==tag('bpmn:exclusiveGateway'): shape.set('isMarkerVisible','true')
        sub(shape,'dc:Bounds',x=x,y=y,width=w,height=h)
        if w<=50: sub(sub(shape,'bpmndi:BPMNLabel'),'dc:Bounds',x=x-45,y=y+h+8,width=125,height=42)
    for id,s,t,*label in flows:
        x,y,w,h=bounds[s]; a,b,c,d=bounds[t]
        if a>=x+w:
            pts=[(x+w,y+h/2),((x+w+a)/2,y+h/2),((x+w+a)/2,b+d/2),(a,b+d/2)]
        else:
            route=max(y+h,b+d)+85
            pts=[(x+w/2,y+h),(x+w/2,route),(a+c/2,route),(a+c/2,b+d)]
        edge=sub(plane,'bpmndi:BPMNEdge',id='Edge_'+id,bpmnElement=id)
        last=None
        for pt in pts:
            if pt!=last: sub(edge,'di:waypoint',x=pt[0],y=pt[1]); last=pt
        if label and label[0]: sub(sub(edge,'bpmndi:BPMNLabel'),'dc:Bounds',x=pts[1][0]+5,y=pts[1][1]-25,width=75,height=20)
    return root

# Block 2: preserve simple reference and add receipt-triggered return window.
save(load('webshop_rendeles_egyszeru.bpmn'),'webshop_egyszeru.bpmn')
nodes=[('s','startEvent','Rendelés beérkezik',150,190),('t1','task','Rendelés rögzítése',250,173),('t2','sendTask','Fizetési link küldése',440,173),('g0','eventBasedGateway','',630,183),('ev1','intermediateCatchEvent','Fizetés megérkezik',750,90),('ev2','intermediateCatchEvent','48 óra letelt',750,420),('t3','task','Csomag összekészítése',860,73),('t4','task','Futárnak átadás',1050,73),('receipt','intermediateCatchEvent','Átvétel visszaigazolása',1250,90),('returns','eventBasedGateway','',1370,83),('days14','intermediateCatchEvent','14 nap letelt',1500,90),('request','intermediateCatchEvent','Visszaküldési igény érkezik',1500,250),('handle','task','Visszáru kezelése',1630,233),('e1','endEvent','Rendelés teljesítve',1820,90),('er','endEvent','Rendelés lezárva visszaküldéssel',1820,250),('t5','task','Rendelés törlése',860,403),('e2','endEvent','Rendelés lezárva fizetés nélkül',1050,420)]
flows=[('f0','s','t1'),('f1','t1','t2'),('f2','t2','g0'),('f3','g0','ev1'),('f4','g0','ev2'),('f5','ev1','t3'),('f6','t3','t4'),('f7','t4','receipt'),('f8','ev2','t5'),('f9','t5','e2'),('f10','receipt','returns'),('f11','returns','days14'),('f12','returns','request'),('f13','days14','e1'),('f14','request','handle'),('f15','handle','er')]
web=make_model('WebshopReturns',nodes,flows); p=web.find('bpmn:process',NS)
for id in ['ev1','receipt','request']: sub(p.find("*[@id='%s']"%id),'bpmn:messageEventDefinition',id=id+'_message')
for id,duration in [('ev2','PT48H'),('days14','P14D')]: sub(sub(p.find("*[@id='%s']"%id),'bpmn:timerEventDefinition',id=id+'_timer'),'bpmn:timeDuration').text=duration
save(web,'webshop_visszakuldes.bpmn')

# Block 3: editable reference, keeping both lanes and four cross-pool messages.
save(load('meridian_karfelvetel.bpmn'),'meridian_karfelvetel.bpmn')

# Block 6: corrected AND join.
r=load('hibas_1.bpmn'); r.find("bpmn:process/*[@id='g2']",NS).tag=tag('bpmn:parallelGateway'); save(r,'hibas_1_javitva.bpmn')
# Credit appraisal is explicitly performed before the approval decision.
r=make_model('CreditFixed',[('s','startEvent','Hitelkérelem beérkezik',150,190),('t1','task','Adatok rögzítése',250,173),('t9','task','Fedezet értékbecslése',440,173),('g1','exclusiveGateway','Hitel jóváhagyható?',630,183),('t2','task','Hitel folyósítása',760,73),('t3','sendTask','Elutasító levél küldése',760,303),('e1','endEvent','Hitel folyósítva',970,90),('e2','endEvent','Hitelkérelem elutasítva',970,320)],[('f0','s','t1'),('f1','t1','t9'),('f6','t9','g1'),('f2','g1','t2','igen'),('f3','g1','t3','nem'),('f4','t2','e1'),('f5','t3','e2')]); save(r,'hibas_2_javitva.bpmn')
# Approval precedes the decision; rejection loops to revision, approval exits.
r=make_model('ComplaintFixed',[('s','startEvent','Panasz beérkezik',150,190),('t1','task','Panasz kivizsgálása',250,173),('t2','task','Válaszlevél írása és javítása',440,173),('t3','userTask','Válaszlevél jóváhagyása',630,173),('g1','exclusiveGateway','Jóváhagyta a vezető?',820,183),('send','sendTask','Jóváhagyott válasz elküldése',950,173),('e','endEvent','Panasz lezárva',1160,190)],[('f0','s','t1'),('f1','t1','t2'),('f2','t2','t3'),('f3','t3','g1'),('f4','g1','send','igen'),('f5','g1','t2','nem'),('f6','send','e')]); save(r,'hibas_3_javitva.bpmn')

def distribution(parent,name,kind,mean,std=None):
    attrs={'type':kind,'arg1':str(mean*60)} if kind=='EXPONENTIAL' else {'type':kind,'mean':str(mean*60)}
    if kind=='NORMAL': attrs['arg1']=str(std*60)
    d=sub(parent,'qbp:'+name,**attrs); sub(d,'qbp:timeUnit').text='minutes'
def scenario(base,name,arrival,count,resources,tasks,probs,warehouse=False):
    r=copy.deepcopy(base)
    sim=sub(r,'qbp:processSimulationInfo',id='Sim_'+name,processId=r.find('bpmn:process',NS).get('id'),processInstances=count,startDateTime='2026-10-05T'+('06' if warehouse else '09')+':00:00+03:00',currency='EUR',version='1')
    distribution(sim,'arrivalRateDistribution','EXPONENTIAL',arrival)
    ts=sub(sim,'qbp:timetables')
    t=sub(ts,'qbp:timetable',id='Default',name='Default',default='true')
    sub(sub(t,'qbp:rules'),'qbp:rule',fromWeekDay='MONDAY',toWeekDay='SUNDAY' if warehouse else 'FRIDAY',fromTime=('06' if warehouse else '09')+':00:00.000+00:00',toTime=('22' if warehouse else '17')+':00:00.000+00:00')
    t=sub(ts,'qbp:timetable',id='QBP_247_TIMETABLE',name='24/7',default='false'); sub(sub(t,'qbp:rules'),'qbp:rule',fromWeekDay='MONDAY',toWeekDay='SUNDAY',fromTime='00:00:00.000+00:00',toTime='23:59:59.999+00:00')
    rs=sub(sim,'qbp:resources')
    for id,label,amount,cost in resources: sub(rs,'qbp:resource',id=id,name=label,totalAmount=amount,costPerHour=cost,timetableId='Default')
    els=sub(sim,'qbp:elements')
    for id,resource,kind,mean,std in tasks:
        el=sub(els,'qbp:element',id='SimElement_'+id,elementId=id,fixedCost='0',simulateAsTask='false')
        distribution(el,'durationDistribution',kind,mean,std)
        sub(sub(el,'qbp:resourceIds'),'qbp:resourceId').text=resource
    fs=sub(sim,'qbp:sequenceFlows')
    for id,prob in probs: sub(fs,'qbp:sequenceFlow',elementId=id,executionProbability=prob)
    sub(sim,'qbp:statsOptions',trimStartProcessInstances='0',trimEndProcessInstances='0')
    save(r,name+'.bpmn')

cafe=E.parse(OUT/'kave_xor.bpmn').getroot()
cafe_tasks=[('t1','Pultos','NORMAL',1.5,.4),('t2','Barista','NORMAL',3.2,.8),('t3','Barista','FIXED',.6,None),('t4','Barista','FIXED',.6,None),('t5','Pultos','NORMAL',1,.3)]
for name,arrival,pultos,barista in [('kave_01_alap_szimulacio',6,1,1),('kave_02_csucs_szimulacio',3,1,1),('kave_03_ket_barista_szimulacio',3,1,2),('kave_04_ket_pultos_szimulacio',3,2,1)]:
    scenario(cafe,name,arrival,100,[('Pultos','Pultos',pultos,8),('Barista','Barista',barista,9)],cafe_tasks,[('f3',.6),('f4',.4)])
warehouse=load('atlas_raktar_alap.bpmn'); save(copy.deepcopy(warehouse),'atlas_raktar_alap.bpmn')
for name,amount,storage in [('raktar_01_alap_szimulacio',8,20),('raktar_02_A_tiz_targoncas_szimulacio',10,20),('raktar_03_B_kulon_betarolas_szimulacio',8,0)]:
    tasks=[('t1','Admin','NORMAL',4,1),('t2','Forklift','NORMAL',40,10),('t3','Warehouse','NORMAL',50,15),('t4','Warehouse','NORMAL',25,10),('t5','Forklift','NORMAL' if storage else 'FIXED',storage,5 if storage else None),('t6','Admin','NORMAL',7,2)]
    scenario(warehouse,name,7,135,[('Admin','Adminisztrátor',2,12),('Forklift','Targoncás',amount,14),('Warehouse','Raktáros',36,10)],tasks,[('f4',.92),('f5',.08)],warehouse=True)

# Structural checks: references, reachability, end reachability and decision labels.
checks=[]
for path in sorted(OUT.glob('*.bpmn')):
    root=E.parse(path).getroot(); ids=[n.get('id') for n in root.iter() if n.get('id')]; assert len(ids)==len(set(ids)),path
    for p in root.findall('bpmn:process',NS):
        nodes={n.get('id'):n for n in p if n.get('id') and n.tag not in [tag('bpmn:sequenceFlow'),tag('bpmn:laneSet')]}
        flows=p.findall('bpmn:sequenceFlow',NS); adj={id:[] for id in nodes}; rev={id:[] for id in nodes}
        for f in flows: assert f.get('sourceRef') in nodes and f.get('targetRef') in nodes,path; adj[f.get('sourceRef')].append(f.get('targetRef')); rev[f.get('targetRef')].append(f.get('sourceRef'))
        def walk(seed,graph):
            seen=set(seed); todo=list(seed)
            while todo:
                for v in graph[todo.pop()]:
                    if v not in seen: seen.add(v); todo.append(v)
            return seen
        starts=[id for id,n in nodes.items() if n.tag==tag('bpmn:startEvent')]; ends=[id for id,n in nodes.items() if n.tag==tag('bpmn:endEvent')]
        assert starts and ends and walk(starts,adj)==set(nodes) and walk(ends,rev)==set(nodes),path
        for id,n in nodes.items():
            if n.tag==tag('bpmn:exclusiveGateway') and len(adj[id])>1:
                assert n.get('name') and all(f.get('name') for f in flows if f.get('sourceRef')==id),path
    checks.append({'file':path.name,'references':'pass','reachable_from_start':'pass','path_to_end':'pass'})
(OUT/'modell_ellenorzes.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
print('Created and structurally checked',len(checks),'BPMN files.')
