function EventsScreen({onNavigate}){
  return <>
    <Hero height={380} eyebrow="Events" headline="Every kind of gathering" subhead="Corporate, wedding, backyard or charity — the setup is the same, the vibe is yours."
      actions={<Button size="lg" variant="reversed" onClick={()=>onNavigate('book')}>Check your date</Button>} />

    <Section>
      <div style={{display:'grid',gap:'var(--space-4)'}}>
        {EVENTS.map((e,i)=>(
          <div key={e.title} style={{display:'grid',gridTemplateColumns:i%2?'1fr 1.1fr':'1.1fr 1fr',gap:'var(--space-3)',alignItems:'center'}}>
            <div style={{order:i%2?2:1}}><Photo label={e.title+' photo'} /></div>
            <div style={{order:i%2?1:2}}>
              <div style={{fontSize:'var(--text-small)',fontWeight:600,letterSpacing:'var(--tracking-eyebrow)',textTransform:'uppercase',color:'var(--text-brand)'}}>0{i+1}</div>
              <h3 style={{margin:'8px 0 0',fontFamily:'var(--font-display)',fontSize:'var(--text-h2)',fontWeight:600,letterSpacing:'1px',color:'var(--text-heading)'}}>{e.title}</h3>
              <p style={{margin:'var(--space-2) 0 0',lineHeight:'var(--leading-body)',maxWidth:'52ch'}}>{e.body}</p>
              <div style={{marginTop:'var(--space-2)'}}><Button variant="ghost" onClick={()=>onNavigate('book')}>Ask about {e.title.toLowerCase()} →</Button></div>
            </div>
          </div>
        ))}
      </div>
    </Section>

    <QuoteBand onNavigate={onNavigate} />
  </>;
}
window.EventsScreen=EventsScreen;
