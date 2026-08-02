function PackagesScreen({onNavigate,onSelect}){
  return <>
    <Section variant="surface" tight align="center" eyebrow="Packages" heading="Tiered packages, with add-ons" lead="Every tier includes delivery, setup, an on-site attendant and breakdown. Add-ons are priced per event — tell us what you need and we'll quote it.">
      <div style={{display:'grid',gridTemplateColumns:'repeat(3,1fr)',gap:'var(--space-3)',alignItems:'stretch'}}>
        {PACKAGES.map(p=>(
          <Card key={p.id} variant="default" featured={p.featured} eyebrow={p.eyebrow} title={p.name}
            footer={<Button fullWidth variant={p.featured?'primary':'outline'} onClick={()=>{onSelect(p.id);onNavigate('book');}}>Get a quote</Button>}>
            <p style={{margin:'0 0 var(--space-2)'}}>{p.blurb}</p>
            <ul style={{margin:0,padding:0,listStyle:'none',display:'grid',gap:'8px'}}>
              {p.includes.map(i=><li key={i} style={{display:'flex',gap:'10px',alignItems:'flex-start',fontSize:'15px',lineHeight:1.5}}>
                <img src={ASSETS+'/icon-flag.png'} alt="" style={{height:16,marginTop:2,flexShrink:0}}/>{i}</li>)}
            </ul>
          </Card>
        ))}
      </div>
      <p style={{textAlign:'center',marginTop:'var(--space-3)',fontSize:'var(--text-small)',color:'var(--text-muted)'}}>Pricing is quoted per event — no published rate card was supplied with the brand package.</p>
    </Section>

    <Section eyebrow="Add-ons" heading="Make it yours" tight>
      <div style={{display:'grid',gridTemplateColumns:'repeat(3,1fr)',gap:'var(--space-2-5)'}}>
        <Card variant="surface" title="Extra hours">Keep the bay open past your package window.</Card>
        <Card variant="surface" title="Custom scoring">Branded leaderboard and a tournament format for your group.</Card>
        <Card variant="surface" title="Second attendant">Faster rotation for events over 100 guests.</Card>
      </div>
    </Section>

    <QuoteBand onNavigate={onNavigate} />
  </>;
}
window.PackagesScreen=PackagesScreen;
