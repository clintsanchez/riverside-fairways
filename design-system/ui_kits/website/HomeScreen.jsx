function HomeScreen({onNavigate}){
  return <>
    <Hero eyebrow="Mobile golf simulator" headline="We bring the fairway to you"
      subhead="Fully mobile — we set up anywhere with access to electricity. Corporate events, weddings, parties and everything in between, across Louisiana and the Mississippi Gulf Coast."
      actions={<><Button size="lg" variant="reversed" onClick={()=>onNavigate('book')}>Get a quote</Button><Button size="lg" variant="outline" style={{color:'var(--rf-white)',borderColor:'var(--rf-white)'}} onClick={()=>onNavigate('packages')}>See packages</Button></>}
      trust={['Fully mobile','No golf experience needed','Setup and breakdown included']} />

    <Section eyebrow="What we do" heading="A championship simulator that travels" lead="You pick the venue. We arrive, set up, run the play and pack it out — all you need is an outlet.">
      <div style={{display:'grid',gridTemplateColumns:'1.1fr 1fr',gap:'var(--space-3)',alignItems:'center'}}>
        <Photo label="Simulator in use at a corporate event" />
        <div style={{display:'grid',gap:'var(--space-2-5)'}}>
          <div><h3 style={{margin:0,fontFamily:'var(--font-display)',fontSize:'var(--text-h3)',fontWeight:600,color:'var(--text-heading)'}}>Anywhere with electricity</h3><p style={{margin:'6px 0 0',lineHeight:'var(--leading-body)'}}>Indoors or out, wifi optional. If there's an outlet, there's a fairway.</p></div>
          <div><h3 style={{margin:0,fontFamily:'var(--font-display)',fontSize:'var(--text-h3)',fontWeight:600,color:'var(--text-heading)'}}>Fun at every skill level</h3><p style={{margin:'6px 0 0',lineHeight:'var(--leading-body)'}}>Scratch golfers and first-timers end up at the same screen, laughing.</p></div>
          <div><h3 style={{margin:0,fontFamily:'var(--font-display)',fontSize:'var(--text-h3)',fontWeight:600,color:'var(--text-heading)'}}>Fourteen more games</h3><p style={{margin:'6px 0 0',lineHeight:'var(--leading-body)'}}>The Feral pack adds soccer, darts, zombie dodgeball and more for younger crowds.</p></div>
        </div>
      </div>
    </Section>

    <Section variant="surface" eyebrow="Events" heading="Built for the room you're already in" align="center">
      <div style={{display:'grid',gridTemplateColumns:'repeat(4,1fr)',gap:'var(--space-2-5)'}}>
        {EVENTS.map(e=><Card key={e.title} title={e.title} media={<Photo label="Event photo" />}>{e.body}</Card>)}
      </div>
      <div style={{textAlign:'center',marginTop:'var(--space-3)'}}><Button variant="outline" onClick={()=>onNavigate('events')}>Explore event types</Button></div>
    </Section>

    <Section tight>
      <div style={{display:'grid',gridTemplateColumns:'repeat(3,1fr)',gap:'var(--space-3)'}}>
        <Stat value="14" label="Extra games in the Feral pack" />
        <Stat value="1 outlet" label="Everything we require on site" />
        <Stat value="Statewide" label="Louisiana & the Gulf Coast" />
      </div>
    </Section>

    <QuoteBand onNavigate={onNavigate} />
  </>;
}
window.HomeScreen=HomeScreen;
