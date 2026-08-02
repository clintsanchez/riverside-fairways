const {Button,Card,Section,Hero,SiteHeader,SiteFooter,Logo}=window.RiversideFairwaysDesignSystem_bd15be;
const ASSETS='../../assets';
const PHONE='(225) 978-2363';
const EMAIL='jase@riversidefairways.com';

const NAV=[{id:'home',label:'Home'},{id:'packages',label:'Packages'},{id:'events',label:'Events'},{id:'about',label:'About'}];

// No photography was supplied with the brand package. Every image well renders
// this honest placeholder rather than invented imagery.
function Photo({label='Photography placeholder',height,ratio='16 / 10',style}){
  return (
    <div style={{position:'relative',height,aspectRatio:height?undefined:ratio,width:'100%',background:'var(--rf-warm-neutral)',display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'center',gap:'10px',...style}}>
      <img src={ASSETS+'/icon-flag.png'} alt="" style={{height:40,opacity:.5}}/>
      <span style={{fontSize:'var(--text-small)',letterSpacing:'var(--tracking-eyebrow)',textTransform:'uppercase',color:'var(--rf-green-dark)',opacity:.7,textAlign:'center',padding:'0 12px'}}>{label}</span>
    </div>
  );
}

function Stat({value,label}){
  return <div><div style={{fontFamily:'var(--font-display)',fontSize:'42px',fontWeight:300,letterSpacing:'2px',color:'var(--text-brand)',lineHeight:1.1}}>{value}</div>
  <div style={{fontSize:'var(--text-small)',letterSpacing:'var(--tracking-eyebrow)',textTransform:'uppercase',color:'var(--text-muted)',marginTop:'6px'}}>{label}</div></div>;
}

function QuoteBand({onNavigate}){
  return <Section variant="brand" tight align="center" heading="Ready to bring the fairway to you?" lead="Tell us the date and the venue — we'll handle the rest.">
    <div style={{display:'flex',gap:'var(--space-2)',justifyContent:'center'}}>
      <Button size="lg" variant="reversed" onClick={()=>onNavigate('book')}>Get a quote</Button>
      <Button size="lg" variant="outline" style={{color:'var(--rf-white)',borderColor:'var(--rf-white)'}} href={'tel:'+PHONE.replace(/[^0-9]/g,'')}>{PHONE}</Button>
    </div>
  </Section>;
}

const PACKAGES=[
  {id:'fairway',name:'The Fairway',eyebrow:'Tier one',blurb:'Our core setup for smaller gatherings and open-house play.',includes:['Simulator, screen and hitting mat','On-site attendant','Four hours of play','Delivery, setup and breakdown']},
  {id:'clubhouse',name:'The Clubhouse',eyebrow:'Most booked',featured:true,blurb:'The full experience for corporate events and receptions.',includes:['Everything in The Fairway','The Feral pack — 14 extra games','Six hours of play','Leaderboard display']},
  {id:'open',name:'The Open',eyebrow:'Tier three',blurb:'All-day play for tournaments, festivals and charity events.',includes:['Everything in The Clubhouse','Full-day play','Two attendants','Custom scoring format']}
];

const EVENTS=[
  {title:'Corporate events',body:'Team building, client entertainment and holiday parties — set up in your lobby, warehouse or parking lot.'},
  {title:'Weddings',body:'Keep guests playing between the ceremony and the reception. Setup is quiet and tucked wherever you need it.'},
  {title:'Parties & celebrations',body:'Birthdays, graduations and backyard get-togethers. The Feral pack keeps kids busy for hours.'},
  {title:'Charity & community',body:'A tournament alternative that fits indoors, rain or shine, with scoring built in.'}
];

Object.assign(window,{Button,Card,Section,Hero,SiteHeader,SiteFooter,Logo,Photo,Stat,QuoteBand,NAV,PACKAGES,EVENTS,PHONE,EMAIL,ASSETS});
